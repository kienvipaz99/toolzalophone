import os
import base64

def input_text(device,text):
        text = str(base64.b64encode(text.encode('utf-8')))[2:-1]
        broadcast_command = f"adb -s {device.serial} shell am broadcast -a ADB_INPUT_B64 --es msg {text}"
        os.system(broadcast_command)
        return
