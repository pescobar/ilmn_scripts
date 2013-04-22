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

%post

/sbin/chkconfig ipmi on

cat << '__HERE__' > /etc/rc.local

# use the MAC address of eth0 for the initial cobbler-register call
# requires a DNS entry for 'cobbler' on the local subdomain
FQDN=`ifconfig eth0 | awk '/HWaddr/{print $5}' | sed 's/://g'`
cobbler-register -s cobbler -f ${FQDN}.foo.illumina.com -P gluster

# trigger a install/firstboot script to set netboot enable for the OS install
# ('add' triggers are run when a system is edited, which results in a loop)
wget -O /dev/null http://cobbler/cblr/svc/op/trig/mode/firstboot/system/${FQDN}.foo.illumina.com
sleep 5
reboot
__HERE__
%end
