import urllib2, json, os, time
import syslog
from urllib import urlencode
import helpers.errors

class Etcd:
    def __init__(self, config):
        self.http_timeout = 3
        self.scope = config["scope"]
        self.ttl = config["ttl"]
        self.get_etcd_leader(config["host"])
        self.etcd_local = config["host"]        

    def get_etcd_leader(self, host):
        attempts = 0
        max_attempts = 3

        while True:
            try:
                url = "http://%s/v2/keys/service/batman/etcd_leader" % (host)
                res = json.loads(urllib2.urlopen(url, None, self.http_timeout).read())
                self.host = res["node"]["value"]
                break
            except (urllib2.HTTPError, urllib2.URLError) as e:
                attempts += 1
                if attempts < max_attempts:
                    time.sleep(3)
                else:           
                    self.host = host

    def get_client_path(self, path, max_attempts=1):
        attempts = 10
        response = None

        while True:
            try:
                response = urllib2.urlopen(self.client_url(path), None, self.http_timeout).read()
                break
            except (urllib2.HTTPError, urllib2.URLError) as e:
                self.get_etcd_leader(self.etcd_local)                              

                if attempts < max_attempts:                    
                    syslog.syslog("Failed to return %s, trying again. (%s of %s)" % (path, attempts, max_attempts))
                    time.sleep(3)
                else:
                    syslog.syslog(str(e))
                    raise e

                attempts += 1
        try:
            return json.loads(response)
        except ValueError:
            return response

    def put_client_path(self, path, data):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(self.client_url(path), data=urlencode(data).replace("false", "False"))
        request.get_method = lambda: 'PUT'
        opener.open(request)

    def client_url(self, path):
        return "http://%s/v2/keys/service/%s%s" % (self.host, self.scope, path)

    def current_leader(self):
        try:
            hostname = self.get_client_path("/leader")["node"]["value"]
            address = self.get_client_path("/members/%s" % hostname)["node"]["value"]

            return {"hostname": hostname, "address": address}
        except urllib2.HTTPError as e:
            if e.code == 404:
                return None
            raise helpers.errors.CurrentLeaderError("Etcd is not responding properly")

    def members(self):
        try:
            members = []

            r = self.get_client_path("/members?recursive=true")
            for node in r["node"]["nodes"]:
                members.append({"hostname": node["key"].split('/')[-1], "address": node["value"]})

            return members
        except urllib2.HTTPError as e:
            if e.code == 404:
                return None
            raise helpers.errors.CurrentLeaderError("Etcd is not responding properly")

    def touch_member(self, member, connection_string):
        self.put_client_path("/members/%s" % member, {"value": connection_string})

    def take_leader(self, value):
        return self.put_client_path("/leader", {"value": value, "ttl": self.ttl}) == None

    def attempt_to_acquire_leader(self, value):
        try:
            return self.put_client_path("/leader", {"value": value, "ttl": self.ttl, "prevExist": False}) == None
        except urllib2.HTTPError as e:
            if e.code == 412:
                syslog.syslog("Could not take out TTL lock: %s" % e)
            return False

    def update_leader(self, value):
        try:
            self.put_client_path("/leader", {"value": value, "ttl": self.ttl, "prevValue": value})
        except urllib2.HTTPError:
            syslog.syslog(syslog.LOG_ERR,"Error updating TTL on ETCD for primary.")
            return False

    def leader_unlocked(self):
        try:
            self.get_client_path("/leader")
            return False
        except urllib2.HTTPError as e:
            if e.code == 404:
                return True
            return False
        except ValueError as e:
            return False

    def am_i_leader(self, value):
        #try:
           reponse = self.get_client_path("/leader")
           syslog.syslog("Lock owner: %s; I am %s" % (reponse["node"]["value"], value))
           return reponse["node"]["value"] == value
        #except Exception as e:
            #return False

    def race(self, path, value):
        try:
            return self.put_client_path(path, {"prevExist": False, "value": value}) == None
        except urllib2.HTTPError:
            return False
