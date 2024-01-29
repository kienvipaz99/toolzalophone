import subprocess

def clone_app(device, original_package_name, clone_package_name):
    try:
        # Sử dụng lệnh adb để cài đặt ứng dụng nhân bản
        cmd = f"adb -s {device.serial}  shell su -c pm clone {original_package_name} " 
        subprocess.run(cmd, shell=True, check=True)
        print(f"Đã nhân bản ứng dụng từ {original_package_name} sang {clone_package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi thực hiện lệnh: {e}")