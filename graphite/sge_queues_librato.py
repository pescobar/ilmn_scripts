#!/usr/bin/env python
import os
import time
from subprocess import Popen,PIPE
from socket import socket
import urllib2
import base64

# librato using pycurl
username='toddjhartmann@gmail.com'
password='82fd0bf2ef9f5b15456d739ee4e1b2558c4ce9229ff9db25ddfefa7ce55d885b'
url='https://metrics-api.librato.com/v1/metrics'
base64string = base64.encodestring('%s:%s' % (username,password)).replace('\n', '')

passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, url, username, password)
authhandler = urllib2.HTTPBasicAuthHandler(passman)
opener = urllib2.build_opener(authhandler)
urllib2.install_opener(opener)

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

hostname = os.environ["HOSTNAME"]
hostname = hostname.replace(".","_")
now = int( time.time() )
queues = str.split(Popen([sge_root + "/bin/" + sge_arch + "/qconf","-sql"], stdout=PIPE).communicate()[0])
for q in queues:
  lines = []
  (cqload, used, res, avail, total) = parse_qstat(q)
  metric_name = "sge_" + q
  librato_data = 'measure_time=%s&source=%s&gauges[0][name]=%s&gauges[0][value]=%s&period=60' %  ( now, metric_name, hostname, used )
  print "librato data: %s" % librato_data
  req = urllib2.Request(url='https://metrics-api.librato.com/v1/metrics',
                        data=librato_data)
  req.add_header("Authorization", "Basic %s" % base64string)
  f = urllib2.urlopen(req)
