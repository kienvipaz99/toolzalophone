def check_xml_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        if content.strip(): 
            return True  
        else:
            return False