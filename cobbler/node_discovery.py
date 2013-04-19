#!/usr/bin/env python
import cobbler.api as capi
import cobbler.item_system as csystem
import re
import sys
import subprocess

def get_next_system_name():
  stack = []
  for system in h.systems():
    m = re.match(r'node(\d+)', system.name)
    if m:
      incr = int(m.group(1)) + 1
      sysname = "node" + str(incr)
      stack.append(sysname)
  if len(stack) > 0:
    return stack.pop()
  else:
    return "node1"

def rename_system(oldname,newname):
  subprocess.call(["/usr/bin/cobbler", "system", "rename", "--name", oldname, "--newname", newname])
  # this works, but only after service cobblerd restart && cobbler sync
  # obviously these api calls only stage the changes; how/why does the service restart & sync enable them?
  #for system in h.systems():
  #  m = re.match(oldname, system.name)
  #  if m:
  #    h.rename_system(system, newname)
  #    h.serialize()
  #    h.sync()

def get_next_ip_address():
  # TODO: almost everything (WIP), including finding largest (smallest?) IP
  for system in h.systems():
    ipaddr = csystem.System.get_ip_address(system,"eth0")
  return ipaddr

def set_system_properties(sysname):
  nodefqdn = sysname + ".foo.illumina.com"
  #subprocess.call(["/usr/bin/cobbler", "system", "edit", "--name", nodename, "--hostname", nodename, "--dns-name", nodefqdn, "--netboot-enabled", "true", "--interface", "eth0", "--static", "true"])
  subprocess.call(["/usr/bin/cobbler", "system", "edit", "--name", sysname, "--hostname", sysname, "--dns-name", nodefqdn, "--netboot-enabled", "true"])
  subprocess.call(["/usr/bin/cobbler", "sync"])

  # this works only after 'service cobblerd restart && cobbler sync' TODO: why?
  #system = h.find_system(sysname) # does this work? must return a system object
  #for system in h.systems():
  #  m = re.match(sysname, system.name)
    # manipulate it
  #  if m:
  #    csystem.System.set_hostname(sysname)
  #    csystem.System.set_name(sysname)
  #    csystem.System.set_netboot_enabled(netboot_enabled=True)
      # csystem.System.set_ip_address(self,address,interface)
      # csystem.System.set_static(self,truthiness,interface)

if __name__ == '__main__':
  h = capi.BootAPI()
  nodename = get_next_system_name()
  rename_system(sys.argv[2],nodename)
  #get_next_ip_address()
  set_system_properties(nodename)
