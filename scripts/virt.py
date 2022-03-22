import hooks
import utils
import errors
GPU_VENDOR = None
ISO_DOWNLOADS = {
    'Windows 10 21H2 English x64': r'https://www.itechtics.com/?dl_id=151',
    'arch': 'test'  # TODO remove this line
}


def init():
    """
    This is the method to run
    It sets everything regarding virt up
    """
    gpu_id = prompt_user_to_choose_gpu()
    gpu_base_id = gpu_id[:6]
    hooks.DEVICES_IDS = get_linked_devices_ids(gpu_base_id)


def prompt_user_to_choose_gpu():
    global GPU_VENDOR
    """
    Prompts the user to choose a gpu
    :return: The id of the chosen gpu
    """
    i = 1
    stop = False
    print("Please choose which gpu you want to use for the guest os")
    msg_lines = prompt_message()
    for line in msg_lines:
        print(f'{i}. {"".join(line)}')
        i = i + 1
    gpu = input()
    while not stop:
        if not gpu.isnumeric():
            gpu = input('Invalid input!\nPlease enter the number before the gpu you want to use !\n')
        elif int(gpu) not in range(1, i):
            gpu = input('Invalid input!\nPlease enter the number before the gpu you want to use !\n')
        else:
            gpu = int(gpu)
            stop = True
    line = msg_lines[gpu - 1]
    if 'AMD' in line:
        GPU_VENDOR = 'AMD'
    elif 'NVIDIA' in line:
        GPU_VENDOR = 'NVIDIA'
    else:
        # TODO (wabulu) Check if input is valid
        GPU_VENDOR = input(
            "Couldn't detect gpu vendor, please enter manually:\nAMD if you are using amd gpu\nNVIDIA if you are using nvidia gpu\n")
        while GPU_VENDOR not in ("NVIDIA", "AMD"):
            print("Invalid input !\nPlease enter NVIDIA or AMD only !\n\n")
            GPU_VENDOR = input(
                "Couldn't detect gpu vendor, please enter manually:\nAMD if you are using amd gpu\nNVIDIA if you are using nvidia gpu\n")

    # return line[line.rfind('['):line.rfind(']') + 1]
    return line[:8]


def prompt_message():
    # TODO (wabulu) Make sure it checks if the gpu is actually supported (valid for single passthrough)
    """
    Returns a list of all `valid` gpus
    """
    msg = utils.get_available_gpus()
    msg_lines = msg.split('\n')
    ret_msg = []
    for line in msg_lines:
        if "VGA" in line:
            ret_msg.append(line + '\n')
    return ret_msg


def get_linked_devices_ids(base_id: str):
    """
    Returns the ids of all devices of the same gpu (audio, vga)
    """
    ids_of_all_passthrough_devices = []
    lines = utils.get_available_gpus().split('\n')
    for line in lines:
        if base_id == line[:6]:  # the address should be at the start
            # device_id = line[line.rfind('[') + 1:line.rfind(']')]
            device_id = line[:7]
            ids_of_all_passthrough_devices.append(device_id)
    format_related_devices_addresses(ids_of_all_passthrough_devices)
    return ids_of_all_passthrough_devices


def format_related_devices_addresses(addresses):
    for i in range(len(addresses)):
        addresses[i].replace(':', '.')
        addresses[i].replace('.', '_')


def gpu_vendor():
    global GPU_VENDOR
    return GPU_VENDOR


def print_os_options():
    i = 1
    for key in ISO_DOWNLOADS.keys():
        print(f'{i}. {key}')
        i += 1


def prompt_user_to_choose_guest_os():
    """
    Asks the user which os he wants to use from OS_DOWNLOADS
    :rtype: str
    :return: download link of the chosen os
    """
    try:
        print('Please choose an os for the virtual machine: ')
        print_os_options()
        chosen_os = input()
        m_len = len(ISO_DOWNLOADS.items())
        while not ('1' <= chosen_os <= f'{m_len}'):
            chosen_os = input(f'Invalid input ! Please enter a number between 1 and {m_len} !')
        return list(ISO_DOWNLOADS.values())[int(chosen_os)-1]
    except Exception as ex:
        errors.Error.report_error_msg(ex, err_code=104)
    return None


