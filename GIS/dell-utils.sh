rm -rf tftpboot
livecd-creator -c /home/thartmann/scripts/GIS/dell-utils.ks -f dell-utils
livecd-iso-to-pxeboot dell-utils.iso
