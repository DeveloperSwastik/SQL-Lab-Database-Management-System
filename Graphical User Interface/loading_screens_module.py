import time
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
import file_branching_module as fbm

# ------------------------------ LOADING SCREEN ------------------------------

def software_loading_splash_screen():
    splash_screen = Tk()

    appWidth = 450
    appHeigth = 360

    screenWidth = splash_screen.winfo_screenwidth()
    screenHeight = splash_screen.winfo_screenheight()

    geometry = (
        f"{int(appWidth)}x{int(appHeigth)}+"
        f"{int((screenWidth - appWidth)/2)}+"
        f"{int((screenHeight - appHeigth)/2)}"
    )
    splash_screen.geometry(geometry)
    splash_screen.overrideredirect(True)

    splash_screen.iconbitmap("Resources\\Images\\sqllablogo.ico")

    style = ttk.Style()
    style.theme_use('default')
    style.configure("splash.Horizontal.TProgressbar", background='#F06AFF')

    img = PhotoImage(file="Resources\\Images\\Software_loading_screen.png")
    background_image_lable = Label(splash_screen, image=img)
    background_image_lable.place(x=0, y=0)

    FUNCTION_FLOW = [
        fbm.create_main_folder, fbm.create_sub_folders_of_main_folder,
        fbm.create_sub_folders_of_system_folder,
        fbm.create_sub_folders_of_Credentials_of_standard_anonymous_guest_account,
        fbm.create_files_for_credential_of_adminstrator_account_folder,
        fbm.add_credentials_of_administrator,
        fbm.create_files_for_credential_of_user_account_folder
    ]

    def bar():
        for i in range(100):
            progress['value'] = i
            
            if i == 0:
                FUNCTION_FLOW[0]()
            elif i == 16:
                FUNCTION_FLOW[1]()
            elif i == 33:
                FUNCTION_FLOW[2]()
            elif i == 50:
                FUNCTION_FLOW[3]()
            elif i == 67:
                FUNCTION_FLOW[4]()
            elif i == 84:
                FUNCTION_FLOW[5]()
            elif i == 99:
                FUNCTION_FLOW[6]()

            splash_screen.update_idletasks()
            time.sleep(0.03)

        splash_screen.destroy()

    progress = Progressbar(
        splash_screen, style="splash.Horizontal.TProgressbar",
        orient=HORIZONTAL, length=470, mode='determinate'
    )
    progress.place(x=-10, y=342)

    bar()
    splash_screen.mainloop()
