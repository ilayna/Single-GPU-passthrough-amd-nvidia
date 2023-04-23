<p align="left">
   <a href="https://discord.gg/ZpXvd2RJVz"><img src="https://img.shields.io/badge/discord-join-7289DA.svg?logo=discord&longCache=true&style=flat" /></a>
</p>

# Single-GPU-passthrough-amd-nvidia

## if you are having troubles please see the '[manual](https://github.com/wabulu/Single-GPU-passthrough-amd-nvidia/tree/3d8666e66d009493a3f5b574bdba15954ed86af5)' branch

### My single gpu passthrough guide, it is fully automatic, and it is as simple as it gets

### DISCLAIMER: This guide is pretty similar to many other single gpu guides, I am not trying to copy them nor take their credits, This guide is combining them all together for a better more fluid guide, this way you can use the scripts on all display-services and both amd/nvidia gpus (there might be some anomalies)

<br />

### Step 1:

- Get the repository on your computer, either by downloading it zipped and extracting or cloning it as below
- If you chose to clone it instead of downloading it you should do <br />
  ```cd ~/Downloads ```<br />
  ```git clone https://github.com/wabulu/Single-GPU-passthrough-amd-nvidia.git```<br />


### Step 2:

- Run the script which would do (almost) everything for you by changing your directory to the folder with <br/>
  ``cd Single-GPU-passthrough-amd-nvidia/ ``<br/>
  and then executing the script with ``sudo bash ./setup.sh`` <br/>

### Step 3:

Now you just need to setup virt-manager as for now the scripts doesn't do it automatically, <br/>
you can do that by visiting
this <a href="https://gitlab.com/risingprismtv/single-gpu-passthrough/-/wikis/5)-Configuring-Virtual-Machine-Manager">
link</a>
After that, all that is left is to **install the scripts** with ``sudo bash ./install_hooks.sh``

### Step 4:

If you did everything right you can try running the vm (make sure it's named win10 otherwise make sure to replace `win10` in /etc/libvirt/hooks/qemu line 8 to the name) <br/>
**nvidia users** might also want to go to
this <a href="https://gitlab.com/risingprismtv/single-gpu-passthrough/-/wikis/6)-Preparation-and-placing-of-the-ROM-file">
link</a>.<br/>
If you have any problems you can join my discord server for faster response (top left) *or* you can mention me in your
reddit post at r/VFIO with u/wabulu.

### Uninstalling
- To uninstall run ``sudo bash ./uninstall.sh`` <br>
keep in mind that it will delete all previously installed virtualization packages on the system and delete the hooks.

## Troubleshooting
### Black Screen on VM Activation
Before that make sure we followed all the steps above correctly (Look for some indications like your HDD LED light, so that you can confirm your Windows has booted up)

If you are encountering a black screen issue when running a virtual machine with single GPU passthrough, you may need to install a GPU driver on the virtual machine to resolve the problem or you need to wait for sometime to let Windows automatically install (Give 10-15 mins) your GPU driver for you. If it doesn't you need to follow these steps:
	1. After installing Windows on the VM, you need to download two main things, the NVIDIA/AMD driver for your GPU (keep it somewhere closer, maybe on Desktop for convenience) and the Teamviewer application for Windows. Install the Teamviewer application and make sure it runs at startup.
	2. Now make sure you have ticked two options "Start TeamViewer with Windows" and "Grant Easy Access (You may need to create an account)". and also Go to Settings -> Security -> In Random Password, make sure to select password strength to Disabled (Bcz your screen will be blank and you can't remotely access yor VM). Then press ok.
	3. Now after everything done when you see your VM is sitting like a limbo, no output on the monitor. Open your secondary Laptop and also install TeamViewer on it (You can use your Android device too, install TeamViewer from Google PlayStore) and login with the same account you've created before. Now after that Go to your devices list and you will see your VM. Connect to it (Bcz we've disabled password and granted easy access). Navigate to that folder where you have downloaded your GPU driver, double click on it (or double tap on it :P ) let it install.
	4. And vola ! your monitor wakes up :O

### Contributing

- You can search the files for #TODOs and do them, it would help me a lot !
- For financial support you can sponsor me [here](https://github.com/sponsors/ilayna)

Check out these amazing people who made this guide possible !

- https://gitlab.com/risingprismtv
- https://gitlab.com/YuriAlek
- https://passthroughpo.st/
