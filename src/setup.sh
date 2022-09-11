#! /bin/bash


get_distro_id(){
	local RES
    RES=$(grep -i '^ID=' /etc/os-release)
    local ID_TMP="${RES:3}" #removing the 'ID='
    local ID="${ID_TMP,,}" # to lower
	echo "$ID"
}

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


install_virtualization(){
    declare -A INSTALL_CMD
    INSTALL_CMD=( 
    [arch]='pacman -S virt-manager qemu vde2 ebtables iptables-nft nftables dnsmasq bridge-utils ovmf -y' 
    [endeavouros]='pacman -S virt-manager qemu vde2 ebtables iptables-nft nftables dnsmasq bridge-utils ovmf -y' 
    [manjaro]='pacman -S virt-manager qemu vde2 ebtables iptables-nft nftables dnsmasq bridge-utils ovmf -y'
    [ubuntu]='apt install qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virt-manager ovmf -y'
    [debian]='apt install qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virt-manager ovmf -y'
    [linuxmint]='apt install qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virt-manager ovmf -y'
    [void]='xbps-install -Sy qemu libvirt bridge-utils virt-manager -y'
    [fedora]='dnf install @virtualization'
    [pop]='apt install qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virt-manager ovmf -y'
    [opensuse]='zypper in libvirt libvirt-client libvirt-daemon virt-manager virt-install virt-viewer qemu qemu-kvm qemu-ovmf-x86_64 qemu-tools -y'
    )
    local KEY
    KEY=$(get_distro_id)
    eval "${INSTALL_CMD["$KEY"]}"
}

echo "DISTRO ID IS $DISTRO_ID"

enable_libvirt_for_user(){
    local CURR_USER
    local DEBIAN_BASED_DISTROS
    DEBIAN_BASED_DISTROS=( "ubuntu" "debian" "pop" "linuxmint" )
    CURR_USER=$(whoami)
    $(usermod -a -G libvirt $CURR_USER) # CURR_USER will always be root here.
    $(systemctl start libvirtd)
    $(systemctl enable libvirtd)
    if [[ " ${DEBIAN_BASED_DISTROS[*]} " =~ " $DISTRO_ID " ]]; then
        $(usermod -a -G kvm,libvirt $CURR_USER)
    fi
    eval 'virsh net-autostart default' # enable network on start-up
}


edit_libvirtd(){
    local LIBVIRTD_PATH
    local SOCK_LINE
    local SOCK_LINE_RAW
    LIBVIRTD_PATH="/etc/libvirt/libvirtd.conf"
    SOCK_LINE='unix_sock_group = "libvirt"'
    SOCK_LINE_RAW='unix_sock_rw_perms = "0770"'
    if ! grep -q "^$SOCK_LINE$" "$LIBVIRTD_PATH"; then
        $(sed -i -e '$aunix_sock_group = "libvirt"' "$LIBVIRTD_PATH")
    fi
    if ! grep -q "^$SOCK_LINE_RAW$" "$LIBVIRTD_PATH"; then
        $(sed -i -e '$aunix_sock_rw_perms = "0770"' "$LIBVIRTD_PATH")
    fi
    # enable detailed log
    if ! grep -q '^log_filters="1:qemu"$' "$LIBVIRTD_PATH"; then
        $(sed -i -e '$alog_filters="1:qemu"' "$LIBVIRTD_PATH")
    fi
    if ! grep -q '^log_outputs="1:file:/var/log/libvirt/libvirtd.log"$' "$LIBVIRTD_PATH"; then
        $(sed -i -e '$alog_outputs="1:file:/var/log/libvirt/libvirtd.log"' "$LIBVIRTD_PATH")
    fi
}
finalize(){
    declare -A UPDATE_BOOTLOADER_CMD
    UPDATE_BOOTLOADER_CMD=( 
    [arch]='grub-mkconfig -o /boot/grub/grub.cfg' 
    [endeavouros]='grub-mkconfig -o /boot/grub/grub.cfg' 
    [manjaro]='update-grub'
    [ubuntu]='update-grub'
    [debian]='update-grub'
    [linuxmint]='update-grub'
    [void]='update-grub'
    [fedora]='grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg'
    [pop]='bootctl update'
    [opensuse]='grub2-mkconfig -o /boot/grub2/grub.cfg'
    )
    local KEY
    KEY=$(get_distro_id)
    eval "${UPDATE_BOOTLOADER_CMD["$KEY"]}"
    $(systemctl restart libvirtd)
}

edit_kernel_boot_parameters
install_virtualization
edit_libvirtd
enable_libvirt_for_user
finalize

echo "Done ! Please restart now and continue to configure your VM."