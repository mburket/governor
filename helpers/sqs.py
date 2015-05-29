from boto import sqs
from boto.sqs.message import Message
import json

# docs: 
# http://boto.readthedocs.org/en/latest/ref/sqs.html
# http://boto.readthedocs.org/en/latest/sqs_tut.html#getting-a-queue-by-name

class Sqs:
	def __init__(self, config):	
		self.conn = sqs.connect_to_region(config["region"])
		self.queue = self.conn.get_queue(config["name"])

	def send(self, hostname):
		try:
			msg = { "master": hostname }
			m = Message()
			m.set_body(json.dumps(msg))
			res = self.queue.write(m)
			return res
		except Exception, e:
			raise e

	def read(self):
		try:
			rs = self.queue.get_messages()
			if len(rs) > 0:
				m = rs[0]
				return m
		except Exception, e:
			raise e

	def delete(self, m):
		try:
			res = self.queue.delete_message(m)
			return res
		except Exception, e:
			raise e