from subprocess import Popen,PIPE
from xml.dom.minidom import parseString

def parse_qstat(name):
  ''' parse the output of qstat -f -xml to get #slots used/#slots '''
  output = Popen(["/opt/gridengine/bin/lx26-amd64/qstat","-f","-xml"], stdout=PIPE).communicate()[0]
  doc = parseString(output)
  taglist = doc.getElementsByTagName(name)
  slots = 0 
  for item in range(taglist.length):
    xmlTag = taglist.item(item).toxml()
    xmlData = xmlTag.replace('<','').replace('>','').replace('/','').replace(name,'').replace(name,'')
    slots = slots + int(xmlData)

  return uint(slots)

def metric_init(params):
  global descriptors

  d1 = {'name' : 'slots_total',
    'call_back' : parse_qstat,
    'time_max' : 90,
    'value_type': 'uint',
    'units': 'slots',
    'slope': 'both',
    'format': '%d',
    'description': 'Total # Slots',
    'groups': 'SGE'}

  d2 = {'name' : 'slots_used',
    'call_back' : parse_qstat,
    'time_max' : 90,
    'value_type': 'uint',
    'units': 'slots',
    'slope': 'both',
    'format': '%d',
    'description': 'Slots in use',
    'groups': 'SGE'}

  descriptors = [ d1, d2 ]

  return descriptors

def metric_cleanup():
  '''Clean up the metric module.'''
  pass

# debugging 
if __name__ == '__main__':
  descriptors = metric_init({})
  for d in descriptors:
    v = d['call_back'](d['name'])
    print 'value for %s is %u' % (d['name'], v)
