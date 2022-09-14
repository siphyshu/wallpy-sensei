# =====================
#   wallpy-sensei
#   author: siphyshu
#   version: 1.0
# =====================


# python libraries
# ================
import os, sys
import json
import time, datetime
import configparser
# ================

# utils package
# =============
from utils import *
# =============

# global variables
# ================
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
# ================


def setWallpaper(system, wall_path):
    if system == "win32":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, wall_path , 0)
    else:
        print("not implemented yet for {system}")

if __name__ == '__main__':
    config_file_path = os.path.join(ABS_PATH, 'config.ini')
    config_file = configparser.ConfigParser()
    config_file.read(config_file_path)

    pack_name = config_file["Settings"]["packname"]
    pack_dir = config_file["Settings"]["packdir"]
    schedule = config_file["Settings"]["schedule"]
    scheduleObj = json.load(open(schedule))

    curr_time = datetime.datetime.now().strftime("%H:%M")
    t1 = datetime.datetime.strptime(curr_time,"%H:%M")

    min_delta = (99999999999999, None, None)
    for i in scheduleObj:
        t2 = datetime.datetime.strptime(i, "%H:%M")
        td = abs(t2-t1).total_seconds()
        
        if td < min_delta[0]:
            min_delta = (td, i, scheduleObj[i])

    wall_name = min_delta[2]
    wall_path = os.path.join(pack_dir, wall_name)
    
    system = sys.platform
    setWallpaper(system, wall_path)