import os
from subprocess import Popen,PIPE

def parse_qstat(name):
  ''' parse the output of qstat -g c to get queue info '''
  output = os.popen("/opt/gridengine/bin/lx26-amd64/qstat -g c")
  #output = Popen(["/opt/gridengine/bin/lx26-amd64/qstat","-g","c"], stdout=PIPE).communicate()[0]
  for i in output:
    print i
    foo = i.split

  return 12

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
