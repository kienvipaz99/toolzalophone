import xml.etree.ElementTree as ET
import re
import os
import subprocess
import hashlib
from readingfile import check_xml_data
from lxml import etree
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
    filename = "captured_texts.txt"
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