# Single-GPU-passthrough-amd-nvidia
My way of doing single gpu passthrough the simplest way, I've gathered many sources together to make the perfect Single GPU passthrough guide the simplest and easiest way.

DISCLAIMER: This guide is pretty similar to many other single gpu guides, I am not trying to copy them and or take their credit, This guide is combining them for the better, this way you can use the scripts on all display-services (there might be some anomalies)

Step 1:
    go to this url https://gitlab.com/risingprismtv/single-gpu-passthrough/-/wikis/1)-Preparations
    and follow steps 1-6, you could follow the rest of the guide but I believe my way is a bit more efficient and works more of the time..

Step 2:
      clone my repo and and copy the hooks folder to /etc/libvirt/

      cd ~/Downloads
      git clone https://github.com/wabulu/Single-GPU-passthrough-amd-nvidia.git
      cd Single-GPU-passthrough-amd-nvidia/{Nvidia/AMD depends on which graphics card you have}
      sudo cp -r hooks/ /etc/libvirt

Step 3:
       Now that the hooks folder is in the right place you are going to change the kvm.conf file to match your setup.
       to do this you first need to write:
       ``
       sudo lspci -nnk
       ``
       it should spit out something similar to this:
       ![lspci -nnk](https://user-images.githubusercontent.com/58913586/128605396-fce323da-14b1-44c0-a5f9-ffa01cb7573b.png)
                   you need to look for your gpu and audio pci number and change it accordingly in the kvm.conf file, for this all you have to do is write:
       ``
       sudo nano /etc/libvirt/hooks/kvm.conf
       ``
      (reminder: you start writing the numbers after pci_0000_{your numbers} and all dots should be replaced with _)
      
Step 4: If you did everything right you can try running the vm (make sure it's named win10 otherwise make sure the folder win10 in /etc/libvirt/hooks/qemu.d is named accordingly) nvidia users might also want to go to the url mentions at step 1 and follow the rest.

if you have any problems you can mention me in your reddit post at r/VFIO with u/wabulu.

CREDITS:
        https://gitlab.com/risingprismtv        
        https://gitlab.com/YuriAlek        
        https://passthroughpo.st/
        
