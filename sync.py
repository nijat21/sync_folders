import os
import sys
import hashlib
import datetime
import time
from filecmp import dircmp
import shutil


# Class file
class File:
    def __init__ (self, name, location, hash_md5='', location2=''):
        self.name = name
        self.location =location
        self.hash_md5=hash_md5
        self.location2=location2


# Remove last slash if there's any 
def trim_slash(input_location):
    if input_location[-1] == '/':
        input_location = input_location[:-1]
    return input_location
    
# User input
source = trim_slash(sys.argv[1])
target = trim_slash(sys.argv[2])
sync_interval = int(sys.argv[3]) # in seconds
log_file_path = sys.argv[4]


while True: 

    # Print text in purple
    def print_color(text):
        print('\033[1;75m'+text+'\033[1;m')


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
    with open(log_file_path, "w") as sync_log_output:

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
        sync_log_output.write("Files that has been found on Source folder only: " + '\n')
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
        sync_log_output.write("Directories that has been found on Source folder only: " + '\n')
        sync_log_output.write("Directories found: " + str(len(dirs_on_source)) + '\n\n')

        for d_on_source in dirs_on_source:
            sync_log_output.write("[" + str(counter) + "]")
            sync_log_output.write("Location : " + d_on_source + '\n')
            counter += 1
        sync_log_output.write("###############################################################################################" + '\n\n')


        # Write files found on target folder only 
        counter = 1
        sync_log_output.write("Files that has been found on Target folder only: " + '\n')
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
        sync_log_output.write("Directories that has been found on Target folder only: " + '\n')
        sync_log_output.write("Directories found: " + str(len(dirs_on_target)) + '\n\n')

        for d_on_target in dirs_on_target:
            sync_log_output.write("[" + str(counter) + "] + '\n'")
            sync_log_output.write("Location : " + d_on_target + '\n')
            counter += 1
        sync_log_output.write("###############################################################################################" + '\n\n')



        # Copying files from Source not found in Target
        if len(files_on_source) > 0:
            print_color("Copying missing files from Source to Target: \n")
            sync_log_output.write("Copying missing files from Source to Target: \n")
            for f_on_source in files_on_source:
                if os.path.isfile(f_on_source.location):
                    location1 = f_on_source.location
                    location2 = replicate_file_path(target, location1)
                    # Copy
                    shutil.copy2(location1, location2) # Using shutil for portability purposes
                    sync_log_output.write("Copied " + f_on_source.name + "to Target" + '\n')
                    print("Copied: ", f_on_source.name, '\n') 
            
            sync_log_output.write("###############################################################################################" + '\n\n')
            print("Files copied successfully. \n\n")


        # Copying dirs from Source not found in Target
        if len(dirs_on_source) > 0:
            print_color("Copying missing directories from Source to Target: \n")
            sync_log_output.write("Copying missing directories from Source to Target: \n")
            for dir_on_source in dirs_on_source:
                if os.path.dirname(dir_on_source):
                    location1 = dir_on_source
                    location2 = replicate_file_path(target, location1)
                    # Copy
                    copy_command = 'cp -a "' + location1 + '" "' + location2 + '" '
                    shutil.copytree(location1, location2) # Using shutil for portability purposes
                    sync_log_output.write("Copied " + dir_on_source + "to Target" + '\n')
                    print("Copied: ", dir_on_source, '\n') 
            
            sync_log_output.write("###############################################################################################" + '\n\n')
            print("Directories copied successfully. \n\n")


        # Deleting files only found in Target
        if len(files_on_target) > 0:
            print_color("Deleting files found only in Target: \n")
            sync_log_output.write("Deleting files that don't exist in Source folder" + '\n\n')
            for f_on_target in files_on_target:
                if os.path.isfile(f_on_target.location):
                    os.remove(f_on_target.location) # Using os for portability
                    sync_log_output.write("Deleted: " + f_on_target.name + '\n')
                    print("Deleted: ", f_on_target.name, '\n') 
            
            sync_log_output.write("###############################################################################################" + '\n\n')
            print("Files deleted successfully. \n\n")


        # Deleting dirs only found in Target
        if len(dirs_on_target) > 0:
            print_color("Deleting directories found only in Target: \n")
            sync_log_output.write("Deleting directories that don't exist in Source folder" + '\n\n')
            for d_on_target in dirs_on_target:
                if os.path.dirname(d_on_target):
                    shutil.rmtree(d_on_target) # Using os for portability
                    sync_log_output.write("Deleted: " + d_on_target + '\n')
                    print("Deleted: ", d_on_target, '\n') 
            
            sync_log_output.write("###############################################################################################" + '\n\n')
            print("Directories deleted successfully. \n\n")


    print_color("Finished writing sync_log.txt")
    print()


    # Sleep for specific interval
    time.sleep(sync_interval)