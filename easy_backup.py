import sys
import os
import filecmp
import shutil

# The following lines enable files in parent_dir to be recognized even if the
# current directory at runtime is elsewhere
parent_dir, filename = os.path.split(os.path.realpath(__file__))
sys.path.insert(1, parent_dir)


class BackupInputError(Exception):
    pass


class UnknownError(Exception):
    pass


def ext(og: str, to_ext: str) -> str:
    return os.path.join(og, to_ext)


def _check_inputs_copy_paste(copy_dir: str, paste_dir: str, depth) -> None:
    
    if not os.path.exists(copy_dir):
        raise BackupInputError(f"The file you are trying to copy at [{copy_dir}] does not exist.")

    if not os.path.exists(paste_dir):
        raise BackupInputError(f"The dir you are trying to paste in at [{paste_dir}] does not exist")
    
    if depth == 0 and not os.path.isdir(copy_dir):
        raise BackupInputError(f"Your copy_dir at [{copy_dir}] is not a directory. Check the file's code and try again.")
    
    if not os.path.isdir(paste_dir):
        raise BackupInputError(f"Your paste_dir at [{paste_dir}] is not a directory. Check your code and try again")

def copy_paste(copy_dir: str, paste_dir: str, depth=0, exclude=[]) -> None:

    _check_inputs_copy_paste(copy_dir, paste_dir, depth)
    
    # Base case
    if os.path.isfile(copy_dir):

        name = os.path.split(copy_dir)[1]
        to_make = ext(paste_dir, name)

        reprint(f"Copying {name}")

        # Only remake if the file does not already exist or if it is different
        if not os.path.exists(to_make) or not filecmp.cmp(copy_dir, to_make):
            shutil.copyfile(copy_dir, to_make)
    
    # If <copy_dir> is not a file, it is a directory. 
    # So, call the function recursively.
    else:
        for name in os.listdir(copy_dir):
            to_copy = ext(copy_dir, name)
            to_make = ext(paste_dir, name)

            reprint(f"Copying {name}")
            
            if to_copy in exclude:
                continue

            elif os.path.isdir(to_copy):
                if not os.path.exists(to_make):
                    os.mkdir(to_make)
                copy_paste(to_copy, to_make, depth+1, exclude)
            
            else:
                copy_paste(to_copy, paste_dir, depth+1, exclude)

# Following functions are just for aesthetic output manipulation

def reprint(message: str) -> None:
    sys.stdout.write("\x1b[K\r")
    sys.stdout.write(f"{message}")

if __name__ == "__main__":

    try:
        from from_and_to import backup_from, backup_to, exclude
    except:
        message = "Error... place backup_files.py in the same directory as " \
        "easy_backup.py for it to properly read the 'from' and 'to' directories"
        raise BackupInputError(message)

    # Uncomment the next line to always keep backup_from to be the directory in 
    # which this script is placed

    # backup_from = parent_dir

    # Run 2 threads
    # one runs the main copy_paste function while the other
    # Runs a timer to be displayed in the console window
    from time import sleep, time
    from threading import Thread

    # define the main function to run in one thread
    stop_timer = False
    success = False
    def main_run():
        global stop_timer
        try:
            copy_paste(backup_from, backup_to, exclude=exclude)
            reprint("")
            print()
            success = True
            stop_timer = True

        except BackupInputError:
            stop_timer = True
            raise

        except:
            stop_timer = True
            raise UnknownError("Unknown Error with copy_paste. Please report issue/ debug to check")
        

    t1 = Thread(target=main_run)
    
    # define the time counting function to run in main thread
    elapsed = 0
    def _display():
        from time import time
        from tkinter import Tk, Label
        start = time()
        global stop_timer
        global elapsed

        root = Tk()
        root.title("Backup Timer")
        root.geometry("250x75")

        timer_label = Label(root, text="", font=("Courier", 15))
        timer_label.pack(pady=20)

        def _count():
            global elapsed

            elapsed = time() - start
            to_print = str(round(elapsed, 1))
            timer_label.config(text="Time elapsed: " + to_print + "s")
            if not stop_timer:
                timer_label.after(1, _count)
            else:
                root.after(3000, root.destroy)
                return None
        
        _count()

        root.mainloop()
 
    t1.start()
    _display()
    t1.join()
    
    # Now log the backup info to the relevant directories if <success> is True
    if success:
        from datetime import datetime

        for logfile_dir in [backup_from, backup_to]:
            logfile_name = ext(logfile_dir, "backup_log.txt")
            
            with open(logfile_name, "a") as out_file:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = f"{now} : [{backup_from}] to [{backup_to}] in {round(elapsed, 5)}s.]"
                out_file.write("\n" + message)

        print("\nBackup successful ...")
        sleep(30)
    else:
        sleep(30)
    