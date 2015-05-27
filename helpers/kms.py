from boto import kms

# docs: http://boto.readthedocs.org/en/latest/ref/kms.html

class Kms:
	def __init__(self, config):	
		self.conn = sns.connect_to_region(config["region"])
		self.arn = config["arn"]

	def decrypt(self, ciphertext):
		pass