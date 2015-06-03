#!/usr/bin/env python

import subprocess


try:
	cmd = [ '/bin/etcdctl', 'cluster-health' ]
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	out, err = p.communicate()
	print out
		
	outIter = iter(out)
	for i in outIter:
		print i

except Exception, e:
	raise e

