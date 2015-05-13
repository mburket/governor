#!/bin/bash
/bin/nohup /var/lib/pgsql/governor/governor.py /var/lib/pgsql/governor/postgres.yml > /tmp/governor.log &