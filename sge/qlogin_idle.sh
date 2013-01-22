#!/bin/bash

qstat -u '*' | awk '/QLOGIN/{print $4,$6}'
