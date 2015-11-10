#!/usr/bin/env python

import sys
import os
sys.path.append('..')
from helpers.kms import Kms

config = {}
config["region"] = "us-east-1"
kms = Kms(config)

try:
	base64_ciphertext = sys.argv[1]
	text = kms.decrypt(base64_ciphertext)
	print text
except Exception, e:
	raise e
