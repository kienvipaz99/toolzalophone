import xml.etree.ElementTree as ET
import re
import os,time
import subprocess
import hashlib
from readingfile import check_xml_data
from tab import tap
from swip import swip
from  testadb import sleep
import random
from input import input_text
from datetime import datetime
from btnback import back
def dumpXml(serial: str):
    srdev = serial

    serial_hash = hashlib.md5(serial.encode('utf-8-sig')).hexdigest()
    serial_dir = os.path.join(os.getcwd(), serial_hash)
    
    if not os.path.exists(serial_dir):
        os.mkdir(serial_dir)
    xml_path = os.path.join(serial_dir, "ui.xml") 
    if not os.path.exists(xml_path):
        with open(xml_path, "w+"):
            pass
    subprocess.run(f'adb -s {srdev} shell "uiautomator dump /sdcard/uidump.xml"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    subprocess.run(f'adb -s {srdev} pull /sdcard/uidump.xml "{xml_path}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def get_element(serial, attrib, name):
    dumpXml(serial)
    elements_list = []
    pattern = re.compile(r"\d+")
    path=(f"{hashlib.md5(serial.encode('utf-8-sig')).hexdigest()}/ui.xml")
    try:
        xml_file_path = os.path.join(os.getcwd(), hashlib.md5(serial.encode('utf-8-sig')).hexdigest(), "ui.xml")
        if check_xml_data(path):
            tree = ET.ElementTree(file=xml_file_path)
            for elem in tree.iter(tag="node"):
                name = name.lower()
                if elem.attrib.get(attrib, '').lower() == name:
                    bounds = elem.attrib["bounds"]
                    coord = pattern.findall(bounds)
                    Xpoint = int((int(coord[2]) + int(coord[0])) / 2.0)
                    Ypoint = int((int(coord[3]) + int(coord[1])) / 2.0)
                    elements_list.append((Xpoint, Ypoint))

            if elements_list:
                x, y = elements_list[0]
                return x, y
            else:
                x, y = 0, 0
                return x, y
        else:
            x, y = 0, 0
            return x, y
                
    except ET.ParseError:
        x, y = 0, 0
        return x, y

def get_coordinates_capcha(serial, attrib, name):
    dumpXml(serial)
    pattern = re.compile(r"\d+")
    try:
        tree = ET.ElementTree(file=os.path.join(os.getcwd(), hashlib.md5(serial.encode('utf-8-sig')).hexdigest(), "ui.xml"))
        for elem in tree.iter(tag="node"):
            if elem.attrib.get(attrib)== name:
                bounds = elem.attrib["bounds"]
                coord = pattern.findall(bounds)
                return coord[0],coord[1],coord[2],coord[3]
            
    except ET.ParseError:
        
        print("Lỗi phân tích XML hoặc không tìm thấy tệp.")
        return None  
    except Exception as e:
        # Xử lý các ngoại lệ khác
        print(f"Lỗi: {e}")
        return None 



def get_coordinates_capcha(serial, attrib, name):
    dumpXml(serial)
    pattern = re.compile(r"\d+")
    try:
        tree = ET.ElementTree(file=os.path.join(os.getcwd(), hashlib.md5(serial.encode('utf-8-sig')).hexdigest(), "ui.xml"))
        for elem in tree.iter(tag="node"):
            if elem.attrib.get(attrib)== name:
                bounds = elem.attrib["bounds"]
                coord = pattern.findall(bounds)
                return coord[0],coord[1],coord[2],coord[3]
            
    except ET.ParseError:
        
        print("Lỗi phân tích XML hoặc không tìm thấy tệp.")
        return None  
    except Exception as e:
        # Xử lý các ngoại lệ khác
        print(f"Lỗi: {e}")
        return None 
def find_coordinates_friend(serial, id_value):
    dumpXml(serial)
    pattern = re.compile(r"\d+")
    filename = f"{serial}captured_texts.txt"
    filepath = os.path.join(os.getcwd(), filename)

   
    xml_path = os.path.join(os.getcwd(), hashlib.md5(serial.encode('utf-8-sig')).hexdigest(), "ui.xml")
    tree = ET.ElementTree(file=xml_path)

    if not os.path.exists(filepath):
        open(filepath, "a").close()

    existing_entries = []
    with open(filepath, "r") as file:
        existing_entries = file.read().splitlines()

    for elem in tree.iter(tag="node"):
        if elem.attrib.get('resource-id') == id_value:
                text_value = elem.attrib.get("text", "").strip()
                bounds = elem.attrib["bounds"]
                coord = pattern.findall(bounds)
                Xpoint = int((int(coord[2]) + int(coord[0])) / 2)
                Ypoint = int((int(coord[3]) + int(coord[1])) / 2)
                entry = f"{text_value}"
                
                if entry not in existing_entries:
                    with open(filepath, "a") as file:
                        file.write(entry + "\n")
                        return Xpoint, Ypoint

    return 0, 0  
def findElementById(device, id):
    center_x,center_y=get_element(device.serial,"resource-id",id)
    return center_x,center_y
def findElementByName(device, name):
     center_x,center_y=get_element(device.serial,'text',name)
     return center_x,center_y

def findElementByClass(device, className):
    center_x,center_y=get_element(device.serial,"class",className)
    return center_x,center_y
def post1(device, min_number, max_number, content,file_list):
        for file_path in file_list:
            current_timestamp = time.mktime(datetime.now().timetuple())
            os.utime(file_path, (current_timestamp, current_timestamp))
            file_name = os.path.basename(file_path)
            destination_path = f"/sdcard/DCIM/{file_name}"
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
def in_ra_text(serial, name):
    dumpXml(serial)
    xml_file_path = os.path.join(os.getcwd(), hashlib.md5(serial.encode('utf-8-sig')).hexdigest(), "ui.xml")
    tree = ET.parse(xml_file_path)
    for elem in tree.iter(tag="node"):
        text = elem.attrib.get("text")
        if text and name in text:
            # Tìm vị trí của dấu ngoặc đơn đầu tiên và thứ hai trong chuỗi
            start_index = text.find('(')
            end_index = text.find(')')
            if start_index != -1 and end_index != -1:  # Kiểm tra xem có dấu ngoặc đơn không
                content_inside_brackets = text[start_index + 1:end_index]
                return content_inside_brackets
                
def dumpxmlfindnumber(device):
    dumpXml(device.serial)
    pattern = re.compile(r"\d+")
    xml_path = os.path.join(os.getcwd(), hashlib.md5(device.serial.encode('utf-8-sig')).hexdigest(), "ui.xml")
    tree = ET.parse(xml_path)
    root = tree.getroot()
    members = root.findall(".//node[@class='android.widget.FrameLayout']")
    data_member=[]
    for member in members:
        text_value = member.attrib.get("text", "").strip()
        if text_value and "Trưởng nhóm" not in text_value and "Phó nhóm" not in text_value and "Bạn" not in text_value and "Thành viên" not in text_value and "Gợi ý thêm thành viên" not in text_value and "Duyệt thành viên" not in text_value and "Trưởng cộng đồng" not in text_value and "Phó cộng đồng" not in text_value:
            bounds = member.attrib["bounds"]
            coord = pattern.findall(bounds)
            Xpoint = int((int(coord[2]) + int(coord[0])) / 2)
            Ypoint = int((int(coord[3]) + int(coord[1])) / 2)
            new_text = text_value.split("\n", 1)[0]
            coordinates = [new_text, Xpoint, Ypoint]
            data_member.append(coordinates)
    return  data_member
def findmember(device,min_number,max_number,content,file_list,number_member,divided):
    filename = f"{device.serial}member.txt"
    filepath = os.path.join(os.getcwd(), filename)
    if not os.path.exists(filepath):
        open(filepath, "a").close()
    with open(filepath, "r") as file:
        existing_entries = file.read().splitlines()
    selected_item = None
    data_member = dumpxmlfindnumber(device)
    if len(data_member) == 0:
        back(device)
        back(device)
        back(device)
        return False
    i=0
    while int(number_member)-1 > i:
        for item in data_member:
            if ' '.join(map(str, item[0])) not in existing_entries:
                selected_item = item
                break
        if not selected_item:
            i += 1
            swip(device,514,897,535,533)
            data_member = dumpxmlfindnumber(device)
            for item in data_member:
                if ' '.join(map(str, item[0])) not in existing_entries:
                    selected_item = item
                    break
            continue
        else:
            break
    if selected_item:
        tap(device, selected_item[1], selected_item[2])
        with open(filepath, "a") as file:
            file.write(' '.join(map(str, selected_item[0])) + "\n")
        existing_entries.append(' '.join(map(str, selected_item[0])))
        sleep(random.randint(min_number, max_number))
        x,y=findElementById(device,'com.zing.zalo:id/item_view_profile')
        tap(device,x,y)
        sleep(random.randint(min_number, max_number))
        if int(divided)==1: 
            center_x, center_y = findElementById(device, 'com.zing.zalo:id/btn_send_friend_request')
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
        center_x, center_y = findElementByName(device, 'Nhắn tin')
        tap(device, center_x, center_y)
        sleep(random.randint(min_number, max_number))
        if(len(file_list)):
            center_x, center_y = findElementById(device, 'com.zing.zalo:id/new_chat_input_btn_show_gallery')
            tap(device, center_x, center_y)
            sleep(random.randint(min_number, max_number))
            post1(device, min_number, max_number, content,file_list)
            center_x,center_y=findElementById(device,'com.zing.zalo:id/media_picker_layout')
            tap(device,center_x,center_y)
            sleep(5)
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
        if content:
            center_x,center_y=findElementById(device,'com.zing.zalo:id/chatinput_text')
            tap(device, center_x, center_y)
            sleep(2)
            input_text(device, text=content)
            sleep(random.randint(min_number, max_number))
            center_x,center_y=findElementById(device,'com.zing.zalo:id/new_chat_input_btn_chat_send')
            tap(device, center_x, center_y)
            sleep(random.randint(min_number, max_number))
            back(device)
            
        back(device)

        
        return True

    else:
        for item in data_member:
            if ' '.join(map(str, item[0])) not in existing_entries:
                selected_item = item
                break
            if not selected_item:
                    back(device)
                    back(device)
                    back(device)
                    return False

            
            