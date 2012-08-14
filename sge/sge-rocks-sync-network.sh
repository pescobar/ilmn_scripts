#!/bin/bash

LIST="uscp-prd-lncn-8-9 uscp-prd-lncn-8-10 uscp-prd-lncn-8-11 uscp-prd-lncn-8-12"

for HOST in $LIST; do
  # submit a blocking job that disables the queue on $HOST
  qsub -p 1024 -sync y -m b -M thartmann@illumina.com -pe fill_node 12 -q prod-s.q@$HOST restartq.sh
  # sync the network config - after the job completes
  rocks sync host network $HOST
  # test nfs mounts still work
  ssh $HOST ls /home/thartmann
  if [ $? == 0 ]; then
    # re-enable the queue instance
    qmod -e prod-s.q@$HOST
  fi
done
