from ppadb.client import Client as AdbClient
from openapp import openapp,start_link
from time import sleep
from find_image import find_image_coordinates
from input import input_text
from tab import tap
import os
import random
import subprocess
# from delete_cache import delete_cache
from gencapcha import slide_captcha
from find_text import get_coordinates_capcha,find_coordinates_friend,findmember,findElementById,findElementByName,in_ra_text
from btnback import back
from swip import swip
# from killapp import kill_and_restart_app
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


def add_friend_numberphone(device, mins, max, maxaction, data, type):
    center_x,center_y =findElementById(device,'com.zing.zalo:id/maintab_message')
    tap(device, center_x, center_y)
    sleep(random.randint(mins, max))
    if(type == 'Kết bạn theo sđt'):
        center_x, center_y = find_image_coordinates('assets/images/find_friend.png', device)
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
                
                center_x, center_y = findElementById(device, 'com.zing.zalo:id/chatinput_text')
                if(center_x>0 and center_y>0):
                    back(device)
                    sleep(random.randint(mins, max))
                    center_x, center_y = find_image_coordinates('assets/images/find_friend.png', device)
                    tap(device, center_x, center_y)
                    sleep(random.randint(mins, max))
                    continue
                    
                center_x, center_y = findElementById(device, 'com.zing.zalo:id/btn_send_friend_request')
                if center_x == 0 and center_y == 0:
                    back(device)
                    continue
                x, y = findElementByName(device, 'Hủy kết bạn')
                if x==0 and y==0:
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
                sleep(3)
                back(device)
        sleep(2)
        back(device)
        sleep(2)
    elif(type=='Kết bạn theo gợi ý'):
        while True:
            x, y = find_image_coordinates('assets/images/find_more.png', device)
            if x==0 and y==0:
               swip(device, 690, 1722, 536, 569)
            else:
                
                center_x, center_y = find_image_coordinates('assets/images/viewadd.png', device)
                if(center_x>0 and center_y>0):     
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
def swip_newfeed(device,min_number,max_number,number_action):
        sleep(random.randint(min_number,max_number))
        center_x, center_y = find_image_coordinates('assets/images/newfeed.png', device)
        tap(device, center_x, center_y)
        center_x, center_y = find_image_coordinates('assets/images/newfeed1.png', device)
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
            center_x, center_y = find_image_coordinates('assets/images/love.png', device)
            if center_x > 0 and center_y > 0:
                tap(device, center_x, center_y)
                actions_performed += 1 
                swip(device, 690, 1722, 536, 569)
                sleep(4)
            else:
                swip(device, 516, 1676, 536, 569)
def post1(device, min_number, max_number, content, file_list):
    for file_path in file_list:
            current_timestamp = time.mktime(datetime.now().timetuple())
            os.utime(file_path, (current_timestamp, current_timestamp))
            file_name = os.path.basename(file_path)
            destination_path = f'/sdcard/DCIM/{file_name}'
            # Đẩy file lên thiết bị
            subprocess.run(['adb', '-s', device.serial, 'push', file_path, destination_path], capture_output=True)
            # Kích hoạt trình quét media
            subprocess.run(['adb', '-s', device.serial, 'shell', 'am', 'broadcast', '-a', 'android.intent.action.MEDIA_SCANNER_SCAN_FILE', '-d', f'file://{destination_path}'], capture_output=True)
    center_x, center_y = findElementByName(device, 'CHO PHÉP TRUY CẬP')
    if center_x > 0 and center_y > 0:
        tap(device, center_x, center_y)
        sleep(random.randint(min_number, max_number))
        center_x, center_y = findElementByName(device, 'CHO PHÉP')
        tap(device, center_x, center_y)
    center_x, center_y = findElementById(device, 'com.zing.zalo:id/media_picker_layout')
    tap(device, center_x, center_y)
    sleep(5)

def post2(device, min_number, max_number,file_list):
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
            
        center_x, center_y = findElementById(device,'com.zing.zalo:id/new_chat_input_btn_show_gallery')
        tap(device, center_x, center_y)
        sleep(random.randint(min_number, max_number))
        center_x,center_y=findElementByName(device,'CHO PHÉP TRUY CẬP')
        if center_x >0 and center_y >0:
            tap(device,center_x,center_y)
            sleep(random.randint(min_number, max_number))
            center_x,center_y=findElementByName(device,'CHO PHÉP')
            tap(device,center_x,center_y)
        center_x,center_y=findElementById(device,'com.zing.zalo:id/media_picker_layout')
        tap(device,center_x,center_y)
        sleep(5)
        # Đăng bài
def post(device, min_number, max_number, content, files):
        if isinstance(files, str):
            file_list = files.split()
        else:
            file_list = files
        center_x, center_y = find_image_coordinates('assets/images/newfeed.png', device)
        tap(device, center_x, center_y)
        center_x, center_y = find_image_coordinates('assets/images/newfeed1.png', device)
        tap(device, center_x, center_y)
        sleep(random.randint(min_number, max_number))
        center_x,center_y=findElementById(device,'com.zing.zalo:id/action_bar_new_post_btn')
        tap(device, center_x, center_y)
        sleep(random.randint(min_number, max_number))
        if(len(file_list)>0):
            post1(device, min_number, max_number, content,file_list)
            action=0
            while action < len(file_list):
                center_x, center_y = find_image_coordinates('assets/images/select_image.png', device)
                if center_x==0 and center_y==0: 
                    tap(device,450, 450)
                    sleep(2)
                if center_x>0 and center_y>0:
                    tap(device,center_x, center_y)
                    swip(device, 985, 1064, 55, 1171)
                    sleep(2)
                    action+=1

            center_x, center_y = find_image_coordinates('assets/images/comfirm_image.png', device)
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
    center_x, center_y = find_image_coordinates('assets/images/danhba.png', device)
    tap(device,center_x, center_y)
    center_x, center_y = find_image_coordinates('assets/images/danhba1.png', device)
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
    center_x, center_y = find_image_coordinates('assets/images/danhba.png', device)
    tap(device,center_x, center_y)
    center_x, center_y = find_image_coordinates('assets/images/danhba1.png', device)
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
                    center_x, center_y = find_image_coordinates('assets/images/recall.png', device)
                    if center_x >0 and center_y>0:
                        tap(device,center_x, center_y)
                        sleep(2)
                        x, y = find_image_coordinates('assets/images/wanning.png', device)
                        
                        if x>0 and y>0:
                            break
                        sleep(random.randint(min_number, max_number))
                        action+=1
                    else:
                        swip(device, 557, 688, 573, 443)
                        if(center_x==0 and center_y==0):
                            break
            back(device)
       
    elif type == 'Thu hồi tất cả':
            while True:       
                    center_x, center_y = find_image_coordinates('assets/images/recall.png', device) 
                    if center_x >0 and center_y>0:
                        tap(device,center_x, center_y)
                        sleep(2)
                        x, y = find_image_coordinates('assets/images/wanning.png', device)
                        if x>0 and y>0:
                            break
                        sleep(random.randint(min_number, max_number))
                    else:
                        swip(device, 557, 688, 573, 443)
                        if(center_x==0 and center_y==0):
                            break
            back(device)
            # nhắn tin
def sent_messages(device,min_number,max_number,content,number_action,file,type,data_number,id,divided,group_link):
        if isinstance(file, str):
            file_list = file.split()
        else:
            file_list = file
        linkgroup = str(group_link).split()
        data_group = list(set(linkgroup))
        if(type=='Theo SĐT'):
            center_x,center_y =findElementById(device,'com.zing.zalo:id/maintab_message')
            tap(device, center_x, center_y)
            sleep(random.randint(min_number, max_number))
            center_x, center_y = find_image_coordinates('assets/images/find_friend.png', device)
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
                    if(divided==1):
                        center_x, center_y = findElementById(device, 'com.zing.zalo:id/btn_send_friend_request')
                        if center_x == 0 and center_y == 0:
                            break
                        x, y = findElementByName(device, 'Hủy kết bạn')
                        if x==0 and y==0:
                            
                            tap(device, center_x, center_y)
                            sleep(random.randint(min_number, max_number))
                            center_x, center_y = findElementById(device, 'com.zing.zalo:id/btnSendInvitation')
                            tap(device, center_x, center_y)
                            sleep(random.randint(min_number, max_number))
                            center_x, center_y = findElementByName(device, 'Đã hiểu')
                            if (center_x>0 and center_y>0):
                                tap(device, center_x, center_y)
                                sleep(random.randint(min_number, max_number))
                                i =0
                                while i<3:
                                    i+=1
                                    back(device)
                                    sleep(2)
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
                        center_x,center_y=findElementById(device,'com.zing.zalo:id/landing_page_layout_send')
                        tap(device, center_x, center_y)
                      
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
        elif type =='Nhóm':
            action=0
            for i in data_group:
                start_link(device,i)
                sleep(5)
                center_x, center_y = findElementByName(device,'Zalo')
                if center_x > 0 and center_y > 0:
                    tap(device,center_x,center_y)
                    sleep(2)
                center_x, center_y = findElementById(device,'android:id/button_always')
                if center_x > 0 and center_y > 0:
                    tap(device,center_x,center_y)
                    sleep(2)
                center_x, center_y = findElementByName(device,'Link tham gia nhóm bạn vừa truy cập không còn hiệu lực. Vui lòng liên hệ trưởng nhóm để biết thêm chi tiết.')
                if center_x >0 and center_y>0:
                    back(device)
                    sleep(random.randint(min_number, max_number))
                    continue
                
                    
                center_x, center_y = findElementById(device,'com.zing.zalo:id/btn_join_group')
                if (center_x >0 and center_y >0):
                    tap(device,center_x,center_y)
                    sleep(random.randint(min_number, max_number))
                    center_x, center_y = findElementByName(device,'Đã yêu cầu tham gia')
                    if center_x>0 and  center_y>0:
                        back(device)
                        continue
                    center_x, center_y = findElementById(device,'com.zing.zalo:id/et_content')
                    tap(device,center_x,center_y)
                    sleep(random.randint(min_number, max_number))
                    input_text(device,text='Oke')
                    sleep(random.randint(min_number, max_number))
                    center_x, center_y = findElementById(device,'com.zing.zalo:id/btn_send_request_join')
                    tap(device,center_x,center_y)
                    sleep(random.randint(min_number, max_number))
                    center_x, center_y = findElementByName(device,'Đã yêu cầu tham gia')
                    if center_x>0 and  center_y>0:
                        back(device)
                        continue
                    
                x,y=findElementByName(device,'Chỉ trưởng và phó nhóm được gửi tin nhắn vào nhóm. Tìm hiểu thêm ')
                if(x>0 and y>0):
                    back(device)
                    sleep(random.randint(min_number, max_number))
                else:
                    if len(file_list)>0:
                        post2(device, min_number, max_number,file_list)
                        for i in range(len(file_list)):
                            center_x, center_y = find_image_coordinates('assets/images/select_image.png', device)
                            if(center_x==0 and center_y==0):
                                tap(device,450, 450)
                                sleep(2)
                            if center_x>0 and center_y>0:
                                tap(device,center_x, center_y)
                                swip(device, 985, 1064, 55, 1171)
                                sleep(2)
                        center_x, center_y = find_image_coordinates('assets/images/sent_image.png', device)
                        tap(device,center_x, center_y)
                        sleep(random.randint(min_number, max_number))
  
                    if(content):
                        center_x, center_y = findElementById(device,'com.zing.zalo:id/chatinput_text')
                        tap(device,center_x, center_y)
                        sleep(random.randint(min_number, max_number))
                        input_text(device,text=content)
                        sleep(random.randint(min_number, max_number))
                        center_x, center_y = findElementById(device,'com.zing.zalo:id/new_chat_input_btn_chat_send')
                        tap(device,center_x, center_y)
                        sleep(random.randint(min_number, max_number))
                        back(device)
                        sleep(2)
                    action+=1
                    back(device)
                    sleep(2)
                   
                    if(action==int(number_action)):
                        break       
        elif type =='Bạn bè':
            center_x,center_y =find_image_coordinates('assets/images/danhba.png',device)
            tap(device, center_x, center_y)
            center_x, center_y = find_image_coordinates('assets/images/danhba1.png', device)
            tap(device, center_x, center_y)
            sleep(random.randint(min_number, max_number))
            center_x,center_y =find_image_coordinates('assets/images/friend.png',device)
            tap(device, center_x, center_y)
            sleep(random.randint(min_number, max_number))
            i=0
            while (i < number_action):
                center_x,center_y=find_coordinates_friend(device.serial,'com.zing.zalo:id/cel_contact_tab_contact_cell')
                if center_x >0 and center_y>0:
                    tap(device, center_x, center_y)
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
                            if center_x ==0 and center_y ==0:
                                tap(device,400, 400)
                                sleep(2)
                            if center_x>0 and center_y>0:
                                tap(device,center_x, center_y)
                                sleep(2)
                                swip(device, 985, 1064, 55, 1171)
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
                    i+=1
                    back(device)
                    sleep(3)
                    back(device)
                    swip(device,500,1543,500,1253)

                else:
                    break
            os.remove(f"{device.serial}captured_texts.txt")
        elif type =='Thành viên nhóm':
            ia=0
            for i in data_group:
                while True:
                    start_link(device,i)
                    sleep(3)
                    center_x, center_y = findElementByName(device,'Zalo')
                    if center_x > 0 and center_y > 0:
                        tap(device,center_x,center_y)
                        sleep(2)
                    center_x, center_y = findElementById(device,'android:id/button_always')
                    if center_x > 0 and center_y > 0:
                        tap(device,center_x,center_y)
                        sleep(2)
                    center_x, center_y = findElementByName(device,'Link tham gia nhóm bạn vừa truy cập không còn hiệu lực. Vui lòng liên hệ trưởng nhóm để biết thêm chi tiết.')
                    if center_x >0 and center_y>0:
                        back(device)
                        sleep(random.randint(min_number, max_number))
                        break
                    center_x, center_y = findElementById(device,'com.zing.zalo:id/btn_join_group')
                    if (center_x >0 and center_y >0):
                        tap(device,center_x,center_y)
                        sleep(random.randint(min_number, max_number))
                        center_x, center_y = findElementByName(device,'Đã yêu cầu tham gia')
                        if center_x>0 and  center_y>0:
                            back(device)
                            break
                        center_x, center_y = findElementById(device,'com.zing.zalo:id/et_content')
                        tap(device,center_x,center_y)
                        sleep(random.randint(min_number, max_number))
                        input_text(device,text='Oke')
                        sleep(random.randint(min_number, max_number))
                        center_x, center_y = findElementById(device,'com.zing.zalo:id/btn_send_request_join')
                        tap(device,center_x,center_y)
                        sleep(random.randint(min_number, max_number))
                        center_x, center_y = findElementByName(device,'Đã yêu cầu tham gia')
                        if center_x>0 and  center_y>0:
                            back(device)
                            break
                    center_x, center_y = find_image_coordinates('assets/images/menu.png', device)
                    tap(device, center_x, center_y)
                    sleep(random.randint(min_number, max_number))
                    while True:
                        swip(device,500,1543,500,1053)
                        center_x, center_y = find_image_coordinates('assets/images/viewmember.png', device)
                        if center_x>0 and center_y>0:
                            tap(device, center_x, center_y)
                            break
                    number_member=in_ra_text(device.serial,'Thành viên')
                    status=findmember(device,min_number,max_number,content,file_list,number_member,divided)
                    ia+=1
                    if(status==False):
                        break
                    if ia == int(number_action):
                        break
                if ia == int(number_action):
                    os.remove(f"{device.serial}member.txt")
                    break               
def comment_post(device,min_number,max_number,number_action,content,love):
    center_x, center_y = find_image_coordinates('assets/images/newfeed.png', device)
    tap(device, center_x, center_y)
    center_x, center_y = find_image_coordinates('assets/images/newfeed1.png', device)
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
            if love:
                timx, timy = find_image_coordinates('assets/images/love.png', device)
                tap(device, timx, timy)
            tap(device, center_x, center_y)
            tap(device, x, y)
            sleep(random.randint(min_number, max_number))
            center_x,center_y=findElementById(device,'com.zing.zalo:id/comment_input_bar')
            tap(device, center_x, center_y)
            input_text(device,text=content)
            sleep(random.randint(min_number, max_number))
            center_x,center_y=findElementById(device,'com.zing.zalo:id/cmtinput_send')
            tap(device, center_x, center_y)
            i+=1
            sleep(random.randint(min_number, max_number))
            back(device)
            sleep(2)
            swip(device, 690, 1722, 536, 410)
        else:
            swip(device, 516, 1676, 536, 410)
#Mời tham gia nhóm
def invite_join_group(device,min_number,max_number,number_action,type,group_link,data_number):
    linkgroup = str(group_link).split()
    data_group = list(set(linkgroup))
    for i in data_group:
        start_link(device,i)
        sleep(3)
        center_x, center_y = findElementByName(device,'Zalo')
        tap(device,center_x,center_y)
        sleep(2)
        center_x, center_y = findElementById(device,'android:id/button_always')
        tap(device,center_x,center_y)
        sleep(5)
        center_x, center_y = findElementByName(device,'Link tham gia nhóm bạn vừa truy cập không còn hiệu lực. Vui lòng liên hệ trưởng nhóm để biết thêm chi tiết.')
        if center_x >0 and center_y>0:
            back(device)
            sleep(random.randint(min_number, max_number))
            continue
        center_x, center_y = findElementById(device,'com.zing.zalo:id/btn_join_group')
        if (center_x >0 and center_y >0):
             tap(device,center_x,center_y)
             sleep(random.randint(min_number, max_number))
             center_x, center_y = findElementByName(device,'Đã yêu cầu tham gia')
             if center_x>0 and  center_y>0:
                 back(device)
                 continue
             center_x, center_y = findElementById(device,'com.zing.zalo:id/et_content')
             tap(device,center_x,center_y)
             sleep(random.randint(min_number, max_number))
             input_text(device,text='Oke')
             sleep(random.randint(min_number, max_number))
             center_x, center_y = findElementById(device,'com.zing.zalo:id/btn_send_request_join')
             tap(device,center_x,center_y)
             sleep(random.randint(min_number, max_number))
             center_x, center_y = findElementByName(device,'Đã yêu cầu tham gia')
             if center_x>0 and  center_y>0:
                 back(device)
                 continue
        center_x,center_y=findElementById(device,'com.zing.zalo:id/menu_drawer')
        tap(device, center_x, center_y)
        sleep(random.randint(min_number, max_number))
        center_x,center_y = find_image_coordinates('assets/images/add_member.png', device)
        tap(device,center_x,center_y)
        sleep(random.randint(min_number, max_number))
        if(type=='Danh sách bạn bè'):
            i=0
            while i<number_action:
                center_x,center_y = find_image_coordinates('assets/images/select.png', device)
                tap(device,center_x,center_y)
                i+=1
                sleep(random.randint(min_number, max_number))
                swip(device,514,897,535,533)
                x,y=findElementByName(device,'bạn')
                if (center_x==0 and center_y==0) and (x>0 and y >0):
                    break
            center_x,center_y=findElementById(device,'com.zing.zalo:id/btn_done_invite_to_group')
            tap(device, center_x, center_y)
            sleep(random.randint(min_number, max_number))
        elif type =='Danh sách sđt':
            data_phone = str(data_number).split()
            data_list = list(set(data_phone))
            num_iterations = min(len(data_list), int(number_action))
            for i in range(num_iterations):
                center_x,center_y=findElementById(device,'com.zing.zalo:id/search_input_text')
                tap(device, center_x, center_y)
                number = data_list[i]
                sleep(random.randint(min_number, max_number))
                input_text(device,text=number)
                sleep(random.randint(min_number, max_number))
                
                center_x,center_y=findElementByName(device,'Đã tham gia')
                if center_x >0 and center_y >0:
                    center_x,center_y = find_image_coordinates('assets/images/clear.png', device)
                    tap(device,center_x,center_y)
                    sleep(random.randint(min_number, max_number))
                    continue
                center_x,center_y=findElementByName(device,'Không tìm thấy kết quả phù hợp.')
                if center_x >0 and center_y >0:
                    center_x,center_y = find_image_coordinates('assets/images/clear.png', device)
                    tap(device,center_x,center_y)
                    sleep(random.randint(min_number, max_number))
                    continue
                
                center_x,center_y=findElementById(device,'com.zing.zalo:id/name')
                tap(device, center_x, center_y)
                sleep(random.randint(min_number, max_number))
            center_x,center_y=findElementById(device,'com.zing.zalo:id/btn_done_invite_to_group')
            tap(device, center_x, center_y)
            sleep(random.randint(min_number, max_number))
            if center_x ==0 and center_y ==0:
                back(device)
                sleep(1)
                back(device)
                sleep(1)
                back(device)
                sleep(1)
                
    back(device)
    sleep(random.randint(min_number, max_number))
         
def login(device,account_info):
    openapp(device)
    sleep(random.randint(20,30))
    center_x,center_y=findElementById(device,'com.zing.zalo:id/btnLogin')
    if(center_x>0 and center_y>0):
        # delete_cache(device,"com.zing.zalo")
        # sleep(random.randint(5,10))
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
        center_x,center_y=findElementById(device,'com.zing.zalo:id/btnLogin')
        tap(device,center_x,center_y)
        sleep(random.randint(15,20))
        while True:
            center_x,center_y=findElementByName(device,'Xác thực bằng Captcha')
            if center_x==0 and center_y==0:
                x,y=findElementById(device,'com.zing.zalo:id/btnLogin')
                if x==0 and y==0:
                    break
                else:
                    tap(device,x,y)
            else:
                center_x, center_y = findElementById(device,'track_btn')
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
    else:
        openapp(device)

     


