import os
import time
from subprocess import Popen,PIPE
from xml.dom.minidom import parseString
from socket import socket

# Carbon
CARBON_SERVER='10.12.36.90'
CARBON_PORT=2003
delay=60

sock = socket()
try:
  sock.connect( (CARBON_SERVER,CARBON_PORT) )
except:
  print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
  sys.exit(1)

def getDirs():
  # enumerate directories with quotas
  dirList = []
  p1 = Popen(["/usr/bin/isi","quota","get","--export"], stdout=PIPE).communicate()[0]
  doc = parseString(p1)
  taglist = doc.getElementsByTagName('path')
  for item in range(taglist.length):
    xmlTag = taglist.item(item).toxml()
    xmlData = xmlTag.replace('<','').replace('>','').replace('path','')
    dirList.append(xmlData)

  dirList = list(set(dirList)) # uniq
  return(dirList)

def getQuotas(dir):
  quotaList = []
  p1 = Popen(["isi","quota","get","--path=" + dir], stdout=PIPE)
  p2 = Popen(["grep","^directory"], stdin=p1.stdout, stdout=PIPE)
  list = str.split(p2.communicate()[0])

  try:
    hard = list[3]
  except:
    hard = "0T"

  try:
    used = list[6]
  except:
    used = "0T"

  # TODO: convert human-readable to bytes (and percents?)
  if hard.find('T') > 0:
    hard = hard.replace('T','')
    hard = float(hard)
    hard = hard * 1099511627776
  elif hard.find('G') > 0:
    hard = hard.replace('G','')
    hard = float(hard)
    hard = hard * 1073741824
  elif hard.find('M') > 0:
    hard = hard.replace('M','')
    hard = float(hard)
    hard = hard * 1048576
  elif hard.find('K') > 0:
    hard = hard.replace('K','')
    hard = float(hard)
    hard = hard * 1024

  if used.find('T') > 0:
    used = used.replace('T','')
    used = float(used)
    used = used * 1099511627776
  elif used.find('G') > 0:
    used = used.replace('G','')
    used = float(used)
    used = used * 1073741824
  elif used.find('M') > 0:
    used = used.replace('M','')
    used = float(used)
    used = used * 1048576
  elif used.find('K') > 0:
    used = used.replace('K','')
    used = float(used)
    used = used * 1024

  return(hard,used)


# graphite
while True:
  now = int( time.time() )
  lines = []
  p1 = Popen(["/usr/bin/isi","status"], stdout=PIPE)
  p2 = Popen(["awk","/Cluster Name/{print $3}"], stdin=p1.stdout, stdout=PIPE)
  clusterName = p2.communicate()[0]
  clusterName = clusterName.rstrip("\n\r") # chomp
  dirs = getDirs()
  for d in dirs:
    (hard,used) = getQuotas(d)
    d = d.replace("/","_")
    lines.append("isilon." + clusterName + "." + d + ".hard %s %d" % (hard,now))
    lines.append("isilon." + clusterName + "." + d + ".used %s %d" % (used,now))
    message = '\n'.join(lines) + '\n'
    print message 
    sock.sendall(message)
  time.sleep(delay)
