#!/usr/bin/env python
import os
import time
from subprocess import Popen,PIPE
from socket import socket

# Carbon
CARBON_SERVER='ussd-prd-lngr01.illumina.com'
CARBON_PORT=2003

# SGE
try:
  '''if this is unset, chances are no other SGE env vars are'''
  os.environ["SGE_ROOT"]
except:
  os.environ["SGE_ROOT"] = "/opt/gridengine"
  os.environ["SGE_CELL"] = "default"
  os.environ["SGE_ARCH"] = "lx26-amd64"
  os.environ["SGE_EXECD_PORT"] = "537"
  os.environ["SGE_QMASTER_PORT"] = "536"

sge_root = os.environ["SGE_ROOT"]
sge_cell = os.environ["SGE_CELL"]
sge_arch = os.environ["SGE_ARCH"]

def parse_qstat(name):
  p1 = Popen([sge_root + "/bin/" + sge_arch + "/qstat","-g","c"], stdout=PIPE)
  p2 = Popen(["grep", name ], stdin=p1.stdout, stdout=PIPE)
  [ queue, cqload, used, res, avail, total, aoacds, cdsue ] = str.split(p2.communicate()[0])

  if cqload == "-NA-":
    cqload = 0.00

  return (cqload, used, res, avail, total)

# graphite
sock = socket()
try:
  sock.connect( (CARBON_SERVER,CARBON_PORT) )
except:
  print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
  sys.exit(1)

#hostname = os.environ["HOSTNAME"]
hostname = "ussd-prd-qm01.illumina.com"
hostname = hostname.replace(".","_")
now = int( time.time() )
queues = str.split(Popen([sge_root + "/bin/" + sge_arch + "/qconf","-sql"], stdout=PIPE).communicate()[0])
for q in queues:
  lines = []
  (cqload, used, res, avail, total) = parse_qstat(q)
  q = q.replace(".","_")
  lines.append("sge." + hostname + ".queue." + q + ".cqload %s %d" % (cqload,now))
  lines.append("sge." + hostname + ".queue." + q + ".used %s %d" % (used,now))
  lines.append("sge." + hostname + ".queue." + q + ".res %s %d" % (res,now))
  lines.append("sge." + hostname + ".queue." + q + ".avail %s %d" % (avail,now))
  lines.append("sge." + hostname + ".queue." + q + ".total %s %d" % (total,now))
  message = '\n'.join(lines) + '\n'
  print message
  sock.send(message)
