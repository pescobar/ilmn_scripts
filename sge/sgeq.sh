#!/bin/bash
. /etc/profile.d/sge-binaries.sh

# if we want alerts for each and every queue instance that has an issue
# then I don't see any way around creating checks for all queue instances if running on qmaster
# this script will have to enumerate all queues, return 0 for OK, 1 or 2 for error or alarm

# option 2: run this check on every sgexecd host - one extra local check per compute node
# qhost -h `hostname` -q -xml | awk '/state_string/'


ERROR=`qstat -f -qs aduE | awk '/amd64/{print $1}' | sed 's/\.lo.*//'`
if [ -n "$ERROR" ]; then
  for q in $ERROR; do
    echo "1 SGE_alarm - $q is in error"
  done
else
  echo "0 SGE_alarm - all queues are normal"
fi
