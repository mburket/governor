#!/usr/bin/env python

import sys, yaml, time, subprocess, os, shutil

from helpers.sqs import Sqs
from helpers.sns import Sns

f = open(sys.argv[1], "r")
config = yaml.load(f.read())
f.close()

sns = Sns(config["sns"])
sqs = Sqs(config["sqs"])

m = sqs.read()

print m
print m.get_body()