#!/usr/bin/env python

# import sys, os, yaml, time, urllib2, atexit
# import logging

from helpers.etcd import Etcd
import local_lib

# main
# vars
discovery = "https://discovery.etcd.io/f71aca0ff87c3e7f9dcd9838266b7631"
data_dir = "/var/lib/etcd/default.etcd/"
etcd_ip = local_lib.ec2_ip()
etcd_name = ocal_lib.ec2_name()
#print etcd_ip

# test that etcd exists
cmd = "/bin/etcd -bind-addr=0.0.0.0:4001 -addr=" + etcd_ip + ":4001 -discovery=" + discovery + " -name=" + etcd_name
print cmd
try:
	pass
except Exception, e:
	raise e

# run etcd




# keep updating the etcd_leader key every 30 seconds
