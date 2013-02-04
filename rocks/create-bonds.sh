#!/bin/bash

BASENAME="ussd-prd-lncn-b-8-"

for i in `seq 3 8`; do
	# gigabit ethernet - use the IP set by rocks for the private interface
	IP=`rocks list host interface ${BASENAME}${i} | awk '/private/{print $4}'`
	echo "rocks add host bonded ${BASENAME}${i} channel=bond1 interfaces=eth2,eth3 ip=$IP network=private"
	echo "rocks set host interface options ${BASENAME}${i} bond1 options="miimon=100 mode=0""

	# 10GbE 
	#rocks add host bonded ${BASENAME}${i} channel=bond0 interfaces=eth0,eth1 ip=10.128.3.1${i} network=uscp-prd-isi01b
	#rocks set host interface options ${BASENAME}${i} bond0 options="miimon=100 mode=0"

	# Isilon zones
	#rocks set host interface subnet uscp-prd-lncn-3-${i} bond0 uscp-prd-isi01a
	#rocks set host interface ip uscp-prd-lncn-3-${i} bond0 10.128.1.${i}
	#rocks list host interface uscp-prd-lncn-3-${i}
done
