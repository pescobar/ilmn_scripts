from subprocess import Popen,PIPE
import re

def parse_rockscmd():
  """ parse rocks command output """
  rocks_cmd = str.split("rocks list host interface")

  try:
    output = str.splitlines(Popen(rocks_cmd, stdout=PIPE).communicate()[0])
  except OSError:
    print "Cannot execute %s command" % rocks_cmd
    sys.exit(1)

  d1 = {} 
  hostdata = []
  for line in output:
    m = re.match(r'(.*?):\s+\w+\s+(eth\d)\s+(..:..:..:..:..:..)\s+(\d+?\.\d+?\.\d+?\.\d+?)\s+(\d+?\.\d+?\.\d+?\.\d+?)', line)
    if m:
      if m.group(2) == "eth0":
        hostdata = [m.group(2), m.group(3), m.group(4), m.group(5)]
      else:
        hostdata.append(m.group(2))
        hostdata.append(m.group(3))
        hostdata.append(m.group(4))
        hostdata.append(m.group(5))
      d1[m.group(1)] = hostdata

  return(d1)

if __name__ == '__main__':
  #print "wwsh node new %s --netdev=%s --hwaddr=%s --ipaddr=%s --netmask=%s" % (host,iface,mac,ip,nm)
  d2 = parse_rockscmd()
  for k, v in d2.iteritems():
    a = d2[k]
    #print k, v
    print "wwsh node new %s --netdev=%s --hwaddr=%s --ipaddr=%s --netmask=%s" % (k,a[0],a[1],a[2],a[3])
    print "wwsh node set %s --netdev=%s --hwaddr=%s --ipaddr=%s --netmask=%s" % (k,a[4],a[5],a[6],a[7])
