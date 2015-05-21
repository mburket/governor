#!/usr/bin/env python

import sys, yaml, time, subprocess, os, shutil

from helpers.etcd import Etcd
from socket import gethostname
from subprocess import check_output
from subprocess import call

f = open(sys.argv[1], "r")
config = yaml.load(f.read())
f.close()

etcd = Etcd(config["etcd"])

# check if receiver is running
def reciver_checker():
	name = "postgres"
	reciever_cmd_str = "postgres: wal receiver process"
	status = False
	try:
		try:
			pids = map(str,check_output(["pidof",name]).split())
			for p in pids:
				p_file = "/proc/%s/cmdline" % (p)
				f = open(p_file, "r")
				cmdline = f.read()
				f.close()
				find = cmdline.find(reciever_cmd_str)
				if find == 0:
					status = True
					break

		except Exception, e:
			return status

		return status	

	except Exception, e:
		raise e

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

# main
try:
	# determine that we are slave
	if etcd.current_leader()["hostname"] != gethostname().split('.')[0]:
		# determine if reciver is not running
		max_count = 6
		count = 0
		while True:
			if reciver_checker() == False:
				count += 1
				time.sleep(10)
				if count > max_count:
					# stop governor cleanup the data dir and start the governor				
					cmd = [ '/bin/systemctl', 'stop', 'governor' ]
					call(cmd)
					rm('/pg_cluster/pgsql/9.4/data/')
					cmd = [ '/bin/systemctl', 'start', 'governor' ]
					call(cmd)
					break
			else:
				break

	else:
		print "i am the leader"
except Exception, e:
	raise e
