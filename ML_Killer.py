import psutil
import os
import time
import signal

odt="OculusDebugTool.exe"
odtkra="ODTKRA.exe"
odtkra_path="ODTKRA.exe" # Change this to your ODTKRA.exe path

os.startfile(odtkra_path)
time.sleep(5)

def get_pid(name):
    for proc in psutil.process_iter():
        if proc.name() == name:
            pid = proc.pid
            return pid
            
def get_ram(pid):
    process = psutil.Process(pid)

    memory_info = process.memory_info()
    rss = memory_info.rss / 2**20

    return round(rss, 2)

def kill_process(odt_pid, odtkra_pid):
    try:
        os.kill(odtkra_pid, signal.SIGTERM)
    except:
        print("Error killing ODTKRA")

    try:
        os.kill(odt_pid, signal.SIGTERM)
    except:
        print("Error killing ODT")

    
while True:

    leak_size= get_ram(get_pid(odt))

    print("pid: " + str(get_pid(odt)) + " | odt is using " + str(leak_size) + " MB of RAM")

    if leak_size > 750:
        print("MEMORY LEAK DETECTED!!!")
        print("KILLING ODT!!!")

        kill_process(get_pid(odt), get_pid(odtkra))
        time.sleep(0.5)
        
        print("RESTARTING ODT!!!")
        os.startfile(odtkra_path)

    time.sleep(60)
