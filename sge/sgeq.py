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
# check for a(larm), c(onfig), o(rphaned), u(nknown), A(larm), E(rror). a(larm) is sched threshold, A(larm) is suspend thresh
# output string looks something like:
# devel.q@ussd-prd-lncn-2-14.loc BIP   0/0/8          0.00     lx26-amd64    E
output = Popen([os.environ["SGE_ROOT"] + "/bin/" + os.environ["SGE_ARCH"] + "/qstat","-f"], stdout=PIPE).communicate()[0]

# re.findall returns a list of strings
match = re.findall(r"(.*\@.*) BIP.*amd64\s+(.*)", output)
for line in match:
  error = re.findall(r"[aduE]+$", line[1])
  if error:
    print "1 SGE_%s - error is %s" % (line[0], error)
  else:
    print "0 SGE_%s - is OK" % line[0]
