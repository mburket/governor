from boto import kms
import base64

# docs: http://boto.readthedocs.org/en/latest/ref/kms.html

class Kms:
	def __init__(self, config):	
		self.conn = kms.connect_to_region(config["region"])

	def decrypt(self, base64_ciphertext):
		try:
			res = self.conn.decrypt(base64.decode(base64_ciphertext))
			return res["Plaintext"]
		except Exception, e:
			raise e

	def encrypt(self, key_id, plaintext):
		try:
			res = self.conn.encrypt(key_id, plaintext)
			return base64.b64encode(res["CiphertextBlob"])
		except Exception, e:
			raise e