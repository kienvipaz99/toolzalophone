from customtkinter import *
from CTkTable import *
from PIL import Image 
from tkinter import ttk,simpledialog,filedialog
import tkinter as tk
import sqlite3
from tkinter import filedialog
from tkinter import messagebox
import tkinter.messagebox
import threading,time,subprocess
from time import sleep
from testadb import get_devices,login,add_friend_numberphone,swip_newfeed,post,check_key_board,agree_to_make_friends
def get_device_imei(device):
    result = device.shell("service call iphonesubinfo 1 s16 com.android.shell  | cut -d \"'\" -f2 | grep -Eo '[0-9]' | xargs | sed 's/ //g'")
    imei = result.strip()
    return imei
new_window = None
sent_message = None
window_comment = None
add_friend = None
new_feed= None
post_window=None
agree_window=None
unfriend_window=None
invite_group=None
font_text=("Adobe Kaiti Std R", 15)
conn_account = sqlite3.connect("database/account.db")
cursor_account = conn_account.cursor()

cursor_account.execute('''
                    CREATE TABLE IF NOT EXISTS accounts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        proxy TEXT
                    )
                ''')
conn = sqlite3.connect('database/timeline.db')
cursor = conn.cursor()
cursor.execute('''
            CREATE TABLE IF NOT EXISTS timeline (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
            ''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS action (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timeline_id INTEGER,
        name_action TEXT NOT NULL,
        time_min INTEGER,
        time_max INTEGER,
        quantity INTEGER,
        type TEXT,
        content TEXT,
        auto TEXT,
        file_path TEXT,
        datalist_phone TEXT,
        divided BOOLEAN,
        datalist_mess TEXT,
        
        FOREIGN KEY (timeline_id) REFERENCES timeline (id)
    )
''')

class DashboardScreen(CTk):
    def __init__(self, root):
        self.root = root
        self.create_dashboard_frame()
        self.button_clicked(0)
        self.thread = None
        self.paused = False
        self.pause_cond = threading.Condition(threading.Lock())
        self.stop_flag = False
        self.selected_value = StringVar()
    def perform_action(self,device,action_name,item):
        min_number=item[3]
        max_number=item[4]
        number_action=item[5]
        data_number=item[10]
        type=item[6]
        content=item[7]
        file=item[9]
        if action_name == 'Thêm bạn bè':
            add_friend_numberphone(device,min_number,max_number,number_action,data_number,type)
            print('Đã hoàn thành')
        elif action_name == 'nhắn tin':
            # Gọi hành động nhắn tin ở đây
            print('Thực hiện hành động: Nhắn tin')
        elif action_name == 'Lướt new feed':
            swip_newfeed(device,min_number,max_number,number_action,type)
        elif action_name=='Đăng bài':
            post(device,min_number,max_number,content,file)
        elif action_name=='Đồng ý kết bạn':
            agree_to_make_friends(device,min_number,max_number,number_action,type)
        else:
            print(f'Hành động không xác định: {action_name}')
    def process_device(self,device,account_info,data):
        # if not check_key_board(device.serial, "com.android.adbkeyboard"):
        #     subprocess.call(['adb', '-s', device.serial, 'install', 'screen/login/ADBKeyboard.apk'])
        #     sleep(10)
        # ime_command = f"adb -s {device.serial} shell ime set com.android.adbkeyboard/.AdbIME"
        # os.system(ime_command)
        # login(device,account_info)
        # time.sleep(3)
        for item in data:
            action_name = item[2]
            self.perform_action(device,action_name,item)
    def get_accounts_data1(self):
        conn_account = sqlite3.connect("database/account.db")
        cursor_account = conn_account.cursor()
        cursor_account.execute("SELECT * FROM accounts")
        accounts = cursor_account.fetchall()
        conn_account.close()
        return accounts
    def get_data_timeline(self):
        conn = sqlite3.connect("database/timeline.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM action WHERE timeline_id = ?", (self.selected_value.get(),))
        data = cursor.fetchall()
        conn.close()
        return data
    def main(self):
                devices = get_devices()
                if not devices:
                    messagebox.showwarning("Thông báo",'Không có thiết bị nào được phát hiện. Kiểm tra lại')
                    return
                accounts = self.get_accounts_data1()
                data=self.get_data_timeline()
                num_devices = len(devices)
                num_accounts = len(accounts)
                if num_devices == 0 or num_accounts == 0:
                    print("Không có thiết bị hoặc tài khoản để xử lý.")
                    return
                logins_per_device = max(1, num_accounts) // num_devices
                threads = []
                for index, device in enumerate(devices):
                    account_index = index * logins_per_device % num_accounts
                    account_info = accounts[account_index]
                    thread = threading.Thread(target=self.process_device, args=(device, account_info,data))
                    threads.append(thread)
                    thread.start()

                for thread in threads:
                    thread.join()

    def start_action(self):
        if self.thread is None or not self.thread.is_alive():
            self.stop_flag = False
            self.thread = threading.Thread(target=self.main)
            self.thread.start()
        else:
            print("Đã bắt đầu.")
    def create_dashboard_frame(self):
        self.frame_width = self.root.winfo_screenwidth()
        self.frame_height = self.root.winfo_screenheight()
        self.dashboard_frame = CTkFrame(master=self.root, width=self.frame_width, height=self.frame_height, fg_color="#f6f6f6")
        self.dashboard_frame.pack_propagate(0)
        self.dashboard_frame.pack(expand=True, anchor="center")
        sidebar_frame = CTkFrame(master=self.dashboard_frame, fg_color="#F1F4FA", width=self.frame_width*0.2, height=self.frame_height, corner_radius=0)
        sidebar_frame.pack_propagate(0)
        sidebar_frame.pack(fill="y", anchor="w", side="left")
        logoapp = Image.open('assets/iconapp/zalo.png')
        ctk_image = CTkImage(light_image=logoapp, size=(50, 50))
        title = CTkLabel(sidebar_frame, text_color='black', text='Phần mềm auto Zalo', font=("Adobe Kaiti Std R", 20), image=ctk_image, compound="left")
        title.pack(anchor='center', pady=20, padx=(0, 10))
        button_names = ['Tài khoản', 'Hành động', 'Thiết bị']
        icon_tab = ['assets/iconapp/account.png', 'assets/iconapp/message.png', 'assets/iconapp/phones.png']
        self.ctk_buttons = []
        for index, path in enumerate(icon_tab):
            logo_img_data = Image.open(path)
            ctk_image = CTkImage(light_image=logo_img_data, size=(30, 30))
            button_text = button_names[index]
            button = CTkButton(sidebar_frame, image=ctk_image, text=button_text, corner_radius=5, text_color='black', command=lambda i=index: self.button_clicked(i), font=("Adobe Kaiti Std R", 17), width=self.frame_width*0.19, height=50, anchor='center', fg_color='transparent', hover_color='#A9DFFD')
            button.pack(pady=10)
            self.ctk_buttons.append(button)
        self.main_view_frame = CTkScrollableFrame(master=self.dashboard_frame,fg_color='white',scrollbar_button_color='white',orientation="vertical",scrollbar_button_hover_color='white')
        self.main_view_frame.pack(anchor="nw",expand=True,fill='both')

    def reset_button_colors(self):
        for button in self.ctk_buttons:
            button.configure(fg_color='transparent', text_color='black')
            
    def close_all_toplevels(self):
        # Duyệt qua tất cả các cửa sổ và đóng chúng
        for window in self.dashboard_frame.winfo_children():
            if isinstance(window, CTkToplevel):
                window.destroy()
    def button_clicked(self, index):
        self.reset_button_colors() 
        button = self.ctk_buttons[index]
        button.configure(fg_color='#A9DFFD')
        self.close_all_toplevels()
        if index == 0:
            self.hien_thi_man_hinh("Tài khoản")
        elif index == 1:
            self.hien_thi_man_hinh("Hành động")
        elif index == 2:
            self.hien_thi_man_hinh("Thiết bị")

    def hien_thi_man_hinh(self, loai_man_hinh):
        for widget in self.main_view_frame.winfo_children():
            widget.destroy()
        if loai_man_hinh == "Tài khoản":
            fame1 = CTkFrame(self.main_view_frame,fg_color='white')
            fame1.pack(side='left', anchor='nw', padx=10,pady=20)  
            label = CTkLabel(fame1, text="Thêm tài khoản", font=("Arial", 20), fg_color="white", anchor='w')
            label.pack(padx=10)
            input_taikhoan = CTkEntry(fame1, placeholder_text='Tài khoản', corner_radius=10, font=("Adobe Kaiti Std R", 14), height=40, width=150)
            input_taikhoan.pack(pady=10, padx=10)
            input_mk = CTkEntry(fame1, placeholder_text='Mật khẩu', corner_radius=10, font=("Adobe Kaiti Std R", 14), height=40, width=150)
            input_mk.pack(pady=10, padx=10)
            info_frame = CTkFrame(self.main_view_frame,fg_color='white')
            info_frame.pack(side='left', anchor='nw', pady=20, padx=20)
            CTkLabel(info_frame, text='Thông tin tài khoản', font=("Adobe Kaiti Std R", 20)).pack(side='top')
            treeFrame = ttk.Frame(info_frame,borderwidth=1)
            treeFrame.pack(side='left', pady=10, padx=20)
            treeScroll = ttk.Scrollbar(treeFrame)
            treeScroll.pack(side="right", fill="y")
            cols = ("Stt", "Id","Tài khoản",  "Trạng thái","Proxy")
            treeview = ttk.Treeview(treeFrame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=14)
            treeview.column("Stt", width=50)
            treeview.column("Id", width=50)
            treeview.column("Tài khoản", width=150)
            treeview.column("Trạng thái", width=100)
            treeview.column("Proxy", width=100)
            treeview.heading("Stt", text="Stt")
            treeview.heading("Id", text="Id")
            treeview.heading("Tài khoản", text="Tài khoản")
            treeview.heading("Trạng thái", text="Trạng thái")
            treeview.heading("Proxy", text="Proxy")
            treeview.pack()

            def load_data():
                cursor_account.execute("SELECT * FROM accounts")
                data_account=cursor_account.fetchall()
                treeview.delete(*treeview.get_children())
                stt = 1
                for row in data_account:
                    id = row[0]
                    tai_khoan = row[1]
                    proxy = row[3] if row[3] else ''
                    treeview.insert("", "end", values=(stt, id, tai_khoan, proxy))
                    stt += 1
                context_menu = tk.Menu(treeview, tearoff=0)
                context_menu.add_command(label="Xóa")
                context_menu.config(font=("Arial", 20), type="menubar")
            def them_du_lieu():
                taikhoan=input_taikhoan.get()
                matkahu=input_mk.get()
                tai_khoan = taikhoan 
                mat_khau = matkahu  
                proxy = None  
                if tai_khoan and mat_khau:
                    stt = len(treeview.get_children()) + 1
                    treeview.insert("", "end", values=(stt, tai_khoan))
                    cursor_account.execute("INSERT INTO accounts (username, password, proxy) VALUES (?, ?, ?)", (tai_khoan, mat_khau, proxy))
                    conn_account.commit()
                load_data()
            def update_stt():
                for i, child in enumerate(treeview.get_children(), start=1):
                    values = treeview.item(child)['values']
                    values[0] = i
                    treeview.item(child, values=values)
            def delete_account():
                selected_items = treeview.selection()
                for selected_item in selected_items:
                    selected_row = treeview.item(selected_item)
                    account_id = selected_row['values'][1]
                    treeview.delete(selected_item)
                    cursor_account.execute("DELETE FROM accounts WHERE id=?", (account_id,))
                    conn_account.commit()
                    update_stt()
            def add_file_text():
                try:
                    filename = filedialog.askopenfilename(initialdir="/", title="Chọn file text",
                            filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
                    if filename:
                        with open(filename, 'r') as file:
                            lines = file.readlines()
                            for line in lines:
                                data = line.strip().split('|')
                                tai_khoan = data[0]
                                mat_khau = data[1]
                                proxy = data[2] if len(data) > 2 else ''
                                stt = len(treeview.get_children()) + 1
                                treeview.insert("", "end", values=(stt, tai_khoan, proxy))
                                cursor_account.execute("INSERT INTO accounts (username, password, proxy) VALUES (?, ?, ?)",
                                            (tai_khoan, mat_khau, proxy))
                        conn_account.commit()
                        
                    load_data()
                except Exception as e:
                    tkinter.messagebox.showerror("Lỗi", e)
            btn_them = CTkButton(fame1, corner_radius=10, fg_color='#A9DFFD', height=40, width=100, text='Thêm', font=("Adobe Kaiti Std R", 15), text_color='black',command=them_du_lieu,hover=False)
            btn_them.pack(anchor='c',pady=(20,0))
            btn_them_file = CTkButton(fame1, corner_radius=10, fg_color='#A9DFFD', height=40, width=100, text='Thêm từ file .txt', font=("Adobe Kaiti Std R", 15), text_color='black',command=add_file_text,hover=False)
            btn_them_file.pack(anchor='c',pady=(20,0))
            btn_xoa = CTkButton(fame1, corner_radius=10, fg_color='#ED1B2F', height=40, width=100, text='Xóa', font=("Adobe Kaiti Std R", 15), text_color='white',command=delete_account,hover=False)
            btn_xoa.pack(anchor='c',pady=(20,0))
            load_data()
        elif loai_man_hinh == "Hành động":
            def fetch_data():
                cursor.execute("SELECT * FROM timeline")
                rows = cursor.fetchall()
                return rows
            img_pen = Image.open('assets/iconapp/pen.png')
            img_pen = CTkImage(light_image=img_pen, size=(20, 20))
            img_bin = Image.open('assets/iconapp/bin.png')
            img_bin = CTkImage(light_image=img_bin, size=(20, 20))
            
            def load_data1():
                data = fetch_data()
                for row_index, row_data in enumerate(data, start=1):
                    radio_button = CTkRadioButton(table_frame, fg_color='#566169', text=row_data[1], command=lambda: calldata(), variable=self.selected_value, value=row_data[0], width=100)
                    radio_button.grid(row=row_index, column=0, sticky='w', padx=25)
                    CTkButton(table_frame, text='Sửa', command=lambda row=row_data: edit_timeline(row), width=150, image=img_pen).grid(row=row_index, column=1, sticky='w', pady=5, padx=10)
                    CTkButton(table_frame, image=img_bin, text='Xoá', command=lambda id=row_data[0]: delete_timeline(id), width=150).grid(row=row_index, column=2, sticky='w', pady=5, padx=10)
                    separator = ttk.Separator(table_frame, orient='horizontal')
                    separator.grid(row=row_index, column=0, columnspan=3, sticky='ew', pady=(0, 40))
            def show_add_timeline_modal():
                new_timeline_name = simpledialog.askstring("Tạo Timeline Mới", "Nhập tên của Timeline:")
                if new_timeline_name:
                    cursor.execute("INSERT INTO timeline (name) VALUES (?)", (new_timeline_name,))
                    conn.commit()
                    load_data1()
            def edit_timeline(row):
                new_name = simpledialog.askstring("Sửa Timeline", f"Sửa tên của Timeline ({row[1]}):", initialvalue=row[1])
                if new_name:
                    cursor.execute("UPDATE timeline SET name = ? WHERE id = ?", (new_name, row[0]))
                    conn.commit()
                    load_data1()
            def clear_table_frame(keep_header=True):
                start_index = 3 if keep_header else 0
                for widget in table_frame.winfo_children()[start_index:]:
                    widget.destroy()
            def delete_timeline(id):
                confirmation = messagebox.askyesno("Xóa Timeline", "Bạn có chắc chắn muốn xóa Timeline này?")
                if confirmation:
                    clear_table_frame2()
                    cursor.execute("DELETE FROM timeline WHERE id = ?", (id,))
                    conn.commit()
                    clear_table_frame()
                    load_data1()
            farme1 = CTkFrame(self.main_view_frame,fg_color='white')
            farme1.pack(side='left', padx=20, pady=10, anchor='nw')
            header_frame = CTkFrame(farme1, width=400, height=100, fg_color='#182240')
            header_frame.pack(pady=20, padx=30, side='top', fill='x') 
            timeline_label = CTkLabel(header_frame, text='Timeline', text_color='white')
            timeline_label.pack(side='left', padx=20, pady=10)
            btn_add_timeline = CTkButton(header_frame, text='+ Tạo timeline mới', text_color='white', command=show_add_timeline_modal)
            btn_add_timeline.pack(side='right', padx=20, pady=10)
            table_frame = CTkFrame(farme1)
            table_frame.pack(pady=10, padx=10, side='bottom')  
            columns = ['Tên', 'Sửa', 'Xóa']
            for i, column in enumerate(columns):
                label = CTkLabel(master=table_frame, text=column,width=150)
                label.grid(row=0, column=i, sticky='w',pady=10,padx=10)
            load_data1()
            def clear_table_frame2(keep_header=True):
                start_index = 4 if keep_header else 0
                for widget in my_frame.winfo_children()[start_index:]:
                    widget.destroy()
            def calldata():
                clear_table_frame2()
                cursor.execute("SELECT * FROM action WHERE timeline_id = ?", (self.selected_value.get(),))
                data= cursor.fetchall()   
                if(data):
                    
                    for row_index, row_data in enumerate(data, start=1):
                        stt = row_index
                        CTkLabel(my_frame,text=stt,width=150).grid(row=row_index, column=0,sticky="nsew",padx=5,pady=5)
                        CTkLabel(my_frame,text=row_data[2],width=150).grid(row=row_index, column=1,sticky="nsew",padx=5,pady=5)
                        CTkButton(my_frame,text='Sửa', command=lambda row=row_data: edit_timeline(row),width=130,image=img_pen).grid(row=row_index, column=2, sticky="nsew",pady=5,padx=5)
                        CTkButton(my_frame ,image=img_bin,text='Xoá',width=130, command=lambda id=row_data[0]: delete_action(id)).grid(row=row_index, column=3, sticky="nsew",pady=5,padx=5)
                        separator = ttk.Separator(my_frame, orient='horizontal')
                        separator.grid(row=row_index, column=0, columnspan=len(table_action), sticky='ew', pady=(0, 40))
                        if hasattr(my_frame, "no_action_label"):
                            my_frame.no_action_label.destroy()
                        start_button = CTkButton(farme2, text='Bắt đầu', height=40, command=self.start_action)
                        start_button.pack(side='bottom', anchor='w', padx=10)
                        if hasattr(farme2, "start_button"):
                            farme2.start_button.destroy()
                        farme2.start_button = start_button 
                else:
                        no_action_label = CTkLabel(farme2, text='Không tìm thấy hành động.')
                        no_action_label.pack(side='top', padx=20, pady=10, anchor='n')
                        if hasattr(my_frame, "no_action_label"):
                            my_frame.no_action_label.destroy()
                        my_frame.no_action_label = no_action_label 
                        if hasattr(farme2, "start_button"):
                            farme2.start_button.destroy()
            def delete_action(id):
                confirmation = messagebox.askyesno("Xóa Timeline", "Bạn có chắc chắn muốn xóa hành động này?")
                if confirmation:
                    cursor.execute("DELETE FROM action WHERE id = ?", (id,))
                    conn.commit()
                    calldata()
            farme2 = CTkFrame(self.main_view_frame,fg_color='white')
            farme2.pack(side='right', padx=20, pady=10,anchor='ne')
            header2=CTkFrame(farme2,height=100,fg_color='#182240',)
            header2.pack(pady=20, padx=30,side='top', fill='x')
            title2=CTkLabel(header2, text='Chi tiết hành động',text_color='white')
            title2.pack(side='left',padx=20,pady=10)
            btn_add_action=CTkButton(header2, text='+ Thêm hành động',text_color='white',command=lambda: open_add_action_window())
            btn_add_action.pack(side='right',padx=20,pady=10,fill="y")
            my_frame = CTkFrame(farme2)
            my_frame.pack(pady=10, padx=10,fill='x')
            table_action = ['ID', 'Tên hành động','Sửa','Xoá']
            for i, column in enumerate(table_action):
                label = CTkLabel(my_frame, text=column,width=150)
                label.grid(row=0, column=i, sticky='w', pady=5,padx=5)
            calldata()
            def open_window_comment():
                    global window_comment
                    def toggle_window():
                        if window_comment.state() == "normal":
                            window_comment.withdraw()
                        else:
                            window_comment.deiconify()
                    if window_comment is not None:
                        toggle_window()
                        return
                    def on_close():
                        global window_comment
                        window_comment.destroy()
                        window_comment = None
                    window_width = 500
                    window_comment = CTkToplevel(self.main_view_frame)
                    window_comment.title("Bình luận bài viết")
                    window_comment.resizable(False,False)
                    window_comment.deiconify()
                    container_frame_max_min = CTkFrame(window_comment, fg_color='transparent')
                    container_frame_max_min.pack(fill='x', padx=10, pady=5, anchor='ne', side='top') 
                    input_frame_min = CTkFrame(container_frame_max_min, fg_color='transparent')   
                    input_frame_min.pack(fill='x', side='left')  
                    text_2 = CTkLabel(input_frame_min, text='Delay min', text_color='black', font=font_text)
                    text_2.pack(side='top', anchor='w')
                    input_min = CTkEntry(input_frame_min, placeholder_text='Nhập gian thời Delay min', text_color='black', font=font_text, width=window_width/2.3, height=40,border_color='black',border_width=1)
                    input_min.pack(side='top')
                    input_frame_max = CTkFrame(container_frame_max_min, fg_color='transparent')
                    input_frame_max.pack(fill='x', padx=10, pady=5, anchor='nw', side='right') 
                    text_1 = CTkLabel(input_frame_max, text='Delay max', text_color='black', font=font_text)
                    text_1.pack(side='top', anchor='w')
                    input_max = CTkEntry(input_frame_max, placeholder_text='Nhập thời gian Delay max', text_color='black', font=font_text, width=window_width/2.3, height=40,border_color='black',border_width=1)
                    input_max.pack(side='top', anchor='w')
                    frame = CTkFrame(window_comment, fg_color='transparent')
                    frame.pack(fill='x', padx=10, pady=5, anchor='ne', side='top')
                    text_3 = CTkLabel(frame, text='Số lượng tin nhắn gửi đi', text_color='black', font=font_text)
                    text_3.pack(side='top', anchor='w')
                    input_max_message = CTkEntry(frame, placeholder_text='Nhập số lượng tin nhắn gửi đi', text_color='black', font=font_text, width=window_width*0.9, height=40)
                    input_max_message.pack(fill='x', side='top')
                    text_4 = CTkLabel(frame, text='Nội dung(ngăn cách các loại tin bằng khoảng cách 3 dòng)', text_color='black', font=font_text)
                    text_4.pack(side='top', anchor='w')
                    input_content =CTkTextbox(frame , text_color='black', width=window_width, height=100,border_color='black',border_width=1)
                    input_content.pack(side='top', anchor='w')
                    CTkScrollbar(frame,command=input_content.yview)
                    input_content.pack(side='top', anchor='w')
                    def save_comment():
                        try:
                                id=self.selected_value.get()    
                                delaymin=input_min.get()
                                delaymax=input_max.get()
                                quantity=input_max_message.get()
                                data_list = input_content.get("1.0", "end-1c")
                                cursor.execute('''
                                INSERT INTO action (timeline_id, name_action, time_min, time_max, quantity, content)
                                VALUES (?, 'Bình luận bài viết', ?, ?, ?, ?)
                                ''', (id, delaymin, delaymax, quantity, data_list))
                                conn.commit()
                                calldata()
                                on_close()
                        except Exception as e:
                                print("Lỗi khi thêm dữ liệu bạn bè:", e)
                    CTkButton(frame,fg_color='orange',width=100,text='Lưu',font=font_text,text_color='white',height=45,corner_radius=5, command=save_comment).pack(side='top',anchor='n',pady=(20,20))
                    window_comment.protocol("WM_DELETE_WINDOW", on_close)
            def add_friend_window():
                        global add_friend
                        def toggle_window():
                            if add_friend.state() == "normal":
                                add_friend.withdraw()
                            else:
                                add_friend.deiconify()
                        if add_friend is not None:
                            toggle_window()
                            return
                        def on_close():
                            global add_friend
                            add_friend.destroy()
                            add_friend = None

                        window_width = 500
                        add_friend = CTkToplevel(self.main_view_frame)
                        add_friend.title("Gửi kết bạn")
                        add_friend.resizable(False,False)
                        add_friend.deiconify()
                        container_frame_max_min = CTkFrame(add_friend, fg_color='transparent')
                        container_frame_max_min.pack(fill='x', padx=10, pady=5, anchor='ne', side='top') 
                        input_frame_max = CTkFrame(container_frame_max_min, fg_color='transparent')   
                        input_frame_max.pack(fill='x', side='left')  
                        text_2 = CTkLabel(input_frame_max, text='Delay min', text_color='black', font=font_text)
                        text_2.pack(side='top', anchor='w')
                        input_min = CTkEntry(input_frame_max, placeholder_text='Nhập gian thời Delay min', text_color='black', font=font_text, width=window_width/2.3, height=40,border_color='black',border_width=1)
                        input_min.pack(side='top')
                        input_frame = CTkFrame(container_frame_max_min, fg_color='transparent')
                        input_frame.pack(fill='x', padx=10, pady=5, anchor='nw', side='right') 
                        text_1 = CTkLabel(input_frame, text='Delay max', text_color='black', font=font_text)
                        text_1.pack(side='top', anchor='w')
                        input_max = CTkEntry(input_frame, placeholder_text='Nhập thời gian Delay max', text_color='black', font=font_text, width=window_width/2.3, height=40,border_color='black',border_width=1)
                        input_max.pack(side='top', anchor='w')
                        frame = CTkFrame(add_friend, fg_color='transparent')
                        frame.pack(fill='x', padx=10, pady=5, anchor='ne', side='top')
                        text_3 = CTkLabel(frame, text='Kết bạn tối đa', text_color='black', font=font_text)
                        text_3.pack(side='top', anchor='w')
                        input_max_friend = CTkEntry(frame, placeholder_text='Nhập số lượng kết bạn', text_color='black', font=font_text, width=window_width*0.9, height=40)
                        input_max_friend.pack(fill='x', side='top')
                        CTkLabel(frame, text='Kết bạn từ', text_color='black', font=font_text).pack(side='top', anchor='w')
                        item_auto=['Kết bạn theo sđt','Kết bạn theo gợi ý','Kết bạn trong nhóm(trừ trưởng ,phó nhóm)']
                        selected_item_auto = StringVar(value='Kết bạn theo sđt')
                        frame_checkbox=CTkFrame(frame)
                        frame_checkbox.pack(side='top', anchor='w',pady=5)
                        for item in item_auto:
                            tk.Radiobutton(frame_checkbox,text=item,indicatoron=10,font=("Adobe Kaiti Std R", 12),value=item,
                                           variable=selected_item_auto,command=lambda:check()).pack(side='left', anchor='w')
                        label_input_phone=CTkLabel(frame,text_color='black',font=font_text,text='Danh sách số điện thoại (mỗi số 1 dòng)')
                        input_phone =CTkTextbox(frame , text_color='black', width=window_width, height=100,border_color='black',border_width=1)
                        check_number=CTkCheckBox(frame,text='Chia đều sđt cho thiết bị',font=font_text,text_color='black')
                        def check():
                            if(selected_item_auto.get()=='Kết bạn theo sđt'):
                                label_input_phone.pack(side='top',anchor='w',pady=5)
                                input_phone.pack(side='top', anchor='w',pady=5)
                                check_number.pack(side='top', anchor='w',pady=5)
                            else:
                                input_phone.pack_forget()
                                label_input_phone.pack_forget()
                                check_number.pack_forget()
                        check()
                        def add_data():
                            try:
                                id=self.selected_value.get()    
                                delaymin=input_min.get()
                                delaymax=input_max.get()
                                numbermax=input_max_friend.get()
                                type=selected_item_auto.get()
                                data_list = input_phone.get("1.0", "end-1c")
                                
                                cursor.execute('''
                                INSERT INTO action (timeline_id, name_action, time_min, time_max, quantity, type, datalist_phone, divided)
                                VALUES (?, 'Thêm bạn bè', ?, ?, ?, ?, ?, ?)
                                ''', (id, delaymin, delaymax, numbermax,type, data_list, True))
                                conn.commit()
                                calldata()
                                on_close()
                            except Exception as e:
                                print("Lỗi khi thêm dữ liệu bạn bè:", e)
                            
                        CTkScrollbar(frame,command=input_phone.yview)
                        CTkButton(frame,fg_color='orange',width=100,text='Lưu',font=font_text,text_color='white',height=45,corner_radius=5,command=add_data).pack(side='bottom',anchor='n',pady=(20,0))
                        add_friend.protocol("WM_DELETE_WINDOW", on_close)
            def sent_message_window():
                        global sent_message
                        def toggle_window():
                            if sent_message.state() == "normal":
                                sent_message.withdraw()
                            else:
                                 sent_message.deiconify()
                        if sent_message is not None:
                            toggle_window()
                            return
                        def on_close():
                            global sent_message
                            sent_message.destroy()
                            sent_message = None

                        window_width = 500
                        sent_message = CTkToplevel(self.main_view_frame)
                        sent_message.title("Nhắn tin")
                        sent_message.resizable(False,False)
                        sent_message.deiconify()
                        container_frame_max_min = CTkFrame(sent_message, fg_color='transparent')
                        container_frame_max_min.pack(fill='x', padx=10, pady=5, anchor='ne', side='top') 
                        input_frame_max = CTkFrame(container_frame_max_min, fg_color='transparent')   
                        input_frame_max.pack(fill='x', side='left')  
                        text_2 = CTkLabel(input_frame_max, text='Delay min', text_color='black', font=font_text)
                        text_2.pack(side='top', anchor='w')
                        input_min = CTkEntry(input_frame_max, placeholder_text='Nhập gian thời Delay min', text_color='black', font=font_text, width=window_width/2.3, height=40,border_color='black',border_width=1)
                        input_min.pack(side='top')
                        input_frame = CTkFrame(container_frame_max_min, fg_color='transparent')
                        input_frame.pack(fill='x', padx=10, pady=5, anchor='nw', side='right') 
                        text_1 = CTkLabel(input_frame, text='Delay max', text_color='black', font=font_text)
                        text_1.pack(side='top', anchor='w')
                        input_max = CTkEntry(input_frame, placeholder_text='Nhập thời gian Delay max', text_color='black', font=font_text, width=window_width/2.3, height=40,border_color='black',border_width=1)
                        input_max.pack(side='top', anchor='w')
                        frame = CTkFrame(sent_message, fg_color='transparent')
                        frame.pack(fill='x', padx=10, pady=5, anchor='ne', side='top')
                        text_3 = CTkLabel(frame, text='Số lượng tin nhắn gửi đi', text_color='black', font=font_text)
                        text_3.pack(side='top', anchor='w')
                        input_max_message = CTkEntry(frame, placeholder_text='Nhập số lượng tin nhắn gửi đi', text_color='black', font=font_text, width=window_width*0.9, height=40)
                        input_max_message.pack(fill='x', side='top')
                        text_4 = CTkLabel(frame, text='Nội dung', text_color='black', font=font_text)
                        text_4.pack(side='top', anchor='w')
                        input_content =CTkTextbox(frame , text_color='black', width=window_width, height=100,border_color='black',border_width=1)
                        input_content.pack(side='top', anchor='w')
                        CTkScrollbar(frame,command=input_content.yview)
                        input_content.pack(side='top', anchor='w')
                        text_5 = CTkLabel(frame, text='Tự động', text_color='black', font=font_text)
                        text_5.pack(side='top', anchor='w')
                        selected_item_auto =tk.StringVar(value='Nhắn tin theo số điện thoại')
                        item_auto=['Nhắn tin theo số điện thoại','Nhắn tin theo nhóm','Nhắn tin theo danh bạ']
                        frame_checkbox=CTkFrame(frame)
                        frame_checkbox.pack(side='top', anchor='w',pady=5)
                        input_phone =CTkTextbox(frame , text_color='black', width=window_width, height=100,border_color='black',border_width=1)
                        CTkScrollbar(frame,command=input_phone.yview)
                        def toggle_input_max():
                            if selected_item_auto.get() == 'Nhắn tin theo số điện thoại':
                                    input_phone.pack(side='top', anchor='w',pady=5)
                            else:
                                input_phone.pack_forget()
                        for item in item_auto:
                            tk.Radiobutton(frame_checkbox,text=item,indicatoron=10,font=("Adobe Kaiti Std R", 12),value=item,variable=selected_item_auto,command=toggle_input_max).pack(side='left', anchor='w')  
                        toggle_input_max()
                        def save_sent_message():
                            try:
                                id=self.selected_value.get()    
                                delaymin=input_min.get()
                                delaymax=input_max.get()
                                quantity=input_max_message.get()
                                content=input_content.get("1.0", "end-1c")
                                auto=selected_item_auto.get()
                                datalist_mess=input_phone.get("1.0", "end-1c")
                                
                                cursor.execute('''
                                    INSERT INTO action (timeline_id, name_action, time_min, time_max, quantity, content, auto, datalist_mess)
                                    VALUES (?, 'Nhắn tin', ?, ?, ?, ?, ?, ?)
                                ''', (id, delaymin, delaymax, quantity, content, auto, datalist_mess))
                                conn.commit()
                                calldata()
                            except Exception as e:
                                print("Đã xảy ra lỗi:", e)
                            on_close()
                                
                        CTkButton(frame,fg_color='orange',width=100,text='Lưu',font=font_text,text_color='white',height=45,corner_radius=5, command=save_sent_message).pack(side='bottom',anchor='n',pady=(20,0))
                        sent_message.protocol("WM_DELETE_WINDOW", on_close)
            def upload_post_window():
                        global post_window
                        def toggle_window():
                            if post_window.state() == "normal":
                            
                                post_window.withdraw()
                            else:
                                 post_window.deiconify()
                        if post_window is not None:
                            toggle_window()
                            return
                        def on_close():
                            global post_window
                            post_window.destroy()
                            post_window = None

                        window_width = 500
                        post_window = CTkToplevel(self.main_view_frame)
                        post_window.title("Đăng bài")
                        post_window.resizable(False, False)
                        post_window.deiconify()

                        scroll = CTkScrollableFrame(post_window, fg_color='transparent',height=410,width=500,scrollbar_button_color='#ebebeb',scrollbar_button_hover_color='#ebebeb')
                        scroll.pack(fill='both')

                        container_frame_max_min = CTkFrame(scroll, fg_color='transparent')
                        container_frame_max_min.pack(fill='x', padx=10, pady=5, anchor='ne', side='top')

                        input_frame_max = CTkFrame(container_frame_max_min, fg_color='transparent')
                        input_frame_max.pack(fill='x', side='left')

                        text_2 = CTkLabel(input_frame_max, text='Delay min', text_color='black', font=font_text)
                        text_2.pack(side='top', anchor='w')

                        input_min = CTkEntry(input_frame_max, placeholder_text='Nhập gian thời Delay min', text_color='black', font=font_text, width=window_width/2.3, height=40, border_color='black', border_width=1)
                        input_min.pack(side='top')

                        input_frame = CTkFrame(container_frame_max_min, fg_color='transparent')
                        input_frame.pack(fill='x', padx=10, pady=5, anchor='nw', side='right')

                        text_1 = CTkLabel(input_frame, text='Delay max', text_color='black', font=font_text)
                        text_1.pack(side='top', anchor='w')

                        input_max = CTkEntry(input_frame, placeholder_text='Nhập thời gian Delay max', text_color='black', font=font_text, width=window_width/2.3, height=40, border_color='black', border_width=1)
                        input_max.pack(side='top', anchor='w')
                        frame = CTkFrame(scroll, fg_color='transparent')
                        frame.pack(fill='x', padx=10, pady=5, anchor='ne', side='top')
                        text_4 = CTkLabel(frame, text='Nội dung bài viết', text_color='black', font=font_text)
                        text_4.pack(side='top', anchor='w')
                        input_content = CTkTextbox(frame, text_color='black', width=window_width, height=100, border_color='black', border_width=1)
                        input_content.pack(side='top', anchor='w')
                        CTkLabel(frame, text='File đính kèm', text_color='black', font=font_text).pack(side='top', anchor='w')
                        label_file_path = CTkLabel(frame, text="", justify="left")
                        label_file_path.pack(side='top', anchor='w')
                        CTkButton(frame, text='Tải lên file đính kèm', command=lambda: open_file_dialog(label_file_path), text_color='white', font=font_text).pack(side='top', anchor='w', pady=(10, 0))
                        def save_post_window():
                            try:
                                id=self.selected_value.get()    
                                delaymin=input_min.get()
                                delaymax=input_max.get()
                                content=input_content.get("1.0", "end-1c")
                                file_path = label_file_path.cget("text")
                                cursor.execute('''
                                    INSERT INTO action (timeline_id, name_action, time_min, time_max, content,file_path)
                                    VALUES (?, 'Đăng bài', ?, ?, ?, ?)
                                ''', (id, delaymin, delaymax, content,file_path))
                                conn.commit()
                                calldata()
                            except Exception as e:
                                print("Đã xảy ra lỗi:", e)
                            on_close()
                        CTkButton(frame, fg_color='orange', width=100, text='Lưu', font=font_text, text_color='white', height=45, corner_radius=5, command= save_post_window).pack(side='top', anchor='n', pady=(10, 0))

                        def open_file_dialog(label):
                            file_paths = filedialog.askopenfilenames(title="Chọn tệp", filetypes=[("Ảnh", ("*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp"))])
    
                            valid_image_paths = []
                            for file_path in file_paths:
                                try:
                                    # Kiểm tra xem tệp có thể mở được bằng thư viện PIL không (ảnh hợp lệ)
                                    Image.open(file_path)
                                    valid_image_paths.append(file_path)
                                except (IOError, Image.DecompressionBombError):
                                    pass

                            if valid_image_paths:
                                label.configure(text="\n".join(valid_image_paths))
                            else:
                                # Thông báo hoặc xử lý khi không có ảnh nào hợp lệ được chọn
                                pass

                        post_window.protocol("WM_DELETE_WINDOW", on_close)

            def new_feed_window():
                        global new_feed
                        def toggle_window():
                            if new_feed.state() == "normal":
                                new_feed.withdraw()
                            else:
                                 new_feed.deiconify()
                        if new_feed is not None:
                            toggle_window()
                            return
                        def on_close():
                            global new_feed
                            new_feed.destroy()
                            new_feed = None

                        window_width = 500
                        window_height = 340
                        new_feed = CTkToplevel(self.main_view_frame)
                        new_feed.title("Lướt new feed")
                        new_feed.resizable(False,False)
                        new_feed.deiconify()
                        position_x = int((self.frame_width - window_width) / 2)
                        position_y = int((self.frame_height - window_height) / 2)
                        new_feed.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
                        container_frame_max_min = CTkFrame(new_feed, fg_color='transparent')
                        container_frame_max_min.pack(fill='x', padx=10, pady=5, anchor='ne', side='top') 
                        input_frame_max = CTkFrame(container_frame_max_min, fg_color='transparent')   
                        input_frame_max.pack(fill='x', side='left')  
                        text_2 = CTkLabel(input_frame_max, text='Delay min', text_color='black', font=font_text)
                        text_2.pack(side='top', anchor='w')
                        input_min = CTkEntry(input_frame_max, placeholder_text='Nhập gian thời Delay min', text_color='black', font=font_text, width=window_width/2.3, height=40,border_color='black',border_width=1)
                        input_min.pack(side='top')
                        input_frame = CTkFrame(container_frame_max_min, fg_color='transparent')
                        input_frame.pack(fill='x', padx=10, pady=5, anchor='nw', side='right') 
                        text_1 = CTkLabel(input_frame, text='Delay max', text_color='black', font=font_text)
                        text_1.pack(side='top', anchor='w')
                        input_max = CTkEntry(input_frame, placeholder_text='Nhập thời gian Delay max', text_color='black', font=font_text, width=window_width/2.3, height=40,border_color='black',border_width=1)
                        input_max.pack(side='top', anchor='w')
                        frame = CTkFrame(new_feed, fg_color='transparent')
                        frame.pack(fill='x', padx=10, pady=5, anchor='ne', side='top')
                        text_3 = CTkLabel(frame, text='Số lượng bài viết tương tác', text_color='black', font=font_text)
                        text_3.pack(side='top', anchor='w')
                        input_max_message = CTkEntry(frame, placeholder_text='Nhập số lượng bài viết tương tác', text_color='black', font=font_text, width=window_width*0.9, height=40)
                        input_max_message.pack(fill='x', side='top')
                        text_4 = CTkLabel(frame, text='Loại', text_color='black', font=font_text)
                        text_4.pack(side='top', anchor='w')
                        
                        type=['Tim lần lượt','Tim random']
                        selected_item_auto = StringVar(value='Tim lần lượt')
                        frame_checkbox=CTkFrame(frame)
                        frame_checkbox.pack(side='top', anchor='w',pady=5)
                        for item in type:
                            tk.Radiobutton(frame_checkbox,text=item,indicatoron=10,font=("Adobe Kaiti Std R", 14),value=item,variable=selected_item_auto).pack(side='left', anchor='w')
                        def save_new_feed():
                            try:
                                id=self.selected_value.get()    
                                delaymin=input_min.get()
                                delaymax=input_max.get()
                                quantity=input_max_message.get()
                                auto=selected_item_auto.get()
                                cursor.execute('''
                                    INSERT INTO action (timeline_id, name_action, time_min, time_max, quantity,type)
                                    VALUES (?, 'Lướt new feed', ?, ?, ?, ?)
                                ''', (id, delaymin, delaymax, quantity,auto))
                                conn.commit()
                                calldata()
                            except Exception as e:
                                print("Đã xảy ra lỗi:", e)
                            on_close()

                        CTkButton(frame,fg_color='orange',width=100,text='Lưu',font=font_text,text_color='white',height=45,corner_radius=5, command=save_new_feed).pack(side='top', anchor='n',pady=(20,0))
                        new_feed.protocol("WM_DELETE_WINDOW", on_close)
            def agree_add_friend():
                        global agree_window
                        def toggle_window():
                            if agree_window.state() == "normal":
                                agree_window.withdraw()
                            else:
                                 agree_window.deiconify()
                        if agree_window is not None:
                            toggle_window()
                            return
                        def on_close():
                            global agree_window
                            agree_window.destroy()
                            agree_window = None
                        
                        window_width = 500
                       
                        agree_window = CTkToplevel(self.main_view_frame)
                        agree_window.title("Đồng ý kết bạn")
                        agree_window.resizable(False,False)
                        agree_window.deiconify()
                   
                
                        container_frame_max_min = CTkFrame(agree_window, fg_color='transparent')
                        container_frame_max_min.pack(fill='x', padx=10, pady=5, anchor='ne', side='top') 
                        input_frame_max = CTkFrame(container_frame_max_min, fg_color='transparent')   
                        input_frame_max.pack(fill='x', side='left')  
                        text_2 = CTkLabel(input_frame_max, text='Delay min', text_color='black', font=font_text)
                        text_2.pack(side='top', anchor='w')
                        input_min = CTkEntry(input_frame_max, placeholder_text='Nhập gian thời Delay min', text_color='black', font=font_text, width=window_width/2.3, height=40,border_color='black',border_width=1)
                        input_min.pack(side='top')
                        input_frame = CTkFrame(container_frame_max_min, fg_color='transparent')
                        input_frame.pack(fill='x', padx=10, pady=5, anchor='nw', side='right') 
                        text_1 = CTkLabel(input_frame, text='Delay max', text_color='black', font=font_text)
                        text_1.pack(side='top', anchor='w')
                        input_max = CTkEntry(input_frame, placeholder_text='Nhập thời gian Delay max', text_color='black', font=font_text, width=window_width/2.3, height=40,border_color='black',border_width=1)
                        input_max.pack(side='top', anchor='w')
                        frame = CTkFrame(agree_window, fg_color='transparent')
                        frame.pack(fill='x', padx=10, pady=5, anchor='ne', side='top')
                        text_5 = CTkLabel(frame, text='Tự động', text_color='black', font=font_text)
                        text_5.pack(side='top', anchor='w')
                        item_auto=['Đồng ý tất cả','Đồng ý theo số lượng']
                        selected_item_auto = StringVar(value='Đồng ý tất cả')
                        frame_checkbox=CTkFrame(frame)
                        frame_checkbox.pack(side='top', anchor='w',pady=5)
                        
                        def toggle_input_max():
                            if selected_item_auto.get() == 'Đồng ý theo số lượng':
                                input_max_message.pack(fill='x', side='top',pady=(15,0))
                            else:
                                input_max_message.pack_forget()
                        for item in item_auto:
                            tk.Radiobutton(frame_checkbox,text=item,indicatoron=10,font=("Adobe Kaiti Std R", 12),value=item, variable=selected_item_auto, command=toggle_input_max).pack(side='left', anchor='w')
                        input_max_message = CTkEntry(frame, placeholder_text='Nhập số lượt đồng ý', text_color='black', font=font_text, width=window_width*0.9, height=40)
                        def save_agree_window():
                            try:
                                id=self.selected_value.get()    
                                delaymin=input_min.get()
                                delaymax=input_max.get()
                                type=selected_item_auto.get()
                                quantity=input_max_message.get()
                                cursor.execute('''
                                    INSERT INTO action (timeline_id, name_action, time_min, time_max, type,quantity)
                                    VALUES (?, 'Đồng ý kết bạn', ?, ?, ?, ?)
                                ''', (id, delaymin, delaymax, type,quantity))
                                conn.commit()
                                calldata()
                            except Exception as e:
                                print("Đã xảy ra lỗi:", e)
                            on_close()
                        CTkButton(frame,fg_color='orange',width=100,text='Lưu',font=font_text,text_color='white',height=45,corner_radius=5, command=save_agree_window).pack(side='bottom',anchor='n',pady=(20,0))
                        agree_window.protocol("WM_DELETE_WINDOW", on_close)
            def un_friend():
                        global unfriend_window
                        def toggle_window():
                            if unfriend_window.state() == "normal":
                                unfriend_window.withdraw()
                            else:
                                 unfriend_window.deiconify()
                        if unfriend_window is not None:
                            toggle_window()
                            return
                        def on_close():
                            global unfriend_window
                            unfriend_window.destroy()
                            unfriend_window = None

                        window_width = 500
                        window_height = 300
                        unfriend_window = CTkToplevel(self.main_view_frame)
                        unfriend_window.title("Huỷ kết bạn")
                        unfriend_window.resizable(False,False)
                        unfriend_window.deiconify()
                        position_x = int((self.frame_width - window_width) / 2)
                        position_y = int((self.frame_height - window_height) / 2)
                        unfriend_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
                        container_frame_max_min = CTkFrame(unfriend_window, fg_color='transparent')
                        container_frame_max_min.pack(fill='x', padx=10, pady=5, anchor='ne', side='top') 
                        input_frame_max = CTkFrame(container_frame_max_min, fg_color='transparent')   
                        input_frame_max.pack(fill='x', side='left')  
                        text_2 = CTkLabel(input_frame_max, text='Delay min', text_color='black', font=font_text)
                        text_2.pack(side='top', anchor='w')
                        input_min = CTkEntry(input_frame_max, placeholder_text='Nhập gian thời Delay min', text_color='black', font=font_text, width=window_width/2.3, height=40,border_color='black',border_width=1)
                        input_min.pack(side='top')
                        input_frame = CTkFrame(container_frame_max_min, fg_color='transparent')
                        input_frame.pack(fill='x', padx=10, pady=5, anchor='nw', side='right') 
                        text_1 = CTkLabel(input_frame, text='Delay max', text_color='black', font=font_text)
                        text_1.pack(side='top', anchor='w')
                        input_max = CTkEntry(input_frame, placeholder_text='Nhập thời gian Delay max', text_color='black', font=font_text, width=window_width/2.3, height=40,border_color='black',border_width=1)
                        input_max.pack(side='top', anchor='w')
                        frame = CTkFrame(unfriend_window, fg_color='transparent')
                        frame.pack(fill='x', padx=10, pady=5, anchor='ne', side='top')
                        text_5 = CTkLabel(frame, text='Tự động', text_color='black', font=font_text)
                        text_5.pack(side='top', anchor='w')
                        item_auto=['Huỷ tất cả','Huỷ theo số lượng']
                        selected_item_auto = StringVar(value='Huỷ tất cả')
                        frame_checkbox=CTkFrame(frame)
                        frame_checkbox.pack(side='top', anchor='w',pady=5)

                        def toggle_input_max():
                            if selected_item_auto.get() == 'Huỷ theo số lượng':
                                input_max_message.pack(fill='x', side='top',pady=(15,0))
                            else:
                                input_max_message.pack_forget()
                        for item in item_auto:
                            tk.Radiobutton(frame_checkbox,text=item,indicatoron=10,font=("Adobe Kaiti Std R", 12),value=item, variable=selected_item_auto, command=toggle_input_max).pack(side='left', anchor='w')
                        input_max_message = CTkEntry(frame, placeholder_text='Nhập số lượt huỷ', text_color='black', font=font_text, width=window_width*0.9, height=40)
                        def save_unfriend_window():
                            try:
                                id=self.selected_value.get()    
                                delaymin=input_min.get()
                                delaymax=input_max.get()
                                type=selected_item_auto.get()
                                quantity=input_max_message.get()
                                cursor.execute('''
                                    INSERT INTO action (timeline_id, name_action, time_min, time_max, type,quantity)
                                    VALUES (?, 'Huỷ kết bạn', ?, ?, ?, ?)
                                ''', (id, delaymin, delaymax, type,quantity))
                                conn.commit()
                                calldata()
                            except Exception as e:
                                print("Đã xảy ra lỗi:", e)
                            on_close()
                        CTkButton(frame,fg_color='orange',width=100,text='Lưu',font=font_text,text_color='white',height=45,corner_radius=5, command=save_unfriend_window).pack(side='bottom',anchor='n',pady=(20,0))
                        unfriend_window.protocol("WM_DELETE_WINDOW", on_close)   
            def invite_group_window():
                        global invite_group
                        def toggle_window():
                            if invite_group.state() == "normal":
                                invite_group.withdraw()
                            else:
                                 invite_group.deiconify()
                        if invite_group is not None:
                            toggle_window()
                            return
                        def on_close():
                            global invite_group
                            invite_group.destroy()
                            invite_group = None

                        window_width = 500
                        invite_group = CTkToplevel(self.main_view_frame)
                        invite_group.title("Mời tham gia nhóm")
                        invite_group.resizable(False,False)
                        invite_group.deiconify()
                        container_frame_max_min = CTkFrame(invite_group, fg_color='transparent')
                        container_frame_max_min.pack(fill='x', padx=10, pady=5, anchor='ne', side='top') 
                        input_frame_max = CTkFrame(container_frame_max_min, fg_color='transparent')   
                        input_frame_max.pack(fill='x', side='left')  
                        text_2 = CTkLabel(input_frame_max, text='Delay min', text_color='black', font=font_text)
                        text_2.pack(side='top', anchor='w')
                        input_min = CTkEntry(input_frame_max, placeholder_text='Nhập gian thời Delay min', text_color='black', font=font_text, width=window_width/2.3, height=40,border_color='black',border_width=1)
                        input_min.pack(side='top')
                        input_frame = CTkFrame(container_frame_max_min, fg_color='transparent')
                        input_frame.pack(fill='x', padx=10, pady=5, anchor='nw', side='right') 
                        text_1 = CTkLabel(input_frame, text='Delay max', text_color='black', font=font_text)
                        text_1.pack(side='top', anchor='w')
                        input_max = CTkEntry(input_frame, placeholder_text='Nhập thời gian Delay max', text_color='black', font=font_text, width=window_width/2.3, height=40,border_color='black',border_width=1)
                        input_max.pack(side='top', anchor='w')
                        frame = CTkFrame(invite_group, fg_color='transparent')
                        frame.pack(fill='x',pady=5, anchor='ne', side='top')
                        CTkLabel(frame,text='Số lượng lời mời mỗi tài khoản',text_color='black',font=font_text).pack(side='top',anchor='w',pady=5,padx=10)
                        input_max_message = CTkEntry(frame, placeholder_text='Nhập số lời mời tối đa', text_color='black', font=font_text, width=window_width, height=40)
                        input_max_message.pack(side='top',anchor='n',pady=(0,20),padx=10)
                        select=['Danh sách sđt',' Danh sách bạn bè']
                        selected_item_auto = StringVar(value='Danh sách sđt')
                        CTkLabel(frame,text='Mời theo',text_color='black',font=font_text).pack(side='top',anchor='w',pady=5,padx=10)
                        frame_checkbox=CTkFrame(frame)
                        frame_checkbox.pack(side='top', anchor='w',pady=5,fill='y', expand=True)
                        input_phone =CTkTextbox(frame , text_color='black', width=window_width, height=100,border_color='black',border_width=1)
                        CTkScrollbar(frame,command=input_phone.yview)
                        def toggle_input_max():
                            if selected_item_auto.get() == 'Danh sách sđt':
                                    input_phone.pack(side='top', anchor='w',pady=5,padx=10)
                            else:
                                input_phone.pack_forget()
                        for item in select:
                            tk.Radiobutton(frame_checkbox, value=item,text=item,font=font_text,indicatoron=10,variable=selected_item_auto,command=toggle_input_max).pack(side='left',anchor='w',fill='y', expand=True)
                        toggle_input_max()
                        def save_invite_group():
                            try:
                                id=self.selected_value.get()    
                                delaymin=input_min.get()
                                delaymax=input_max.get()
                                type=selected_item_auto.get()
                                quantity=input_max_message.get()
                                datalist_phone=input_phone.get("1.0", "end-1c")
                                cursor.execute('''
                                    INSERT INTO action (timeline_id, name_action, time_min, time_max, type,quantity,datalist_phone)
                                    VALUES (?, 'Mời tham gia nhóm', ?, ?, ?, ?, ?)
                                ''', (id, delaymin, delaymax, type,quantity,datalist_phone))
                                conn.commit()
                                calldata()
                            except Exception as e:
                                print("Đã xảy ra lỗi:", e)
                            on_close()  
                        CTkButton(frame,fg_color='orange',width=100,text='Lưu',font=font_text,text_color='white',height=45,corner_radius=5, command=save_invite_group).pack(side='bottom',anchor='n',pady=(20,20))
                        invite_group.protocol("WM_DELETE_WINDOW", on_close)                                                                                  
            def open_add_action_window():
                    if(self.selected_value.get()):
                        global new_window
                        def toggle_window():
                            if new_window.winfo_exists():   
                                new_window.deiconify()                  
                        if new_window is not None:  
                            toggle_window()
                            return   
                        def on_close():
                            global new_window
                            new_window.destroy()
                            new_window = None
                        new_window = CTkToplevel(self.main_view_frame)
                        new_window.title("Thêm hành động")
                        window_width = 1000
                        window_height = 500
                        new_window.resizable(False,False)
                        position_x = int((self.frame_width - window_width) / 2)
                        position_y = int((self.frame_height - window_height) / 2)
                        new_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
                        frame_width = window_width / 3.3
                        frame_height = window_height * 0.8
                        # Frame Tương Tác
                        interact_frame = CTkFrame(new_window, width=frame_width, height=frame_height, border_color='black', fg_color='white', border_width=1)
                        interact_frame.pack(side='left', anchor='nw', pady=10, padx=15, fill='y', expand=True)
                        CTkLabel(interact_frame,text='Tương tác',text_color='black',font=("Adobe Kaiti Std R", 17)).pack(pady=10, padx=20,anchor='nw')
                        img_interact = Image.open('assets/iconapp/tuongtac.png')
                        interact_image = CTkImage(light_image=img_interact, size=(frame_width*0.9,frame_height*0.35))
                        CTkLabel(interact_frame, image=interact_image, text='').pack(pady=10, padx=20)
                        def new_feed_action():
                            new_feed_window()
                            on_close()
                        CTkButton(interact_frame,fg_color='white',hover=False,border_color='black',border_width=1,width=frame_width*0.9,height=frame_height*0.1,text='Lướt new feed',text_color='black',font=("Adobe Kaiti Std R", 15),command=new_feed_action).pack(pady=10, padx=20)

                        def window_comment():
                            open_window_comment()
                            on_close()
                        def window_post():
                            upload_post_window()
                            on_close()
                            
                        CTkButton(interact_frame,fg_color='white',hover=False,border_color='black',border_width=1,width=frame_width*0.9,height=frame_height*0.1,text='Bình luận bài viết',text_color='black',font=("Adobe Kaiti Std R", 15),command=window_comment).pack(pady=10, padx=20)
                        CTkButton(interact_frame,fg_color='white',hover=False,border_color='black',border_width=1,width=frame_width*0.9,height=frame_height*0.1,text='Đăng bài viết',text_color='black',font=("Adobe Kaiti Std R", 15),command=window_post).pack(pady=10, padx=20)
                        # Frame Bạn Bè
                        def on_button_click_friend():
                            add_friend_window()
                            on_close()
                        def on_agree_add_friend():
                            agree_add_friend()
                            on_close()
                        def on_un_friend():
                            un_friend()
                            on_close()
                        friend_frame = CTkFrame(new_window, width=frame_width, height=frame_height, border_color='black', fg_color='white', border_width=1)
                        CTkLabel(friend_frame,text='Bạn bè',text_color='black',font=("Adobe Kaiti Std R", 17)).pack(pady=10, padx=20,anchor='nw')
                        friend_frame.pack(side='left', anchor='e', pady=10, padx=15, fill='y', expand=True)
                        img_interact = Image.open('assets/iconapp/friendship.png')
                        friend_image = CTkImage(light_image=img_interact, size=(frame_height*0.35,frame_height*0.35))
                        CTkLabel(friend_frame, image=friend_image, text='').pack(pady=10, padx=20)
                        CTkButton(friend_frame,fg_color='white',hover=False,border_color='black',border_width=1,width=frame_width*0.9,height=frame_height*0.1,text='Gửi kết bạn',command=on_button_click_friend,text_color='black',font=("Adobe Kaiti Std R", 15)).pack(pady=10, padx=20)
                        CTkButton(friend_frame,fg_color='white',hover=False,border_color='black',border_width=1,width=frame_width*0.9,
                        command=on_agree_add_friend,height=frame_height*0.1,text='Đồng ý kết bạn',text_color='black',font=("Adobe Kaiti Std R", 15)).pack(pady=10, padx=20)
                        CTkButton(friend_frame,fg_color='white',hover=False,border_color='black',border_width=1,width=frame_width*0.9,height=frame_height*0.1,text='Huỷ kết bạn',text_color='black',font=("Adobe Kaiti Std R", 15),command=on_un_friend).pack(pady=10, padx=20)
                        # Frame Nhóm
                        def on_button_click_message():
                            sent_message_window()
                            on_close()
                        def on_button_click_invite_group():
                            invite_group_window()
                            on_close()
                        group_frame = CTkFrame(new_window, width=frame_width, height=frame_height, border_color='black', fg_color='white', border_width=1)
                        group_frame.pack(side='left', anchor='w', pady=10, padx=15, fill='y', expand=True)
                        CTkLabel(group_frame,text='Nhóm',text_color='black',font=("Adobe Kaiti Std R", 17)).pack(pady=10, padx=20,anchor='nw')
                        img_interact = Image.open('assets/iconapp/group1.png')
                        friend_image = CTkImage(light_image=img_interact, size=(frame_height*0.35,frame_height*0.35))
                        CTkLabel(group_frame, image=friend_image, text='').pack(pady=10, padx=20)
                       
                        CTkButton(group_frame,fg_color='white',hover=False,border_color='black',border_width=1,width=frame_width*0.9,height=frame_height*0.1,text='Nhắn tin',text_color='black',font=("Adobe Kaiti Std R", 15),command=on_button_click_message).pack(pady=10, padx=20)
                        CTkButton(group_frame,fg_color='white',hover=False,border_color='black',border_width=1,width=frame_width*0.9,height=frame_height*0.1,text='Mời tham gia nhóm',command=on_button_click_invite_group,text_color='black',font=("Adobe Kaiti Std R", 15)).pack(pady=10, padx=20)

                        new_window.protocol("WM_DELETE_WINDOW", on_close)
                    else:
                        messagebox.showwarning(title='Thông báo',message='Bạn chưa chọn timeline')

            
        elif loai_man_hinh == "Thiết bị":           
            CTkLabel(self.main_view_frame, text='Quản lý thiết bị', font=("Adobe Kaiti Std R", 20)).pack(side='top',anchor='nw')
            treeFrame = ttk.Frame(self.main_view_frame,borderwidth=1)
            treeFrame.pack(side='left', anchor='nw', pady=10, padx=20)
            treeScroll = ttk.Scrollbar(treeFrame)
            treeScroll.pack(side="right", fill="y")
            cols = ("Stt", "Tên máy", "Mã máy" ,"IMEI", "Trạng thái", "Tác vụ")
            treeview = ttk.Treeview(treeFrame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=14)
            treeview.column("Stt", width=50)
            treeview.column("Tên máy", width=150)
            treeview.column("Mã máy", width=150)
            treeview.column("IMEI", width=150)
            treeview.column("Trạng thái", width=100)
            treeview.column("Tác vụ", width=100)
            treeview.heading("Stt", text="Stt")
            treeview.heading("Tên máy", text="Tên máy")
            treeview.heading("Mã máy", text="Mã máy")
            treeview.heading("IMEI", text="IMEI")
            treeview.heading("Trạng thái", text="Trạng thái")
            treeview.heading("Tác vụ", text="Tác vụ")
            treeview.pack()
            if(get_devices()):
                for device in get_devices():
                    device_properties = device.get_properties()
                    treeview.insert("", "end", values=(1, device_properties.get('ro.product.model', 'Unknown Device'),device.serial,get_device_imei(device), device.get_state()))
    def cc():
        print('12312')
if __name__ == "__main__":
    root = CTk()
    dashboard_screen = DashboardScreen(root)
    root.title('Phần mềm auto tool Zalo')
    icon = tk.PhotoImage(file="assets/iconapp/zalo.png")
    root.iconphoto(False, icon)
    # root.resizable(False,False)
    root.state('zoomed')
    root.mainloop()
