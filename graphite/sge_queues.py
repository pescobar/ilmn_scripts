import os
import time
from subprocess import Popen,PIPE
from socket import socket

# Carbon
CARBON_SERVER='10.1.1.4'
CARBON_PORT=2003
delay=10

# SGE
os.environ["SGE_ROOT"] = "/opt/gridengine"
os.environ["SGE_CELL"] = "default"
os.environ["SGE_ARCH"] = "lx26-amd64"
os.environ["SGE_EXECD_PORT"] = "537"
os.environ["SGE_QMASTER_PORT"] = "536"

def parse_qstat(name):
  p1 = Popen([os.environ["SGE_ROOT"] + "/bin/" + os.environ["SGE_ARCH"] + "/qstat","-g","c"], stdout=PIPE)
  p2 = Popen(["grep", name ], stdin=p1.stdout, stdout=PIPE)
  [ queue, cqload, used, res, avail, total, aoacds, cdsue ] = str.split(p2.communicate()[0])

  if cqload == "-NA-":
    cqload = 0.00

  return (cqload, used, res, avail, total)

#sock = socket()
#try:
#  sock.connect( (CARBON_SERVER,CARBON_PORT) )
#except:
#  print "Coudln't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }

# graphite
while True:
  hostname = os.environ["HOSTNAME"]
  now = int( time.time() )
  queues = str.split(Popen([os.environ["SGE_ROOT"] + "/bin/" + os.environ["SGE_ARCH"] + "/qconf","-sql"], stdout=PIPE).communicate()[0])
  for q in queues:
    lines = []
    (cqload, used,res,avail,total) = parse_qstat(q)
    q = q.replace(".","")
    lines.append("sge." + hostname + "." + q + ".cqload %s %d" % (cqload,now))
    lines.append("sge." + hostname + "." + q + ".used %s %d" % (used,now))
    lines.append("sge." + hostname + "." + q + ".res %s %d" % (res,now))
    lines.append("sge." + hostname + "." + q + ".avail %s %d" % (avail,now))
    lines.append("sge." + hostname + "." + q + ".total %s %d" % (total,now))
    message = '\n'.join(lines) + '\n'
    print message 
    #sock.sendall(message)

  time.sleep(delay)
