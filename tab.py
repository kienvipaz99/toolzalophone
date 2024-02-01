def tap(device, x, y):
    if(x>0 and y>0): 
     device.shell(f'input tap {x} {y}')
    else:
        pass