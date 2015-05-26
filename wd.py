#!/usr/bin/env python

import sys, yaml, time, subprocess, os, shutil

from helpers.etcd import Etcd
from helpers.sns import Sns
from socket import gethostname
from subprocess import check_output
from subprocess import call

import syslog

f = open(sys.argv[1], "r")
config = yaml.load(f.read())
f.close()

etcd = Etcd(config["etcd"])
sns = Sns(config["sns"])

# check if receiver is running
def reciver_checker():
	name = "postgres"
	reciever_cmd_str = "postgres: wal receiver process"
	status = False
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
			max_count = 6
			count = 0
			while True:
				reciver_checker_status = reciver_checker()
				print reciver_checker_status
				if reciver_checker_status == False:		
					count += 1
					time.sleep(10)
					if count > max_count:
						# stop governor cleanup the data dir and start the governor
						err_msg = "can't see reciver proc. re-initilizing slave."
						syslog.syslog(err_msg)
						sns.publish(err_msg)
						cmd = [ '/bin/systemctl', 'stop', 'governor' ]
						call(cmd)
						rm('/pg_cluster/pgsql/9.4/data/')
						cmd = [ '/bin/systemctl', 'start', 'governor' ]
						call(cmd)
						break
				else:
					break

			os.unlink(lock_file)

		else:
			# check the age of lockfile if too old remove
			delta = time.time() - os.path.getmtime(lock_file)
			max_age = 60 * 60 * 2
			if delta > max_age:
				os.unlink(lock_file)

	else:
		print "i am the leader"
except Exception, e:
	raise e
