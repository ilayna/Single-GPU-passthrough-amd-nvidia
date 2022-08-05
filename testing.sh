#! /bin/bash

get_distro_id(){
	local RES
    RES=$(grep -i '^ID=' /etc/os-release)
    local ID_TMP="${RES:3}" #removing the 'ID='
    local ID="${ID_TMP,,}" # to lower
	echo "$ID"
}
DEBIAN_BASED_DISTROS=( "ubuntu" "debian" "pop" "linuxmint" )
DISTRO_ID=$(get_distro_id)
edit_kernel_boot_parameters(){
    # WORKS ON GRUB, BOOTCTL
    # not checking if iommu=pt in, should probably do that.
    case "$DISTRO_ID" in
    "pop")
        local BOOT_CONFIG_FILE
        BOOT_CONFIG_FILE="/boot/efi/loader/entries/Pop_OS-current.conf"
        if ! grep -q "intel_iommu" "$BOOT_CONFIG_FILE" && ! grep -q "amd_iommu" "$BOOT_CONFIG_FILE"; then
            if grep -q intel "/proc/cpuinfo"; then     
                $(sed -i 's/options root=/&intel_iommu=on iommu=pt /' "$BOOT_CONFIG_FILE")
            elif grep -q amd "proc/cpuinfo"; then             
                $(sed -i 's/options root=/&amd_iommu=on iommu=pt /' "$BOOT_CONFIG_FILE")
            fi
        fi
    ;;
    *)
        local BOOT_CONFIG_FILE
        BOOT_CONFIG_FILE="/etc/default/grub"
        if ! grep -q "intel_iommu" "$BOOT_CONFIG_FILE" && ! grep -q "amd_iommu" "$BOOT_CONFIG_FILE"; then
            if grep -q intel "/proc/cpuinfo"; then     
                $(sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="/&intel_iommu=on iommu=pt /' "$BOOT_CONFIG_FILE")
            elif grep -q amd "proc/cpuinfo"; then             
                $(sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="/&amd_iommu=on iommu=pt /' "$BOOT_CONFIG_FILE")
            fi
        fi
    ;;
    esac
}

enable_libvirt_for_user(){
    local CURR_USER
    CURR_USER=$(whoami)
    $(usermod -a -G libvirt $CURR_USER) # CURR_USER will always be root here.
    $(systemctl start libvirtd)
    $(systemctl enable libvirtd)
    if [[ " ${DEBIAN_BASED_DISTROS[*]} " =~ " $DISTRO_ID " ]]; then
        $(usermod -a -G kvm,libvirt $CURR_USER)
    fi
}

finalize(){
    $(systemctl restart libvirtd)
}
enable_libvirt_for_user
finalize