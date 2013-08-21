#!/bin/bash

BASENAME="ussd-prd-lncn-b-6-"
TENGIG="10.128.3"
ISIZONE="ussd-prd-isi02a"

for i in `seq 1 20`; do
	# gigabit ethernet - use the IP set by rocks for the private interface
	IP=`rocks list host interface ${BASENAME}${i} | awk '/private/{print $4}'`
	#rocks add host bonded ${BASENAME}${i} channel=bond1 interfaces=eth2,eth3 ip=$IP network=private
	#rocks set host interface options ${BASENAME}${i} bond1 options="miimon=100 mode=1"

	# Add 10GbE bonded interfaces
        LAST=`echo $IP | awk -F '.' '{print $4}'`
        #rocks add host bonded ${BASENAME}${i} channel=bond0 interfaces=eth0,eth1 ip=${TENGIG}.${LAST} network=${ISIZONE}
        #rocks set host interface options ${BASENAME}${i} bond0 options="miimon=100 mode=1"

	# Assign 10GbE bonded interfaces to Isilon zones
	#rocks set host interface subnet ${BASENAME}${i} bond0 ${ISIZONE}
done
