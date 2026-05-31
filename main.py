
try:
    from termcolor import colored
    print("[ ",colored("x","green")," ]","    Library Importing Succesfull.")
except:
    print(print("[ ","x"," ]","    Library Importing Succesfull."))
try:
    import os
    import sys
    import subprocess 
    import logging
    from datetime import datetime
    import builtins
    print("[ ",colored("x","green")," ]","    Library Importing Succesfull.")
except:
    print("[ ",colored("x","red")," ]","    Library Importing Failed.")
    
    
from clean_logs import ROOT
LOGS = ROOT/"logs"
# creating log directory if it doesn't exists
os.makedirs(LOGS, exist_ok=True)


# Create timestamped log file
log_filename = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    filename    =   LOGS/log_filename,
    level       =   logging.INFO,
    format      =   "%(asctime)s | %(message)s"
)

# Store original print
original_print = builtins.print

# Override print
def print(*args, **kwargs):
    message = " ".join(str(arg) for arg in args)
    logging.info(message)
    original_print(*args, **kwargs)



# Script File Paths
dataset_gen_path    =   r"dataset_gen.py"
sweep_path          =   r"sweep.py"
log_clean_path      =   r"clean_logs.py"

print("[ ",colored("x","green")," ]","    File paths used: ")
print("[ ",colored("x","green")," ]    ",    dataset_gen_path)
print("[ ",colored("x","green")," ]","    Checking the Dataset validity...")

#process_2 = subprocess.run([sys.executable, log_clean_path])
import dataset_gen
import sweep