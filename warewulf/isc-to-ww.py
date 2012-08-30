import sys
import re
import socket

dhcpd_conf = "/etc/dhcpd.conf"

def parse_isc(dhcpd_conf):
  """ parse isc dhcpd.conf """
  try:
    f = open(dhcpd_conf,'r')
  except IOError:
    print "Cannot open %s file for reading" % dhcpd_conf
    sys.exit(1)

  list = {}
  for line in f:
    m = re.match(r'\s+hardware ethernet (\w\w:\w\w:\w\w:\w\w:\w\w:\w\w);', line)
    if m:
      mac = m.group(1)
    m = re.match(r'\s+option host-name\s"(.*.local)', line)
    if m:
      host = m.group(1)
      list[mac] = host
  return(list)

if __name__ == '__main__':
  hostlist = parse_isc(dhcpd_conf)
  for hwaddress, hostname in hostlist.iteritems():
    ip = socket.gethostbyname(hostname)
    print "wwsh node new %s --netdev=eth0 --hwaddr=%s --ipaddr=%s --netmask=255.255.254.0" % (hostname, hwaddress, ip)
