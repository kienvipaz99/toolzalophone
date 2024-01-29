import subprocess
import random
import sys
import time
from ppadb.client import Client as AdbClient

def generate_random_imei():
    imei = "35" + ''.join(str(random.randint(0, 9)) for _ in range(12))
    imei_sum = sum(int(digit) for digit in imei[0::2])
    imei_sum += sum(int(digit) * 2 // 10 + int(digit) * 2 % 10 for digit in imei[1::2])
    luhn_digit = (10 - imei_sum % 10) % 10
    return imei + str(luhn_digit)

def get_device_imei(device):
    result = device.shell("service call iphonesubinfo 1 s16 com.android.shell  | cut -d \"'\" -f2 | grep -Eo '[0-9]' | xargs | sed 's/ //g'")
    imei = result.strip()
    return imei
def is_fastboot_mode(device):
    # Kiểm tra trạng thái hiện tại của thiết bị
    current_state = device.get_state()
    print(current_state,'123')
    # Chuyển trạng thái về chuỗi và kiểm tra xem có phải là "fastboot" không
    return current_state == "device" or current_state == "fastboot"

def main():
    client = AdbClient(host="127.0.0.1", port=5037)
    client.create_connection()

    devices = client.devices()

    if not devices:
        print('Không có thiết bị nào kết nối')
        sys.exit(1)

    device = devices[0]
    device_name = device.serial

    imei = generate_random_imei()
    print(f"IMEI mới: {imei}")

    try:
        subprocess.run(["adb", "-s", device_name, "reboot", "bootloader"])
        time.sleep(60)  # Wait for the device to reboot
        subprocess.run(["fastboot", "-s", device_name, "reboot"], stdout=subprocess.DEVNULL)
        time.sleep(10)
        subprocess.run(["fastboot", "-s", device_name, "oem", "writeimei", imei], stdout=subprocess.DEVNULL)
        time.sleep(10)
        # Check the new IMEI
        new_imei = get_device_imei(device)

        print(f"IMEI cũ: {imei}\nIMEI mới: {new_imei}")

    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")
    if is_fastboot_mode(device):
        print("Thiết bị đang ở chế độ fastboot.")
    else:
        print("Thiết bị không ở chế độ fastboot.")
if __name__ == "__main__":
    main()
