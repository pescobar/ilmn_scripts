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

  rocks_host_interface = {} 
  data = []
  for line in output:
    m = re.match(r'(.*?):\s+(\w+)\s+(eth\d)\s+(..:..:..:..:..:..)\s+(\d+?\.\d+?\.\d+?\.\d+?)\s+(\d+?\.\d+?\.\d+?\.\d+?)', line)
    if m:
      if not m.group(1) in dict.keys(rocks_host_interface): # haven't seen this host before
        data = [m.group(2), m.group(3), m.group(4), m.group(5), m.group(6)]
      else:
        data.append(m.group(2))
        data.append(m.group(3))
        data.append(m.group(4))
        data.append(m.group(5))
        data.append(m.group(6))
      rocks_host_interface[m.group(1)] = data
  return(rocks_host_interface)

if __name__ == '__main__':
  host_data = parse_rockscmd()
  for host,data in host_data.iteritems():
    d2 = {}
    while data:
      # how about a dict here that keys off of subnet name?
      # values are the list of remaining data
      # then we can pull out the data using the key - 'private' etc.
      sn = data.pop(0)
      nd = data.pop(0)
      hw = data.pop(0)
      ip = data.pop(0)
      nm = data.pop(0)
      net_data = [nd,hw,ip,nm]
      d2[sn] = net_data 
      #print "new subnet '%s' found for host %s" % (subnet,host)
      #print net_data
      # pull out the private subnet data to create the ww node
    (netdev,hwaddr,ipaddr,netmask) = d2["private"]
    print "wwsh node new %s --netdev=%s --hwaddr=%s --ipaddr=%s --netmask=%s" % (host,netdev,hwaddr,ipaddr,netmask)
    for k,v in d2.iteritems():
      if not k == "private":
        # next if key is "private"
        (netdev,hwaddr,ipaddr,netmask) = v
        print "wwsh node set %s --netdev=%s --hwaddr=%s --ipaddr=%s --netmask=%s" % (host,netdev,hwaddr,ipaddr,netmask)
