#!/usr/bin/python3

import getpass
import os
from pathlib import Path
import pwd
import re
import subprocess


def main():
    # Configuration info
    home_dir = str(Path.home())
    
    docker_files_dir = home_dir + "/docker-Containers/"     # ADJUST TO YOUR SETUP
    docker_regex = ".*docker-compose.yml$"
    
    tmp_dir_name = "docker-compose-backup.tmp/"
    tmp_dir_path = f"{home_dir}/{tmp_dir_name}"
    
    output_dir = home_dir + "/"
    output_file_name = "docker-compose-archive.tar.7z"
    
    encrypt = True

    # Creating a tmp file
    try:
        os.mkdir(tmp_dir_path)
    except FileExistsError as e:
        confirm = input(f"File {tmp_dir_path} already exists. Removing and recreate? (y/N) ")
        if confirm != "y": return
        
        subprocess.run(f"sudo rm -r {tmp_dir_path}", shell=True, text=True)
        os.mkdir(tmp_dir_path)
        
    # Getting all docker-compose.yml paths
    compose_paths = subprocess.run(f"sudo find {docker_files_dir} -maxdepth 2 -type f -regex '{docker_regex}'", shell=True, text=True, stdout=subprocess.PIPE).stdout
    compose_paths = compose_paths.split("\n")
    
    # The expected number of subdirectories of a path for a top level docker-compose.yml file
    expected_size = len(docker_files_dir.split("/")) + 1
    
    # Cleaning the bigger paths - They include sub-sub dirs docker-compose.yml files.
    # Theses are probably for dependencies. They were NOT made by me
    # for key, value in compose_paths_dict.items():
    compose_paths_dict = dict()
    for p in compose_paths:
        dirs = p.split("/")
        if len(dirs) <= expected_size and len(dirs) != 1:
            compose_paths_dict[p] = dirs
    
    
    # Creating directories in tmp_dir_name and moving docker-compose.yml files
    for path, parts in compose_paths_dict.items():
        dir_to_create = f"{tmp_dir_path}{parts[-2]}"
        
        # Creating dir
        try:
            os.mkdir(dir_to_create)
        except FileExistsError as e:
            subprocess.run(f"sudo rm -r {dir_to_create}", shell=True, text=True)
            os.mkdir(dir_to_create)
    
        # Moving docker-compose.yml files
        subprocess.run(f"sudo cp {path} {dir_to_create}", shell=True, text=True)
        

    # Prompting for password
    if encrypt:
        while True:
            try:
                password = getpass.getpass(prompt="Encryption password:")
                password_confirmation = getpass.getpass(prompt="Confirm password:")
            except Exception as error:
                print('ERROR', error)

            if password == password_confirmation: break
        
            print("\nPasswords do not match. Retrying")

    
    # Encrypting with password
    if encrypt: subprocess.run(f"cd {home_dir} && tar -cf - {tmp_dir_name} | 7za a -p'{password}' -si {output_dir}{output_file_name}", shell=True, text=True)    
    else:       subprocess.run(f"cd {home_dir} && tar -cf - {tmp_dir_name} | 7za a -si {output_dir}{output_file_name}", shell=True, text=True)    
    
    # Cleaning up tmp dir
    subprocess.run(f"sudo rm -r {tmp_dir_path}", shell=True, text=True)


if __name__ == "__main__":
    main()