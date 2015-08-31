#!/usr/bin/env python
import subprocess
import re

cmd = [ "barman", "list-backup", "all" ]
try:
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, err = p.communicate()
    if len(err) > 0:
        raise Exception(str(err))
    # print out
    it = iter(out.splitlines())
    for i in it:
        # print i
        if "FAILED" in i:
            args = re.split('\s+', i)
            cmd = [ "barman", "delete", args[0], args[1] ]
            subprocess.call(cmd)
except Exception as e:
    print str(e)
    raise e
