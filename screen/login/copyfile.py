import subprocess

def copy_and_install_apk(device, package):
    try:
        # Lấy đường dẫn của gói ứng dụng trên thiết bị
        link = subprocess.check_output(['adb', '-s', device.serial, 'shell', 'pm', 'path', package]).decode().strip()
        cleaned_link = link.replace('package:', '').strip()
        
        # Tạo tên file APK mới từ tên gói ứng dụng
        new_package_name = package.replace('.', '_')
        
        # Tải file APK về máy tính
        subprocess.run(['adb', '-s', device.serial, 'pull', cleaned_link, f'{new_package_name}.apk'])
        print(package,new_package_name)
        # Cài đặt ứng dụng với tên gói mới
        subprocess.run(['adb', '-s', device.serial, 'install', '--package-name', "com.zing3.zalo", f'{new_package_name}.apk'])     
        print(f"Cài đặt thành công file APK của {package}")
        # # Xoá file APK sau khi cài đặt
        # subprocess.run(['rm', f'{new_package_name}.apk'])
        # print(f"Đã xoá file APK sau khi cài đặt")
        
    except subprocess.CalledProcessError as e:
        print(f"Lỗi: {e}")