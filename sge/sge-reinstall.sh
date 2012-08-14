#!/bin/sh

ME=`hostname`
EXECHOSTS=`qconf -sel`

for TARGETHOST in $EXECHOSTS; do
	if [ "$ME" == "$TARGETHOST" ]; then
		echo "Skipping $ME. This is the submission host"
	else
		numprocs=`qconf -se $TARGETHOST | \
			awk '/^processors/ {print $2}'`
		/opt/rocks/bin/rocks set host boot $TARGETHOST action=install
		qsub -p 1024 -pe mpi $numprocs -q all.q@$TARGETHOST \
			/opt/gridengine/examples/jobs/reboot.qsub
		echo "Set $TARGETHOST for Reinstallation"
	fi
done
