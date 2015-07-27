#!/usr/bin/env python

import sys, os, yaml, time, urllib2, atexit

from helpers.etcd import Etcd
from helpers.postgresql import Postgresql
from helpers.ha import Ha
from helpers.ec2 import Ec2
from helpers.rt53 import Rt53
from helpers.sns import Sns
from helpers.sqs import Sqs
from helpers.kms import Kms

import syslog
from socket import gethostname

# add system path
psql_bin_path = "/usr/pgsql-9.4/bin"
os.environ['PATH'] += os.pathsep + psql_bin_path

ec2 = Ec2()
our_ip = ec2.ec2_ip()

f = open(sys.argv[1], "r")
config = yaml.load(f.read())
f.close()

# kms is needed to decryot config
kms = Kms(config["kms"])
# configure the postgres
hostname = gethostname()
config["postgresql"]["name"] = hostname.split('.')[0]
config["postgresql"]["listen"] = our_ip + ":" + str(config["postgresql"]["port"])
postgresql = Postgresql(config["postgresql"], kms, hostname)

config["rt53"]["our_ip"] = our_ip
rt53 = Rt53(config["rt53"])
etcd = Etcd(config["etcd"])
sns = Sns(config["sns"], kms)
sqs = Sqs(config["sqs"])
ha = Ha(postgresql, etcd, rt53, sns, sqs, hostname)

# stop postgresql on script exit
def stop_postgresql():
    postgresql.stop()
atexit.register(stop_postgresql)

# wait for etcd to be available
etcd_ready = False
while not etcd_ready:
    try:
        etcd.touch_member(postgresql.name, postgresql.connection_string)
        etcd_ready = True
    except urllib2.URLError:
        syslog.syslog("waiting on etcd")
        time.sleep(5)

# is data directory empty?
if postgresql.data_directory_empty():
    # racing to initialize
    if etcd.race("/initialize", postgresql.name):
        postgresql.initialize()
        etcd.take_leader(postgresql.name)
        postgresql.start()
        postgresql.create_replication_user()
    else:
        synced_from_leader = False
        while not synced_from_leader:
            leader = etcd.current_leader()
            if not leader:
                time.sleep(5)
                continue
            if postgresql.sync_from_leader(leader):
                postgresql.write_recovery_conf(leader)
                postgresql.start()
                synced_from_leader = True
            else:
                time.sleep(5)
else:
    postgresql.write_recovery_conf({"address": "postgres://169.0.0.1:5432"})
    postgresql.start()

while True:
    try:
        syslog.syslog(str(ha.run_cycle()))
    except Exception as e:
        syslog.syslog(str(e))
        postgresql.stop()
        break

    # create replication slots
    if postgresql.is_leader():
        try:
            nodes = etcd.get_client_path("/members?recursive=true")["node"]["nodes"]
        except Exception as e:
            syslog.syslog(str(e))
            postgresql.stop()
            break

        for node in nodes:
            member = node["key"].split('/')[-1]
            if member != postgresql.name:
                postgresql.query("DO LANGUAGE plpgsql $$DECLARE somevar VARCHAR; BEGIN SELECT slot_name INTO somevar FROM pg_replication_slots WHERE slot_name = '%(slot)s' LIMIT 1; IF NOT FOUND THEN PERFORM pg_create_physical_replication_slot('%(slot)s'); END IF; END$$;" % {"slot": member})

    time.sleep(config["loop_wait"])
