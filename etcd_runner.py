#!/usr/bin/env python

# import sys, os, yaml, time, urllib2, atexit
# import logging

from helpers.etcd import Etcd
import local_lib

# main
etcd_ip = local_lib.ec2_ip()
print etcd_ip

# test that etcd exists
cmd = "/bin/etcd"
try:
	pass
except Exception, e:
	raise e

# run etcd




# keep updating the etcd_leader key every 30 seconds
