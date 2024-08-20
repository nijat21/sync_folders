import os
import sys
import hashlib
import datetime
import subprocess
from filecmp import dircmp


# Class file
class File:
    def __init__ (self, name, location, hash_md5='', location2=''):
        self.name = name
        self.location =location
        self.hash_md5=hash_md5
        self.location2=location2


# Print text in purple
def print_color(text):
    print('\033[1;75m'+text+'\033[1;m')


# Remove last slash if there's any 
def trim_slash(input_location):
    if input_location[-1] == '/':
        input_location = input_location[:-1]
    return input_location


# Replicating file path of source for target
def replicate_file_path(target,location):
    # Ensure target is absolute or correctly formatted
    target = os.path.abspath(target)

    # Compute the relative path of the location from the source root
    relative_path = os.path.relpath(location, start=source)

    # Combine the target path with the relative path to get the full target location
    target_location = os.path.join(target, relative_path)
    
    return target_location


# Caclulate MD5 hash
deleted_dirs = []

def md5(file):
    hash_md5 = hashlib.md5()
    try:
        with open(file,"rb") as d:
            for chunk in iter(lambda: d.read(4096), b""):
                hash_md5.update(chunk)
    except:
        deleted_dirs.append(file)

    return hash_md5.hexdigest()


# Compare folders
files_on_source = []
dirs_on_source = []
files_on_target = []
dirs_on_target = []
modified_files = []

def compare_folders(dcomp):
    # Changed files
    for file_name in dcomp.diff_files:
        location = dcomp.left + '/' + file_name
        location2 = dcomp.right  + '/' + file_name
        the_file = File(file_name, location, md5(location), location2)
        modified_files.append(the_file)
    
    for sub_dcomp in dcomp.subdirs.values():
        compare_folders(sub_dcomp)

    
    # Files/dirs in source folder only
    for file_name in dcomp.left_only:
        location = dcomp.left + '/' + file_name
        if os.path.isfile(location):
            the_file = File(file_name, location, md5(location))
            files_on_source.append(the_file)
        else: dirs_on_source.append(location)
    

    # Files/dirs on target folder only
    for file_name in dcomp.right_only:
        location = dcomp.right + '/' + file_name
        if os.path.isfile(location):
            the_file=File(file_name, location, md5(location))
            files_on_target.append(the_file)
        else: dirs_on_target.append(location)

    
# User input
source = trim_slash(sys.argv[1])
target = trim_slash(sys.argv[2])

dcomp = dircmp(source, target)
compare_folders(dcomp)

# Printing modified files
counter = 1
print_color("Modified files: ")
print("Modified files found: ", len(modified_files),"\n")

for m_file in modified_files:
    print("[",counter,"]")
    print("Filename     : ", m_file.name)
    print("Source       : ", m_file.location)
    print("Destination  : ", m_file.location2)
    print("MD5          : ", m_file.hash_md5)
    print()
    counter += 1


# Printing files on source folder only
counter = 1
print_color("Files that has been found on Source folder only: ")
print("Files found: ", len(files_on_source), '\n')

for f_on_source in files_on_source:
    print("[",counter,"]")
    print("Filename     : ", f_on_source.name)
    print("Source       : ", f_on_source.location)
    print("Destination  : ", f_on_source.location2)
    print("MD5          : ", f_on_source.hash_md5)
    print()
    counter += 1


# Printing dirs found on source folder only
counter = 1
print_color("Directories that has been found only in Source folder: " + str(len(dirs_on_source)) + '\n')

for dir_on_source in dirs_on_source:
    print("[",counter,"]")
    print("Location     : ", dir_on_source)
    print()
    counter += 1


# Printing files on target folder only 
counter = 1
print_color("Files that has been found on Target folder only: ")
print("Files found: ", len(files_on_target), '\n')

for f_on_target in files_on_target:
    print("[",counter,"]")
    print("Filename     : ", f_on_target.name)
    print("Location     : ", f_on_target.location)
    print("MD5          : ", f_on_target.hash_md5)
    print()
    counter += 1


# Printing dirs found on source folder only
counter = 1
print_color("Directories that has been found only in Target folder: " + str(len(dirs_on_target)) + '\n')

for dir_on_target in dirs_on_target:
    print("[",counter,"]")
    print("Location     : ", dir_on_target)
    print()
    counter += 1


# Output to text files

# Current Date and Time
now = datetime.datetime.now()
now = now.strftime("%y%m%d")

filename = "sync_log [" + str(now) + "].txt"
print_color("Writing sync_log.txt")
sync_log_output = open(filename, "w")

# Write modified files' names
counter = 1
sync_log_output.write("Modified files: ")
sync_log_output.write("Modified files found: " + str(len(modified_files)) + '\n\n')

for m_file in modified_files:
    sync_log_output.write("[" + str(counter) + "] + '\n'")
    sync_log_output.write("Filename : " + m_file.name + '\n')
    sync_log_output.write("Source : " + m_file.location + '\n')
    sync_log_output.write("Destination : " + m_file.location2 + '\n')
    sync_log_output.write("MD5 : " + m_file.name + '\n\n')
    counter += 1
sync_log_output.write("###############################################################################################" + '\n\n')


# Write files found on source folder only 
counter = 1
sync_log_output.write("Files that has been found on Source folder only: ")
sync_log_output.write("Files found: " + str(len(files_on_source)) + '\n\n')

for f_on_source in files_on_source:
    sync_log_output.write("[" + str(counter) + "] + '\n'")
    sync_log_output.write("Filename : " + f_on_source.name + '\n')
    sync_log_output.write("Location : " + f_on_source.location + '\n')
    sync_log_output.write("MD5 : " + f_on_source.name + '\n\n')
    counter += 1
sync_log_output.write("###############################################################################################" + '\n\n')


# Write directories found on source folder only 
counter = 1
sync_log_output.write("Directories that has been found on Source folder only: ")
sync_log_output.write("Directories found: " + str(len(dirs_on_source)) + '\n\n')

for d_on_source in dirs_on_source:
    sync_log_output.write("[" + str(counter) + "]")
    sync_log_output.write("Location : " + d_on_source + '\n')
    counter += 1
sync_log_output.write("###############################################################################################" + '\n\n')


# Write files found on target folder only 
counter = 1
sync_log_output.write("Files that has been found on Target folder only: ")
sync_log_output.write("Files found: " + str(len(files_on_target)) + '\n\n')

for f_on_target in files_on_target:
    sync_log_output.write("[" + str(counter) + "] + '\n'")
    sync_log_output.write("Filename : " + f_on_target.name + '\n')
    sync_log_output.write("Location : " + f_on_target.location + '\n')
    sync_log_output.write("MD5 : " + f_on_target.name + '\n\n')
    counter += 1
sync_log_output.write("###############################################################################################" + '\n\n')


# Write directories found on target folder only 
counter = 1
sync_log_output.write("Directories that has been found on Target folder only: ")
sync_log_output.write("Directories found: " + str(len(dirs_on_target)) + '\n\n')

for d_on_target in dirs_on_target:
    sync_log_output.write("[" + str(counter) + "] + '\n'")
    sync_log_output.write("Location : " + d_on_target + '\n')
    counter += 1
sync_log_output.write("###############################################################################################" + '\n\n')


sync_log_output.close()
print_color("Finished writing sync_log.txt")
print()


# Copying files from Source not found in Target

if len(files_on_source) > 0:
    user_input = input("Copy missing files from source to targe?t Y/n : ").upper()
    if user_input == 'Y':

        print_color("Copying files:")
        for f_on_source in files_on_source:
            location1 = f_on_source.location
            location2 = replicate_file_path(target, location1)
            # Copy
            subprocess.run(['cp', location1, location2])
        print("Files copied successfully./n")


if len(dirs_on_source) > 0:
    user_input = input("Copy missing directories from source to targe?t Y/n : ").upper()
    if user_input == 'Y':

        print_color("Copying directories:")
        for dir_on_source in dirs_on_source:
            location1 = dir_on_source
            location2 = replicate_file_path(target, location1)
            # Copy
            copy_command = 'cp -a "' + location1 + '" "' + location2 + '" '
            subprocess.call(copy_command, shell=True)
        print("Directories copied successfully. \n\n")