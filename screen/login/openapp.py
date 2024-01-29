def openapp(device):
   device.shell('monkey -p com.zing.zalo -c android.intent.category.LAUNCHER 1')