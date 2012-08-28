import os
from subprocess import Popen,PIPE

queues = str.split(Popen([os.environ["SGE_ROOT"] + "/bin/" + os.environ["SGE_ARCH"] + "/qconf","-sql"], stdout=PIPE).communicate()[0])
os.environ["SGE_ROOT"] = "/opt/gridengine"
os.environ["SGE_CELL"] = "default"
os.environ["SGE_ARCH"] = "lx26-amd64"
os.environ["SGE_EXECD_PORT"] = "537"
os.environ["SGE_QMASTER_PORT"] = "536"


def parse_qstat(name):
  p1 = Popen([os.environ["SGE_ROOT"] + "/bin/" + os.environ["SGE_ARCH"] + "/qstat","-g","c"], stdout=PIPE)
  p2 = Popen(["awk", "/" + name + "/{print $3}"], stdin=p1.stdout, stdout=PIPE)
  output2 = p2.communicate()[0]

  return int(output2)


def metric_init(params):
  global descriptors
  global queues

  descriptors = []
  # works nice but unfortunately to use this as a ganglia metric
  # the list of metrics (queues in this case) has to be hard-coded in a .pyconf file
  for q in queues:
    descriptors.append({'name' : q,
      'call_back' : parse_qstat,
      'time_max' : 90,
      'value_type': 'uint',
      'units': 'slots',
      'slope': 'both',
      'format': '%d',
      'description': 'devel.q',
      'groups': 'SGE'})

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
