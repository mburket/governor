#!/usr/bin/env python

import time
import subprocess
import urllib2
from urllib import urlencode

from helpers.ec2 import Ec2

ec2 = Ec2()

# vars
base = "https://discovery.etcd.io/"
etcd_cluster = "168ae83577546eb25f2f9c117511730a"
discovery = base + etcd_cluster
data_dir = "/var/lib/etcd/default.etcd/"
ip = ec2.ec2_ip()
hostname = ec2.ec2_name()
config = { "scope": "batman", "ttl": 45, "host": "127.0.0.1:4001" }
host = ip + ":4001"

# main
# run etcd
cmd = [ "/bin/etcd", "-bind-addr=0.0.0.0:4001", "-addr=" + ip + ":4001", "-discovery=" + discovery, "-name=" + hostname, "-peer-addr=" + ip + ":7001", "-peer-bind-addr=0.0.0.0:7001", "-peer-heartbeat-interval=100", "-peer-election-timeout=500" ]
try:
	subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
except Exception, e:
	raise e

# update leader key
while True:
	try:
		data = { "value": host, "ttl": config["ttl"] }
		path = "http://%s/v2/keys/service/batman/etcd_leader" % (config["host"])
		opener = urllib2.build_opener(urllib2.HTTPHandler)
		request = urllib2.Request(path, data=urlencode(data).replace("false", "False"))
		request.get_method = lambda: 'PUT'
		opener.open(request)			
		print "i am etcd leader. updated leader key."
	except (urllib2.HTTPError, urllib2.URLError) as e:
		print "i am etcd follower."

	time.sleep(30)		
