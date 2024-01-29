from customtkinter import *
from PIL import Image
from Home import DashboardScreen
app = CTk()
app.geometry("600x480+{}+{}".format((app.winfo_screenwidth() - 600) // 2, (app.winfo_screenheight() - 480) // 2))
app.resizable(False, False)
cancel_icon = Image.open("assets/iconapp/cancel.png")
google_icon = CTkImage(dark_image=cancel_icon, light_image=cancel_icon, size=(17,17))
app.title("Phần mềm auto tool Zalo")
frame = CTkFrame(master=app, width=600, height=480, fg_color="#ffffff")
frame.pack_propagate(0)
def show_dashboard():
        app.destroy() 
        root=CTk()
        dashboard_screen = DashboardScreen(root)
        dashboard_screen.show()
        root.mainloop()

def Login():
    if entry1.get() == 'admin' and entry2.get() == 'admin':
        err.configure(text='Đăng nhập thành công!')
        show_dashboard()
    else:
        err.configure(text='Đăng nhập thất bại. Vui lòng kiểm tra lại tài khoản và mật khẩu.')
frame.pack(expand=True, anchor="center")
label1 = CTkLabel(master=frame, text="Xin chào \nNguyễn Văn Kiên!", text_color="#601E88", anchor="center", justify="left", font=("Adobe Kaiti Std R Bold", 24))
label1.pack(anchor="center", pady=(50, 5), padx=(25, 0))
entry1 = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="black", border_width=1, text_color="#000000",placeholder_text='Tài khoản',height=40,corner_radius=30,font=('Adobe Kaiti Std R',15))
entry1.pack(anchor="center", padx=(25, 0),pady=(25, 25))
entry2 = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="black", border_width=1, text_color="#000000", show="*",placeholder_text='Mật khẩu',height=40,corner_radius=30,font=('Adobe Kaiti Std R',15))
entry2.pack(anchor="center", padx=(25, 0))
err = CTkLabel(master=frame, text='', text_color="red", anchor="center", justify="center", font=("Adobe Kaiti Std R", 14))
err.pack(anchor="center", pady=(5, 5))
button = CTkButton(master=frame,height=45,command=Login, text="Đăng nhập",fg_color="#601E88", hover_color="#E44982", font=("Adobe Kaiti Std R Bold", 20), text_color="#ffffff", width=225,corner_radius=30)
button.pack(anchor="center", pady=(10, 0), padx=(25, 0))
app.mainloop()
