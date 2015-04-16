#!/usr/bin/env python

# import sys, os, yaml, time, urllib2, atexit
# import logging

import local_lib
from helpers.etcd import Etcd
import time
from subprocess import call

# vars
base = "https://discovery.etcd.io/"
etcd_cluster = "f71aca0ff87c3e7f9dcd9838266b7631"
discovery = base + etcd_cluster
data_dir = "/var/lib/etcd/default.etcd/"
ip = local_lib.ec2_ip()
hostname = local_lib.ec2_name()
config = { "scope": "batman", "ttl": 45, "host": "127.0.0.1:4001" }
etcd = Etcd(config)

# main
cmd = "/bin/etcd -bind-addr=0.0.0.0:4001 -addr=" + ip + ":4001 -discovery=" + discovery + " -name=" + hostname + " -peer-addr=" + ip + ":7001 -peer-bind-addr=0.0.0.0:7001 -peer-heartbeat-interval=100 -peer-election-timeout=500&"
call(cmd)
try:
	# update the etcd leader key
	etcd.put_client_path("/etcd_leader", { "host": ip, "ttl": config["ttl"] })
	time.sleep(30)
except Exception, e:
	pass
