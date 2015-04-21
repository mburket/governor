import logging
from boto import route53

class rt53:
	def __init__(self, config):
		self.region = config["region"]
		self.conn = route53.connect_to_region(self.region)
		self.zone = self.conn.get_zone(config["zone"])

	