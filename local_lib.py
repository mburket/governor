#!/usr/bin/env python

import urllib2

# methods
# get instance id from EC2 api
def ec2_ip():
    url = "http://169.254.169.254/latest/meta-data/local-ipv4"
    try:
        return urllib2.urlopen(url).read()
    except (urllib2.HTTPError, urllib2.URLError) as e:
        raise e

def ec2_name():
    url = "http://169.254.169.254/latest/meta-data/hostname"
    try:
        return urllib2.urlopen(url).read()
    except (urllib2.HTTPError, urllib2.URLError) as e:
        raise e        