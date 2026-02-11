#!/bin/bash

# Install Python 3.10
if command -v apt-get &> /dev/null; then
    sudo apt update
    sudo apt install -y software-properties-common
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install -y python3 python3-venv python3-tk
fi

# Upgrade pip
python3 -m pip install --user --upgrade pip

# Create a virtual environment using Python 3.10
python3 -m venv virtual_env
source virtual_env/bin/activate

# Check if the virtual environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "env created!"
    pip install -r requirements.txt
    alias norminette=flake8
else
    echo "env is not working!"

fi