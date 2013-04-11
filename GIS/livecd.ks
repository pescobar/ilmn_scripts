lang en_US
keyboard us
timezone  America/Los_Angeles
auth  --useshadow  --enablemd5
selinux --disabled
firewall --disabled

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
dmidecode
shadow-utils
vim-minimal
vim-common
openssh-clients
which

# custom utils from illumina repo
ilmn_megacli
dell-pec-bmc-tool
dell-pec-setupbios
dell-pec-ipmiflash
dell-pec-ldstate
dell-pec-pecagent

%post --interpreter /bin/bash
/sbin/chkconfig ipmi on

cat << __HERE__ >> /etc/rc.local
# configure the LSI RAID 
/usr/bin/MegaCli -CfgClr -a0
/usr/bin/MegaCli -CfgLdAdd -r5[252:0, 252:1, 252:2, 252:3, 252:4, 252:5] -sz100GB -a0
/usr/bin/MegaCli -CfgLdAdd -r5[252:0, 252:1, 252:2, 252:3, 252:4, 252:5] -a0

# Configure BIOS and BMC settings
/opt/dell/pec/bmc nic_mode set dedicated
/opt/dell/pec/bmc set_chassis_power_cap disable
/opt/dell/pec/bmc attr set poweron_stagger_ac_recovery 1
/opt/dell/pec/setupbios setting set ioat_dma_engine enabled
#/opt/dell/pec/bmc attr set dns_dhcp_enable 1
#/opt/dell/pec/bmc attr set dns_get_domain_from_dhcp 1
#/opt/dell/pec/bmc attr set dns_register_bmc 1

__HERE__
%end
