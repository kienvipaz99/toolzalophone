# import subprocess
# import cv2
# def find_image_coordinates(image_path, device, name_image,threshold=0.99):
#     # Chụp màn hình thiết bị Android và lưu vào file
#     subprocess.run(['adb', '-s', device.serial, 'shell', 'screencap', f'/sdcard/{name_image}.png'])
#     # Sao chép tệp tin từ thiết bị vào máy tính
#     subprocess.run(['adb', '-s', device.serial, 'pull', f'/sdcard/{name_image}.png', f'assets/images/{name_image}.png'])
#     # Xóa tệp tin trên thiết bị sau khi đã sao chép
#     subprocess.run(['adb', '-s', device.serial, 'shell', 'rm', f'/sdcard/{name_image}.png'])
#     screenshot = cv2.imread(f'assets/images/{name_image}.png')
#     template = cv2.imread(image_path)
#     # Chuyển đổi ảnh và mẫu về định dạng đúng
#     screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
#     template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
#     # Tìm kiếm toạ độ của mẫu trong ảnh chụp màn hình
#     result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
#     _, max_val, _, max_loc = cv2.minMaxLoc(result)
#     # Lấy toạ độ tương đối
#     if max_val < threshold:
#         return 0,0   
#     x, y = max_loc
#     # Lấy kích thước của mẫu
#     template_height, template_width = template_gray.shape
#     # Tính toán toạ độ ở chính giữa hình ảnh mẫu
#     center_x = x + template_width // 2
#     center_y = y + template_height // 2
#     # delete_image(f'assets/images/{name_image}.png')
#     # Trả về toạ độ tương đối ở chính giữa hình ảnh mẫu
#     return center_x, center_y
# def delete_image(image_path):
#     # Xoá tệp tin trên máy tính
#     subprocess.run(['rm', image_path])
    
    
import subprocess
import cv2
import numpy as np
def find_image_coordinates(image_path, device, name_image, threshold=0.99):
    screenshot_bytes = subprocess.check_output(['adb', '-s', device.serial, 'shell', 'screencap', '-p'])
    screenshot_np = cv2.imdecode(np.frombuffer(screenshot_bytes, np.uint8), cv2.IMREAD_COLOR)

    template = cv2.imread(image_path)
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val < threshold:
        return 0, 0

    x, y = max_loc
    template_height, template_width = template_gray.shape
    center_x = x + template_width // 2
    center_y = y + template_height // 2
    
    return center_x, center_y
