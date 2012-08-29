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
  i = 0
  for hostname,data in d2.iteritems():
    while data:
      netdev = data.pop(0)
      hwaddr = data.pop(0)
      ipaddr = data.pop(0)
      netmask = data.pop(0)
      if netdev == "eth0":
        print "wwsh node new %s --netdev=%s --hwaddr=%s --ipaddr=%s --netmask=%s" % (hostname,netdev,hwaddr,ipaddr,netmask)
      else:
        print "wwsh node set %s --netdev=%s --hwaddr=%s --ipaddr=%s --netmask=%s" % (hostname,netdev,hwaddr,ipaddr,netmask)
