#!/bin/bash
. /etc/profile.d/sge-binaries.sh

# single check for all disabled queues
# more efficient than inventorying all queue instances - e.g. uscp
DISABLED=`qstat -f -qs d | awk '/amd64/{print $1}' | sed 's/\.lo.*//'`
if [ -n "$DISABLED" ]; then
  for q in $DISABLED; do
    echo "1 SGE_disabled - SGE queue is disabled"
  done
fi

ALARM=`qstat -f -qs a | awk '/amd64/{print $1}' | sed 's/\.lo.*//'`
if [ -n "$ALARM" ]; then
  for q in $ALARM; do
    echo "1 SGE_alarm - SGE queue is in alarm"
  done
fi

ERROR=`qstat -f -qs E | awk '/amd64/{print $1}' | sed 's/\.lo.*//'`
if [ -n "$ERROR" ]; then
  for q in $ERROR; do
    echo "1 SGE_alarm - SGE queue is in error"
  done
fi
