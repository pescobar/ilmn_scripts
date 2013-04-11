lang en_US
keyboard us
timezone  America/Los_Angeles
auth  --useshadow  --enablemd5
selinux --disabled
firewall --disabled

repo --name=source-1 --baseurl=http://ussd-prd-lnym01/mrepo/centos5-x86_64/RPMS.os/
repo --name=illumina --baseurl=http://ussd-prd-lnym01/mrepo/illumina-x86_64/RPMS.illumina/
repo --name=omsa-independent --baseurl=http://linux.dell.com/repo/hardware/latest/platform_independent/rh50_64/
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
ilmn_megacli
shadow-utils
vim-minimal
vim-common

# dell omsa - useful for reporting(?)
srvadmin-base
srvadmin-omcommon
srvadmin-omacore

%post 
OMCONFIG="/opt/dell/srvadmin/bin/omconfig"

cat <<__HERE__ >> /root/config_node.sh
# configure the LSI RAID controller during boot
/usr/bin/MegaCli -CfgClr -a0
/usr/bin/MegaCli -CfgLdAdd -r5[252:0, 252:1, 252:2, 252:3, 252:4, 252:5] -sz100GB -a0
/usr/bin/MegaCli -CfgLdAdd -r5[252:0, 252:1, 252:2, 252:3, 252:4, 252:5] -a0

# idracadm/omconfig doesn't work on c6xxx series...use ipmitool here or in puppet after

# cobbler-register utility from koan package

__HERE__
%end
