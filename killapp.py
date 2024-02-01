import subprocess
def kill_and_restart_app(package_name):
    # Gửi lệnh để "kill" ứng dụng
    subprocess.run(["adb", "shell", "am", "force-stop", package_name])

    # Gửi lệnh để khởi động lại ứng dụng
    subprocess.run(["adb", "shell", "am", "start", "-n", f"{package_name}/com.zing.zalo.ui.ZaloLauncherActivity"])