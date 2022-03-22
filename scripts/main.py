from grub import init as grub_init
from hooks import init as hooks_init
from libvirt import init as lib_init
from virt import init as virt_init
import virt
HOME_DIR = '$HOME'
if __name__ == '__main__':
    grub_init()
    lib_init()
    # printing in green, so it is easier for the user to spot it.
    # TODO (wabulu) find a better way to remember state
    print("\033[92mPlease restart to continue installation !\nAfter restart please rerun the script and press "
          "enter at this message !\033[0m")
    input('Only press enter if you already restarted !')
    virt_init()
    hooks_init()
    print('Done !\nYou just need to configure virt-manager now !')
    virt.prompt_user_to_choose_guest_os()
