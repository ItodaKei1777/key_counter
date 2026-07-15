from pynput.keyboard import Listener
import threading
import time
import collections
import csv
import json
import os

DEFAULT_CONFIG = {
    "save_interval": 5,
    "print_log": True
}

if not os.path.exists("config.json"):
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

csv_data = {}
datas = []
if not os.path.exists("key_datas.csv"):
    with open("key_datas.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["label", "count"])

        for c in range(ord("a"), ord("z") + 1):
            writer.writerow([repr(chr(c)), 0])

with open("key_datas.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        csv_data[row["label"]] = int(row["count"])


lock = threading.Lock()

def function1():
    def on_release(key):
        with lock:
            datas.append(str(key))
    
    with Listener(on_release=on_release) as listener:
        listener.join() 

def function2():
    global datas
    global csv_data
    while True:
        with lock:
            corrent = datas.copy()
            datas.clear()
        
        count_result = collections.Counter(corrent)

        for key, value in count_result.items():
            csv_data[key] = csv_data.get(key, 0) + value

        with open("key_datas.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["label", "count"])

            for key, value in sorted(csv_data.items()):
                writer.writerow([key, value])

        if config["print_log"] == True:
            nowtime = int(time.time()) 
            elapsed_time = nowtime - starttime
            print("elapsed time:" + str(elapsed_time))

        time.sleep(config["save_interval"])

starttime = int(time.time()) 

if config["print_log"] == True:
    print("start counting……!")

thread_1 = threading.Thread(target=function1)
thread_2 = threading.Thread(target=function2)

thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join()