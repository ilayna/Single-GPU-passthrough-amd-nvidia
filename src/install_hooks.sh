#!/bin/bash

if test -e /etc/libvirt/ && ! test -e /etc/libvirt/hooks;
then
    mkdir -p /etc/libvirt/hooks;
fi
if test -e /etc/libvirt/hooks/qemu;
then
    mv /etc/libvirt/hooks/qemu /etc/libvirt/hooks/qemu_last_backup
fi
if test -e /bin/vfio-startup.sh;
then
    mv /bin/vfio-startup.sh /bin/vfio-startup.sh.bkp
fi
if test -e /bin/vfio-teardown.sh;
then
    mv /bin/vfio-teardown.sh /bin/vfio-teardown.sh.bkp
fi
if test -e /etc/systemd/system/libvirt-nosleep@.service;
then
    rm /etc/systemd/system/libvirt-nosleep@.service
fi

cp systemd-no-sleep/libvirt-nosleep@.service /etc/systemd/system/libvirt-nosleep@.service
cp hooks/vfio-startup.sh /bin/vfio-startup.sh
cp hooks/vfio-teardown.sh /bin/vfio-teardown.sh
cp hooks/qemu /etc/libvirt/hooks/qemu

chmod +x /bin/vfio-startup.sh
chmod +x /bin/vfio-teardown.sh
chmod +x /etc/libvirt/hooks/qemu
