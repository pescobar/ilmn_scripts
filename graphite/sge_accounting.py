# basic idea is to tail the accounting log file
# ($SGE_ROOT/default/common/accounting)
# and feed data to carbon (part of graphite package) for trend 
# analysis

# naming scheme: sge.qname.user.jobid.metrics
# where metrics is all the stuff we care about

# sge accounting file fields:
#
# qname:hostname:group:owner:job_name:job_number:account:priority:
# submission_time:start_time:end_time:failed:exit_status:ru_wallclock:
# ru_utime:ru_stime:ru_maxrss:ru_ixrss:ru_ismrss:ru_idrss:ru_isrss:
# ru_minflt:ru_majflt:ru_nswap:ru_inblock:ru_oublock:ru_msgsnd:ru_msgrcv:
# ru_nsignals:ru_nvcsw:ru_nivcsw:project:department:granted_pe:slots:
# task_number:cpu:mem:io:category:iow:pe_taskid:maxvmem:arid:
# ar_submission_time

import time
import os
import platform
import subprocess
from socket import socket

CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003

def get_sge_accounting():
  return lines

sock=socket()
try:
  sock.connect ( (CARBON_SERVER,CARBON_PORT) )
except:
  print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
  sys.exit(1)

while True:
  now = int ( time.time() )
  lines = []

