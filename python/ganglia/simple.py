#!/usr/bin/python


def handler(name):
  ''' parse the output of qstat -f -xml to get #slots used/#slots '''
  if name == 'data1':
    return 12
  if name == 'data2':
    return 0


def metric_init(params):

  d1 = {'name' : 'data1',
    'call_back' : handler,
    'time_max' : 90,
    'value_type': 'uint',
    'units': 'foo',
    'slope': 'both',
    'format': '%u',
    'description': 'Total # foo',
    'groups': 'test'}

  d2 = {'name' : 'data2',
    'call_back' : handler,
    'time_max' : 90,
    'value_type': 'uint',
    'units': 'foo',
    'slope': 'both',
    'format': '%u',
    'description': 'Foo in use',
    'groups': 'test'}

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
