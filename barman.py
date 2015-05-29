#!/usr/bin/env python

import sys, yaml, time, subprocess, os, shutil, json

from helpers.sqs import Sqs
from helpers.sns import Sns

f = open(sys.argv[1], "r")
config = yaml.load(f.read())
f.close()

sns = Sns(config["sns"])
sqs = Sqs(config["sqs"])

try:
	m = sqs.read()
	raw_body = m.get_body()
	body = json.loads(raw_body)
	master = body["master"]
	sns.publish('starting backup in 10 minutes...')
	sqs.delete(m)
	time.sleep(600)
	cmd = [ "/bin/barman", "backup", master ]
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	out, err = p.communicate()
	sns.publish(out)
except Exception, e:
	pass
