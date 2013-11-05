rm -rf tftpboot
livecd-creator -c /home/thartmann/scripts/GIS/livecd.ks -f livecd
livecd-iso-to-pxeboot livecd.iso
