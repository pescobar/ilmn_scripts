#!/usr/bin/env python
import os
import daemon
import time
from subprocess import Popen,PIPE
from socket import socket

# Carbon
CARBON_SERVER='10.12.36.90'
CARBON_PORT=2003
delay=60

# SGE
try:
  '''if this is unset chances are no other SGE vars are set either'''
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

# daemonize
d = daemon.DaemonContext()
d.open()

def parse_qstat(name):
  p1 = Popen([os.environ["SGE_ROOT"] + "/bin/" + os.environ["SGE_ARCH"] + "/qstat","-u",name,"-s","r"], stdout=PIPE)
  p2 = Popen(["grep", name ], stdin=p1.stdout, stdout=PIPE)
  output = p2.communicate()[0]
  print output
  output = output.split()

  if not output:
    slots = 0

  return (slots)

# graphite
while True:
  sock = socket()
  try:
    sock.connect( (CARBON_SERVER,CARBON_PORT) )
  except:
    print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }

  hostname = os.environ["HOSTNAME"]
  hostname = hostname.replace(".","_")
  now = int( time.time() )
  users = str.split(Popen([os.environ["SGE_ROOT"] + "/bin/" + os.environ["SGE_ARCH"] + "/qconf","-suserl"], stdout=PIPE).communicate()[0])
  for u in users:
    lines = []
    slots = parse_qstat(u)
    lines.append("sge." + hostname + "." + u + ".slots %s %d" % (slots,now))
    message = '\n'.join(lines) + '\n'
    sock.send(message)
  time.sleep(delay)
