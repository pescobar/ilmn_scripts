#!/bin/env python
###############################################################################
# re-implementation of insert-ethers for cobbler
# goal is to run this to do node discovery similar to insert-ethers on rocks
# TODO: argument passing for --basename and --profile
# TODO: get cobbler server IP, netmask, gateway, domainname
###############################################################################
import re
import sys
import netaddr
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import sniff,DHCP,Ether,IP,BOOTP
import cobbler.api

api = cobbler.api.BootAPI()

def dhcp_callback(pkt):
  # does cobbler know about this MAC address?
  #   yes - do nothing
  #   no  - add the node to cobbler using the basename and profile specified as arguments

  # RFC2132 DHCPDISCOVER == 1
  if pkt[DHCP] and pkt[DHCP].options[0][1] == 1:
    mymac = pkt[Ether].src

    # generate lists of all MAC and IP addresses known to cobbler
    mac = []
    ip  = []
    for system in api.systems():
      mac.append(system.get_mac_address("eth0"))
      m = re.match(r'node(\d+)', system.name) # assumes compute nodes are all named node(\d+)
      if m:
        ip.append(netaddr.IPAddress(system.get_ip_address("eth0")))

    # find the next available IP in the range
    provisioning_subnet = "10.1.1.0/24" # temp hard code for testing
    if len(ip) > 0:
      ip.sort()
      ip.reverse()
      last  = ip.pop()
      newip = str(last.__isub__(1))
    else:
      newip = str(list(provisioning_subnet).pop().__isub__(1))

    if mymac in mac:
      print "duplicate mac found; next IP is %s" % newip
    else:
      print "mac not found, adding system with IP %s" % newip
      # TODO: determine uniqueName, netmask, dns-name, gateway
      #cobbler system add --name=uniqueName --netboot-enabled=true --hostname=uniqueName --gateway=fromdhcp --mac-address=mymac --ip-address=newip --netmask=fromdhcp --dns-name=fromdhcp --interface=eth0

  # RFC2132 DHCPOFFER == 2
  # Pull the DHCP server, router, and subnet mask from the DHCP offer
  # should be other ways to get this...like from the cobbler server itself? It's on the same VLAN as the nodes
  #if pkt[DHCP] and pkt[DHCP].options[0][1] == 2:
  #  dhcp_server = pkt[IP].src
  #  netmask     = pkt[DHCP].options[3][1]
  #  gateway     = pkt[DHCP].options[4][1]
  #  subdomain   = pkt[DHCP].options[6][1]

  return

  #########################################################
  # identify a new node name and IP address
  #########################################################
  #sn = dhcp_server + '/24'
  #provisioning_subnet = netaddr.IPNetwork(sn)

  #for system in api.systems():
  #  m = re.match(r'node(\d+)', system.name)
  #  if m:
  #    nodes.append(int(m.group(1)))
  #    ip.append(netaddr.IPAddress(system.get_ip_address("eth0")))

  ###############################################
  # configure the new node in cobbler
  # and set it to netboot into kickstart
  # (after koan cobbler-register registers it)
  ###############################################
  #system = api.find_system(name)
  #system.set_hostname(fqdn)
  #system.set_dns_name(fqdn,'eth0')
  #system.set_ip_address(newip,'eth0')
  #system.set_netmask(netmask,'eth0')
  #system.set_gateway(gateway)
  #system.set_static('True','eth0')
  #system.set_netboot_enabled('True')
  #api.rename_system(system,fqdn)
  #api.serialize()
  #api.sync() 

# sniff dhcp traffic
sniff(prn=dhcp_callback,filter="((port 67 or 68) and (udp[8:1] = 0x1))", store=0, count=200)
