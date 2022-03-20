from utils import *

INTEL = is_intel()
AMD = is_amd()
GRUB_FILE = grub_file_location()


def init():
    edit_grub()
    update_grub()


def edit_grub():
    line = get_line_where_text("GRUB_CMDLINE_LINUX_DEFAULT", GRUB_FILE)
    text_to_add = ''
    txt = ''
    if AMD:
        text_to_add = 'amd_iommu=on iommu=pt'
    elif INTEL:
        text_to_add = 'intel_iommu=on iommu=pt'

    with open(GRUB_FILE, 'r') as f:
        txt = f.readlines()
        # if you run the script twice or have already done this part we shouldn't do it again
        if text_to_add in txt:
            return
        index_first_space = txt[line].find(' ')
        txt[line] = txt[line][:index_first_space] + ' ' + text_to_add + ' ' + txt[line][index_first_space + 1:]
        txt = ''.join(txt)

    with open(GRUB_FILE, 'w') as f:
        f.write(txt)


def update_grub():
    if DISTRO in ('arch', 'endeavouros'):
        os.system("grub-mkconfig -o /boot/grub/grub.cfg")
    elif DISTRO in (
            'manjaro', 'ubuntu', 'linuxmint', 'debian', 'void'):  # not sure about the debain one, it wasn't specified
        os.system("update-grub")
    elif DISTRO == 'fedora':
        os.system("grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg")
    elif DISTRO == 'pop':
        os.system("bootctl update")
    elif DISTRO == 'opensuse':
        os.system("grub2-mkconfig -o /boot/grub2/grub.cfg")
    else:
        print("Distro not in database, please update grub manually and report this issue at "
              "https://github.com/wabulu/Single-GPU-passthrough-amd-nvidia")
