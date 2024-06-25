#!/bin/bash

# Function to create and activate Conda environment
create_and_activate() {
    env_name=$1
    file_path=$2

    echo "Creating Conda environment: $env_name"
    conda env create -f $file_path
    if [ $? -eq 0 ]; then
        echo "$env_name environment created successfully."
    else
        echo "Failed to create $env_name environment. Attempting to activate if it exists..."
        conda activate $env_name
        if [ $? -eq 0 ]; then
            echo "Activated existing $env_name environment."
        else
            echo "Failed to activate $env_name environment. It may not exist."
        fi
    fi
}

# Paths to the YAML files for environment creation
create_and_activate "AudioCraft" "venvs/audiocraft.yml"
create_and_activate "AudioLDM" "venvs/audioldm.yml"
create_and_activate "AudioSR" "venvs/audiosr.yml"
create_and_activate "WavCraft" "venvs/wavcraft.yml"
