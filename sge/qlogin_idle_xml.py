#!/usr/bin/python
import os
from subprocess import Popen,PIPE
from xml.dom.minidom import parseString

# SGE setup
try:
  '''if SGE_ROOT isn't set, pretty good odds no SGE vars are set'''
  os.environ["SGE_ROOT"]
except:
  os.environ["SGE_ROOT"] = "/opt/gridengine"
  os.environ["SGE_CELL"] = "default"
  os.environ["SGE_ARCH"] = "lx26-amd64"
  os.environ["SGE_EXECD_PORT"] = "537"
  os.environ["SGE_QMASTER_PORT"] = "536"

sge_root = os.environ["SGE_ROOT"]
sge_arch = os.environ["SGE_ARCH"]

output = Popen([sge_root + "/bin/" + sge_arch + "/qstat","-u","*","-xml"], stdout=PIPE).communicate()[0]
doc = parseString(output)

elements = doc.getElementsByTagName('JB_name') # elements == nodelist
for item in range(elements.length):
  xmlTag = elements.item(item).toxml()
  xmlData = xmlTag.replace('<JB_name>','').replace('</JB_name>','')
  print xmlData

elements = doc.getElementsByTagName('JAT_start_time') # elements == nodelist
for item in range(elements.length):
  xmlTag = elements.item(item).toxml()
  xmlData = xmlTag.replace('<JAT_start_time>','').replace('</JAT_start_time>','')
  print xmlData

# assign to dict (hash) => output of 2nd loop as key, output of 1st as value

