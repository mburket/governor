from boto import sqs

# docs: http://boto.readthedocs.org/en/latest/ref/sqs.html

class Sqs:
	def __init__(self, config):	
		self.conn = sqs.connect_to_region(config["region"])
		self.arn = config["arn"]

	def send(self):
		pass

	def receive(self):
		pass