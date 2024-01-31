from ppadb.client import Client as AdbClient
from openapp import openapp
from time import sleep
from find_image import find_image_coordinates
from input import input_text
from tab import tap
from key_event import key_event
import os
import random
import subprocess
from delete_cache import delete_cache
from gencapcha import slide_captcha
from find_text import get_element,get_coordinates_capcha
from btnback import back
from swip import swip
from killapp import kill_and_restart_app
from datetime import datetime
import time
def get_devices():

    try:
        subprocess.run(["adb", "start-server"])
        client = AdbClient(host="127.0.0.1", port=5037)
        devices = client.devices()
        if not devices: 
            return []
        return devices
    except:
       return []
        

def check_key_board(device_serial, package_name):
    result = subprocess.run(['adb', '-s', device_serial, 'shell', 'pm', 'list', 'packages', package_name], capture_output=True, text=True)
    return package_name in result.stdout
def findElementByName(device, name):
     center_x,center_y=get_element(device.serial,'text',name)
     return center_x,center_y
def findElementById(device, id):
    center_x,center_y=get_element(device.serial,"resource-id",id)
    return center_x,center_y
def findElementByClass(device, className):
    center_x,center_y=get_element(device.serial,"class",className)
    return center_x,center_y

def add_friend_numberphone(device, mins, max, maxaction, data, type):
    center_x,center_y =findElementById(device,'com.zing.zalo:id/maintab_message')
    tap(device, center_x, center_y)
    sleep(random.randint(mins, max))
    if(type == 'Kết bạn theo sđt'):
        center_x, center_y = find_image_coordinates('assets/images/find_friend.png', device, device.serial)
        tap(device, center_x, center_y)
        sleep(random.randint(mins, max))
        data_phone = str(data).split()
        data_list = list(set(data_phone))
        num_iterations = min(len(data_list), maxaction)

        for i in range(num_iterations):
            number = data_list[i]
            input_text(device, text=number)
            center_x, center_y = findElementById(device, 'com.zing.zalo:id/btn_search_result')
            
            if(center_x == 0 and center_y == 0):
                center_x, center_y = findElementById(device, 'com.zing.zalo:id/clear_btn')
                tap(device, center_x, center_y)
            else:
                tap(device, center_x, center_y)
                sleep(random.randint(mins, max))
                center_x, center_y = findElementById(device, 'com.zing.zalo:id/btn_send_friend_request')
                tap(device, center_x, center_y)
                sleep(random.randint(mins, max))
                center_x, center_y = findElementById(device, 'com.zing.zalo:id/btnSendInvitation')
                tap(device, center_x, center_y)
                sleep(random.randint(mins, max))
                center_x, center_y = findElementByName(device, 'Đã hiểu')
                if (center_x>0 and center_y>0):
                    tap(device, center_x, center_y)
                    sleep(random.randint(mins, max))
                    i =0
                    while i<3:
                        i+=1
                        back(device)
                        sleep(2)
                        
                back(device)
                center_x, center_y = findElementById(device, 'com.zing.zalo:id/clear_btn')
                tap(device, center_x, center_y)
        
        back(device)
        sleep(2)
        back(device)

    elif(type=='Kết bạn theo gợi ý'):
        while True:
            x, y = find_image_coordinates('assets/images/find_more.png', device, device.serial)
            if x==0 and y==0:
                swip(device,514,897,535,533)
            else:
                center_x, center_y = find_image_coordinates('assets/images/viewadd.png', device, device.serial)
                tap(device,center_x,center_y)
                sleep(random.randint(mins,max))
                
                for i in range(maxaction):
                    center_x, center_y = findElementById(device, 'com.zing.zalo:id/btn_combine_func_1')
                    if(center_x>0 and center_y>0):
                        tap(device,center_x,center_y)
                        sleep(random.randint(mins,max))
                        swip(device,514,897,535,533)
                            
                    else:
                        break
                back(device)
                break
    elif(type=='Kết bạn trong nhóm(trừ trưởng ,phó nhóm)'):
        print('Kết bạn trong nhóm(trừ trưởng ,phó nhóm)')
    #Lướt New feed
def swip_newfeed(device,min_number,max_number,number_action):
        center_x, center_y = find_image_coordinates('assets/images/newfeed.png', device, device.serial)
        tap(device, center_x, center_y)
        sleep(random.randint(min_number, max_number))
        actions_performed = 0 
        while actions_performed < number_action:
            
            x,y=findElementById(device,'com.zing.zalo:id/feedItemLastSuggest')
            if(x>0 and y>0):
                break
            center_x,center_y=findElementById(device,'com.zing.zalo:id/btnLogin')
            if(center_x>0 and center_y>0):
                break
            center_x, center_y = find_image_coordinates('assets/images/love.png', device, device.serial)
            if center_x > 0 and center_y > 0:
                tap(device, center_x, center_y)
                actions_performed += 1 
                swip(device, 690, 1722, 536, 569)
                sleep(4)
            else:
                swip(device, 516, 1676, 536, 569)
        print('oke')
def post1(device, min_number, max_number, content,file_list):
        for file_path in file_list:
            current_timestamp = time.mktime(datetime.now().timetuple())

            # Thay đổi ngày sửa đổi của tệp thành thời gian hiện tại
            os.utime(file_path, (current_timestamp, current_timestamp))

            file_name = os.path.basename(file_path)
            destination_path = f'/sdcard/DCIM/{file_name}'

            # Đẩy file lên thiết bị
            subprocess.run(['adb', '-s', device.serial, 'push', file_path, destination_path], capture_output=True)

            # Kích hoạt trình quét media
            subprocess.run(['adb', '-s', device.serial, 'shell', 'am', 'broadcast', '-a', 'android.intent.action.MEDIA_SCANNER_SCAN_FILE', '-d', f'file://{destination_path}'], capture_output=True)
        
        center_x,center_y=findElementByName(device,'CHO PHÉP TRUY CẬP')
        if center_x >0 and center_y >0:
            tap(device,center_x,center_y)
            sleep(random.randint(min_number, max_number))
            center_x,center_y=findElementByName(device,'CHO PHÉP')
            tap(device,center_x,center_y)
        center_x,center_y=findElementById(device,'com.zing.zalo:id/media_picker_layout')
        tap(device,center_x,center_y)
        sleep(5)
def post2(device, min_number, max_number, content,file_list):
        for file_path in file_list:
            # Lấy thời gian hiện tại dưới dạng timestamp
            current_timestamp = time.mktime(datetime.now().timetuple())

            # Thay đổi ngày sửa đổi của tệp thành thời gian hiện tại
            os.utime(file_path, (current_timestamp, current_timestamp))

            file_name = os.path.basename(file_path)
            destination_path = f'/sdcard/DCIM/{file_name}'

            # Đẩy file lên thiết bị
            subprocess.run(['adb', '-s', device.serial, 'push', file_path, destination_path], capture_output=True)

            # Kích hoạt trình quét media
            subprocess.run(['adb', '-s', device.serial, 'shell', 'am', 'broadcast', '-a', 'android.intent.action.MEDIA_SCANNER_SCAN_FILE', '-d', f'file://{destination_path}'], capture_output=True)
            
        center_x, center_y = find_image_coordinates('assets/images/library.png', device, device.serial)
        tap(device, center_x, center_y)
        sleep(random.randint(min_number, max_number))
        center_x, center_y = find_image_coordinates('assets/images/allow_access.png', device, device.serial)
        if center_x >0 and center_y >0:
            tap(device,center_x,center_y)
            sleep(random.randint(min_number, max_number))
            center_x, center_y = find_image_coordinates('assets/images/access.png', device, device.serial)
            tap(device,center_x,center_y)
        center_x,center_y=find_image_coordinates(device,'take_a_ photo.png')
        tap(device,center_x,center_y+200)
        sleep(5)
        # Đăng bài
def post(device, min_number, max_number, content, files):
        if isinstance(files, str):
            file_list = files.split()
        else:
            file_list = files
        center_x, center_y = find_image_coordinates('assets/images/newfeed.png', device, device.serial)
        tap(device, center_x, center_y)
        sleep(random.randint(min_number, max_number))
        center_x,center_y=findElementById(device,'com.zing.zalo:id/action_bar_new_post_btn')
        tap(device, center_x, center_y)
        sleep(random.randint(min_number, max_number))
        if(len(file_list)>0):
            post1(device, min_number, max_number, content,file_list)
            action=0
            while action < len(file_list):
                center_x, center_y = find_image_coordinates('assets/images/select_image.png', device, device.serial)
                if center_x==0 and center_y==0: 
                    tap(device,450, 450)
                    sleep(2)
                if center_x>0 and center_y>0:
                    tap(device,center_x, center_y)
                    swip(device, 985, 1064, 55, 1171)
                    sleep(2)
                    action+=1

            center_x, center_y = find_image_coordinates('assets/images/comfirm_image.png', device, device.serial)
            tap(device,center_x,center_y)
            sleep(random.randint(min_number, max_number))
        center_x,center_y=findElementById(device,'com.zing.zalo:id/etDesc')
        tap(device, center_x, center_y)
        sleep(random.randint(min_number, max_number))
        input_text(device,text=content)
        sleep(random.randint(min_number, max_number))
        center_x,center_y=findElementById(device,'com.zing.zalo:id/bt_post_feed')
        tap(device,center_x,center_y)
        #Đồng ý kết bạn
def agree_to_make_friends(device,min_number,max_number,number_action,type):
    center_x, center_y = find_image_coordinates('assets/images/danhba.png', device, device.serial)
    tap(device,center_x, center_y)
    center_x, center_y = find_image_coordinates('assets/images/danhba1.png', device, device.serial)
    tap(device,center_x, center_y)
    sleep(random.randint(min_number, max_number))
    center_x,center_y=findElementById(device,'com.zing.zalo:id/tvFriendRequest')
    tap(device,center_x, center_y)
    sleep(random.randint(min_number, max_number))
    x,y=findElementById(device,'com.zing.zalo:id/btn_accept')
    if(type =='Đồng ý theo số lượng'):
        if number_action >0:
            action=0
            while action < number_action:        
                    if x >0 and y>0:
                        tap(device,x, y)
                        sleep(random.randint(min_number, max_number))
                        center_x,center_y=findElementById(device,'com.zing.zalo:id/btn_accept')
                        tap(device,center_x,center_y)
                        center_x,center_y=findElementById(device,'com.zing.zalo:id/btnAccept')
                        tap(device,center_x,center_y)
                        action+=1
                    else:
                        if(x==0 and y==0):
                            swip(device, 557, 688, 573, 443)
                        break
        back(device)

    elif type == 'Đồng ý tất cả':
            while True:        
                    if center_x >0 and center_y>0:
                        tap(device,center_x, center_y)
                        swip(device, 557, 688, 573, 443)
                        sleep(random.randint(min_number, max_number))
                        center_x,center_y=findElementById(device,'com.zing.zalo:id/btnAccept')
                        tap(device,center_x,center_y)
                        center_x,center_y=findElementById(device,'com.zing.zalo:id/btnAccept')
                        tap(device,center_x,center_y)
                    else:
                        if(x==0 and y==0):
                            swip(device, 557, 688, 573, 443)
                        break
            back(device)
#Huỷ kết bạn
def unfriend(device,min_number,max_number,number_action,type):
    center_x, center_y = find_image_coordinates('assets/images/danhba.png', device, device.serial)
    tap(device,center_x, center_y)
    center_x, center_y = find_image_coordinates('assets/images/danhba1.png', device, device.serial)
    sleep(random.randint(min_number, max_number))
    center_x,center_y=findElementById(device,'com.zing.zalo:id/tvFriendRequest')
    tap(device,center_x, center_y)
    sleep(random.randint(min_number, max_number))
    center_x,center_y=findElementById(device,'com.zing.zalo:id/tvTabRequesFromMe')
    tap(device,center_x, center_y)
    sleep(random.randint(min_number, max_number))
    if(type =='Thu hồi theo số lượng'):
            action=0 
            while action < number_action:
                    center_x, center_y = find_image_coordinates('assets/images/recall.png', device, device.serial)
                    if center_x >0 and center_y>0:
                        tap(device,center_x, center_y)
                        sleep(random.randint(min_number, max_number))
                        action+=1
                    else:
                        swip(device, 557, 688, 573, 443)
                        if(center_x==0 and center_y==0):
                            break
            back(device)
       
    elif type == 'Thu hồi tất cả':
            while True:       
                    center_x, center_y = find_image_coordinates('assets/images/recall.png', device, device.serial) 
                    if center_x >0 and center_y>0:
                        tap(device,center_x, center_y)
                        sleep(random.randint(min_number, max_number))
                    else:
                        swip(device, 557, 688, 573, 443)
                        if(center_x==0 and center_y==0):
                            break
            back(device)
            # nhắn tin
def sent_messages(device,min_number,max_number,content,number_action,file,type,data_number):
        if isinstance(file, str):
            file_list = file.split()
        else:
            file_list = file
        if(type=='Nhắn tin theo số điện thoại'):
            center_x,center_y =findElementById(device,'com.zing.zalo:id/maintab_message')
            tap(device, center_x, center_y)
            sleep(random.randint(min_number, max_number))
            center_x, center_y = find_image_coordinates('assets/images/find_friend.png', device, device.serial)
            tap(device, center_x, center_y)
            sleep(random.randint(min_number, max_number))
            data_phone = str(data_number).split()
            data_list = list(set(data_phone))
            num_iterations = min(len(data_list), int(number_action))
            for i in range(num_iterations):
                number = data_list[i]
                input_text(device, text=number)
                center_x, center_y = findElementById(device, 'com.zing.zalo:id/btn_search_result')
                if(center_x == 0 and center_y == 0):
                    center_x, center_y = findElementById(device, 'com.zing.zalo:id/clear_btn')
                    tap(device, center_x, center_y)
                else:
                    tap(device, center_x, center_y)
                    sleep(random.randint(min_number, max_number))
                    center_x, center_y = findElementById(device, 'com.zing.zalo:id/tvSendMes_ob')
                    tap(device, center_x, center_y)
                    center_x, center_y = findElementById(device, 'com.zing.zalo:id/btn_send_message')
                    tap(device, center_x, center_y)
                    sleep(random.randint(min_number, max_number))
                    
                    if(len(file_list)):
                        center_x, center_y = findElementById(device, 'com.zing.zalo:id/new_chat_input_btn_show_gallery')
                        tap(device, center_x, center_y)
                        post1(device, min_number, max_number, content,file_list)
                        center_x,center_y=findElementById(device,'com.zing.zalo:id/landing_page_tv_hd')
                        tap(device,center_x, center_y)
                        sleep(2)
                        center_x,center_y=findElementByName(device,'GHI NHỚ')
                        tap(device,center_x, center_y)
                        sleep(2)
                        for i in range(len(file_list)):
                            center_x,center_y=findElementById(device,'com.zing.zalo:id/landing_page_tv_select')
                            if center_x>0 and center_y>0:
                                tap(device,center_x, center_y)
                                sleep(2)
                                swip(device, 985, 1064, 55, 1171)
                            else:
                                kill_and_restart_app('com.zing.zalo')
                                sleep(10)
                                post1(device, min_number, max_number, content,file_list)
                                tap(device,center_x, center_y)
                                sleep(2)    
                                break
                        center_x,center_y=findElementById(device,'com.zing.zalo:id/landing_page_layout_send')
                        tap(device, center_x, center_y)
                        sleep(random.randint(min_number, max_number))
                        
                        
                    center_x,center_y=findElementById(device,'com.zing.zalo:id/chatinput_text')
                    tap(device, center_x, center_y)
                    sleep(2)
                    input_text(device, text=content)
                    sleep(random.randint(min_number, max_number))
                    center_x,center_y=findElementById(device,'com.zing.zalo:id/new_chat_input_btn_chat_send')
                    tap(device, center_x, center_y)
                    i =0
                    while i<3:
                        i+=1
                        back(device)
                        sleep(2)
                    center_x, center_y = findElementById(device, 'com.zing.zalo:id/clear_btn')
                    tap(device, center_x, center_y)
                    sleep(random.randint(min_number, max_number))
            back(device)
            sleep(2)
            back(device)
            sleep(2)
            
        elif type =='Nhắn tin vào hội nhóm':
            center_x,center_y =find_image_coordinates('assets/images/danhba.png',device,device.serial)
            tap(device, center_x, center_y)
            center_x, center_y = find_image_coordinates('assets/images/danhba1.png', device, device.serial)
            sleep(random.randint(min_number, max_number))
            center_x, center_y = find_image_coordinates('assets/images/select_group.png', device, device.serial)
            tap(device, center_x, center_y)
            center_x, center_y = find_image_coordinates('assets/images/zerogroup.png', device, device.serial)
            if center_x==0 and center_y==0:
                center_x, center_y = find_image_coordinates('assets/images/group.png', device, device.serial)
                i=0
                while i< max_number:
                    swip(device, 363, 1400, 360, 1150)
                    tap(device,center_x, center_y)
                    sleep(random.randint(min_number, max_number))
                    if len(file_list)>0:
                        post2(device, min_number, max_number, content,file_list)
                        for i in range(len(file_list)):
                            center_x, center_y = find_image_coordinates('assets/images/select_image.png', device, device.serial)
                            if(center_x==0 and center_y==0):
                                tap(device,450, 450)
                                sleep(2)
                            if center_x>0 and center_y>0:
                                tap(device,center_x, center_y)
                                swip(device, 985, 1064, 55, 1171)
                                sleep(2)
                        center_x, center_y = find_image_coordinates('assets/images/sent_image.png', device, device.serial)
                        tap(device,center_x, center_y)
                        sleep(random.randint(min_number, max_number))
                    center_x, center_y = find_image_coordinates('assets/images/meesage.png', device, device.serial)
                    tap(device,center_x, center_y)
                    input_text(device,text=content)
                    sleep(random.randint(min_number, max_number))
                    center_x, center_y = find_image_coordinates('assets/images/sent.png', device, device.serial)
                    tap(device,center_x, center_y)
                    sleep(random.randint(min_number, max_number))
                    back(device)
                    i+=1
def comment_post(device,min_number,max_number,number_action,content):
    center_x, center_y = find_image_coordinates('assets/images/newfeed.png', device, device.serial)
    tap(device, center_x, center_y)
    sleep(random.randint(min_number, max_number))
    i=0
    while i < number_action:
        center_x,center_y=findElementById(device,'com.zing.zalo:id/btnLogin')
        if(center_x>0 and center_y>0):
            break
        x,y=findElementById(device,'com.zing.zalo:id/feedItemLastSuggest')
        if(x>0 and y>0):
                break
        center_x,center_y=findElementById(device,'com.zing.zalo:id/comment_input_bar')
        x,y=findElementById(device,'com.zing.zalo:id/btn_comment')
        
        if (center_x > 0 and center_y > 0) or(x>0 and y>0) :
            tap(device, center_x, center_y)
            sleep(random.randint(min_number, max_number))
            center_x,center_y=findElementById(device,'com.zing.zalo:id/comment_input_bar')
            tap(device, center_x, center_y)
            input_text(device,text=content)
            sleep(random.randint(min_number, max_number))
            center_x,center_y=findElementById(device,'com.zing.zalo:id/cmtinput_send')
            tap(device, center_x, center_y)
            
            sleep(random.randint(min_number, max_number))
            back(device)
            sleep(2)
            swip(device, 690, 1722, 536, 410)
            i+=1
        else:
            swip(device, 516, 1676, 536, 410)
def login(device,account_info):
    delete_cache(device,"com.zing.zalo")
    sleep(random.randint(5,10))
    openapp(device)
    sleep(random.randint(20,30))
    center_x,center_y=findElementById(device,'com.zing.zalo:id/btnLogin')
    tap(device,center_x,center_y)
    sleep(random.randint(3,5))
    center_x,center_y=findElementByName(device,'CHO PHÉP')
    tap(device,center_x,center_y)
    sleep(random.randint(3,5))
    center_x,center_y=findElementByName(device,'CHO PHÉP')
    if center_x != 0 and center_y != 0:
        tap(device,center_x,center_y)
        sleep(random.randint(3,5))
    center_x,center_y=findElementById(device,'com.zing.zalo:id/edtAccount')
    tap(device,center_x,center_y)
    input_text(device,text=account_info[1])
    sleep(random.randint(2,5))
    center_x,center_y=findElementById(device,'com.zing.zalo:id/edtPass')
    tap(device,center_x,center_y)
    sleep(random.randint(2,5))
    input_text(device,text=account_info[2])
    sleep(random.randint(2,5))
    center_x,center_y=get_element(device.serial,'resource-id','com.zing.zalo:id/btnLogin')
    tap(device,center_x,center_y)
    sleep(random.randint(15,20))
    while True:
        center_x,center_y=findElementByName(device,'Xác thực bằng Captcha')
        if center_x==0 and center_y==0:
            x,y=get_element(device.serial,'resource-id','com.zing.zalo:id/btnLogin')
            if x==0 and y==0:
               
                break
            else:
                tap(device,x,y)
        else:
         center_x, center_y = get_element(device.serial,'resource-id','track_btn')
         so,so2,so3,so4=get_coordinates_capcha(device.serial,"resource-id",'sd_bg')
         slide_captcha(device, center_x, center_y,so,so2,so3,so4)
         sleep(5)
    center_x, center_y = findElementById(device,'com.zing.zalo:id/btn_ignore')
    tap(device,center_x,center_y)
    center_x, center_y = findElementById(device,'com.zing.zalo:id/btn_positive_modal')
    tap(device,center_x,center_y)
    sleep(random.randint(5,10))
    center_x,center_y= findElementById(device,'com.zing.zalo:id/btn_skip')
    tap(device,center_x,center_y)
    sleep(random.randint(5,10))
    center_x,center_y= findElementById(device,'com.zing.zalo:id/btn_negative_modal')
    tap(device,center_x,center_y)
    sleep(random.randint(4,5))
    center_x,center_y=findElementByName(device,'CHO PHÉP')
    tap(device,center_x,center_y)
    sleep(random.randint(4,5))
    center_x,center_y=findElementByName(device,'CHO PHÉP')
    tap(device,center_x,center_y)
    sleep(random.randint(4,5))
    center_x,center_y=findElementById(device,'com.android.permissioncontroller:id/permission_allow_foreground_only_button')
    tap(device,center_x,center_y)
    sleep(random.randint(4,5))
    center_x,center_y= findElementById(device,'com.zing.zalo:id/button2')
    tap(device,center_x,center_y)
    sleep(random.randint(4,5))
    center_x,center_y= findElementById(device,'com.zing.zalo:id/btnConfirmPhonebookNoType2')
    if center_x>0 and center_y>0:
        tap(device,center_x,center_y)
        sleep(random.randint(4,5))
    

     


