#!/bin/bash
# Helpful to read output when debugging
set -x

## Load the config file with our environmental variables
source "/etc/libvirt/hooks/kvm.conf"

# Stop display manager (KDE specific)
systemctl stop display-manager

# Unbind VTconsoles
echo 0 > /sys/class/vtconsole/vtcon0/bind
echo 0 > /sys/class/vtconsole/vtcon1/bind

# Unbind EFI-Framebuffer
echo efi-framebuffer.0 > /sys/bus/platform/drivers/efi-framebuffer/unbind

# Avoid a race condition
sleep 5

# Unload all AMD drivers
modprobe -r amdgpu

# Unbind the GPU from display driver
virsh nodedev-detach $VIRSH_GPU_VIDEO
virsh nodedev-detach $VIRSH_GPU_AUDIO

# Load VFIO kernel module
modprobe vfio
modprobe vfio_pci
modprobe vfio_iommu_type1
