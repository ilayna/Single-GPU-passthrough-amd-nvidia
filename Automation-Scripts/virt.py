from utils import *


def init():
    """
    This is the method to run
    It sets everything regarding virt up
    """
    gpu_id = prompt_user_to_choose_gpu()
    gpu_base_id = gpu_id[:6]
    print(get_linked_devices_ids(gpu_base_id))


def prompt_user_to_choose_gpu():
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
    # return line[line.rfind('['):line.rfind(']') + 1]
    return line[:8]


def prompt_message():
    # TODO (wabulu) Make sure it checks if the gpu is actually supported (valid for single passthrough)
    """
    Returns a list of all `valid` gpus
    """
    msg = get_available_gpus()
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
    lines = get_available_gpus().split('\n')
    for line in lines:
        if base_id == line[:6]:  # the address should be at the start
            # device_id = line[line.rfind('[') + 1:line.rfind(']')]
            device_id = line[:7]
            ids_of_all_passthrough_devices.append(device_id)
    return ids_of_all_passthrough_devices
