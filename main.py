import time
import os
from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading


lowest_brightness = 1

def decrease_brightness():
    os.system(f"powershell -Command (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, {lowest_brightness}) ")
    print(f"brightness set to {lowest_brightness}")



def current_brightness():
    result = os.popen("powershell (Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightness).CurrentBrightness")
    return result.read().strip()



def increase_brightness(brightness):
     os.system(f"powershell -Command (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, {brightness}) ")
     print(f"Increased screen brightness to {brightness}%")


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
    
        
        os.system("powershell [System.Media.SystemSounds]::Asterisk.Play()")
        decrease_brightness()
    
        time.sleep(delay)
    
        os.system("powershell [System.Media.SystemSounds]::Hand.Play()") #playes a bell sound on completion
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