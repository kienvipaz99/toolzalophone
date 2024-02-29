import subprocess,os
from time import sleep
def check_and_install_adb_ime(device):
    ime_list_command = f"adb -s {device.serial} shell ime list -a"
    result = subprocess.run(ime_list_command, shell=True, capture_output=True, text=True)
    if "com.android.adbkeyboard/.AdbIME" not in result.stdout:
        subprocess.call(['adb', '-s', device.serial, 'install', 'path/to/ADBKeyboard.apk'])
        ime_command = f"adb -s {device.serial} shell ime set com.android.adbkeyboard/.AdbIME"
        os.system(ime_command)