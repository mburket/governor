#!/bin/bash
# helper scrit to run the governor from systemd service
# /bin/nohup /var/lib/pgsql/governor/governor.py /var/lib/pgsql/governor/postgres.yml > /tmp/governor.log &
/var/lib/pgsql/governor/governor_no_auto.py /var/lib/pgsql/governor/postgres.yml
