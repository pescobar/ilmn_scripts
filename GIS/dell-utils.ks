# kickstart profile for livecd image to configure dell c6220
# RAID and BIOS settings
# 
# To create a pxeboot-able image:
#   livecd-creator -c dell-c6xxx.ks -f dell-c6xxx
#   livecd-iso-to-pxeboot dell-c6xxx.iso
#
# This will create a tftpboot directory with a vmlinuz0 and initrd0.img file
# suitable for PXE booting

lang en_US
keyboard us
timezone  America/Los_Angeles
auth  --useshadow  --enablemd5
selinux --disabled
firewall --disabled
network --device=eth0 --bootproto=dhcp

repo --name=source-1 --baseurl=http://ussd-prd-lnym01/mrepo/centos5-x86_64/RPMS.os/
repo --name=illumina --baseurl=http://ussd-prd-lnym01/mrepo/illumina-x86_64/RPMS.illumina/
repo --name=epel --baseurl=http://ussd-prd-lnym01/mrepo/epel5-x86_64/RPMS.epel5/

%packages
# required packages
bash
kernel
syslinux
passwd
policycoreutils
chkconfig
authconfig
rootfiles
comps-extras
xkeyboard-config
device-mapper
wget
perl
yum

# utilities
OpenIPMI
OpenIPMI-tools
koan
ethtool
python-ethtool
dmidecode
shadow-utils
vim-minimal
vim-common
openssh-clients
which
dhclient
memtester
sys_basher

# custom utils from illumina repo
ilmn_megacli
dell-pec-bmc-tool
dell-pec-setupbios
dell-pec-ipmiflash
dell-pec-ldstate
dell-pec-pecagent

%post --interpreter /bin/bash
/sbin/chkconfig ipmi on

#cat << '__HERE__' > /etc/rc.local
# configure the LSI RAID 
#/usr/bin/MegaCli -CfgClr -a0
#/usr/bin/MegaCli -CfgLdAdd -r5[252:0, 252:1, 252:2, 252:3, 252:4, 252:5] -sz100GB -a0
#/usr/bin/MegaCli -CfgLdAdd -r5[252:0, 252:1, 252:2, 252:3, 252:4, 252:5] -a0

# Configure BIOS and BMC settings
#/opt/dell/pec/bmc nic_mode set dedicated
#/opt/dell/pec/bmc set_chassis_power_cap disable
#/opt/dell/pec/bmc attr set poweron_stagger_ac_recovery 1
#/opt/dell/pec/setupbios setting set ioat_dma_engine enabled
#
#sleep 5
#reboot

#__HERE__
%end
