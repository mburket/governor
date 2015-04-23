import logging
from boto import route53

# docs: http://boto.readthedocs.org/en/latest/ref/route53.html#module-boto.route53.record

class rt53:
	def __init__(self, config):
		self.ttl = 15
		conn = route53.connect_to_region(config["region"])
		self.zone = conn.get_zone(config["zone"])
		self.domain = config["zone"]

	def update(self, args):
		record = self.zone.get_a(args["key"])
		# add_a(name, value, ttl=None, identifier=None, comment='')
		# update_a(name, value, ttl=None, identifier=None, comment='')
		value = "database.prod.%s" % (self.domain)
		try:
			self.zone.update_a(args["key"], args['value'], ttl = self.ttl)
		except AttributeError:
			try:
				self.zone.add_a(args["key"], args['value'], ttl = self.ttl)
			except Exception, e:
				raise e