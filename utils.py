import json
import time, datetime
import os, ctypes


# wallpaper utils
# ===============
def setWallpaper(system, wall_path):
    if system == "win":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, wall_path , 0)


# misc utils
# ==========
def parseSchedule(wallpack_path):
    '''
    Parses map.json object and builds a masterSchedule
    ready to be used for changing wallpapers for a given wallpack
    '''
    schedule = {}
    pack_items = os.listdir(wallpack_path)

    sunriseTime = [datetime.time(4,30), datetime.time(6,59)]
    morningTime = [datetime.time(7,00), datetime.time(10,29)]
    noonTime = [datetime.time(10,30), datetime.time(15,59)]
    eveningTime = [datetime.time(16,00), datetime.time(17,59)]
    sunsetTime = [datetime.time(18,00), datetime.time(19,59)]
    nightTime = [datetime.time(20,00), datetime.time(4,29)]
    dayTime = [datetime.time(7,00), datetime.time(17,59)]
    totd = {"Sunrise":(sunriseTime), "Morning":(morningTime), "Sunset":(sunsetTime), "Night":(nightTime), "Noon":(noonTime), "Daytime":(dayTime), "Evening":(eveningTime)}

    image_exts = ["png", "jpg", "jpeg", "jfif"]
    extension = pack_items[0].split(".")[1]
 
    # parsing the map.json file here
    wallmap_path = os.path.join(wallpack_path,"map.json")
    wallmap_json = json.load(open(wallmap_path))
    wallmap = {}
    for i in wallmap_json.keys():
        wallmap_item = []
        # list comprehension flex aka faltu ki complexity
        [[wallmap_item.append(x) for x in i] for i in [list(range(ranges[0],ranges[1]+1)) for ranges in [list(map(int,i.split("-"))) for i in [ranges for ranges in wallmap_json[i].split(",")]]]]
        wallmap[i] = [num for num in wallmap_item]

    # calculating the time intervals
    time_interval_map = {}

    for i in wallmap:
        totalWalls = len(wallmap[i])
        if i == "Night":
            time_interval = (time2num(totd[i][1]) + abs(24 - time2num(totd[i][0])))/totalWalls
        else:    
            time_interval = abs(time2num(totd[i][1]) - time2num(totd[i][0]))/totalWalls
        time_interval_map[i] = time_interval

        # making the schedule
        
        for j in wallmap[i]:
            wall_time = (time2num(totd[i][0]) + time_interval*(wallmap[i].index(j)))%24
            schedule[num2htime(wall_time)] = j

    # sorting the schedule
    schedule_sorted = {}
    ordered_schedule = sorted(schedule.items(), key=lambda kv:(kv[1], kv[0]))
    for x,y in ordered_schedule:
        wall_filename = f"{y}.{extension}"
        schedule_sorted[x] = wall_filename

    return schedule_sorted


def writeMasterSchedule(schedule, master_schedule_path):
    scheduleJson = json.dumps(schedule, indent=4)

    with open(master_schedule_path, "w") as f:
        f.write(scheduleJson)


def time2num(timeObj):
    return round(timeObj.hour + timeObj.minute/60, 2)

def num2time(num):
    hours = int(num//1)
    minutes = (num%1)*60
    return datetime.time(int(hours), int(minutes))

def num2htime(num):
    hours = int(num//1)
    minutes = int((num%1)*60)
    return f"{hours}:{minutes}"


def listPacks(wallpack_dir_path):
    wallpacks = os.listdir(wallpack_dir_path)
    [print(i) for i in wallpacks]