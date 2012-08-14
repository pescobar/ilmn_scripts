#!/bin/bash

# Idea is to submit a job to take up an entire node
# once the jobs starts running, run rocks commands
# on the master to sync the network

LIST="uscp-prd-lncn-7-3 uscp-prd-lncn-7-4 uscp-prd-lncn-7-5 uscp-prd-lncn-7-6 uscp-prd-lncn-7-7 uscp-prd-lncn-7-8"

for HOST in $LIST; do
  qsub -sync y -m b -M thartmann@illumina.com -pe fill_up 12 -q prod-s.q@$HOST sleep.sh
  #rocks sync host network $HOST
done

