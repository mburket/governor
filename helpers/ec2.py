#!/usr/bin/env python

import urllib2

# methods
# get instance id from EC2 api

class Ec2:
    def __init__(self):
        pass

    def ec2_ip(slef):
        url = "http://169.254.169.254/latest/meta-data/local-ipv4"
        try:
            return urllib2.urlopen(url).read()
        except (urllib2.HTTPError, urllib2.URLError) as e:
            raise e

    def ec2_name(self):
        url = "http://169.254.169.254/latest/meta-data/hostname"
        try:
            return urllib2.urlopen(url).read()
        except (urllib2.HTTPError, urllib2.URLError) as e:
            raise e