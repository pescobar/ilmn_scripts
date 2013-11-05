rm -rf tftpboot
livecd-creator -c /home/thartmann/scripts/GIS/dell-c6xxx.ks -f dell-c6xxx
livecd-iso-to-pxeboot dell-c6xxx.iso
