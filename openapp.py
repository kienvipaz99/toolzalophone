def openapp(device):
   device.shell('monkey -p com.zing.zalo -c android.intent.category.LAUNCHER 1')
def start_link(device,link):
   device.shell(f'am start -a android.intent.action.VIEW -d {link}')