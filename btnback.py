import subprocess
def back(device):
    subprocess.run(f'adb -s {device.serial} shell input keyevent 4', shell=True, check=True)
   