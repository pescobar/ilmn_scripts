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

# custom utils from illumina repo
ilmn_megacli

%post --interpreter /bin/bash
/sbin/chkconfig ipmi on

cat << __HERE__ >> /root/config_node.sh
# configure the LSI RAID controller during boot
/usr/bin/MegaCli -CfgClr -a0
/usr/bin/MegaCli -CfgLdAdd -r5[252:0, 252:1, 252:2, 252:3, 252:4, 252:5] -sz100GB -a0
/usr/bin/MegaCli -CfgLdAdd -r5[252:0, 252:1, 252:2, 252:3, 252:4, 252:5] -a0

# idracadm/omconfig doesn't work on c6xxx series...and neither does syscfg
# use ipmitool here? or later e.g. in puppet?
# advantage puppet - more facts available for e.g. setting static IP, registering with DNS, etc.

# cobbler-register utility from koan package - need to establish UID for hostname
#   dmidecode -s system-serial-number should work, but c6100 chassis report same for all 4 nodes in chassis
#   dmidecode -s chassis-serial-number should work, but c6100 chassis report same for all 4 nodes in chassis
#   dmidecode -s system-uuid should work, but c6100 chassis report same for all 4 nodes in chassis
#   essentially leaves us with MAC address of eth0...

FQDN=`ifconfig eth0 | awk '/HWaddr/{print $5}' | sed 's/://g'`
cobbler-register -b -s $HOSTNAME -f \$FQDN -p gluster

__HERE__
%end
