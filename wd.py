#!/usr/bin/env python

import sys, yaml, time, subprocess, os, shutil, syslog, tarfile

from helpers.etcd import Etcd
from helpers.sns import Sns
from helpers.kms import Kms
from helpers.ec2 import Ec2
from helpers.postgresql import Postgresql
from socket import gethostname



os.environ['PATH'] += os.pathsep + '/usr/sbin'
governor_start_cmd = [ '/bin/systemctl', 'start', 'governor' ]
governor_stop_cmd = [ '/bin/systemctl', 'stop', 'governor' ]

f = open(sys.argv[1], "r")
config = yaml.load(f.read())
f.close()

etcd = Etcd(config["etcd"])
kms = Kms(config["kms"])
sns = Sns(config["sns"], kms)
# configure the postgres
ec2 = Ec2()
our_ip = ec2.ec2_ip()
hostname = gethostname()
config["postgresql"]["listen"] = our_ip + ":" + str(config["postgresql"]["port"])
config["postgresql"]["name"] = hostname.split('.')[0]
postgresql = Postgresql(config["postgresql"], kms, hostname)

# vars
data_dir = "/pg_cluster/pgsql/9.4/data/"
archive_file = "/pg_cluster/pgsql/9.4/data.tar.gz"

# make a tar.gz backup of a directory
def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

# check if receiver is running
def receiver_checker():
	name = "postgres"
	name_backup = "pg_basebackup"
	reciever_cmd_str = "postgres: wal receiver process"
	status = False
	try:
		pids = map(str, subprocess.check_output(["pidof", name]).split())
		if isinstance(pids, list):
			for p in pids:
				p_file = "/proc/%s/cmdline" % (p)
				f = open(p_file, "r")
				cmdline = f.read()
				f.close()
				find = cmdline.find(reciever_cmd_str)
				if find == 0:
					status = True
					return status
                    			break

	except Exception, e:
		try:
			# check if we are in restore phase
			pids = map(str, subprocess.check_output(["pidof", name_backup]).split())
			if isinstance(pids, list):
				status = True
				return status
			else:
				return status
		except Exception, e:
			return status

# rm everything in a folder
def rm(folder):
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception, e:
			raise e

# make lock file
def mk_lock_file(lock):
    f = open(lock, 'w')
    f.write('')
    f.close()

# main
lock_file = "/tmp/wd.lck"

try:
	# determine that we are slave
	if not etcd.current_leader()["hostname"] == gethostname().split('.')[0]:
		if not os.path.isfile(lock_file):
			mk_lock_file(lock_file)

			# determine if reciver is not running
			receiver_checker_status = receiver_checker()
			if receiver_checker_status == False receiver_checker_status == None:
				# stop governor cleanup the data dir and start the governor
				err_msg = "slave is out of sync on %s, re-initilizing" % (hostname)
				syslog.syslog(err_msg)
				sns.publish(err_msg)
				# re-initilize
				subprocess.call(governor_stop_cmd)
				# backup the file before blowing away the data dir
				try:
					os.unlink(archive_file)
					# make_tarfile(archive_file, data_dir)
				except Exception as e:
					# make_tarfile(archive_file, data_dir)
                    			pass

				rm(data_dir)
				subprocess.call(governor_start_cmd)

			os.unlink(lock_file)

		else:
			# check the age of lockfile if too old remove
			delta = time.time() - os.path.getmtime(lock_file)
			max_age = 60 * 60 * 2
			if delta > max_age:
				os.unlink(lock_file)

	else:
		print "i am the leader"
        query = "select * from pg_stat_replication;"
except Exception, e:
	subprocess.call(governor_start_cmd)
