#!/bin/bash
# helper scrit to run the governor from systemd service
/bin/nohup /var/lib/pgsql/governor/governor.py /var/lib/pgsql/governor/postgres.yml > /tmp/governor.log &