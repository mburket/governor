import logging
from boto import route53

# docs: http://boto.readthedocs.org/en/latest/ref/route53.html#module-boto.route53.record

class Rt53:
	def __init__(self, config):
		self.ttl = 15
		conn = route53.connect_to_region(config["region"])
		self.zone = conn.get_zone(config["zone"])
		self.domain = config["zone"]
		self.stack = config["stack"]
		self.our_ip = config["our_ip"]

	def update(self):
		key = "database-%s.%s" % (self.stack, self.domain)
		try:
			self.zone.update_a(key, self.our_ip, ttl = self.ttl)
		except AttributeError:
			try:
				self.zone.add_a(key, self.our_ip, ttl = self.ttl)
			except Exception, e:
				raise e