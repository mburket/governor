#!/usr/bin/env python

import sys, os, yaml, time, urllib2, atexit, syslog
from socket import gethostname
from helpers.postgresql import Postgresql
from helpers.kms import Kms
from helpers.ec2 import Ec2

f = open(sys.argv[1], "r")
config = yaml.load(f.read())
f.close()

# kms is needed to decryot config
kms = Kms(config["kms"])

# configure the postgres
ec2 = Ec2()
our_ip = ec2.ec2_ip()
hostname = gethostname()
config["postgresql"]["name"] = hostname.split('.')[0]
config["postgresql"]["listen"] = our_ip + ":" + str(config["postgresql"]["port"])
postgresql = Postgresql(config["postgresql"], kms, hostname)

# start postgres
postgresql.start()
