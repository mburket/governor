#!/usr/bin/env python

import time, subprocess, urllib2, syslog, json
from urllib import urlencode
from helpers.ec2 import Ec2

ec2 = Ec2()

# vars
base = "https://discovery.etcd.io/"
etcd_cluster = "dde4550af1c3829d876fd969d127eb85"
discovery = base + etcd_cluster
data_dir = "/var/lib/etcd/default.etcd/"
ip = ec2.ec2_ip()
hostname = ec2.ec2_name()
config = { "scope": "batman", "ttl": 30, "host": "127.0.0.1:4001" }
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
cmd = [ "/bin/etcd", "-bind-addr=0.0.0.0:4001", "-addr=" + ip + ":4001", "-discovery=" + discovery, "-name=" + hostname, "-peer-addr=" + ip + ":7001", "-peer-bind-addr=0.0.0.0:7001", "-data-dir=" + data_dir ]
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
		j = json.loads(out)
		test = j['leader']
		print test

		update_leader_key(data)			
		syslog.syslog("i am etcd leader. updated leader key.")

	except Exception, e:
		print str(e)
		syslog.syslog("i am etcd follower.")

	time.sleep(15)
