lang en_US
keyboard us
timezone  America/Los_Angeles
auth  --useshadow  --enablemd5
selinux --disabled
firewall --disabled

repo --name=source-1 --baseurl=http://ussd-prd-lnym01/mrepo/centos5-x86_64/RPMS.os/
repo --name=illumina --baseurl=http://ussd-prd-lnym01/mrepo/illumina-x86_64/RPMS.illumina/

%packages
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
system-config-firewall-base

device-mapper
wget
yum
OpenIPMI
ilmn_megacli
shadow-utils
vim-minimal
vim-common
%end
