#!/usr/bin/env python

import time
import subprocess
import urllib2
from urllib import urlencode
import syslog

from helpers.ec2 import Ec2

ec2 = Ec2()

# vars
base = "https://discovery.etcd.io/"
etcd_cluster = "7678a1a67ab72a04852aecd08dbfeaf3"
discovery = base + etcd_cluster
data_dir = "/var/lib/etcd/default.etcd/"
ip = ec2.ec2_ip()
hostname = ec2.ec2_name()
config = { "scope": "batman", "ttl": 45, "host": "127.0.0.1:4001" }
host = ip + ":4001"

# subs
def update_leader_key(data):
	try:
		path = "http://%s/v2/keys/service/batman/etcd_leader" % (config["host"])
		opener = urllib2.build_opener(urllib2.HTTPHandler)
		request = urllib2.Request(path, data=urlencode(data).replace("false", "False"))
		request.get_method = lambda: 'PUT'
		opener.open(request)		
	except Exception, e:
		raise e

# main
# run etcd
cmd = [ "/bin/etcd", "-bind-addr=0.0.0.0:4001", "-addr=" + ip + ":4001", "-discovery=" + discovery, "-name=" + hostname, "-peer-addr=" + ip + ":7001", "-peer-bind-addr=0.0.0.0:7001", "-peer-heartbeat-interval=100", "-peer-election-timeout=500", "-data-dir=" + data_dir ]
print cmd

try:
	subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
except Exception, e:
	print str(e)

# update leader key
while True:
	try:
		data = { "value": host, "ttl": config["ttl"] }
		leader_url = "http://%s/v2/stats/leader" % (config["host"])
		print leader_url

		# test for etcd cluster leader
		req = urllib2.Request(leader_url)
		r = urllib2.urlopen(req)
		out = r.read()
		print out
		j = json.loads(out)
		print j
		test = j['leader']
		print test

		update_leader_key(data)			
		syslog.syslog("i am etcd leader. updated leader key.")

	except Exception, e:
		print str(e)
		syslog.syslog("i am etcd follower.")

	time.sleep(30)
