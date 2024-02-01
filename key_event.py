def key_event(device,key):
    device.shell(f'input keyevent {key}')
    