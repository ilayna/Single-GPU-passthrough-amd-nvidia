#! /bin/bash

get_distro_id(){
	local RES
    RES=$(grep -i '^ID=' /etc/os-release)
    local ID_TMP="${RES:3}" #removing the 'ID='
    local ID="${ID_TMP,,}" # to lower
	echo "$ID"
}

DISTRO_ID=$(get_distro_id)

remove_virtualization(){
    declare -A REMOVE_CMD
    REMOVE_CMD=( 
    [arch]='pacman -R virt-manager qemu vde2 ebtables iptables-nft nftables dnsmasq bridge-utils ovmf -y' 
    [endeavouros]='pacman -R virt-manager qemu vde2 ebtables iptables-nft nftables dnsmasq bridge-utils ovmf -y' 
    [manjaro]='pacman -R virt-manager qemu vde2 ebtables iptables-nft nftables dnsmasq bridge-utils ovmf -y'
    [ubuntu]='apt remove qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virt-manager ovmf -y'
    [debian]='apt remove qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virt-manager ovmf -y'
    [linuxmint]='apt remove qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virt-manager ovmf -y'
    [void]='xbps-remove -y qemu libvirt bridge-utils virt-manager -y'
    [fedora]='dnf remove @virtualization'
    [pop]='apt remove qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virt-manager ovmf -y'
    [opensuse]='zypper rm libvirt libvirt-client libvirt-daemon virt-manager virt-install virt-viewer qemu qemu-kvm qemu-ovmf-x86_64 qemu-tools -y'
    )
    local KEY
    KEY=$(get_distro_id)
    eval "${REMOVE_CMD["$KEY"]}"
}

remove_hooks(){
	eval "rm -r /etc/libvirt/hooks"
	eval "rm -r /bin/vfio-startup.sh"
	eval "rm -r /bin/vfio-teardown.sh"
}


echo "About to remove /etc/lbivirt/hooks, /bin/vfio-startup.sh,  /bin/vfio-teardown.sh and delete virtualization packages !"
while true; do
    read -p "Do you wish to uninstall anyway? y/n " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

remove_hooks
remove_virtualization
echo "Uninstalled !"