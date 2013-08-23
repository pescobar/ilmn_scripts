#!/usr/bin/python
from sys import exit
import re
import pythoncm

# set some essential variables
mgmt_subnet = '10.12.59'
ipmi_subnet = '10.12.60'
data_subnet = '10.129.3'
isilon_zone = 'ussd-prd-isi01b'
basename = 'ussd-tst-lncn'
category = 'ilmn-cseries'
rack = 'B5'

# Add connection to your cluster using cmsh certificate
clustermanager = pythoncm.ClusterManager()
cluster = clustermanager.addCluster('https://localhost:8081', '/cm/local/apps/cmd/etc/cert.pem', '/cm/local/apps/cmd/etc/cert.key');

if not cluster.connect():
  print "Unable to connect"
  print cluster.getLastError()
  exit(1)

internalnet = cluster.find('internalnet')
datanet = cluster.find(isilon_zone)
ipminet = cluster.find('ipminet')
  
for i in range(1, 16):
  node = pythoncm.PhysicalNode()
  cluster.add(node)
  node.hostname = basename + '%02d' % i
  node.partition = cluster.find('base')
  node.category = cluster.find(category, 'Category')

  # When creating objects belonging to node, add them as soon as possible
  # add all four interfaces - this is required to create bonds
  node.interfaces = [pythoncm.NetworkPhysicalInterface()]
  node.interfaces[0].name = 'eth0'
  node.interfaces = node.interfaces + [pythoncm.NetworkPhysicalInterface()]
  node.interfaces[1].name = 'eth1'
  node.interfaces = node.interfaces + [pythoncm.NetworkPhysicalInterface()]
  node.interfaces[2].name = 'eth2'
  node.interfaces = node.interfaces + [pythoncm.NetworkPhysicalInterface()]
  node.interfaces[3].name = 'eth3'

  # bonded interfaces
  node.interfaces = node.interfaces + [pythoncm.NetworkBondInterface()]
  node.interfaces[4].name = 'bond0'
  node.interfaces[4].ip = mgmt_subnet + '.%d' % (i +200)
  node.interfaces[4].network = internalnet
  node.interfaces[4].mode = 1
  node.interfaces[4].interfaces = ['eth0','eth1']
  # bug in CentOS - can't supply options for provisioning interface (workaround in finalize script)
  #node.interfaces[4].options = 'miimon=100'

  node.interfaces = node.interfaces + [pythoncm.NetworkBondInterface()]
  node.interfaces[5].name = 'bond1'
  node.interfaces[5].ip = data_subnet + '.%d' % (i +200)
  node.interfaces[5].mode = 1
  node.interfaces[5].network = datanet
  node.interfaces[5].interfaces = ['eth2','eth3']
  node.interfaces[5].options = 'miimon=100'

  # ipmi
  node.interfaces = node.interfaces + [pythoncm.NetworkBmcInterface()]
  node.interfaces[6].name = 'ipmi0'
  node.interfaces[6].ip = ipmi_subnet + '.%d' % (i) 
  node.interfaces[6].network = ipminet

  # provision using bond0
  node.provisioningInterface = node.interfaces[4]

  # set the rack position
  node.rack = cluster.find(rack)
  node.rackPosition = i
  node.rackHeight = 1

  # default is apc if not specified
  node.powerControl = 'ipmi0'

  # set the switch port
  # requires that Bright is able to walk the switch *that the provisioning interface* is attached to
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
