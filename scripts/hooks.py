from libvirt import restart_libvirt
from utils import *
from virt import DEVICES_IDS


def init():
    move_hooks_folder()
    if DEVICES_IDS is None:
        # for now...
        print("Something went wrong... DEVICES_IDS is None !")
    else:
        edit_hooks(DEVICES_IDS)
    make_hooks_executable()


def move_hooks_folder():
    os.system(fr"cp -r ../{GPU_VENDOR.lower()}/hooks/ /etc/libvirt")


def edit_hooks(devices_addresses: list):
    # TODO (wabulu) Make so if you have more then just the audio and video addresses it adds them too

    # Example :
    # VIRSH_GPU_VIDEO=pci_0000_01_00_0
    # VIRSH_GPU_AUDIO=pci_0000_01_00_1
    txt = ''
    with open(r'/etc/libvirt/hooks/kvm.conf', 'r') as f:
        txt = f.read()
    with open(r'/etc/libvirt/hooks/kvm.conf', 'w') as f:
        if len(devices_addresses) < 2:
            print("ERROR: No devices found ! Please report this issue !")
        txt = txt.replace('01_00_0', devices_addresses[0])
        txt = txt.replace('01_00_1', devices_addresses[1])
        f.write(txt)
        if len(devices_addresses) > 2:  # TODO (wabulu) remove this once fixed this issue
            print(
                "Warning: More than 2 device addresses found, if you have problems starting your vm please add the "
                "extra missing addresses to /etc/libvirt/hooks/kvm.conf and your start.sh and revert.sh "
                f"accordingly\nThe addresses are {devices_addresses}\nFor help please join the discord "
                f"server\nhttps://discord.com/invite/ZpXvd2RJVz")
    restart_libvirt()


def make_hooks_executable():
    os.system('chmod +x /etc/libvirt/hooks/qemu')
    os.system('chmod +x /etc/libvirt/hooks/qemu.d/win10/prepare/begin/start.sh')
    os.system('chmod +x /etc/libvirt/hooks/qemu.d/win10/release/end/revert.sh')
