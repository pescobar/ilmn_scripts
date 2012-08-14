#!/bin/bash

. /etc/profile.d/sge-binaries.sh

HOST=`hostname`
qmod -d prod-s.q@$HOST
