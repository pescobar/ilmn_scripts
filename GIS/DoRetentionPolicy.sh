#!/bin/bash

source /illumina/scratch/retention/.bashrc
rm /illumina/scratch/retention/rm.e*
rm /illumina/scratch/retention/rm.o*
rm /illumina/scratch/retention/gzip.e*
rm /illumina/scratch/retention/gzip.o*
rm /illumina/scratch/retention/DoDeletionAndCompression.sh.e*
rm /illumina/scratch/retention/DoDeletionAndCompression.sh.o*

qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /harmonia/SeqRuns 24

qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /bruno/ARG 24

qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /bruno/Avatar 24
qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /bruno/Avatar/MiSeqRuns 24
qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /bruno/Avatar/MiSeqRuns/OneDyeAnalysisOutput 24
qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /bruno/Avatar/CMOS_SeqRuns 45

qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /bruno/Bolt 8

qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /bruno/Cypress 24

qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /bruno/EigerSanction 24

qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /bruno/Gilbert/Runs 24
qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /bruno/Gilbert 24

qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /bruno/KnightRider 24

qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /bruno/Magellan 24

#qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /bruno/OncologyDiscovery/Apollo 24

qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /bruno/Tiesto 24

qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /illumina/scratch/Invenious 24

qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /illumina/scratch/Nitro 24

qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /illumina/scratch/Oreo 24

qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /illumina/scratch/Zebra 24

qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /illumina/scratch/TRex 14

qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /illumina/scratch/Falcon 24

# Tremor
qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /illumina/scratch/Falcon/Tremor 24
qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /illumina/scratch/Tremor 14

# Spark
qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /illumina/scratch/Spark/Proto1B_Runs/SeqRuns 14
qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /illumina/scratch/Spark/MiSeq\ Ultem 14
qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /illumina/scratch/Spark/BBFRaw 14
qsub -cwd -b y -V -p -1023 /illumina/scratch/retention/DoDeletionAndCompression.sh /illumina/scratch/Spark/KPazam 14
