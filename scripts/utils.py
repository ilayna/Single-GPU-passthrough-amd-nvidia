import os
import distro
import errors

"""
this dictionary contains the default grub location for each distro,
to add support for a distro all you need to do is add it to this dictionary 
"""
GRUB_UPDATE_CMND = {
    'arch': 'grub-mkconfig -o /boot/grub/grub.cfg',
    'endeavouros': 'grub-mkconfig -o /boot/grub/grub.cfg',
    'manjaro': 'update-grub',
    'ubuntu': 'update-grub',
    'linuxmint': 'update-grub',
    'void': 'update-grub',
    'fedora': 'grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg',
    'pop': 'bootctl update',
    'opensuse': 'grub2-mkconfig -o /boot/grub2/grub.cfg'
}

LIBVIRT_INSTALL = {
    'arch': 'pacman -S virt-manager qemu vde2 ebtables iptables-nft nftables dnsmasq bridge-utils ovmf -y',
    'endeavouros': 'pacman -S virt-manager qemu vde2 ebtables iptables-nft nftables dnsmasq bridge-utils ovmf -y',
    'manjaro': 'pacman -S virt-manager qemu vde2 ebtables iptables-nft nftables dnsmasq bridge-utils ovmf -y',
    'ubuntu': 'apt install qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virt-manager ovmf -y',
    'linuxmint': 'apt install qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virt-manager ovmf -y',
    'void': 'xbps-install -Sy qemu libvirt bridge-utils virt-manager -y',
    'fedora': 'dnf install @virtualization',
    'pop': 'apt install qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virt-manager ovmf -y',
    'opensuse': 'zypper in libvirt libvirt-client libvirt-daemon virt-manager virt-install virt-viewer qemu qemu-kvm qemu-ovmf-x86_64 qemu-tools -y'
}

REPO_LINK = r"https://github.com/wabulu/Single-GPU-passthrough-amd-nvidia/"


def current_distro():
    return distro.id()


DISTRO = current_distro()


def is_intel():
    """
    Checks whether we are on an intel platform or not
    WORKS ONLY ON LINUX
    :rtype: bool
    """
    with open('/proc/cpuinfo', 'r') as f:
        return 'intel' in f.read().lower()


def is_amd():
    """
    Checks whether we are on an amd platform or not
    WORKS ONLY ON LINUX
    :rtype: bool
    """
    with open('/proc/cpuinfo', 'r') as f:
        return 'amd' in f.read().lower()


def grub_file_location():
    if DISTRO == 'pop':
        return '/boot/efi/loader/entries/Pop_OS-current.conf'
    """
    Every other `supported` distro uses this as default grub config location 
    """
    return '/etc/default/grub'


def get_line_where_text(str_to_look_for: str, file: str):
    """
    Returns the index of :param str in :param file
    :param file: the file to search for str
    :return: Returns the index of :param str in :param file, if :param str_to_look_for not in file, returns None
    """
    try:
        with open(file, 'r') as f:
            text = f.readlines()
            for i in range(len(text)):
                if str_to_look_for in text[i]:
                    return i
    except FileNotFoundError as e:
        errors.Error.report_error_msg(e)
    return None


def get_current_unix_user():
    return os.getlogin()


def get_available_gpus():
    """
    returns a formatted text with the available gpus for passthrough
    """
    com = r"""
lspci -nnk
"""
    return os.popen(com).read()
