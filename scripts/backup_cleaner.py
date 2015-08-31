#!/usr/bin/env python
import subprocess


cmd = [ "barman", "list-backup", "all" ]
try:
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, err = p.communicate()
    if len(err) > 0:
        raise Exception(str(err))
    for i in out:
        print i
except Exception as e:
    print str(e)
    raise e
