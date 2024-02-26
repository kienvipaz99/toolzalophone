import subprocess
def thayDoiProxy(device_serial, ip):
    subprocess.call(f'adb -s {device_serial} shell settings put global http_proxy {ip}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)

def xoaProxy(device):
    subprocess.call(f'adb -s {device.serial} shell settings put global http_proxy :0', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)