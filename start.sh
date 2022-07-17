#!/bin/bash
#Checking if running as root !
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

pip install distro
python3 $(pwd)/scripts/main.py


