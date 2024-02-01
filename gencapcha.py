import subprocess,cv2
import numpy as np
from swip import swip
def bypass_slide(devices,so,so2,so3,so4):
    num_attempts=5
    for _ in range(num_attempts):
        pipe = subprocess.Popen(f'adb -s {devices} exec-out screencap -p',
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, shell=True)
        image_bytes = pipe.stdout.read()
        image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        so = int(so)
        so2 = int(so2)
        so3 = int(so3)
        so4 = int(so4)
        img = image[so2:so4,so:so3]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img3 = cv2.Canny(gray, 200, 200, L2gradient=True)
        kernel = np.ones([23,23])
        kernel[2:,2:] = -0.1
        im = cv2.filter2D(img3/255, -1, kernel)
        im1 = im[:,:125]
        y1,x1 = np.argmax(im1)//im1.shape[1], np.argmax(im1)%im1.shape[1]
        im2 = im[:,125:]
        y2,x2 = np.argmax(im2)//im2.shape[1], np.argmax(im2)%im2.shape[1] + 125
        difference = x2 - x1

    return difference
def slide_captcha(device,x,y,so,so2,so3,so4):
    captcha = bypass_slide(device.serial,so,so2,so3,so4)
    swip(device,x, y, int(captcha)+x, y)
    return True