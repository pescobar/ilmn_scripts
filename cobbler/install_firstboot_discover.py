import re

def register():
  return "/var/lib/cobbler/triggers/install/firstboot/*"

def run(api, args, logger):
  objtype = args[0]
  name    = args[1]
  bootip  = args[2]

  #########################################################
  # generate a new node name
  #########################################################
  # this assumes nodes are alphabetically sorted in h.systems()
  # appears to be a valid assumption, but may change in future
  stack = []
  for system in api.systems():
    m = re.match(r'node(\d+)', system.name)
    if m:
      incr = int(m.group(1)) + 1
      sysname = "node" + str(incr)
      stack.append(sysname)

  if len(stack) > 0:
    newname = stack.pop()
  else:
    newname = "node1"

  fqdn = newname + ".foo.illumina.com"

  ########################################################
  # assign a static IP address
  ########################################################
  # TODO


  ###############################################
  # configure the new node
  # and set it to boot into kickstart
  ###############################################
  system = api.find_system(name)
  system.set_hostname(fqdn)
  system.set_dns_name(fqdn,'eth0')
  system.set_comment('firstboot_trigger')
  system.set_netboot_enabled('True')
  api.rename_system(system,fqdn)
  api.serialize()
  api.sync()
  return 0
