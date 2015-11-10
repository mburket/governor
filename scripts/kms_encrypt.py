#!/usr/bin/env python

import sys 
import os
sys.path.append('..')
from helpers.kms import Kms

config = {}
config["region"] = "us-east-1"
kms = Kms(config)

try:
	key_id = sys.argv[1]
	text = sys.argv[2]
	ciphertext = kms.encrypt(key_id, text)
	print ciphertext
except Exception, e:
	raise e