# import subprocess
# import cv2
# def find_image_coordinates(image_path, device,threshold=0.99):
#     # Chụp màn hình thiết bị Android và lưu vào file
#     subprocess.run(['adb', '-s', device.serial, 'shell', 'screencap', f'/sdcard/{device.serial}.png'])
#     # Sao chép tệp tin từ thiết bị vào máy tính
#     subprocess.run(['adb', '-s', device.serial, 'pull', f'/sdcard/{device.serial}.png', f'assets/images/{device.serial}.png'])
#     # Xóa tệp tin trên thiết bị sau khi đã sao chép
#     subprocess.run(['adb', '-s', device.serial, 'shell', 'rm', f'/sdcard/{device.serial}.png'])
#     screenshot = cv2.imread(f'assets/images/{device.serial}.png')
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
import pytesseract
def find_image_coordinates(image_path, device):
    threshold=0.99
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
def readimage(device,image_path):
    screenshot_bytes = subprocess.check_output(['adb', '-s', device.serial, 'shell', 'screencap', '-p'])
    screenshot_np = cv2.imdecode(np.frombuffer(screenshot_bytes, np.uint8), cv2.IMREAD_COLOR)
    template = cv2.imread(image_path)
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    x, y = max_loc
    template_height, template_width = template_gray.shape

    x1 = x
    x2 = x + template_width+200
    y1 = y
    y2 = y + template_height

    cropped_img = screenshot_np[y1:y2, x1:x2]

    # Chuyển đổi ảnh sang không gian màu HSV
    hsv = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([0, 0, 175])
    upper_bound = np.array([179, 255, 255])
    msk = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Phóng to vùng mask
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
    dilated = cv2.dilate(msk, kernel, iterations=1)
    thresholded = 255 - cv2.bitwise_and(dilated, msk)

    # Sử dụng OCR để nhận dạng văn bản
    extracted_text = pytesseract.image_to_string(thresholded, config="--psm 10")
    so = extracted_text[extracted_text.find('(') + 1:extracted_text.find(')')]
    return so