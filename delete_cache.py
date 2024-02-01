import subprocess

def delete_cache(device, package):
    try:
        subprocess.run(["adb", "-s", device.serial, "shell", "pm", "clear", package], check=True)
    except subprocess.CalledProcessError as e:
        pass