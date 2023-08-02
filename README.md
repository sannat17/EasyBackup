# Disclaimer
I made this little personal project while learning how to program during my first semester at the University of Toronto (CSC108H1: Introduction to Computer Programming) to apply my learnings to solve a real world problem I faced: Creating local backups (perhaps to a directory synced with a cloud provider) of files and directories with granular control over what I want backed up.

# Welcome to EasyBackup!
This is a little project I started to make a custom backup script (using Python) for myself to use on any file/ folder I want.

I made it so that I can run manual backups of important files and folders on my PC as and when I wish to.

**I am open to any help/ suggestions to make this script more efficient, add more features and learn more!**

**Click** [here](#how-to-help) **to scroll down and see how you can contribute/ help.**
## How to use
 - Add `easy_backup.py` to a directory.
 - Edit the `backup_to` and `backup_from` directories in `from_and_to.py`.
 - Run `easy_backup.py` and follow the directions in the console window.
 - Once execution is complete, check `backup_log.txt` to see the history of backups including which directories were involved and how much time the backup took.

## Learnings from this project
### Includes knowledge and practice of:
 - Multithreading:
    - By using Python's `threading` library
 - Trees and Recursion:
   - This is due to the similarity of the file structure in a PC to the Tree ADT.
 - Writing python scripts to automate PC tasks:
   - Manipulating files using Python.
 - Advanced I/O manipulation in Python.

## Shortcomings:
 - There is no failure management system in case the script is stopped or system is shut down before execution is complete.
 - Does not delete files present in the `backup_to` folder that are removed from `backup_from` folder

## How to help
If anybody is even reading this and has suggestions regarding the features/ issues below, or wants to add something to work on, contact me to figure out how to help.

### Currently working on:
 - Code cleanup
 - Capability to exclude certain files/ folders.
 - Increase efficiency using multithreading to recurse through multiple folders simultaneously.
 - Delete files present in the `backup_to` folder that are removed from `backup_from` folder

### For the future:
 - Failure management
 - GUI
   - Use Python's `tkinter` library or find some other toolkit.
   - Manage multiple files/ folders to backup along with locations, all from a single, unified GUI.
   - Could add scheduled tasks (and instructions on how to set it up)
 - Replicate this using other programming languages.
 - Try different methods than the one I used to see what works best.
