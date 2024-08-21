# Sync Folders

![Sync Visual](https://sixbytes.io/filesync/images/web1.png) <!-- Replace with actual URL to sync visual -->

## Overview

This script unidirectionally synchronizes the contents of two folders (`source` and `target`) by comparing their files and directories. It logs the differences and performs the necessary synchronization tasks, such as copying or deleting files and directories to ensure both folders are identical. 

## How It Works

1. **Initialization**:

   - Takes four command-line arguments:
     - `source`: Path to the source folder.
     - `target`: Path to the target folder.
     - `sync_interval`: Interval in seconds for synchronization.
     - `log_file_path`: Path where the synchronization log will be saved.

2. **Folder Comparison**:

   - Uses `filecmp.dircmp` to compare the contents of the `source` and `target` folders.
   - Identifies differences including:
     - Files present in `source` but not in `target`.
     - Files present in `target` but not in `source`.
     - Modified files.

3. **Synchronization Tasks**:

   - **Copy Files and Directories**: Copies files and directories from `source` to `target` if they are missing in the target.
   - **Delete Files and Directories**: Deletes files and directories in `target` that are no longer present in `source`.

4. **Logging**:

   - Logs detailed information about:
     - Modified files.
     - Files and directories found only in `source`.
     - Files and directories found only in `target`.
   - Outputs the log to `log_file_path`.

5. **Repetitive Synchronization**:
   - The script repeats the synchronization process at the specified interval (`sync_interval`).

## Usage

````bash
python sync_folders.py <source> <target> <sync_interval> <log_file_path>

### Command-Line Arguments

- `<source>`: Path to the source folder.
- `<target>`: Path to the target folder.
- `<sync_interval>`: Time in seconds between synchronization checks.
- `<log_file_path>`: Path to the log file for synchronization details.

### Example

```bash
python sync_folders.py /path/to/source /path/to/target 60 /path/to/sync_log.txt
````

## Notes

- Ensure that you have sufficient permissions to read from the source folder and write to the target folder.
- The script assumes the presence of Python's shutil and filecmp modules for file and directory operations.
