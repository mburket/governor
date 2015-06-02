from boto import kms

# docs: http://boto.readthedocs.org/en/latest/ref/kms.html

class Kms:
	def __init__(self, config):	
		self.conn = kms.connect_to_region(config["region"])

	def decrypt(self, ciphertext):
		try:
			text = self.conn.decrypt(ciphertext)
			return text			
		except Exception, e:
			raise e

	def encrypt(self, key_id, plaintext):
		try:
			ciphertext = self.conn.encrypt(key_id, plaintext)
			return ciphertext
		except Exception, e:
			raise e