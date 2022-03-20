import os

import distro


def current_distro():
    return distro.id()


DISTRO = current_distro()
GPU_VENDOR = ''


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
    with open(file, 'r') as f:
        text = f.readlines()
        if DISTRO != 'pop':
            for i in range(len(text)):
                if str_to_look_for in text[i]:
                    return i
        else:
            return len(text) - 1  # last line
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
