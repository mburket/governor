#!/usr/bin/env python

import subprocess, os


try:
	cmd = [ '/bin/etcdctl', 'cluster-health' ]
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	out, err = p.communicate()
	print out
	lines = out.split(os.linesep)

	for l in lines:
		find = l.find('cluster')
		if find == 0:
			print l

except Exception, e:
	raise e

