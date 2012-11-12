#!/bin/bash
#$ -cwd
#$ -M thartmann@illumina.com
#$ -m e
#$ -j y
#$ -p 1024


# submit as an exclusive job (-pe fill_node #slots) and enable notification email

# disable a queue instance once all other jobs have drained
# i.e. for node maintenance

. /etc/profile.d/sge-binaries.sh

qmod -d ${QUEUE}@${HOST}
