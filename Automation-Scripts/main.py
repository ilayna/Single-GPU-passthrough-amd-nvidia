import grub
import utils
import libvirt
import virt

if __name__ == '__main__':
    # grub.edit_grub()
    # grub.update_grub()
    # libvirt.install()
    # libvirt.configure_cfg()
    # libvirt.assign_libvirt_to_user()
    # libvirt.enable_vm_network()

    # printing in green so it is easier for the user to spot it.
    print("\033[92mPlease restart to continue installation !\nAfter restart please rerun the script !\033[0m")

    virt.init()
