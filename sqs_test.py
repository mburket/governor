#!/usr/bin/env python

from helpers.sqs import Sqs
from socket import gethostname

config = {
	"region": "us-east-1",
	"name": "barman-dbha-queue"
}

sqs = Sqs(config)

hostname = gethostname()
res = sqs.send(hostname)
print res