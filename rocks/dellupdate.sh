#!/bin/bash

# pull down the repo and install the basics
wget -q -O - http://linux.dell.com/repo/hardware/latest/bootstrap.cgi | bash
yum install dell_ft_install
yum install $(bootstrap_firmware)

# run the update
update_firmware --yes
reboot
