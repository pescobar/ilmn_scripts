#!/usr/bin/env python
from subprocess import Popen,PIPE
import re

def parse_rockscmd():
  """ parse rocks list host interface command output """
  rocks_cmd = str.split("rocks list host interface")

  try:
    output = str.splitlines(Popen(rocks_cmd, stdout=PIPE).communicate()[0])
  except OSError:
    print "Cannot execute %s command" % rocks_cmd
    sys.exit(1)

  rocks_host_interface = {} 
  data = []
  for line in output:
    m = re.match(r'(.*?):\s+(\w+)\s+(eth\d)\s+(..:..:..:..:..:..)\s+(\d+?\.\d+?\.\d+?\.\d+?)\s+(\d+?\.\d+?\.\d+?\.\d+?)', line)
    # hostname, subnet, netdev, mac, ip, netmask
    if m:
      if not m.group(1) in dict.keys(rocks_host_interface):                 # first time we've seen this host
        data = [m.group(2), m.group(3), m.group(4), m.group(5), m.group(6)] # initialize the data list
      else:
        data.append(m.group(2))
        data.append(m.group(3))
        data.append(m.group(4))
        data.append(m.group(5))
        data.append(m.group(6))

      # key is host name, value is a list of data for all interfaces
      rocks_host_interface[m.group(1)] = data
  return(rocks_host_interface)

if __name__ == '__main__':
  host_data = parse_rockscmd()
  for host,data in host_data.iteritems():
    subnet_data = {}
    while data:
      sn = data.pop(0)
      nd = data.pop(0)
      hw = data.pop(0)
      ip = data.pop(0)
      nm = data.pop(0)

      # key is the subnet name, value is list [netdev,mac,ip,netmask]
      subnet_data[sn] = [nd,hw,ip,nm]

    (netdev,hwaddr,ipaddr,netmask) = subnet_data["private"]
    print "wwsh node new %s --netdev=%s --hwaddr=%s --ipaddr=%s --netmask=%s" % (host,netdev,hwaddr,ipaddr,netmask)
    for subnet,sn_values in subnet_data.iteritems():
      if not subnet == "private":
        (netdev,hwaddr,ipaddr,netmask) = sn_values
        print "wwsh node set %s --netdev=%s --hwaddr=%s --ipaddr=%s --netmask=%s" % (host,netdev,hwaddr,ipaddr,netmask)
