#!/usr/bin/python
import os
from subprocess import Popen,PIPE
from xml.dom.minidom import parseString

# SGE
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

output = Popen([sge_root + "/bin/" + sge_arch + "/qstat","-f","-xml"], stdout=PIPE).communicate()[0]
doc = parseString(output)
elements = doc.getElementsByTagName('slots_total') # elements == nodelist
slots = 0
for item in range(elements.length):
  xmlTag = elements.item(item).toxml()
  xmlData = xmlTag.replace('<slots_total>','').replace('</slots_total>','')
  slots = slots + int(xmlData)
  #print xmlData
  #print elements.item(item).toxml()

print slots
