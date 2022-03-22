from utils import *

INTEL = is_intel()
AMD = is_amd()
GRUB_FILE = grub_file_location()


def init():
    edit_grub()
    update_grub()


def edit_grub():
    line = None
    if DISTRO != 'pop':
        line = get_line_where_text("GRUB_CMDLINE_LINUX_DEFAULT", GRUB_FILE)
    else:
        with open(GRUB_FILE, 'r', ) as f:
            line = f.readlines()[-1]  # on pop, it's the last line unlike any other distro so far
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
    try:
        os.system(GRUB_UPDATE_CMND[DISTRO])
    except Exception as ex:
        errors.Error.report_error_msg(ex, 102)
