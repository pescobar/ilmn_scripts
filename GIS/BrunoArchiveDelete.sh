#!/bin/bash

find /illumina/scratch/BrunoDatabase/Archived -type f -mtime +30 | mail -s "BrunoArchive" thartmann@illumina.com
