#!/bin/bash
. /etc/profile.d/sge-binaries.sh

# problem with this as a check_mk local check is 
# that it creates a new service for each queue instance
# uscp is going to be huge - and take forever to check and jack the load on the qmaster
QUEUES=`qstat -f | awk '/amd64/{print $1}' | sed 's/\.lo.*//'`

if [ -n "$QUEUES" ]; then
  for q in $QUEUES; do
    IS_DISABLED=`qstat -f -q $q -qs d | awk '/amd64/{print $1}' | sed 's/\.lo.*//'`
    if [ -n "$IS_DISABLED" ]; then
      status=1
      statustxt=WARNING
    else
      status=0
      statustxt=OK
    fi
    #echo "$status SGE_queue_${q} - SGE queue $q is $statustxt"
  done
fi


# TODO: create a single check which can return data on multiple disabled queues

DISABLED=`qstat -f -qs d | awk '/amd64/{print $1}' | sed 's/\.lo.*//'`
if [ -n "$DISABLED" ]; then
  for q in $DISABLED; do
    echo "1 SGE_disabled - SGE queue $q is disabled"
  done
fi

ALARM=`qstat -f -qs a | awk '/amd64/{print $1}' | sed 's/\.lo.*//'`
if [ -n "$ALARM" ]; then
  for q in $ALARM; do
    echo "1 SGE_alarm - SGE queue $q is in alarm"
  done
fi
