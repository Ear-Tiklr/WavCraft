#!/bin/bash

# Function to create, remove if necessary, and recreate Conda environment
create_env() {
    env_name=$1
    file_path=$2

    echo "Attempting to create Conda environment: $env_name"
    conda env create -f $file_path
    if [ $? -eq 0 ]; then
        echo "$env_name environment created successfully."
    else
        echo "Creation failed. Removing existing $env_name environment if it exists..."
        conda remove --name $env_name --all -y
        echo "Recreating the $env_name environment..."
        conda env create -f $file_path
        if [ $? -eq 0 ]; then
            echo "$env_name environment recreated successfully."
        else
            echo "Failed to recreate $env_name environment. Please check the YAML file and environment settings."
        fi
    fi
}

# Paths to the YAML files for environment creation
#create_env "AudioCraft" "venvs/audiocraft.yml"
#create_env "AudioLDM" "venvs/audioldm.yml"
#create_env "AudioSR" "venvs/audiosr.yml"
create_env "WavCraft" "venvs/wavcraft.yml"
