#!/usr/bin/env python
import os
import re
from subprocess import Popen,PIPE

# check_mk local check for SGE queue states
# calls qstat to detect queues in abnormal states

# configure SGE environment
os.environ["SGE_ROOT"] = "/opt/gridengine"
os.environ["SGE_CELL"] = "default"
os.environ["SGE_ARCH"] = "lx26-amd64"
os.environ["SGE_EXECD_PORT"] = "537"
os.environ["SGE_QMASTER_PORT"] = "536"


def parse_qstat(queue_state):
  if(queue_state == "disabled"):
    p1 = Popen([os.environ["SGE_ROOT"] + "/bin/" + os.environ["SGE_ARCH"] + "/qstat","-f","-qs","d"], stdout=PIPE)
  elif(queue_state == "alarm"):
    p1 = Popen([os.environ["SGE_ROOT"] + "/bin/" + os.environ["SGE_ARCH"] + "/qstat","-f","-qs","a"], stdout=PIPE)
  else:
    return
  p2 = Popen(["awk", "/lx/{print $1}"], stdin=p1.stdout, stdout=PIPE)
  output2 = p2.communicate()[0]
  
  return (re.sub(r'\.lo.*', '', output2))

disabled=parse_qstat("disabled")
dqueue=disabled.split()

alarm=parse_qstat("alarm")
aqueue=alarm.split()

# check output is of the form: status item_name performance_data check_output
# where status: 0 = OK, 1 = WARNING, 2 = CRITICAL, 3 = UNKNOWN
for queue in dqueue:
  print "1 SGE_disabled-%s - SGE queue %s is disabled" % (queue,queue)

for queue in aqueue:
  print "2 SGE_alarm-%s - SGE queue %s is in alarm" % (queue,queue)
