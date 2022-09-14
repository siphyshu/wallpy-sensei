# =====================
#   wallpy-sensei
#   author: siphyshu
#   version: 1.0
# =====================


# python libraries
# ================
import os, sys, ctypes
import json
import time
import random
import argparse, configparser
# ================

# utils package
# =============
from utils import *
# =============

# global variables
# ================
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
WALLPAPERS_DIR = os.path.join(ABS_PATH, "wallpaper-packs")
ASCII_ART = r'''_\/_                 |                _\/_
/o\\    wallpy-  \       /            //o\
 |      sensei     .---.                |
_|_______     --  /     \  --     ______|__
         `~^~^~^~^~^~^~^~^~^~^~^~`'''
# ================


def arguementParser(argv=None):
    '''
    Returns an argparse object.

    Usage:
    args = arguementParser() <- use supplied args in cli
    args = arguementParser(['arg1', 'arg2']) <- use supplied args in list, good for testing
    '''
    parser = argparse.ArgumentParser(description="Wallpy-Chameleon is a dynamic wallpaper utility (Windows/Mac) to change wallpapers based on the time of the day. Choose from a wide set of wallpaper packs - and even add your own!")

    parser.add_argument("pack", help="Name of the wallpaper pack")

    return parser.parse_args(argv)


if __name__ == "__main__":
    print(ASCII_ART, "\n")

    # arguement parsing stuff
    args = arguementParser()
    # args = arguementParser(["Zelda Wind Walker"])
    packs = os.listdir(WALLPAPERS_DIR)
    
    # wallpaper config stuff
    try:
        wallpack = args.pack.strip()
        wallpack_dir = os.path.join(WALLPAPERS_DIR, wallpack)
        wallpack_items = os.listdir(wallpack_dir)
        schedule_path = os.path.join(wallpack_dir, "schedule.json")
        master_schedule_path = os.path.join(ABS_PATH, "masterSchedule.json")
        config_file = configparser.ConfigParser()
        config_file["Settings"] = {
            "PackName": wallpack,
            "PackDir" : wallpack_dir,
            "Schedule": master_schedule_path
            }
        with open(r"config.ini", "w") as configfileObj:
            config_file.write(configfileObj)
            configfileObj.flush()
            configfileObj.close()
    except FileNotFoundError:
        print("[!] Pack not found")
        print("[*] Packs available: ")
        for i, pack in enumerate(packs):
            print(f"        {i+1}. {pack}")


    # set the schedule
    schedule = parseSchedule(wallpack_dir)
    print(schedule)
    master_schedule_path = os.path.join(ABS_PATH, "masterSchedule.json")
    writeMasterSchedule(schedule, master_schedule_path)