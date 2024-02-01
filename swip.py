def swip(device, x1, y1, x2, y2):
    device.shell(f'input swipe {x1} {y1} {x2} {y2} 1000')