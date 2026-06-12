import time
import subprocess
from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading
import re
import winsound


lowest_brightness = 1

def decrease_brightness():
    subprocess.run(
    ["powershell", "-Command", f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, {lowest_brightness})"],
    creationflags = subprocess.CREATE_NO_WINDOW
    )
    print(f"brightness set to {lowest_brightness}")


def increase_brightness(brightness):
     subprocess.run(
    ["powershell", "-Command", f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, {brightness})"],
    creationflags=subprocess.CREATE_NO_WINDOW
    )
     print(f"Increased screen brightness to {brightness}%")


def current_brightness():
    result = str(subprocess.run(
    ["powershell", "-Command", "(Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightness).CurrentBrightness"],
    capture_output=True,
    text=True,
    creationflags=subprocess.CREATE_NO_WINDOW
    ))

    value_num_list = re.findall(r'\d+', result)

    value = value_num_list[1]
    return value




interval = 20 #in minutes
delay = 20 #in seconds
toggle = True


def eyerest_loop():
    while toggle:
        print(f"waiting {interval} minutes")
        time.sleep(interval*60)
        print("done waiting")
        
        now_brightness = current_brightness()
        print(f"Current brightness = {now_brightness}")
    
        
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)
        decrease_brightness()
    
        time.sleep(delay)
    
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC) #playes a bell sound on completion

        increase_brightness(now_brightness)
    

def setup_tray():
    image = Image.open("W:/Projects/EyeRest/icon.png")
    
    menu = Menu(
        MenuItem("Exit", lambda: icon.stop())
    )
    
    icon = Icon("EyeRest", image, "EyeRest", menu)
    
    threading.Thread(target=eyerest_loop, daemon=True).start()

    icon.run()

if __name__ == "__main__":
    setup_tray()