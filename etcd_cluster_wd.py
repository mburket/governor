#!/usr/bin/env python

import subprocess, os

stop_cmd = [ '/bin/systemctl', 'stop', 'etcd' ]
start_cmd = [ '/bin/systemctl', 'start', 'etcd' ]

try:
	cmd = [ '/bin/etcdctl', 'cluster-health' ]
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	out, err = p.communicate()
	lines = out.split(os.linesep)

	for l in lines:
		find = l.find('cluster')
		if find == 0:
			print l
			args = l.split(' ')
			if not args[2] == 'healthy':
				print 'need to restart'
			else:
				print 'healthy'

except Exception, e:
	raise e

