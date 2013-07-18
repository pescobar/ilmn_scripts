#!/bin/bash
. /etc/profile.d/sge-binaries.sh

ERROR=`qstat -f -qs E | awk '/amd64/{print $1}' | sed 's/\.lo.*//'`
if [ -n "$ERROR" ]; then
  for q in $ERROR; do
    echo "1 SGE_alarm - $ERROR is in error"
  done
else
  echo "0 SGE_alarm - all queues are normal"
fi
