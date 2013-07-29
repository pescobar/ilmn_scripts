#!/bin/bash
wget -q -O - http://linux.dell.com/repo/hardware/latest/bootstrap.cgi | bash
yum install dell_ft_install
yum install $(bootstrap_firmware)
echo "Completed and ready to update firmware"
echo "to check versions run the command --> inventory_firmware"
echo "to update the firmware run the command --> update_firmware --yes" 
