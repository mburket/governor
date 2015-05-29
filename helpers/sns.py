from boto import sns
from socket import gethostname

# docs: http://boto.readthedocs.org/en/latest/ref/sns.html

class Sns:
	def __init__(self, config):	
		self.conn = sns.connect_to_region(config["region"])
		self.arn = config["arn"]
		self.hostname = gethostname()

	def publish(self, message):
		try:
			self.conn.publish(self.arn, message)
		except Exception, e:
			raise e
		