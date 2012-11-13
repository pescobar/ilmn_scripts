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


# check_mk_agent closes stdin which breaks this python construct - how to get around that?
def parse_qstat(queue_state):
  if(queue_state == "disabled"):
    p1 = Popen([os.environ["SGE_ROOT"] + "/bin/" + os.environ["SGE_ARCH"] + "/qstat","-f","-qs","d"], stdout=PIPE)
  elif(queue_state == "alarm"):
    p1 = Popen([os.environ["SGE_ROOT"] + "/bin/" + os.environ["SGE_ARCH"] + "/qstat","-f","-qs","a"], stdout=PIPE)
  else:
    return

  output = p1.communicate()[0]

  # output string looks something like:
  # devel.q@ussd-prd-lncn-2-14.loc BIP   0/0/8          0.00     lx26-amd64    d

  match = re.search(r'.*lx26-amd64.*', output)
  if match:
    queue_list = re.sub(r'\.lo.*', '', match.group(0))
    #return (re.sub(r'\@', '_', queue_list))
    return (queue_list)
  else:
    return



# check output is of the form: status item_name performance_data check_output
# where status: 0 = OK, 1 = WARNING, 2 = CRITICAL, 3 = UNKNOWN
disabled = parse_qstat("disabled")
if disabled:
  dqueue = disabled.split()
  for queue in dqueue:
    print "1 SGE_disabled-%s - SGE queue %s is disabled" % (queue,queue)

alarm = parse_qstat("alarm")
if alarm:
  aqueue= alarm.split()
  for queue in aqueue:
    print "2 SGE_alarm-%s - SGE queue %s is in alarm" % (queue,queue)
