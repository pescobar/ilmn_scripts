import re
import netaddr

# only user-defined value
provisioning_subnet = netaddr.IPNetwork('10.1.1.0/24')

def register():
  # run when called as install/firstboot
  return "/var/lib/cobbler/triggers/install/firstboot/*"

def run(api, args, logger):
  objtype = args[0]
  name    = args[1]
  bootip  = args[2]

  #########################################################
  # identify a new node name and IP address
  #########################################################
  nodes = []
  ip = []

  for system in api.systems():
    m = re.match(r'node(\d+)', system.name)
    if m:
      nodes.append(int(m.group(1)))
      ip.append(netaddr.IPAddress(system.get_ip_address("eth0")))

  if len(nodes) > 0:
    nodes.sort()
    incr = nodes.pop() + 1
    newname = "node" + str(incr)
  else:
    newname = "node1"

  fqdn = newname + ".foo.illumina.com"

  if len(ip) > 0:
    ip.sort()
    ip.reverse()
    last  = ip.pop()
    newip = str(last.__isub__(1))
  else:
    newip = "10.1.1.254"

  netmask = str(provisioning_subnet.netmask)
  gateway = str(provisioning_subnet[1])

  ###############################################
  # configure the new node
  # and set it to netboot into kickstart
  ###############################################
  system = api.find_system(name)
  system.set_hostname(fqdn)
  system.set_dns_name(fqdn,'eth0')
  system.set_ip_address(newip,'eth0')
  system.set_netmask(netmask,'eth0')
  system.set_gateway(gateway)
  system.set_static('True','eth0')
  system.set_netboot_enabled('True')
  api.rename_system(system,fqdn)
  api.serialize()
  api.sync()
  return 0
