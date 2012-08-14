#!/usr/bin/python

from subprocess import Popen,PIPE
from xml.dom.minidom import parseString


output = Popen(["qstat","-f","-xml"], stdout=PIPE).communicate()[0]
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

#xmlTag = doc.getElementsByTagName('slots_total')[0].toxml()
#xmlData = xmlTag.replace('<slots_total>','').replace('</slots_total>','')
#print xmlData
