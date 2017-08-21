#!/usr/bin/python
# ~*~ coding: utf-8 ~*~
# Author: ThinhLP
# Check certificate expired day, if day remain < 45, then warning...
import subprocess
from datetime import datetime
import sys
import argparse

parser = argparse.ArgumentParser(description='For check expired day of certificate')
parser.add_argument('-d', '--domain', help='Domain name', required=True)
parser.add_argument('-w', '--warning', help='number Warning', required=False)
parser.add_argument('-c', '--critical', help='number Critical', required=False)
args = parser.parse_args()

## Set environment ##
if args.warning:
    alert_day_warning = int(args.warning)
else:
    alert_day_warning = 45

if args.critical:
    alert_day_critical = int(args.critical)
else:
    alert_day_critical = 55

domain_name = args.domain

CMD = "curl --insecure -Iv https://" + domain_name + " 2>&1 | awk 'BEGIN { cert=0 } /^\* SSL connection/ { cert=1 } /^\*/ { if (cert) print }'|grep 'expire date'"
info = subprocess.Popen(CMD, shell=True, stdout = subprocess.PIPE)
rs_cmd = info.stdout.readline().split(' ')
exp_date =  "%s %s %s" % (rs_cmd[3], rs_cmd[4], rs_cmd[6])

## convert exp_date to type datetime
exp_datetime_object = datetime.strptime(exp_date, '%b %d %Y').date()

cur_datetime = datetime.now().strftime('%b %d %Y')
cur_datetime_object = datetime.strptime(cur_datetime, '%b %d %Y').date()
day_remain = int((exp_datetime_object - cur_datetime_object).days)

# if day_remain < 45day, then alert.
if day_remain <= alert_day_critical:
    print "Critical Certificate %s  will be expire day in %s" % (domain_name, day_remain)
    sys.exit(2)
elif day_remain <= alert_day_warning:
    print "Warning Certificate %s will be expire day in %s" % (domain_name, day_remain)
    sys.exit(1)
else:
    print "OK Certificate %s in %s days" % (domain_name, day_remain)
    sys.exit(0)
