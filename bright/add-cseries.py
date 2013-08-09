#!/usr/bin/python
from sys import exit
import re
import pythoncm

# set some essential variables
mgmt_subnet = '10.12.59'
ipmi_subnet = '10.12.60'
data_subnet = '10.129.3'
basename = 'ussd-tst-lncn'
category = 'ilmn-cseries'
isilon_zone = 'ussd-prd-isi01b'

# Create an instance of ClusterManager, only one is needed
clustermanager = pythoncm.ClusterManager()

# Add connection to your cluster using cmsh certificate
cluster = clustermanager.addCluster('https://localhost:8081', '/cm/local/apps/cmd/etc/cert.pem', '/cm/local/apps/cmd/etc/cert.key');

if not cluster.connect():
  print "Unable to connect"
  print cluster.getLastError()
  exit(1)

internalnet = cluster.find('internalnet')
datanet = cluster.find(isilon_zone)
ipminet = cluster.find('ipminet')
if not ipminet:
  print "No ipminet found, not adding ipmi0 interfaces"
  
#for i in range(1, 16):
for i in range(4, 5):
  node = pythoncm.PhysicalNode()
  cluster.add(node)
  node.hostname = basename + '%02d' % i
  node.partition = cluster.find('base')
  node.category = cluster.find(category, 'Category')

  # When creating objects belonging to node, add them as soon as possible
  node.interfaces = [pythoncm.NetworkPhysicalInterface()]
  if ipminet:
    node.interfaces = node.interfaces + [pythoncm.NetworkBmcInterface()]
  node.interfaces[0].name = 'eth0'
  node.interfaces[0].ip = mgmt_subnet + '.%d' % (i + 200) 
  node.interfaces[0].network = internalnet
  if ipminet:
    node.interfaces[1].name = 'ipmi0'
    node.interfaces[1].ip = ipmi_subnet + '.%d' % (i + 200) 
    node.interfaces[1].network = ipminet
  node.interfaces = node.interfaces + [pythoncm.NetworkPhysicalInterface()]
  node.interfaces[2].name = 'eth1'
  node.interfaces = node.interfaces + [pythoncm.NetworkPhysicalInterface()]
  node.interfaces[3].name = 'eth2'
  node.interfaces = node.interfaces + [pythoncm.NetworkPhysicalInterface()]
  node.interfaces[4].name = 'eth3'
  node.interfaces = node.interfaces + [pythoncm.NetworkBondInterface()]
  node.interfaces[5].name = 'bond1'
  node.interfaces[5].ip = data_subnet + '.%d' % (i +200)
  node.interfaces[5].mode = 1
  node.interfaces[5].network = datanet
  node.interfaces[5].interfaces = ['eth2','eth3']
  node.interfaces[5].options = 'miimon=100'
  node.provisioningInterface = node.interfaces[0]

  # set the rack position
  node.rack = cluster.find('B5')
  node.rackPosition = i
  node.rackHeight = 1

  # set the switch port
  #node.ethernetSwitch.ethernetSwitch = cluster.find('switch01')
  #node.ethernetSwitch.port = i

  # Save the local changes
  c = node.commit()
  if not c.result:
    print "Commit of %s failed:" % node.resolveName()
    for j in range(c.count):
      print c.getValidation(j).msg
  else:
    print "committed: %s" % node.resolveName()

cluster.disconnect()
