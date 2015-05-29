#!/usr/bin/env python

import sys, yaml, time, subprocess, os, shutil, json

from helpers.sqs import Sqs
from helpers.sns import Sns

f = open(sys.argv[1], "r")
config = yaml.load(f.read())
f.close()

sns = Sns(config["sns"])
sqs = Sqs(config["sqs"])

m = sqs.read()

try:
	raw_body = m.get_body()
	body = json.loads(raw_body)
	master = body["master"]
	cmd = [ "/bin/barman", "backup", master ]
	print cmd
except Exception, e:
	raise e
