#!/bin/bash
#
# Credit to Maagu Karuri (@Karuri) on Gitlab
# https://gitlab.com/Karuri/vfio
#
## Load the config file
source "/etc/libvirt/hooks/kvm.conf"

echo 0 > /proc/sys/vm/nr_hugepages
