from utils import *


def init():
    install()
    configure_cfg()
    assign_libvirt_to_user()
    enable_vm_network()


def install():
    if DISTRO in ('manjaro', 'arch', 'endeavouros'):
        os.system("pacman -S virt-manager qemu vde2 ebtables iptables-nft nftables dnsmasq bridge-utils ovmf -y")
    elif DISTRO == 'ubuntu' or DISTRO == 'linuxmint' or DISTRO == 'pop' or DISTRO == 'debian':
        os.system("apt install qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virt-manager ovmf -y")
    elif DISTRO == 'opensuse':
        os.system(
            "zypper in libvirt libvirt-client libvirt-daemon virt-manager virt-install virt-viewer qemu qemu-kvm qemu-ovmf-x86_64 qemu-tools -y")
    elif DISTRO == 'void':
        os.system('xbps-install -Sy qemu libvirt bridge-utils virt-manager -y')
    else:
        print('Package manager not database, please install virt-manager etc manually and report your issue at '
              f'https://github.com/wabulu/Single-GPU-passthrough-amd-nvidia\nYour distro-id is {DISTRO},please add it to your report !\n')
        exit(1)


def configure_cfg():
    txt = ''
    with open("/etc/libvirt/libvirtd.conf", 'r') as f:
        txt = f.read()
        txt = txt.replace('#unix_sock_group = "libvirt"', 'unix_sock_group = "libvirt"')
        txt = txt.replace('#unix_sock_rw_perms = "0770"', 'unix_sock_rw_perms = "0770"')
        if 'log_filters="1:qemu"' not in txt:
            txt = txt + 'log_filters="1:qemu"\n'
        if 'log_outputs="1:file:/var/log/libvirt/libvirtd.log"' not in txt:
            txt = txt + 'log_outputs="1:file:/var/log/libvirt/libvirtd.log"\n'
    with open("/etc/libvirt/libvirtd.conf", 'w') as f:
        f.write(txt)


def assign_libvirt_to_user():
    os.system(f'usermod -a -G libvirt {get_current_unix_user()}')
    os.system('systemctl start libvirtd')
    os.system('systemctl enable libvirtd')
    """
    Editing qemu.conf
    """
    txt = ''
    with open(r'/etc/libvirt/qemu.conf', 'r') as f:
        txt = f.read()
        txt.replace('#user = "root"', f'user = "{get_current_unix_user()}"\n')
        txt.replace('#group = "root"', f'group = "{get_current_unix_user()}"\n')

    with open(r'/etc/libvirt/qemu.conf', 'w') as f:
        f.write(txt)

    os.system('systemctl restart libvirtd')
    if DISTRO == 'ubuntu' or DISTRO == 'linuxmint' or DISTRO == 'pop' or DISTRO == 'debian':
        os.system(f'usermod -a -G kvm,libvirt {get_current_unix_user()}')


def enable_vm_network():
    os.system('virsh net-autostart default')


def restart_libvirt():
    os.system('systemctl restart libvirtd')
