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

print m
try:
	raw_body = m.get_body()
	body = json.loads(raw_body)
	name = body["name"]
	print name
except Exception, e:
	raise e
