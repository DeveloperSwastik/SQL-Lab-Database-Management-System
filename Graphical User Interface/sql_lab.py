import getpass
import json
import os
import random
import time
import tkinter
from datetime import datetime
from tkinter import *
from tkinter import filedialog, messagebox, ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

import data_encription as de
import file_branching_module as fbm
import license_and_details as lad
import select_pop_up as spu
import working_with_local_db as wwldb
import working_with_system_db as wwsdb


# ----------------------------- LOADING PROCESS ------------------------------

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

    progress = ttk.Progressbar(
        splash_screen, style="splash.Horizontal.TProgressbar",
        orient=HORIZONTAL, length=470, mode='determinate'
    )
    progress.place(x=-10, y=342)

    bar()
    splash_screen.mainloop()


software_loading_splash_screen()


# --------------------------- CLASSES DECLERATION ----------------------------

class ButtonConfig():
    def __init__(
        self, master, font_size, width, height=1,
        place=[], pack=[], padding=[], cursor="hand2", command=None,
        font_name=None, border=3, colour=[], aling=None,
        button_text="Enter the text", bg_less_btn=[False, False],
        on_click_bg_change=False, on_click_state="deactive"
    ):

        def hoverOnBtn(a):
            global current_hovering_btn_bg, current_hovering_btn_fg
            if a == 1:
                current_hovering_btn_bg = self.cget('background')
                current_hovering_btn_fg = self.cget('foreground')

            if not(bg_less_btn[0]):
                if a == 1:
                    self.config(
                        background=COLOUR_COLLECTION["Colour 03"],
                        foreground=COLOUR_COLLECTION["Colour 05"]
                    )
                elif a == 2:
                    self.config(
                        background=current_hovering_btn_bg,
                        foreground=current_hovering_btn_fg
                    )
            else:
                if a == 1:
                    self.config(
                        foreground=COLOUR_COLLECTION["Colour 05"]
                    )
                    if bg_less_btn[1]:
                        self.config(
                            background=COLOUR_COLLECTION["Colour 03"]
                        )
                elif a == 2:
                    self.config(
                        foreground=current_hovering_btn_fg
                    )
                    if bg_less_btn[1]:
                        self.config(
                            background=current_hovering_btn_bg
                        )

        def click_change():
            global current_hovering_btn_bg, current_hovering_btn_fg

            widgets = master.winfo_children()

            for widget in widgets:

                if widget == self:
                    widget.config(
                        bg=COLOUR_COLLECTION["Colour 02"]
                    )
                    current_hovering_btn_bg = COLOUR_COLLECTION["Colour 02"]
                else:
                    widget.config(
                        bg=COLOUR_COLLECTION["Colour 00"]
                    )

            command()

        self = Button(master)

        if font_name is None:
            font_name = FONT_COLLECTION["Font 2 --> Times New Roman"]
        else:
            font_name = font_name

        if bg_less_btn[0]:
            [bg, fg, active_bg, active_fg] = [COLOUR_COLLECTION["Colour 00"],
                                              COLOUR_COLLECTION["Colour 04"],
                                              COLOUR_COLLECTION["Colour 00"],
                                              COLOUR_COLLECTION["Colour 04"]]
            if border == 3:
                border = 0
        elif not len(colour):
            [bg, fg, active_bg, active_fg] = [COLOUR_COLLECTION["Colour 02"],
                                              COLOUR_COLLECTION["Colour 04"],
                                              COLOUR_COLLECTION["Colour 00"],
                                              COLOUR_COLLECTION["Colour 04"]]
        else:
            [bg, fg, active_bg, active_fg] = colour

        if on_click_state == "active":
            bg = COLOUR_COLLECTION["Colour 02"]

        self.config(
            text=button_text, background=bg,
            foreground=fg, border=border, cursor=cursor,
            activebackground=active_bg, activeforeground=active_fg,
            font=(font_name, font_size), width=width, height=height,
        )

        if aling is not None:
            self.config(
                anchor=aling
            )

        if command is not None:

            if on_click_bg_change:
                self.config(
                    command=click_change
                )
            else:
                self.config(
                    command=command
                )

        if len(place):
            self.place(x=place[0], y=place[1])
        elif len(pack):

            if len(pack) == 3:
                expand = pack[2]
            else:
                expand = False

            if not len(padding):
                self.pack(fill=pack[0], side=pack[1], expand=expand)
            else:
                self.pack(
                    fill=pack[0], side=pack[1], expand=expand,
                    padx=padding[0], pady=padding[1]
                )

        self.bind("<Enter>", lambda event: hoverOnBtn(a=1))
        self.bind("<Leave>", lambda event: hoverOnBtn(a=2))


class LabelConfig():
    def __init__(
        self, master, x_place, y_place,
        font_size, Label_text="Enter the text", colour=[],
        font_name=None, font_style="",
    ):

        self = Label(master)

        if font_name is None:
            font_name = FONT_COLLECTION["Font 2 --> Times New Roman"]
        else:
            font_name = font_name

        if not len(colour):
            [bg, fg] = [COLOUR_COLLECTION["Colour 00"],
                        COLOUR_COLLECTION["Colour 05"]]
        else:
            [bg, fg] = colour

        self.config(
            text=Label_text, background=bg,
            foreground=fg, font=(font_name, font_size, font_style)
        )

        self.place(x=x_place, y=y_place)


class EntryConfig():
    def __init__(
        self, master, x_place, y_place,
        text_variable, entry_lenght, colour=[],
        font_name=None, font_size=17, hide_and_show_text=False,
        hide_and_show_btn_config=[]
    ):

        def show_and_hide_password():
            global count

            if count:
                self.config(
                    show="*"
                )
                count = False
            else:
                self.config(
                    show=""
                )
                count = True

        self = Entry(master)

        if font_name is None:
            font_name = FONT_COLLECTION["Font 2 --> Times New Roman"]
        else:
            font_name = font_name

        if not len(colour):
            [bg, fg] = [COLOUR_COLLECTION["Colour 02"],
                        COLOUR_COLLECTION["Colour 05"]]
        else:
            [bg, fg] = colour

        self.config(
            textvariable=text_variable, background=bg,
            foreground=fg, font=(font_name, font_size),
            width=entry_lenght
        )

        self.place(x=x_place, y=y_place)

        if hide_and_show_text:
            self.config(
                show="*"
            )

            [x_place_btn, y_place_btn, ] = hide_and_show_btn_config

            show_hide_btn = ButtonConfig(
                master, 20, 1, place=[x_place_btn, y_place_btn],
                button_text="👁", bg_less_btn=[True, False],
                command=show_and_hide_password
            )


# ------------------------- ROOT WINDOW DECLARATION --------------------------

root = Tk()
root.resizable(False, False)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.iconbitmap('Resources\\Images\\sqllablogo.ico')


# ----------------------------- MENU DECLARATION -----------------------------

root_menu = Menu(root)
root.config(menu=root_menu)

account_menu = Menu(root_menu, tearoff=OFF)
root_menu.add_cascade(label="Account", menu=account_menu)

help_and_about_menu = Menu(root_menu, tearoff=OFF)
root_menu.add_cascade(label="About", menu=help_and_about_menu)

account_menu.add_cascade(
    label="Create account",
    command=lambda: redirect(create_user_account_window)
)
account_menu.add_cascade(
    label="Admin panel", command=lambda: admin_panel_login()
)

help_and_about_menu.add_cascade(
    label="View License",
    command=lambda: license_window()
)
help_and_about_menu.add_cascade(
    label="Software details",
    command=lambda: software_details_window()
)


# --------------------------------- STYLING ----------------------------------

style = ttk.Style()

style.theme_use('default')
style.map(
    'Treeview', background=[('selected', "Grey")]
)
style.configure(
    "Treeview", fieldbackground="White"
)
style.configure(
    'Treeview.Heading', background="#C4C3D0", foreground="Black"
)


# ------------------------- SOFTWARE DETAILS WINDOW --------------------------

def software_details_window():
    software_detials_frame = Toplevel(
        root,
        background=COLOUR_COLLECTION["Colour 01"]
    )

    app_width = 350
    app_heigth = 300

    software_detials_frame.title("SQL LAB - ABOUT")
    software_detials_frame.resizable(0, 0)
    software_detials_frame.geometry(
        f"{int(app_width)}x{int(app_heigth)}+"
        f"{int((screen_width - app_width)/2)}+"
        f"{int((screen_height - app_heigth)/5)}"
    )
    software_detials_frame.iconbitmap("Resources\\Images\\license.ico")

    logo_img = ImageTk.PhotoImage(
        Image.open(
            "Resources\\Images\\logo.png"
        ).resize((350, 120))
    )

    logo = Label(software_detials_frame, image=logo_img)
    logo.place(x=0, y=0)

    colour = [COLOUR_COLLECTION["Colour 01"], COLOUR_COLLECTION["Colour 05"]]
    y_place = 130

    for key in list(lad.ABOUT.keys()):
        content = LabelConfig(
            software_detials_frame, 5, y_place, 15, key, colour
        )
        colon = LabelConfig(
            software_detials_frame, 140, y_place, 15, ":", colour
        )
        content_description = LabelConfig(
            software_detials_frame, 150, y_place, 15, lad.ABOUT[key], colour
        )
        y_place += 28

    content_description = LabelConfig(
        software_detials_frame, 30, 280, 10,
        "Copyright (c) 2022, Swastik Sharma All rights reserved.", colour
    )

    software_detials_frame.mainloop()


# ----------------------------- LICENSE WINDOW -------------------------------

def license_window():
    license = Toplevel(
        root,
        background=COLOUR_COLLECTION["Colour 01"]
    )

    app_width = 620
    app_heigth = 650

    license.title("SQL LAB - LICENSE")
    license.resizable(0, 0)
    license.geometry(
        f"{int(app_width)}x{int(app_heigth)}+"
        f"{int((screen_width - app_width)/2)}+"
        f"{int((screen_height - app_heigth)/5)}"
    )
    license.iconbitmap("Resources\\Images\\license.ico")

    logo_img = ImageTk.PhotoImage(
        Image.open(
            "Resources\\Images\\logo.png"
        ).resize((620, 200))
    )

    logo = Label(license, image=logo_img)
    logo.place(x=0, y=0)

    heading = LabelConfig(
        license, 165, 180, 20, lad.LICENSE[0],
        [COLOUR_COLLECTION["Colour 01"], COLOUR_COLLECTION["Colour R1"]],
        font_style='underline',
        font_name=FONT_COLLECTION["Font 1 --> Algerian"],
    )

    colour = [COLOUR_COLLECTION["Colour 01"], COLOUR_COLLECTION["Colour 05"]]
    y_place = 220

    for line in lad.LICENSE[2:]:

        if line == "":
            content = LabelConfig(
                license, 5, y_place, 10, line, colour
            )
            y_place += 8
        else:
            content = LabelConfig(
                license, 5, y_place, 10, line, colour
            )
            y_place += 20

    license.mainloop()


# ---------------------------- ADMIN PANEL LOGIN -----------------------------

def admin_panel_login():

    def check_pass(pass_):
        pass_ = de.convert_orignal_data_to_hashes(
            pass_
        )

        with open(
            f'{path_3}admin_credential.json'
        ) as file:
            password_ = json.load(file)[de.PASSWORD]

        if pass_ == password_:
            admin_login.destroy()
            redirect(admin_panel)
        else:
            messagebox.showwarning(
                title='SQL Lab - Message Box',
                message=(
                    'The entered password is incorrect.'
                )
            )
            admin_login.destroy()

    admin_login = Toplevel(
        root, background=COLOUR_COLLECTION["Colour 00"]
    )

    top_level_windows.append(admin_login)

    app_width = 300
    app_heigth = 120
    local_storage_variable_1 = StringVar()

    admin_login.title("SQL Lab - Admin Panel Login")
    admin_login.resizable(0, 0)
    admin_login.geometry(
        f"{int(app_width)}x{int(app_heigth)}+"
        f"{int((screen_width - app_width)/2)}+"
        f"{int((screen_height - app_heigth)/5)}"
    )
    admin_login.iconbitmap("Resources\\Images\\sqllablogo.ico")

    user = LabelConfig(
        admin_login, 10, 20, 15, 'User Name :  Administrator'
    )

    password = LabelConfig(
        admin_login, 10, 50, 15, 'Password   :'
    )

    password_entry = EntryConfig(
        admin_login, 120, 50, local_storage_variable_1, 15, font_size=14,
        hide_and_show_text=True, hide_and_show_btn_config=[268, 37]
    )

    login_btn = ButtonConfig(
        admin_login, 10, 10, place=[110, 80], button_text="Login",
        border=2, command=lambda: check_pass(local_storage_variable_1.get())
    )


# ------------------------------- ADMIN PANEL --------------------------------

def admin_panel():
    global clone_option_bar_frame

    def user_details():
        global clone_user_details_frame

        def fetch_user_data(user_name):
            storage_use = 0
            no_of_db = 0

            path_a = (
                f"{path_2}{user_name}_database_folder"
            )
            path_b = (
                f"{path_1}{user_name}_folder"
            )

            with open(f"{path_b}\\user_credential.json") as file:
                data = json.load(file)

            for file in os.listdir(path_a):
                no_of_db += 1
                storage_use += os.path.getsize(f"{path_a}\\{file}")/1000

            try:

                with open(f"{path_b}\\user_connections.json") as file:
                    no_of_connection = len(json.load(file)[de.ID])

            except json.decoder.JSONDecodeError:
                no_of_connection = 0

            return [
                de.convert_modifide_data_to_orignal_data(
                    user_name
                ).capitalize(),
                de.convert_hashes_to_orignal_data(data[de.PASSWORD]),
                de.convert_hashes_to_orignal_data(
                    data[de.PROFILE]
                ).capitalize(),
                data[de.DATE], data[de.TIME], f"{storage_use:.4f} Kb",
                no_of_db, no_of_connection
            ]

        def show_user_details():
            try:

                with open(
                    f"{path_1}user_names.json"
                ) as file:
                    user_names = [name for name in json.load(file)[
                        de.USER_NAME]]

            except json.decoder.JSONDecodeError:
                user_names = []

            data = [fetch_user_data(name) for name in user_names]

            user_details_tree.delete(*user_details_tree.get_children())

            for index, element in enumerate(data[::-1]):

                if index % 2 == 0:
                    user_details_tree.insert(
                        "", "end", values=[index+1]+element, tags=('evenrow',)
                    )
                else:
                    user_details_tree.insert(
                        "", "end", values=[index+1]+element, tags=('oddrow',)
                    )

        local_frames_destroyer()

        user_details_frame = Frame(
            root, background=COLOUR_COLLECTION["Colour 00"]
        )
        user_details_frame.place(
            x=0, y=app_heigth/15,
            width=app_width, height=app_heigth*(14/15)
        )

        clone_user_details_frame = user_details_frame

        user_details_tree = ttk.Treeview(
            user_details_frame, columns=[
                "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9"
            ],
            show="headings", height=100
        )

        user_details_tree.heading("c1", text="#")
        user_details_tree.heading("c2", text="User name")
        user_details_tree.heading("c3", text="Password")
        user_details_tree.heading("c4", text="Profile")
        user_details_tree.heading("c5", text="Date of account creation")
        user_details_tree.heading("c6", text="Time of account creation")
        user_details_tree.heading("c7", text="Storage occupied")
        user_details_tree.heading(
            "c8", text="Total number of database created"
        )
        user_details_tree.heading(
            "c9", text="Total number of connection created"
        )

        user_details_tree.column("c1", anchor=CENTER, width=40)
        user_details_tree.column("c2", anchor=W)
        user_details_tree.column("c3", anchor=W)
        user_details_tree.column("c4", anchor=CENTER)
        user_details_tree.column("c5", anchor=CENTER)
        user_details_tree.column("c6", anchor=CENTER)
        user_details_tree.column("c7", anchor=CENTER)
        user_details_tree.column("c8", anchor=CENTER)
        user_details_tree.column("c9", anchor=CENTER)

        scrollbar = Scrollbar(user_details_frame)
        scrollbar.pack(side=RIGHT, fill=BOTH)
        user_details_tree.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=user_details_tree.yview)

        scrollbar1 = Scrollbar(user_details_frame, orient=HORIZONTAL)
        scrollbar1.pack(side=BOTTOM, fill=BOTH)
        user_details_tree.config(xscrollcommand=scrollbar1.set)
        scrollbar1.config(command=user_details_tree.xview)

        user_details_tree.tag_configure(
            'evenrow', background=COLOUR_COLLECTION["Colour 00"]
        )

        user_details_tree.tag_configure(
            'oddrow', background=COLOUR_COLLECTION["Colour 03"],
        )

        user_details_tree.pack(fill=BOTH)

        show_user_details()

    def user_manager():
        global clone_user_manager_frame

        def change_user_pass():
            global clone_change_pass_frame

            def verify(user_name):
                try:

                    with open(
                        f"{path_1}user_names.json"
                    ) as file:
                        users_name = json.load(file)[de.USER_NAME]

                except json.decoder.JSONDecodeError:
                    users_name = []

                if users_name.count(user_name):
                    return True

                return False

            def change_pass(user_name, new_password, renterd_new_pass):
                user_name = user_name.replace(' ', '')

                all_entry_fill = [
                    user_name != "", new_password != "",
                    renterd_new_pass != ""
                ]

                if all(all_entry_fill):

                    if punctuation_checker(user_name) == False:
                        user_name = de.convert_orignal_data_to_modifide_data(
                            user_name
                        )

                        if verify(user_name):

                            if new_password == renterd_new_pass:

                                with open(
                                    f"{path_1}{user_name}_folder\\"
                                    "user_credential.json"
                                ) as file:
                                    data = json.load(file)

                                data[de.PASSWORD] = (
                                    de.convert_orignal_data_to_hashes(
                                        new_password
                                    )
                                )

                                with open(
                                    f"{path_1}{user_name}_folder\\"
                                    "user_credential.json", "w"
                                ) as file:
                                    json.dump(data, file)

                                current_user_details = [
                                    user_name, user_name, 'general'
                                ]

                                add_user_action_info(
                                    'Admin change your account password.',
                                    'Action completed successfully.'
                                )

                                current_user_details = []

                                messagebox.showinfo(
                                    title='SQL Lab - Message Box',
                                    message=(
                                        'Password change successfully.'
                                    )
                                )

                                local_storage_variable_1.set(
                                    "Enter the user name here ..."
                                )
                                local_storage_variable_2.set(
                                    "Enter new password here ..."
                                )
                                local_storage_variable_3.set(
                                    "Renter new password here ..."

                                )
                            else:
                                messagebox.showwarning(
                                    title='SQL Lab - Message Box',
                                    message=(
                                        'Rentered password not match.'
                                    )
                                )

                        else:
                            messagebox.showwarning(
                                title='SQL Lab - Message Box',
                                message=(
                                    'The entered user name not exists'
                                )
                            )

                    else:
                        messagebox.showwarning(
                            title='SQL Lab - Message Box',
                            message=(
                                'The entered user name not exists'
                            )
                        )

                else:
                    messagebox.showwarning(
                        title='SQL Lab - Message Box',
                        message=(
                            'Please, fill all entries.'
                        )
                    )

            inner_frame_destroyer()

            frame_width = 520
            frame_height = 400

            local_storage_variable_1 = StringVar()
            local_storage_variable_2 = StringVar()
            local_storage_variable_3 = StringVar()

            change_pass_frame = Frame(
                user_manager_frame, background=COLOUR_COLLECTION["Colour 00"],
                highlightbackground=COLOUR_COLLECTION["Colour 05"],
                highlightthickness=1
            )
            change_pass_frame.place(
                x=(app_width/5 + ((app_width - (app_width/5))/2 -
                                  (frame_width/2))),
                y=((app_heigth - (app_heigth/15))/2 - (frame_height/2)),
                width=frame_width, height=frame_height
            )

            clone_change_pass_frame = change_pass_frame

            icon = LabelConfig(
                change_pass_frame, 100, 20, 30, '🔑'
            )

            heading = LabelConfig(
                change_pass_frame, 130, 30, 20, 'Change User Password',
                font_style='underline'
            )

            user_name_ = LabelConfig(
                change_pass_frame, 30, 100, 20, "User Name"
            )

            user_icon = LabelConfig(
                change_pass_frame, 60, 135, 20, "👤"
            )

            user_name_entry = EntryConfig(
                change_pass_frame, 95, 135, local_storage_variable_1, 32
            )
            local_storage_variable_1.set("Enter the user name here ...")

            password = LabelConfig(
                change_pass_frame, 30, 170, 20, "New Password"
            )

            password_icon = LabelConfig(
                change_pass_frame, 60, 200, 20, "🔑"
            )

            password_entry = EntryConfig(
                change_pass_frame, 95, 205, local_storage_variable_2, 32,
                hide_and_show_text=True, hide_and_show_btn_config=[470, 195]
            )
            local_storage_variable_2.set("Enter new password here ...")

            renter_password = LabelConfig(
                change_pass_frame, 30, 240, 20, "Renter New Password"
            )

            renter_password_icon = LabelConfig(
                change_pass_frame, 60, 270, 20, "🔑"
            )

            renter_password_entry = EntryConfig(
                change_pass_frame, 95, 275, local_storage_variable_3, 32,
                hide_and_show_text=True, hide_and_show_btn_config=[470, 265]
            )
            local_storage_variable_3.set("Renter new password here ...")

            change_pass_btn = ButtonConfig(
                change_pass_frame, 12, 12, place=[200, 330],
                button_text="Change password", border=2,
                command=lambda: change_pass(
                    local_storage_variable_1.get(),
                    local_storage_variable_2.get(),
                    local_storage_variable_3.get()
                )
            )

        def edit(user_name, var_add, task):
            global current_user_details

            user_name = user_name.replace(' ', '')

            if user_name != '':

                if not punctuation_checker(user_name):
                    user_name = de.convert_orignal_data_to_modifide_data(
                        user_name
                    )

                    try:

                        with open(
                            f"{path_1}user_names.json"
                        ) as file:
                            user_names = json.load(file)[de.USER_NAME]

                    except json.decoder.JSONDecodeError:
                        user_names = []

                    if user_names.count(user_name):

                        if task == 'delete':
                            message = (
                                'You want to delete user "'
                                f'{var_add.get()}"?'
                            )
                        elif task == 'clean':
                            message = (
                                'You want to clean all data of user "'
                                f'{var_add.get()}"?'
                            )

                        ask_to_delete = messagebox.askyesno(
                            title='SQL Lab - Message Box', message=message
                        )

                        if ask_to_delete:

                            with open(
                                f"{path_1}{user_name}_folder\\"
                                "user_credential.json"
                            ) as file:
                                data = json.load(file)

                            if task == 'delete':
                                user_names.remove(user_name)
                                data[de.USER_NAME] = user_names

                            for file in os.listdir(
                                f"{path_1}{user_name}_folder\\"
                                "Upanel_folder"
                            ):
                                if task == 'delete':
                                    os.remove(
                                        f"{path_1}{user_name}_folder\\"
                                        f"Upanel_folder\\{file}"
                                    )
                                elif task == 'clean':
                                    with open(
                                        f"{path_1}{user_name}_folder\\"
                                        f"Upanel_folder\\{file}", 'w'
                                    ):
                                        pass

                            for file in os.listdir(
                                f"{path_1}{user_name}_folder"
                            ):
                                if task == 'delete':

                                    try:
                                        os.remove(
                                            f"{path_1}{user_name}_folder"
                                            f"\\{file}"
                                        )
                                    except PermissionError:
                                        os.rmdir(
                                            f"{path_1}{user_name}_folder"
                                            f"\\{file}"
                                        )
                                elif task == 'clean':

                                    try:

                                        if file == 'user_credential.json':
                                            pass
                                        else:

                                            with open(
                                                f"{path_1}{user_name}_folder"
                                                f"\\{file}", 'w'
                                            ):
                                                pass

                                    except PermissionError:
                                        pass

                            if task == 'delete':
                                os.rmdir(
                                    f"{path_1}{user_name}_folder"
                                )

                            for file in os.listdir(
                                f'{path_2}{user_name}_database_folder'
                            ):
                                os.remove(
                                    f'{path_2}{user_name}_database_folder\\'
                                    f'{file}'
                                )

                            if task == 'delete':
                                os.rmdir(
                                    f"{path_2}{user_name}_database_folder"
                                )

                                with open(
                                    f"{path_1}user_names.json", 'w'
                                ) as file:
                                    json.dump(data, file)

                                messagebox.showinfo(
                                    title='SQL Lab - Message Box',
                                    message=(
                                        f'User "{var_add.get()}"'
                                        'deleted successfully.'
                                    )
                                )
                            elif task == 'clean':
                                current_user_details = [
                                    user_name, user_name, 'general'
                                ]

                                add_user_action_info(
                                    'Admin clean all of your user data.',
                                    'Action completed successfully.'
                                )

                                current_user_details = []

                                messagebox.showinfo(
                                    title='SQL Lab - Message Box',
                                    message=(
                                        f'All data of user "{var_add.get()}"'
                                        'deleted successfully.'
                                    )
                                )

                            var_add.set(
                                'Enter the user name here ...'
                            )

                        else:
                            messagebox.showinfo(
                                title='SQL Lab - Message Box',
                                message=(
                                    'Deletation canceled.'
                                )
                            )

                    else:
                        messagebox.showwarning(
                            title='SQL Lab - Message Box',
                            message=(
                                'The entered user name not exists.'
                            )
                        )

                else:
                    messagebox.showwarning(
                        title='SQL Lab - Message Box',
                        message=(
                            'The entered user name not exists.'
                        )
                    )

            else:
                messagebox.showwarning(
                    title='SQL Lab - Message Box',
                    message=(
                        'Please, fill all entries.'
                    )
                )

        def delete_user():
            global clone_delete_user_frame

            inner_frame_destroyer()

            frame_width = 500
            frame_height = 250

            local_storage_variable_1 = StringVar()

            delete_user_frame = Frame(
                user_manager_frame, background=COLOUR_COLLECTION["Colour 00"],
                highlightbackground=COLOUR_COLLECTION["Colour 05"],
                highlightthickness=1
            )
            delete_user_frame.place(
                x=(
                    app_width/5 + ((app_width -
                                    (app_width/5))/2 - (frame_width/2))
                ),
                y=((app_heigth - (app_heigth/15))/2 - (frame_height/2)),
                width=frame_width, height=frame_height
            )

            clone_delete_user_frame = delete_user_frame

            icon = LabelConfig(
                delete_user_frame, 140, 20, 30, '🗳'
            )

            heading = LabelConfig(
                delete_user_frame, 185, 30, 20, 'Delete User',
                font_style='underline'
            )

            user_name_ = LabelConfig(
                delete_user_frame, 30, 100, 20, "User Name"
            )

            user_icon = LabelConfig(
                delete_user_frame, 60, 135, 20, "👤"
            )

            user_name_entry = EntryConfig(
                delete_user_frame, 95, 135, local_storage_variable_1, 32
            )
            local_storage_variable_1.set("Enter the user name here ...")

            delete_user_btn = ButtonConfig(
                delete_user_frame, 12, 12, place=[180, 190],
                button_text="Delete User", border=2,
                command=lambda: edit(
                    local_storage_variable_1.get(), local_storage_variable_1,
                    'delete'
                )
            )

        def clean_user_data():
            global clone_clean_user_data_frame

            inner_frame_destroyer()

            frame_width = 500
            frame_height = 250

            local_storage_variable_1 = StringVar()

            clean_user_data_frame = Frame(
                user_manager_frame, background=COLOUR_COLLECTION["Colour 00"],
                highlightbackground=COLOUR_COLLECTION["Colour 05"],
                highlightthickness=1
            )
            clean_user_data_frame.place(
                x=(
                    app_width/5 + ((app_width -
                                    (app_width/5))/2 - (frame_width/2))
                ),
                y=((app_heigth - (app_heigth/15))/2 - (frame_height/2)),
                width=frame_width, height=frame_height
            )

            clone_clean_user_data_frame = clean_user_data_frame

            icon = LabelConfig(
                clean_user_data_frame, 125, 20, 30, '🗞'
            )

            heading = LabelConfig(
                clean_user_data_frame, 170, 30, 20, 'Clean User Data',
                font_style='underline'
            )

            user_name_ = LabelConfig(
                clean_user_data_frame, 30, 100, 20, "User Name"
            )

            user_icon = LabelConfig(
                clean_user_data_frame, 60, 135, 20, "👤"
            )

            user_name_entry = EntryConfig(
                clean_user_data_frame, 95, 135, local_storage_variable_1, 32
            )
            local_storage_variable_1.set("Enter the user name here ...")

            clean_data_btn = ButtonConfig(
                clean_user_data_frame, 12, 12, place=[180, 190],
                button_text="Clean User Data", border=2,
                command=lambda: edit(
                    local_storage_variable_1.get(), local_storage_variable_1,
                    'clean'
                )
            )

        def change_user_profile():
            global clone_change_user_profile_frame

            def change_state(*args, **kwargs):
                for var in args:
                    var.set(0)

                if list(kwargs.keys()).count('activate'):

                    for var in kwargs['activate']:
                        var.set(1)

            def change_guest_to_standard(
                path, user_type, user_name
            ):
                with open(
                    f'{path}{user_type}{user_name}'
                    '_folder\\user_credential.json'
                ) as file:
                    credential = json.load(file)

                credential[de.PROFILE] = de.convert_orignal_data_to_hashes(
                    'standard'
                )

                with open(
                    f'{path}{user_type}{user_name}'
                    '_folder\\user_credential.json', 'w'
                ) as file:
                    json.dump(credential, file)

                messagebox.showinfo(
                    title='SQL Lab - Message Box',
                    message=(
                        'User Profile Changed '
                        'Successfully'
                    )
                )

            def change_guest_to_anonymous(
                path_1, user_name
            ):
                try:

                    with open(
                        f'{path_1}anonymous_user_names.json'
                    ) as file:
                        anonymous_user_names = json.load(
                            file
                        )[de.USER_NAME]

                except json.decoder.JSONDecodeError:
                    anonymous_user_names = []

                if not anonymous_user_names.count(
                    user_name
                ):
                    no_of_db = len(
                        os.listdir(
                            f'{path_2}{user_name}_database_folder'
                        )
                    )

                    if no_of_db < 3:

                        with open(
                            f'{path_1}{user_name}_folder\\'
                            'user_credential.json'
                        ) as file:
                            credentials = json.load(file)

                        credentials[de.PROFILE] = (
                            de.convert_orignal_data_to_hashes(
                                'anonymous'
                            )
                        )
                        credentials.pop(de.DATE)
                        credentials.pop(de.TIME)

                        with open(
                            f'{path_1}{user_name}_folder\\'
                            'user_credential.json', 'w'
                        ) as file:
                            json.dump(credentials, file)

                        with open(
                            f'{path_1}user_names.json'
                        ) as file:
                            names = json.load(file)
                            names[de.USER_NAME].remove(user_name)

                        with open(
                            f'{path_1}user_names.json', 'w'
                        ) as file:
                            json.dump(names, file)

                        try:

                            with open(
                                f'{path_1}anonymous_user_names.json'
                            ) as file:
                                names = json.load(file)
                                names[de.USER_NAME].append(user_name)

                        except json.decoder.JSONDecodeError:
                            names = {}
                            names[de.USER_NAME] = [user_name]

                        with open(
                            f'{path_1}anonymous_user_names.json', 'w'
                        ) as file:
                            json.dump(names, file)

                        os.rename(
                            f'{path_1}\\{user_name}_folder',
                            f'{path_1}\\anonymous_{user_name}_folder'
                        )

                        os.rename(
                            f'{path_2}\\{user_name}_database_folder',
                            f'{path_2}\\anonymous_{user_name}_database_folder'
                        )

                        messagebox.showinfo(
                            title='SQL Lab - Message Box',
                            message=(
                                'User Profile Changed '
                                'Successfully'
                            )
                        )
                    else:
                        message = (
                            "Can't convert user profile because this guest "
                            "account contains more than 2 databases."
                        )

                        messagebox.showwarning(
                            title='SQL Lab - Message Box', message=message
                        )

                else:
                    messagebox.showwarning(
                        title='SQL Lab - Message Box',
                        message=(
                            "Can't convert user profile due to some security "
                            "measures."
                        )
                    )

            def change_anonymous_to_standard(
                path_1, anonymous_user_name
            ):
                try:

                    with open(
                        f'{path_1}user_names.json'
                    ) as file:
                        user_names = json.load(
                            file
                        )[de.USER_NAME]

                except json.decoder.JSONDecodeError:
                    user_names = []

                if not user_names.count(
                    anonymous_user_name
                ):
                    with open(
                        f'{path_1}anonymous_{anonymous_user_name}'
                        '_folder\\user_credential.json'
                    ) as file:
                        credentials = json.load(file)

                    credentials[de.PROFILE] = (
                        de.convert_orignal_data_to_hashes(
                            'standard'
                        )
                    )
                    credentials[de.DATE] = (
                        str(datetime.today()).split()[0]
                    )
                    credentials[de.TIME] = (
                        datetime.now().strftime("%H:%M:%S")
                    )

                    with open(
                        f'{path_1}anonymous_{anonymous_user_name}'
                        '_folder\\user_credential.json', 'w'
                    ) as file:
                        json.dump(credentials, file)

                    with open(
                        f'{path_1}anonymous_user_names.json'
                    ) as file:
                        names = json.load(file)
                        names[de.USER_NAME].remove(anonymous_user_name)

                    with open(
                        f'{path_1}anonymous_user_names.json', 'w'
                    ) as file:
                        json.dump(names, file)

                    try:

                        with open(
                            f'{path_1}user_names.json'
                        ) as file:
                            names = json.load(file)
                            names[de.USER_NAME].append(anonymous_user_name)

                    except json.decoder.JSONDecodeError:
                        names = {}
                        names[de.USER_NAME] = [anonymous_user_name]

                    with open(
                        f'{path_1}user_names.json', 'w'
                    ) as file:
                        json.dump(names, file)

                    os.rename(
                        f'{path_1}\\anonymous_{anonymous_user_name}_folder',
                        f'{path_1}\\{anonymous_user_name}_folder'
                    )

                    os.rename(
                        f'{path_2}\\anonymous_{anonymous_user_name}'
                        '_database_folder',
                        f'{path_2}\\{anonymous_user_name}_database_folder'
                    )

                    messagebox.showinfo(
                        title='SQL Lab - Message Box',
                        message=(
                            'User Profile Changed '
                            'Successfully'
                        )
                    )
                else:
                    messagebox.showwarning(
                        title='SQL Lab - Message Box',
                        message=(
                            "Can't convert user profile due to some security "
                            "measures."
                        )
                    )

            def change_profile(
                user_name, password, p1, p2, p3, p4
            ):
                all_entries_fill = [
                    user_name != '', password != '',
                    p1 == 1 or p2 == 1,
                    p3 == 1 or p4 == 1
                ]

                if all(all_entries_fill):

                    user_name = user_name.replace(' ', '')

                    if not punctuation_checker(user_name):

                        user_name = (
                            de.convert_orignal_data_to_modifide_data(
                                user_name
                            )
                        )

                        if p1:
                            user_type = ''
                        elif p2:
                            user_type = 'anonymous_'

                        try:

                            with open(
                                f'{path_1}{user_type}user_names.json'
                            ) as file:
                                user_names = json.load(file)[de.USER_NAME]

                        except json.decoder.JSONDecodeError:
                            user_names = []

                        if user_names.count(user_name):

                            with open(
                                f'{path_1}{user_type}{user_name}_folder\\'
                                'user_credential.json'
                            ) as file:
                                data = json.load(file)
                                user_profile = (
                                    de.convert_hashes_to_orignal_data(
                                        data[de.PROFILE]
                                    )
                                )
                                password_ = (
                                    de.convert_hashes_to_orignal_data(
                                        data[de.PASSWORD]
                                    )
                                )

                            if p1 == 1:

                                if user_profile == 'guest':
                                    user_correct = True
                                else:
                                    messagebox.showwarning(
                                        title='SQL Lab - Message Box',
                                        message=(
                                            'The entered user name not exists'
                                            '.'
                                        )
                                    )
                                    user_correct = False

                            else:
                                user_correct = True

                            if user_correct:

                                if password == password_:
                                    password_correct = True
                                else:
                                    messagebox.showwarning(
                                        title='SQL Lab - Message Box',
                                        message=(
                                            "The entered password "
                                            "didn't match."
                                        )
                                    )
                                    password_correct = False

                            else:
                                password_correct = False

                            if password_correct:
                                ask_to_change = messagebox.askyesno(
                                    title='SQL Lab - Message Box',
                                    message=(
                                        'You really want to change '
                                        'user profile?'
                                    )
                                )

                                if p1 == 1 and p3 == 1 and ask_to_change:
                                    change_guest_to_standard(
                                        path_1, user_type, user_name
                                    )
                                elif p1 == 1 and p4 == 1 and ask_to_change:
                                    change_guest_to_anonymous(
                                        path_1, user_name
                                    )
                                elif p2 == 1 and p3 == 1 and ask_to_change:
                                    change_anonymous_to_standard(
                                        path_1, user_name
                                    )
                                elif ask_to_change:
                                    messagebox.showinfo(
                                        title='SQL Lab - Message Box',
                                        message=(
                                            'User Profile Changing Process '
                                            'Terminated.'
                                        )
                                    )

                                local_storage_variable_1.set(
                                    "Enter the user name here ..."
                                )

                                local_storage_variable_2.set(
                                    "Enter password here ..."
                                )

                                change_state(
                                    local_storage_variable_3,
                                    local_storage_variable_4,
                                    local_storage_variable_5,
                                    local_storage_variable_6
                                )

                        else:
                            messagebox.showwarning(
                                title='SQL Lab - Message Box',
                                message=(
                                    'The entered user name not exists.'
                                )
                            )

                    else:
                        messagebox.showwarning(
                            title='SQL Lab - Message Box',
                            message=(
                                'The entered user name not exists.'
                            )
                        )

                else:
                    messagebox.showwarning(
                        title='SQL Lab - Message Box',
                        message=(
                            'Please, fill all entries.'
                        )
                    )

            inner_frame_destroyer()

            frame_width = 500
            frame_height = 450

            local_storage_variable_1 = StringVar()
            local_storage_variable_2 = StringVar()
            local_storage_variable_3 = IntVar()
            local_storage_variable_4 = IntVar()
            local_storage_variable_5 = IntVar()
            local_storage_variable_6 = IntVar()

            change_user_profile_frame = Frame(
                user_manager_frame, background=COLOUR_COLLECTION["Colour 00"],
                highlightbackground=COLOUR_COLLECTION["Colour 05"],
                highlightthickness=1
            )
            change_user_profile_frame.place(
                x=(
                    app_width/5 + ((app_width -
                                    (app_width/5))/2 - (frame_width/2))
                ),
                y=((app_heigth - (app_heigth/15))/2 - (frame_height/2)),
                width=frame_width, height=frame_height
            )

            clone_change_user_profile_frame = change_user_profile_frame

            icon = LabelConfig(
                change_user_profile_frame, 105, 20, 30, '🔀'
            )

            heading = LabelConfig(
                change_user_profile_frame, 150, 30, 20, 'Change User Profile',
                font_style='underline'
            )

            user_name_ = LabelConfig(
                change_user_profile_frame, 30, 100, 20, "User Name"
            )

            user_icon = LabelConfig(
                change_user_profile_frame, 60, 135, 20, "👤"
            )

            user_name_entry = EntryConfig(
                change_user_profile_frame, 95, 135,
                local_storage_variable_1, 32
            )
            local_storage_variable_1.set("Enter the user name here ...")

            password = LabelConfig(
                change_user_profile_frame, 30, 170, 20, "Password"
            )

            password_icon = LabelConfig(
                change_user_profile_frame, 60, 205, 20, "🔑"
            )

            password_entry = EntryConfig(
                change_user_profile_frame, 95, 205,
                local_storage_variable_2, 32, hide_and_show_text=True,
                hide_and_show_btn_config=[460, 195]
            )
            local_storage_variable_2.set("Enter password here ...")

            old_profile = LabelConfig(
                change_user_profile_frame, 30, 240, 20, "Old Profile"
            )

            old_profile_icon = LabelConfig(
                change_user_profile_frame, 60, 275, 20, "🔐"
            )

            guest = Checkbutton(
                change_user_profile_frame, text='Guest',
                background=COLOUR_COLLECTION["Colour 00"],
                font=(FONT_COLLECTION["Font 2 --> Times New Roman"], 15),
                activebackground=COLOUR_COLLECTION["Colour 00"],
                variable=local_storage_variable_3, cursor='hand2',
                command=lambda: change_state(local_storage_variable_4),
            )
            guest.place(x=130, y=277)

            anonymous = Checkbutton(
                change_user_profile_frame, text='Anonymous',
                background=COLOUR_COLLECTION["Colour 00"],
                font=(FONT_COLLECTION["Font 2 --> Times New Roman"], 15),
                activebackground=COLOUR_COLLECTION["Colour 00"],
                variable=local_storage_variable_4, cursor='hand2',
                command=lambda: change_state(
                    local_storage_variable_3, local_storage_variable_6,
                    activate=[local_storage_variable_5]
                )
            )
            anonymous.place(x=250, y=277)

            new_profile = LabelConfig(
                change_user_profile_frame, 30, 310, 20, "New Profile"
            )

            new_profile_icon = LabelConfig(
                change_user_profile_frame, 60, 345, 20, "🔐"
            )

            standard = Checkbutton(
                change_user_profile_frame, text='Standard',
                background=COLOUR_COLLECTION["Colour 00"],
                font=(FONT_COLLECTION["Font 2 --> Times New Roman"], 15),
                activebackground=COLOUR_COLLECTION["Colour 00"],
                variable=local_storage_variable_5, cursor='hand2',
                command=lambda: change_state(local_storage_variable_6),
            )
            standard.place(x=130, y=347)

            anonymous = Checkbutton(
                change_user_profile_frame, text='Anonymous',
                background=COLOUR_COLLECTION["Colour 00"],
                font=(FONT_COLLECTION["Font 2 --> Times New Roman"], 15),
                activebackground=COLOUR_COLLECTION["Colour 00"],
                variable=local_storage_variable_6, cursor='hand2',
                command=lambda: change_state(
                    local_storage_variable_4, local_storage_variable_5,
                    activate=[local_storage_variable_3]
                )
            )
            anonymous.place(x=250, y=347)

            clean_data_btn = ButtonConfig(
                change_user_profile_frame, 12, 12, place=[180, 390],
                button_text="Clean User Data", border=2,
                command=lambda: change_profile(
                    local_storage_variable_1.get(),
                    local_storage_variable_2.get(),
                    local_storage_variable_3.get(),
                    local_storage_variable_4.get(),
                    local_storage_variable_5.get(),
                    local_storage_variable_6.get()
                )
            )

        def inner_frame_destroyer():
            frame_destroyer(
                clone_change_pass_frame,
                clone_delete_user_frame,
                clone_clean_user_data_frame,
                clone_change_user_profile_frame
            )

        local_frames_destroyer()

        user_manager_frame = Frame(
            root, background=COLOUR_COLLECTION["Colour 00"]
        )
        user_manager_frame.place(
            x=0, y=app_heigth/15,
            width=app_width, height=app_heigth*(14/15)
        )

        clone_user_manager_frame = user_manager_frame

        option_frame_of_user_manager = Frame(
            user_manager_frame, background=COLOUR_COLLECTION["Colour 00"],
            highlightbackground=COLOUR_COLLECTION["Colour 05"],
            highlightthickness=1
        )
        option_frame_of_user_manager.place(
            x=0, y=0, width=app_width/5, height=app_heigth*(14/15)
        )

        OPTIONS_LIST = [
            "  🔑 Change User Password", "  🗳 Delete User",
            "  🗞 Clean User Data", "  🔀 Change User Profile"
        ]

        COMMAND_FOR_OPTION_BTN = {
            "  🔑 Change User Password": change_user_pass,
            "  🗳 Delete User": delete_user,
            "  🗞 Clean User Data": clean_user_data,
            "  🔀 Change User Profile": change_user_profile,
        }

        i = 0

        while(
            i < len(OPTIONS_LIST)
        ):
            if i == 0:
                state = "active"
            else:
                state = "deactive"

            options = ButtonConfig(
                option_frame_of_user_manager, 16, 1, 2, pack=['x', TOP],
                button_text=f"{OPTIONS_LIST[i]}", bg_less_btn=[True, True],
                aling="w", padding=[1, 2], on_click_state=state,
                command=COMMAND_FOR_OPTION_BTN[OPTIONS_LIST[i]],
                on_click_bg_change=True,
            )
            i += 1

        change_user_pass()

    def resource_monitor():
        global clone_resource_monitor_frame

        local_frames_destroyer()

        resource_monitor_frame = Frame(
            root, background=COLOUR_COLLECTION["Colour 00"]
        )
        resource_monitor_frame.place(
            x=0, y=app_heigth/15,
            width=app_width, height=app_heigth*(14/15)
        )

        clone_resource_monitor_frame = resource_monitor_frame

        box_1 = Frame(
            resource_monitor_frame, background=COLOUR_COLLECTION["Colour 00"]
        )
        box_1.place(
            x=0, y=0, width=app_width/2, height=app_heigth*(14/15)
        )

        box_2 = Frame(
            resource_monitor_frame, background=COLOUR_COLLECTION["Colour 00"]
        )
        box_2.place(
            x=app_width/2, y=0, width=app_width/2,
            height=app_heigth*(14/15)
        )

        plt.style.use("seaborn-bright")

        users = [
            user for user in os.listdir(path_2)
            if not user.startswith('anonymous_')
        ]
        data = []

        for user in users:
            data_consume = 0

            for file in os.listdir(f'{path_2}{user}'):
                data_consume += int(
                    os.path.getsize(f'{path_2}{user}\\{file}')/1000
                )

            data.append(
                [
                    de.convert_modifide_data_to_orignal_data(
                        user.split('_database_folder')[0]
                    ),
                    data_consume
                ]
            )

        lables = [value[0] for value in data]
        values = [value[1] for value in data]

        if sum(values) == 0:
            values = [100/len(lables) for i in lables]

        figure_1 = plt.Figure(
            figsize=(1, 1), dpi=100, facecolor=COLOUR_COLLECTION["Colour 00"]
        )
        graph_1 = figure_1.add_subplot(111)
        graph_1.pie(
            values, labels=lables, startangle=90, autopct='%1.1f%%'
        )
        graph_1.set_title('Storage Use By Users')
        bar1 = FigureCanvasTkAgg(figure_1, box_1)
        bar1.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True)

        memory = [value[1] for value in data]
        memory.sort(reverse=True)
        memory = memory[:5]

        user_names = []
        storage_use = []

        while(
            len(memory)
        ):
            for user_name, user_size in data:

                if user_size == memory[0]:
                    user_names.append(user_name.capitalize())
                    storage_use.append(user_size)
                    data.pop(data.index([user_name, user_size]))
                    memory.pop(0)
                    break

        user_names.reverse(), storage_use.reverse()

        figure_2 = plt.Figure(
            figsize=(1, 1), dpi=100, facecolor=COLOUR_COLLECTION["Colour 00"]
        )
        graph_2 = figure_2.add_subplot(111)

        graph_2.plot(
            user_names, storage_use, color='#DDA0DD', linewidth=2
        )
        graph_2.set_title('Users Vs Memory Consumption {Kb}')
        bar1 = FigureCanvasTkAgg(figure_2, box_2)
        bar1.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

        data = [
            [
                de.convert_modifide_data_to_orignal_data(
                    user.split('_database_folder')[0]
                ),
                len(os.listdir(f'{path_2}{user}'))
            ]
            for user in os.listdir(path_2)
            if not user.startswith('anonymous_')
        ]

        no_of_db = [value[1] for value in data]
        no_of_db.sort(reverse=True)
        no_of_db = no_of_db[:5]

        user_names = []
        number_of_db = []

        while(
            len(no_of_db)
        ):
            for user_name, db_no in data:
                if db_no == no_of_db[0]:
                    user_names.append(user_name.capitalize())
                    number_of_db.append(db_no)
                    data.pop(data.index([user_name, db_no]))
                    no_of_db.pop(0)
                    break

        output_user_names = []
        output_number_of_db = []

        while(
            len(user_names)
        ):
            choice = random.choice(user_names)
            output_user_names.append(choice)
            output_number_of_db.append(number_of_db[user_names.index(choice)])
            number_of_db.pop(user_names.index(choice))
            user_names.pop(user_names.index(choice))

        figure_3 = plt.Figure(
            figsize=(1, 1), dpi=100, facecolor=COLOUR_COLLECTION["Colour 00"]
        )
        graph_3 = figure_3.add_subplot(111)

        graph_3.bar(
            output_user_names, output_number_of_db, color='#FFA07A'
        )
        graph_3.set_title('Users Vs Number of Databases')
        bar1 = FigureCanvasTkAgg(figure_3, box_2)
        bar1.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    def logout():
        ask_to_logout = messagebox.askyesno(
            title='SQL Lab - Message Box',
            message=(
                f'You want to logout from admin panel?'
            )
        )

        if ask_to_logout:
            desktop_window()
        else:
            pass

    def admin_details():

        def change_admin_pass(new_pass):
            ask_to_change = messagebox.askyesno(
                title='SQL Lab - Message Box',
                message=(
                    'You want to change admin password?'
                )
            )

            if ask_to_change:
                with open(
                    f'{path_3}admin_credential.json'
                ) as file:
                    credential = json.load(file)

                credential[de.PASSWORD] = de.convert_orignal_data_to_hashes(
                    new_pass
                )

                with open(
                    f'{path_3}admin_credential.json', 'w'
                ) as file:
                    json.dump(credential, file)

                messagebox.showinfo(
                    title='SQL Lab - Message Box',
                    message=(
                        'Admin password change successfully.'
                    )
                )
                admin_details.destroy()

            else:
                messagebox.showinfo(
                    title='SQL Lab - Message Box',
                    message=(
                        'Task terminated.'
                    )
                )
                admin_details.destroy()

        with open(f'{path_3}admin_credential.json') as file:
            credentials = json.load(file)

        data = [
            [
                'User name',
                de.convert_hashes_to_orignal_data(
                    credentials[de.USER_NAME]
                ).capitalize()
            ],
            [
                'Password',
                de.convert_hashes_to_orignal_data(
                    credentials[de.PASSWORD]
                )
            ],
            [
                'Profile',
                de.convert_hashes_to_orignal_data(
                    credentials[de.PROFILE]
                )
            ],
            [
                'Date of account creation',
                de.convert_hashes_to_orignal_data(
                    credentials[de.DATE]
                )
            ],
            [
                'Time of account creation',
                de.convert_hashes_to_orignal_data(
                    credentials[de.TIME]
                )
            ]
        ]

        admin_details = Toplevel(
            root, background=COLOUR_COLLECTION["Colour 00"]
        )

        top_level_windows.append(admin_details)

        app_width = 500
        app_heigth = 200
        local_storage_variable_1 = StringVar()

        admin_details.title("SQL Lab - Admin Details")
        admin_details.resizable(0, 0)
        admin_details.geometry(
            f"{int(app_width)}x{int(app_heigth)}+"
            f"{int((screen_width - app_width)/2)}+"
            f"{int((screen_height - app_heigth)/5)}"
        )
        admin_details.iconbitmap("Resources\\Images\\sqllablogo.ico")

        admin_details_frame = Frame(
            admin_details, background=COLOUR_COLLECTION["Colour 00"]
        )
        admin_details_frame.place(
            x=0, y=0, width=500, height=140
        )

        admin_details_tree = ttk.Treeview(
            admin_details_frame, columns=["c1", "c2"], show="headings"
        )

        admin_details_tree.heading("c1", text="Detail name")
        admin_details_tree.heading("c2", text="Description")

        admin_details_tree.column("c1", anchor=W)
        admin_details_tree.column("c2", anchor=W)

        scrollbar1 = Scrollbar(admin_details_frame, orient=HORIZONTAL)
        scrollbar1.pack(side=BOTTOM, fill=BOTH)
        admin_details_tree.config(xscrollcommand=scrollbar1.set)
        scrollbar1.config(command=admin_details_tree.xview)

        admin_details_tree.tag_configure(
            'evenrow', background=COLOUR_COLLECTION["Colour 00"]
        )

        admin_details_tree.tag_configure(
            'oddrow', background=COLOUR_COLLECTION["Colour 03"],
        )

        admin_details_tree.pack(fill=BOTH)

        for index, value in enumerate(data):
            if index % 2 == 0:
                admin_details_tree.insert(
                    "", "end", values=value, tags=('evenrow',)
                )
            else:
                admin_details_tree.insert(
                    "", "end", values=value, tags=('oddrow',)
                )

        password_entry = EntryConfig(
            admin_details, 10, 150, local_storage_variable_1, 30
        )
        local_storage_variable_1.set("Enter new password here ...")

        login_btn = ButtonConfig(
            admin_details, 12, 14, place=[355, 148],
            button_text="🔃 Change Password", border=2,
            command=lambda: change_admin_pass(local_storage_variable_1.get())
        )

    def local_frames_destroyer():
        frame_destroyer(
            clone_user_details_frame, clone_user_manager_frame,
            clone_activity_monitor_frame, clone_resource_monitor_frame
        )

    frame_destroyer(clone_desktop_frame)

    app_width = root.winfo_screenwidth()
    app_heigth = root.winfo_screenheight() - 83

    root.title("SQL Lab - Admin Panel")
    root.resizable(1, 1)
    root.state('zoomed')
    root.geometry(
        f"{int(app_width)}x{int(app_heigth)}+"
        f"{int((screen_width - app_width)/2)}+"
        f"{int((screen_height - app_heigth)/5)}"
    )

    option_bar_frame = Frame(
        root, background=COLOUR_COLLECTION["Colour 02"],
        highlightbackground=COLOUR_COLLECTION["Colour 04"],
        highlightthickness=1
    )
    option_bar_frame.place(
        x=0, y=0,
        width=app_width, height=app_heigth/15
    )

    clone_option_bar_frame = option_bar_frame

    OPTION_NAME = [
        "👤 USERS DETAILS", "🔧 USERS MANAGER", "📺 RESOURCE MONITOR",
        "👑 ADMIN DETAILS", "🔒 LOGOUT"

    ]

    COMMAND_FOR_BTN = {
        "👤 USERS DETAILS": user_details,
        "🔧 USERS MANAGER": user_manager,
        "📺 RESOURCE MONITOR": resource_monitor,
        "👑 ADMIN DETAILS": admin_details,
        "🔒 LOGOUT": logout
    }

    i = 0

    while(
        i < len(OPTION_NAME)
    ):
        on_click_change = True

        if i == 0:
            state = "active"
        else:
            state = "deactive"

        if i == len(OPTION_NAME)-1:
            on_click_change = False

        options = ButtonConfig(
            option_bar_frame, 16, 1, 2, button_text=f"{OPTION_NAME[i]}",
            bg_less_btn=[True, True], aling="center", padding=[1, 2],
            command=COMMAND_FOR_BTN[OPTION_NAME[i]], pack=[BOTH, LEFT, True],
            on_click_bg_change=on_click_change, on_click_state=state,
        )
        i += 1

    user_details()


# ------------------------------ DESKTOP WINDOW ------------------------------

def desktop_window():
    global clone_desktop_frame, login_attempts, resizable

    top_level_window_destroyer()

    frame_destroyer(
        clone_connection_frame, clone_user_panel_login_frame,
        clone_create_user_account_frame, clone_option_frame,
        clone_dashboard_frame, clone_database_frame,
        clone_connections_frame, clone_option_bar_frame,
        clone_user_details_frame, clone_user_manager_frame,
        clone_activity_monitor_frame, clone_resource_monitor_frame,
        clone_explorer_frame, clone_work_area_status_bar_frame,
        clone_work_area_frame, clone_work_area_output_panel,
        clone_status_bar_frame
    )

    for element in ["Create account", 'Admin panel']:
        account_menu.entryconfig(element, state="active")

    app_width = 550
    app_heigth = 330
    login_attempts = 0

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.geometry(
        f"{int(app_width)}x{int(app_heigth)}+"
        f"{int((screen_width - app_width)/2)}"
        f"+{int((screen_height - app_heigth)/5)}"
    )
    root.state("normal")
    root.title("SQL Lab - Desktop")

    if resizable:
        root.resizable(False, False)
    else:
        resizable = True

    desktop_frame = Frame(
        root, background=COLOUR_COLLECTION["Colour 00"]
    )
    desktop_frame.place(
        x=0, y=0,
        width=app_width, height=app_heigth
    )

    clone_desktop_frame = desktop_frame

    software_name = LabelConfig(
        desktop_frame, 130, 20, 50, "SQL LAB",
        font_name=FONT_COLLECTION["Font 1 --> Algerian"],
        font_style="underline"
    )

    login = LabelConfig(
        desktop_frame, 20, 130, 20, "Login to user panel"
    )

    login_btn = ButtonConfig(
        desktop_frame, 24, 12, 2, place=[20, 180],
        button_text="🔐 LOGIN",
        command=lambda: redirect(user_panel_login_window)
    )

    connect = LabelConfig(
        desktop_frame, 280, 130, 20, "Connect with Database"
    )

    connect_btn = ButtonConfig(
        desktop_frame, 24, 12, 2, place=[290, 180],
        button_text="🔗 CONNECT",
        command=lambda: redirect(connection_window)
    )


# ------------------------ CREATE USER ACCOUNT WINDOW ------------------------

def create_user_account_window():
    global clone_create_user_account_frame

    def create_user(user_name, password, profile):
        global current_user_details

        user_name = user_name.lower().replace(' ', '')

        profile = profile.lower().replace(' ', '')

        profile_type_exists = [
            profile == 'standard',
            profile == 'anonymous',
            profile == 'guest'
        ]

        if len(user_name) > 70:
            messagebox.showwarning(
                title='SQL Lab - Message Box',
                message=(
                    'The entered user name cross the '
                    'maximum lenght of 70 words'
                )
            )
        elif punctuation_checker(user_name):
            messagebox.showwarning(
                title='SQL Lab - Message Box',
                message=(
                    'The entered user name contain puntuation marks or'
                    ' special symbol which is not allowed'
                )
            )
        elif not any(profile_type_exists):
            messagebox.showwarning(
                title='SQL Lab - Message Box',
                message=(
                    'The entered profile type not exxists'
                )
            )
        else:
            user_name_list = {}
            user_name = de.convert_orignal_data_to_modifide_data(user_name)

            try:

                if profile != 'anonymous':

                    with open(
                        f"{path_1}user_names.json", 'r'
                    ) as file:
                        user_name_list = json.load(file)

                else:

                    with open(
                        f"{path_1}anonymous_user_names.json", 'r'
                    ) as file:
                        user_name_list = json.load(file)

            except json.decoder.JSONDecodeError:
                user_name_list[de.USER_NAME] = []

            user_name_present = user_name_list[de.USER_NAME].count(user_name)

            if user_name_present:
                messagebox.showwarning(
                    title='SQL Lab - Message Box',
                    message=(
                        'The entered user name already exists'
                    )
                )
            else:
                fbm.create_files_and_folder_of_particular_user_account(
                    user_name, profile
                )

                if profile != 'anonymous':
                    credentials = {
                        de.USER_NAME: user_name,
                        de.PASSWORD:
                        de.convert_orignal_data_to_hashes(password),
                        de.PROFILE:
                        de.convert_orignal_data_to_hashes(profile),
                        de.DATE: str(datetime.today()).split()[0],
                        de.TIME: datetime.now().strftime("%H:%M:%S"),
                    }

                    user_name_list[de.USER_NAME].append(user_name)

                    with open(
                        f"{path_1}user_names.json", 'w'
                    ) as file:
                        json.dump(user_name_list, file)

                else:
                    credentials = {
                        de.USER_NAME: user_name,
                        de.PASSWORD:
                        de.convert_orignal_data_to_hashes(password),
                        de.PROFILE:
                        de.convert_orignal_data_to_hashes(profile),
                    }

                    user_name_list[de.USER_NAME].append(user_name)

                    with open(
                        f"{path_1}anonymous_user_names.json", 'w'
                    ) as file:
                        json.dump(user_name_list, file)

                if profile == 'anonymous':

                    with open(
                        f"{path_1}anonymous_{user_name}_folder\\"
                        "user_credential.json", 'w'
                    ) as file:
                        json.dump(credentials, file)
                else:

                    with open(
                        f"{path_1}{user_name}_folder\\user_credential.json",
                        'w'
                    ) as file:
                        json.dump(credentials, file)

                fbm.create_sub_folders_of_user_folder(profile, user_name)

                orignal_user_name = local_storage_variable_1.get()

                while(
                    orignal_user_name.count('  ')
                ):
                    orignal_user_name = orignal_user_name.replace('  ', ' ')

                orignal_user_name = orignal_user_name.capitalize()

                current_user_details = [
                    user_name, orignal_user_name, profile
                ]

                messagebox.showinfo(
                    title='SQL Lab - Message Box',
                    message=(
                        'Account Created Successfully'
                    )
                )

                clone_create_user_account_frame.destroy()
                add_user_action_info(
                    'Create account.', 'Action completed successfully.'
                )
                upanel_window()

    frame_destroyer(clone_desktop_frame)

    app_width = 550
    app_heigth = 390

    local_storage_variable_1 = StringVar()
    local_storage_variable_2 = StringVar()
    local_storage_variable_3 = StringVar()

    root.title("SQL Lab - Create User Account")
    root.resizable(0, 0)
    root.geometry(
        f"{int(app_width)}x{int(app_heigth)}+"
        f"{int((screen_width - app_width)/2)}+"
        f"{int((screen_height - app_heigth)/5)}"
    )

    create_user_account_frame = Frame(
        root, background=COLOUR_COLLECTION["Colour 00"]
    )
    create_user_account_frame.place(
        x=0, y=0,
        width=app_width, height=app_heigth
    )

    clone_create_user_account_frame = create_user_account_frame

    heading = LabelConfig(
        create_user_account_frame, 50, 20, 30, "CREATE USER ACCOUNT",
        font_name=FONT_COLLECTION["Font 1 --> Algerian"],
        font_style="underline"
    )

    user_name = LabelConfig(
        create_user_account_frame, 40, 100, 20, "User Name"
    )

    user_icon = LabelConfig(
        create_user_account_frame, 70, 135, 20, "👤"
    )

    user_name_entry = EntryConfig(
        create_user_account_frame, 105, 135, local_storage_variable_1, 35
    )
    local_storage_variable_1.set("Enter the user name here ...")

    password = LabelConfig(
        create_user_account_frame, 40, 170, 20, "Password"
    )

    password = LabelConfig(
        create_user_account_frame, 70, 200, 20, "🔑"
    )

    password_entry = EntryConfig(
        create_user_account_frame, 105, 205, local_storage_variable_2, 35,
        hide_and_show_text=True, hide_and_show_btn_config=[500, 195]
    )
    local_storage_variable_2.set("Enter the password here ...")

    profile = LabelConfig(
        create_user_account_frame, 40, 240, 20, "Profile"
    )

    profile_icon = LabelConfig(
        create_user_account_frame, 70, 273, 20, "🔐"
    )

    type_of_account = ttk.Combobox(
        create_user_account_frame, values=TYPE_OF_ACCOUNT,
        textvariable=local_storage_variable_3, width=34,
        font=(FONT_COLLECTION["Font 2 --> Times New Roman"], 17)
    ).place(x=105, y=275)
    local_storage_variable_3.set("Standard")

    connect_btn = ButtonConfig(
        create_user_account_frame, 12, 12, place=[200, 320],
        button_text="Create Account",
        command=lambda: create_user(
            local_storage_variable_1.get(), local_storage_variable_2.get(),
            local_storage_variable_3.get()
        )
    )

    back_btn = ButtonConfig(
        create_user_account_frame, 30, 2, place=[505, -20],
        button_text="🔙", bg_less_btn=[True, False], command=desktop_window
    )


# ------------------------- USER PANEL LOGIN WINDOW --------------------------

def user_panel_login_window():
    global clone_user_panel_login_frame

    def login_process(user_name, password, profile):
        global current_user_details, login_attempts

        user_name = user_name.lower().replace(' ', '')
        profile = profile.lower().replace(' ', '')
        user_name_list = {}

        try:

            if profile != 'anonymous':

                with open(
                    f"{path_1}user_names.json", 'r'
                ) as file:
                    user_name_list = json.load(file)

            else:

                with open(
                    f"{path_1}anonymous_user_names.json", 'r'
                ) as file:
                    user_name_list = json.load(file)

        except json.decoder.JSONDecodeError:
            user_name_list[de.USER_NAME] = []

        profile_type_exists = [
            profile == 'standard',
            profile == 'anonymous',
            profile == 'guest'
        ]

        user_name_present = user_name_list[de.USER_NAME].count(user_name)

        if len(user_name) > 70:
            messagebox.showwarning(
                title='SQL Lab - Message Box',
                message=(
                    'The entered user name cross the '
                    'maximum lenght of 70 words'
                )
            )
        elif punctuation_checker(user_name):
            messagebox.showwarning(
                title='SQL Lab - Message Box',
                message=(
                    'The entered user name contain puntuation marks or'
                    ' special symbol which is not allowed'
                )
            )
        elif not any(profile_type_exists):
            messagebox.showwarning(
                title='SQL Lab - Message Box',
                message=(
                    'The entered profile type not exists'
                )
            )
        else:
            user_name_list = {}
            user_name = de.convert_orignal_data_to_modifide_data(user_name)

            try:

                if profile != 'anonymous':
                    with open(
                        f"{path_1}user_names.json", 'r'
                    ) as file:
                        user_name_list = json.load(file)
                else:
                    with open(
                        f"{path_1}anonymous_user_names.json", 'r'
                    ) as file:
                        user_name_list = json.load(file)

            except json.decoder.JSONDecodeError:
                user_name_list[de.USER_NAME] = []

            user_name_present = user_name_list[de.USER_NAME].count(user_name)

            if user_name_present:
                credentials = {}

                if profile == 'anonymous':

                    with open(
                        f"{path_1}anonymous_{user_name}_folder\\"
                        "user_credential.json", 'r'
                    ) as file:
                        credentials = json.load(file)
                else:

                    with open(
                        f"{path_1}{user_name}_folder\\user_credential.json",
                        'r'
                    ) as file:
                        credentials = json.load(file)

                orignal_user_name = local_storage_variable_1.get()
                password_of_user = credentials[de.PASSWORD]
                user_profile = de.convert_hashes_to_orignal_data(
                    credentials[de.PROFILE]
                ).lower().replace(' ', '')

                while(
                    orignal_user_name.count('  ')
                ):
                    orignal_user_name = orignal_user_name.replace('  ', ' ')

                orignal_user_name = orignal_user_name.capitalize()

                if profile == user_profile:

                    if (
                        de.convert_orignal_data_to_hashes(
                            password
                        ) == password_of_user
                    ):
                        current_user_details = [
                            user_name, orignal_user_name, profile,
                        ]
                        add_user_action_info(
                            'Login to account.',
                            'Action completed successfully.'
                        )
                        upanel_window()
                    else:

                        if login_attempts < 2:
                            messagebox.showwarning(
                                title='SQL Lab - Message Box',
                                message=(
                                    "The entered password didn't match."
                                )
                            )
                        else:
                            messagebox.showwarning(
                                title='SQL Lab - Message Box',
                                message=(
                                    "You cross maximum login attempt limit. "
                                    "You are not an authenticate user.\n"
                                    "Note: Information about unauthenticate "
                                    "attempts of login is send to user."
                                )
                            )
                            login_attempts = -1

                            current_user_details = [
                                user_name, orignal_user_name, profile,
                            ]

                            add_user_action_info(
                                'Login to account.',
                                'Action not completed successfully.'
                            )

                            current_user_details = []

                        login_attempts += 1
                else:
                    messagebox.showwarning(
                        title='SQL Lab - Message Box',
                        message=(
                            "The entered user name didn't exists"
                        )
                    )
            else:
                messagebox.showwarning(
                    title='SQL Lab - Message Box',
                    message=(
                        "The entered user name didn't exists"
                    )
                )

    frame_destroyer(clone_desktop_frame)

    app_width = 550
    app_heigth = 380

    local_storage_variable_1 = StringVar()
    local_storage_variable_2 = StringVar()
    local_storage_variable_3 = StringVar()

    root.title("SQL Lab - User Panel Login")
    root.resizable(0, 0)
    root.geometry(
        f"{int(app_width)}x{int(app_heigth)}+"
        f"{int((screen_width - app_width)/2)}+"
        f"{int((screen_height - app_heigth)/5)}"
    )

    user_panel_login_frame = Frame(
        root, background=COLOUR_COLLECTION["Colour 00"]
    )

    user_panel_login_frame.place(
        x=0, y=0,
        width=app_width, height=app_heigth
    )

    clone_user_panel_login_frame = user_panel_login_frame

    heading = LabelConfig(
        user_panel_login_frame, 105, 20, 30, "LOGIN TO PANEL",
        font_name=FONT_COLLECTION["Font 1 --> Algerian"],
        font_style="underline"
    )

    user_name = LabelConfig(
        user_panel_login_frame, 40, 100, 20, "User Name"
    )

    user_icon = LabelConfig(
        user_panel_login_frame, 70, 135, 20, "👤"
    )

    user_name_entry = EntryConfig(
        user_panel_login_frame, 105, 135, local_storage_variable_1, 35
    )
    local_storage_variable_1.set("Enter the user name here ...")

    password = LabelConfig(
        user_panel_login_frame, 40, 170, 20, "Password"
    )

    password_icon = LabelConfig(
        user_panel_login_frame, 70, 200, 20, "🔑"
    )

    password_entry = EntryConfig(
        user_panel_login_frame, 105, 205, local_storage_variable_2, 35,
        hide_and_show_text=True, hide_and_show_btn_config=[500, 195]
    )
    local_storage_variable_2.set("Enter the password here ...")

    profile_name = LabelConfig(
        user_panel_login_frame, 40, 240, 20, "Profile"
    )

    profile_icon = LabelConfig(
        user_panel_login_frame, 70, 275, 20, "🔐"
    )

    type_of_account = ttk.Combobox(
        user_panel_login_frame, values=TYPE_OF_ACCOUNT,
        textvariable=local_storage_variable_3, width=34,
        font=(FONT_COLLECTION["Font 2 --> Times New Roman"], 17)
    ).place(x=105, y=275)
    local_storage_variable_3.set("Standard")

    login_btn = ButtonConfig(
        user_panel_login_frame, 12, 12, place=[215, 320],
        button_text="🔐 LOGIN", border=2,
        command=lambda: login_process(
            local_storage_variable_1.get(), local_storage_variable_2.get(),
            local_storage_variable_3.get()
        )
    )

    back_btn = ButtonConfig(
        user_panel_login_frame, 30, 2, place=[505, -20],
        button_text="🔙", bg_less_btn=[True, False], command=desktop_window
    )


# ---------------------------- CONNECTION WINDOW -----------------------------

def connection_window():
    global clone_connection_frame

    frame_destroyer(
        clone_desktop_frame, clone_connect_with_db_frame
    )

    app_width = 550
    app_heigth = 300

    root.title("SQL Lab - Connection Window")
    root.resizable(0, 0)
    root.geometry(
        f"{int(app_width)}x{int(app_heigth)}+"
        f"{int((screen_width - app_width)/2)}+"
        f"{int((screen_height - app_heigth)/5)}"
    )

    connection_frame = Frame(
        root, background=COLOUR_COLLECTION["Colour 00"]
    )
    connection_frame.place(
        x=0, y=0,
        width=app_width, height=app_heigth
    )

    clone_connection_frame = connection_frame

    heading = LabelConfig(
        connection_frame, 120, 30, 30, "CONNECT WITH DB",
        font_name=FONT_COLLECTION["Font 1 --> Algerian"],
        font_style="underline"
    )

    local_db = LabelConfig(
        connection_frame, 25, 130, 17, "Connect with local DB"
    )

    local_db_btn = ButtonConfig(
        connection_frame, 24, 12, 2, place=[20, 170],
        button_text="🔗 CONNECT",
        command=lambda: connect_with_db_window('Local db')
    )

    sys_db = LabelConfig(
        connection_frame, 290, 130, 17, "Connect with system DB"
    )

    sys_db_btn = ButtonConfig(
        connection_frame, 24, 12, 2, place=[290, 170],
        button_text="🔗 CONNECT",
        command=lambda: connect_with_db_window('System db')
    )

    back_btn = ButtonConfig(
        connection_frame, 30, 2, place=[505, -20],
        button_text="🔙", bg_less_btn=[True, False], command=desktop_window
    )


# -------------------------- CONNECT WITH DB WINDOW --------------------------

def connect_with_db_window(database_type):
    global clone_connect_with_db_frame, file_path

    def select_file():
        global file_path

        file_path = filedialog.askopenfilename(
            filetypes=[
                ('Sqlite Files', [
                    '*.sqlite', '*.sqlite3', '*sdb', '*db3', '*s3db',
                    '*sl3', '*db2', '*s2db', '*sqlite2', '*sl2'
                ]
                ),
                ('Database Files', '*.db'), ('Sql-lab Files', '*.sqllab'),
            ]
        )

    def connect_with_system_db(
        user, connection_id, password, connection_type
    ):
        global current_connection_details, current_user_details

        if punctuation_checker(user):
            messagebox.showwarning(
                title='SQL Lab - Message Box',
                message=(
                    'The entered user name is invalid.'
                )
            )
        else:
            connection_type = connection_type.lower().replace(' ', '')

            if connection_type == 'anonymous':
                path_of_cre_folder = (
                    f'{path_1}anonymous_'
                    f'{de.convert_orignal_data_to_modifide_data(user)}_folder'
                )
            else:
                path_of_cre_folder = (
                    f'{path_1}'
                    f'{de.convert_orignal_data_to_modifide_data(user)}_folder'
                )

            if (
                os.path.exists(path_of_cre_folder)
                and
                any(
                    [
                        connection_type == 'anonymous',
                        connection_type == 'general'
                    ]
                )
            ):
                try:

                    with open(
                        f'{path_of_cre_folder}\\user_connections.json'
                    ) as file:
                        connection_details = json.load(file)

                    if connection_details[de.ID].count(
                        de.convert_orignal_data_to_hashes(connection_id)
                    ):

                        if connection_details[de.PASSWORD].count(
                            de.convert_orignal_data_to_hashes(password)
                        ):
                            index = connection_details[de.ID].index(
                                de.convert_orignal_data_to_hashes(
                                    connection_id)
                            )

                            current_connection_details = [
                                de.convert_hashes_to_orignal_data(
                                    connection_details[
                                        de.CONNECTION_NAME
                                    ][index]
                                ).capitalize(),
                                de.convert_hashes_to_orignal_data(
                                    connection_details[
                                        de.CONNECTION_TYPE
                                    ][index]
                                ),
                                de.convert_modifide_data_to_orignal_data(
                                    connection_details[de.USER][index]
                                ).capitalize(),
                                de.convert_hashes_to_orignal_data(
                                    connection_details[de.ID][index]
                                ),
                                de.convert_hashes_to_orignal_data(
                                    connection_details[de.SCHEMA][index]
                                ),
                                connection_details[de.USER][index],
                                de.convert_orignal_data_to_modifide_data(
                                    de.convert_hashes_to_orignal_data(
                                        connection_details[de.SCHEMA][index]
                                    )
                                )
                            ]

                            current_user_details = [
                                current_connection_details[5],
                                current_connection_details[2],
                                current_connection_details[1]
                            ]

                            add_user_action_info(
                                'Connect with database by connection "'
                                f'{current_connection_details[0]}".',
                                'Action completed successfully.'
                            )
                            connection_panel_window()
                        else:
                            messagebox.showwarning(
                                title='SQL Lab - Message Box',
                                message=(
                                    'The entered connection'
                                    ' password not match.'
                                )
                            )

                    else:
                        messagebox.showwarning(
                            title='SQL Lab - Message Box',
                            message=(
                                'The entered connection id is invalid.'
                            )
                        )

                except json.decoder.JSONDecodeError:
                    messagebox.showwarning(
                        title='SQL Lab - Message Box',
                        message=(
                            'The entered connection id is invalid.'
                        )
                    )

            elif all(
                [connection_type != 'anonymous', connection_type != 'general']
            ):
                messagebox.showwarning(
                    title='SQL Lab - Message Box',
                    message=(
                        'The entered connection type is invalid.'
                    )
                )
            else:
                messagebox.showwarning(
                    title='SQL Lab - Message Box',
                    message=(
                        'The entered user name is invalid.'
                    )
                )

    def connect_with_local_db(
        connection_name, connection_id
    ):
        global current_connection_details

        conditions = [
            connection_name == "", connection_id == ""
        ]

        if any(conditions):
            messagebox.showwarning(
                title='SQL Lab - Message Box',
                message=(
                    'Please, fill all entries.'
                )
            )
        elif file_path == None or file_path == '':
            messagebox.showwarning(
                title='SQL Lab - Message Box',
                message=(
                    'Please, select schema.'
                )
            )
        else:
            current_connection_details = [
                connection_name, 'Local', getpass.getuser(), connection_id,
                os.path.splitext(os.path.split(file_path)[1])[0], None, None
            ]
            connection_panel_window()

    frame_destroyer(
        clone_connection_frame, clone_connection_with_UACL_frame
    )

    if database_type == 'System db':
        app_heigth = 405
        app_width = 580
    elif database_type == 'Local db':
        app_heigth = 350
        app_width = 560

    local_storage_variable_1 = StringVar()
    local_storage_variable_2 = StringVar()
    local_storage_variable_3 = StringVar()
    local_storage_variable_4 = StringVar()

    root.title(f"SQL Lab - Connect With {database_type}")
    root.resizable(0, 0)
    root.geometry(
        f"{int(app_width)}x{int(app_heigth)}+"
        f"{int((screen_width - app_width)/2)}+"
        f"{int((screen_height - app_heigth)/5)}"
    )

    connect_with_db_frame = Frame(
        root, background=COLOUR_COLLECTION["Colour 00"]
    )
    connect_with_db_frame.place(
        x=0, y=0,
        width=app_width, height=app_heigth
    )

    clone_connect_with_db_frame = connect_with_db_frame

    heading = LabelConfig(
        connect_with_db_frame, 80, 20, 25, f"CONNECT WITH {database_type}",
        font_name=FONT_COLLECTION["Font 1 --> Algerian"],
        font_style="underline"
    )

    if database_type == "Local db":
        file_path = None

        connection_name = LabelConfig(
            connect_with_db_frame, 40, 80, 20, "Connection Name"
        )

        connection_name_icon = LabelConfig(
            connect_with_db_frame, 80, 112, 20, "🔗"
        )

        connection_name_entry = EntryConfig(
            connect_with_db_frame, 115, 115, local_storage_variable_1, 35
        )
    elif database_type == 'System db':
        user_name = LabelConfig(
            connect_with_db_frame, 40, 80, 20, "User Name"
        )

        user_name_icon = LabelConfig(
            connect_with_db_frame, 80, 112, 20, "👤"
        )

        user_name_entry = EntryConfig(
            connect_with_db_frame, 115, 115, local_storage_variable_1, 35
        )

    connection_id = LabelConfig(
        connect_with_db_frame, 40, 150, 20, "Connection ID"
    )

    connection_id_icon = LabelConfig(
        connect_with_db_frame, 80, 182, 20, "🆔"
    )

    connection_id_entry = EntryConfig(
        connect_with_db_frame, 115, 185, local_storage_variable_2, 35
    )

    if database_type == "Local db":
        local_storage_variable_1.set("New Connection")
        local_storage_variable_2.set(id_generator())

        schema = LabelConfig(
            connect_with_db_frame, 40, 220, 20, "Select schema"
        )

        schema_icon = LabelConfig(
            connect_with_db_frame, 80, 252, 20, "🛢"
        )

        schema_button = ButtonConfig(
            connect_with_db_frame, 13, 42, place=[115, 255],
            command=select_file, button_text="Select schema 🛢", border=2
        )

        connect_btn = ButtonConfig(
            connect_with_db_frame, 11, 11, place=[220, 300],
            button_text="🔗 CONNECT", border=2,
            command=lambda: connect_with_local_db(
                local_storage_variable_1.get(), local_storage_variable_2.get()
            )
        )

        place = [515, -20]
    elif database_type == "System db":
        local_storage_variable_1.set("Enter the user name here ...")
        local_storage_variable_2.set("Enter the connection id here ...")

        password = LabelConfig(
            connect_with_db_frame, 40, 220, 20, "Connection Password"
        )

        password_icon = LabelConfig(
            connect_with_db_frame, 80, 252, 20, "🔑"
        )

        password_entry = EntryConfig(
            connect_with_db_frame, 115, 255, local_storage_variable_3, 35,
            hide_and_show_text=True, hide_and_show_btn_config=[510, 247]
        )
        local_storage_variable_3.set("Enter password here ...")

        password = LabelConfig(
            connect_with_db_frame, 40, 290, 20, "Connection Type"
        )

        password_icon = LabelConfig(
            connect_with_db_frame, 80, 322, 20, "🌐"
        )

        type_of_account = ttk.Combobox(
            connect_with_db_frame, values=['General', 'Anonymous'],
            textvariable=local_storage_variable_4, width=34,
            font=(FONT_COLLECTION["Font 2 --> Times New Roman"], 17)
        ).place(x=115, y=325)
        local_storage_variable_4.set("General")

        connect_btn = ButtonConfig(
            connect_with_db_frame, 11, 11, place=[220, 365],
            button_text="🔗 CONNECT", border=2,
            command=lambda: connect_with_system_db(
                local_storage_variable_1.get(),
                local_storage_variable_2.get(),
                local_storage_variable_3.get(),
                local_storage_variable_4.get()
            )
        )

        login_with_uacl_btn = ButtonConfig(
            connect_with_db_frame, 12, 14, place=[445, 375],
            button_text=" Login with 🔗 UACL", bg_less_btn=[True, False],
            command=connect_with_UACL_window
        )

        place = [535, -20]

    back_btn = ButtonConfig(
        connect_with_db_frame, 30, 2, place=place,
        button_text="🔙", bg_less_btn=[True, False],
        command=connection_window
    )


# --------------------- USER PANEL LOGIN WITH UAL WINDOW ---------------------

def connect_with_UACL_window():
    global clone_connection_with_UACL_frame

    def connect():
        global current_user_details

        current_user_details = [
            current_connection_details[5],
            current_connection_details[2],
            current_connection_details[1]
        ]

        add_user_action_info(
            'Connect with database by connection "'
            f'{current_connection_details[0]}" using UACL.',
            'Action completed successfully.'
        )
        connection_panel_window()

    def verify(link):
        global current_connection_details

        link_verified = False
        orignal_link = link
        link = link.strip().split('.')

        if (
            len(link) == 7 and link[0] == 'sqllab' and
            link[1] == 'system' and link[6] == 'uacl'
        ):
            connection_type = de.convert_hashes_to_orignal_data(link[2])
            user_name = de.convert_modifide_data_to_orignal_data(link[3])

            if connection_type == 'Anonymous' or connection_type == 'General':

                if connection_type == 'Anonymous':
                    path_of_cre_folder = (
                        f'{path_1}anonymous_{link[3]}_folder'
                    )
                    username_file = 'anonymous_user_names.json'
                elif connection_type == 'General':
                    path_of_cre_folder = (
                        f'{path_1}{link[3]}_folder'
                    )
                    username_file = 'user_names.json'

                try:

                    with open(
                        f'{path_1}{username_file}'
                    ) as file:
                        user_names = json.load(file)

                except json.decoder.JSONDecodeError:
                    user_names = {de.USER_NAME: []}

                for user_name_ in user_names[de.USER_NAME]:

                    if (
                        de.convert_modifide_data_to_orignal_data(
                            user_name_
                        ) == user_name
                    ):
                        try:

                            with open(
                                f'{path_of_cre_folder}\\'
                                'user_connections.json'
                            ) as file:
                                connection_details = json.load(file)

                        except json.decoder.JSONDecodeError:
                            connection_details = {}

                        if not len(connection_details):
                            messagebox.showwarning(
                                title='SQL Lab - Message Box',
                                message=(
                                    'The entered UACL is invalid.'
                                )
                            )
                        else:
                            _ = de.convert_modifide_data_to_orignal_data
                            __ = de.convert_orignal_data_to_modifide_data

                            for uacls in connection_details[de.UACL]:

                                if (
                                    de.convert_hashes_to_orignal_data(uacls)
                                    == orignal_link
                                ):
                                    index = connection_details[de.UACL].index(
                                        uacls
                                    )
                                    link_verified = True

                                    current_connection_details = [
                                        de.convert_hashes_to_orignal_data(
                                            connection_details[
                                                de.CONNECTION_NAME
                                            ][index]
                                        ).capitalize(),
                                        de.convert_hashes_to_orignal_data(
                                            connection_details[
                                                de.CONNECTION_TYPE
                                            ][index],
                                        ),
                                        _(
                                            connection_details[de.USER][index]
                                        ).capitalize(),
                                        de.convert_hashes_to_orignal_data(
                                            connection_details[de.ID][index]
                                        ),
                                        de.convert_hashes_to_orignal_data(
                                            connection_details[
                                                de.SCHEMA
                                            ][index]
                                        ),
                                        connection_details[de.USER][index],
                                        __(
                                            de.convert_hashes_to_orignal_data(
                                                connection_details[
                                                    de.SCHEMA
                                                ][index],
                                            )
                                        )
                                    ]
                                    break

                            else:
                                messagebox.showwarning(
                                    title='SQL Lab - Message Box',
                                    message=(
                                        'The entered UACL is invalid.'
                                    )
                                )

                        break

                else:
                    messagebox.showwarning(
                        title='SQL Lab - Message Box',
                        message=(
                            'The entered - UACL is invalid.'
                        )
                    )

            else:
                messagebox.showwarning(
                    title='SQL Lab - Message Box',
                    message=(
                        'The entered connection type is invalid.'
                    )
                )

        else:
            messagebox.showwarning(
                title='SQL Lab - Message Box',
                message=(
                    'The entered UACL is invalid.'
                )
            )

        if link_verified:
            widget_list = connection_with_UACL_frame.winfo_children()

            if len(widget_list) == 6:
                connect_btn = ButtonConfig(
                    connection_with_UACL_frame, 15, 25, place=[135, 210],
                    button_text="🔗 Connect", border=2
                )

            connection_with_UACL_frame.winfo_children()[6].config(
                command=connect
            )

    frame_destroyer(clone_connect_with_db_frame)

    app_width = 550
    app_heigth = 350

    local_storage_variable_1 = StringVar()

    root.title("SQL Lab - Connect With UACL")
    root.resizable(0, 0)
    root.geometry(
        f"{int(app_width)}x{int(app_heigth)}+"
        f"{int((screen_width - app_width)/2)}+"
        f"{int((screen_height - app_heigth)/5)}"
    )

    connection_with_UACL_frame = Frame(
        root, background=COLOUR_COLLECTION["Colour 00"]
    )
    connection_with_UACL_frame.place(
        x=0, y=0,
        width=app_width, height=app_heigth
    )

    clone_connection_with_UACL_frame = connection_with_UACL_frame

    heading = LabelConfig(
        connection_with_UACL_frame, 90, 20, 30, "CONNECT WITH UACL",
        font_name=FONT_COLLECTION["Font 1 --> Algerian"],
        font_style="underline",
    )

    uacl = LabelConfig(
        connection_with_UACL_frame, 10, 110, 20,
        "Universally Authenticated Connection Link"
    )

    uacl_icon = LabelConfig(
        connection_with_UACL_frame, 70, 142, 20, "🔗"
    )

    uacl_entry = EntryConfig(
        connection_with_UACL_frame, 105, 145, local_storage_variable_1, 35
    )
    local_storage_variable_1.set("Enter the UACL here ...")

    scearch_btn = ButtonConfig(
        connection_with_UACL_frame, 25, 2, place=[500, 130],
        button_text="🔍", bg_less_btn=[True, False],
        command=lambda: verify(local_storage_variable_1.get())
    )

    back_btn = ButtonConfig(
        connection_with_UACL_frame, 30, 2, place=[505, -20],
        button_text="🔙", bg_less_btn=[True, False],
        command=lambda: connect_with_db_window('System db')
    )


# ------------------------- CONNECTION PANEL WINDOW --------------------------

def connection_panel_window():
    global clone_status_bar_frame, clone_explorer_frame, no_of_query_btn,\
        clone_work_area_status_bar_frame, clone_work_area_frame,\
        clone_work_area_output_panel, list_of_outputs

    def new_query():
        global no_of_query_btn, current_text_area

        def lift_text_area(query_area):
            global current_text_area

            query_area.lift()

            query_area.config(yscrollcommand=scrollbar_for_work_area.set)
            scrollbar_for_work_area.config(command=query_area.yview)

            current_text_area = query_area

        max_no_of_query_btn = int((root.winfo_screenwidth()*(3/4))/100) + 1
        no_of_query_btn += 1

        if max_no_of_query_btn > no_of_query_btn:
            query_area = Text(
                work_area_frame, background=COLOUR_COLLECTION["Colour 00"],
                font=(FONT_COLLECTION["Font 2 --> Times New Roman"], 17)
            )
            query_area.place(
                x=0, y=0, width=(3/4 * (app_width))-18,
                height=(3/4*(app_heigth-((app_heigth/25)*2)))-3
            )
            current_text_area = query_area
            query_area.config(yscrollcommand=scrollbar_for_work_area.set)
            scrollbar_for_work_area.config(command=query_area.yview)

            for widget in work_area_status_bar_frame.winfo_children():
                widget.config(
                    bg=COLOUR_COLLECTION["Colour 00"]
                )

            query_btn = ButtonConfig(
                work_area_status_bar_frame, 11, 12, pack=["y", LEFT],
                button_text="❔ SQL Query", bg_less_btn=[True, True],
                command=lambda: lift_text_area(query_area),
                on_click_bg_change=True, on_click_state="active"
            )
        else:
            messagebox.showinfo(
                title='SQL Lab - Message Box',
                message="Maximum number of query box opened"
            )

    def refresh_connection():

        def add_values_to_tree(value, tree_view):
            tree_view.delete(*tree_view.get_children())

            count = 1

            for element in value:

                if count % 2 != 0:
                    tree_view.insert(
                        "", "end", values=element, tags=('evenrow',)
                    )
                else:
                    tree_view.insert(
                        "", "end", values=element, tags=('oddrow',)
                    )

                count += 1

        if (
            current_connection_details[5] != None
            and
            current_connection_details[6] != None
        ):
            add_values_to_tree(
                wwsdb.fetch_table_info(
                    current_connection_details), table_info_tree
            )

            add_values_to_tree(
                [
                    ['User', current_connection_details[2]],
                    ['Connection name', current_connection_details[0]],
                    ['Connection type', current_connection_details[1]],
                    ['Connection ID', current_connection_details[3]],
                    [
                        'Connected Schema',
                        current_connection_details[4].capitalize()
                    ]
                ], connection_info_tree
            )

            add_values_to_tree(
                wwsdb.fetch_schema_info(current_connection_details),
                schema_info_tree
            )
        else:
            add_values_to_tree(
                wwldb.fetch_table_info(file_path), table_info_tree
            )

            add_values_to_tree(
                [
                    ['User', current_connection_details[2]],
                    ['Connection name', current_connection_details[0]],
                    ['Connection type', current_connection_details[1]],
                    ['Connection ID', current_connection_details[3]],
                    [
                        'Connected Schema',
                        current_connection_details[4].capitalize()
                    ]
                ], connection_info_tree
            )

            add_values_to_tree(
                wwldb.fetch_schema_info(
                    file_path, current_connection_details
                ), schema_info_tree
            )

    def update_output_tree():
        output_tree.delete(*output_tree.get_children())
        count = 0

        for element in list_of_outputs[::-1]:

            if count % 2 == 0:
                output_tree.insert(
                    "", "end", values=[len(list_of_outputs) - count] +
                    element, tags=('evenrow',)
                )
            else:
                output_tree.insert(
                    "", "end", values=[len(list_of_outputs) - count] +
                    element, tags=('oddrow',)
                )

            count += 1

    def query_processor_and_executer():

        try:
            raw_query = current_text_area.selection_get()
        except tkinter.TclError:
            raw_query = current_text_area.get('1.0', END)

        while(
            raw_query.count('  ')
        ):
            raw_query = raw_query.replace('  ', ' ')

        raw_queries = raw_query.strip().split(';')

        queries = [
            f'{raw_query.strip().lower()};'
            for raw_query in raw_queries
            if raw_query != ''
        ]

        for query in queries:
            executable_query = ''
            query = query.replace('"', "'").split('\n')

            for lines in query:
                executable_query += f'{lines} '

            executable_query = executable_query.strip()

            if (
                current_connection_details[5] != None
                and
                current_connection_details[6] != None
            ):
                output = wwsdb.execute_query(
                    executable_query, current_connection_details
                )
            else:
                output = wwldb.execute_query(
                    executable_query, file_path
                )

            list_of_outputs.append(output)

            if output[2] != 'Query executed successfully':
                break

        update_output_tree()

    def create_table_top_level_window():

        def verify_data():
            maximum_no_of_column = (root.winfo_screenheight() - 150)//25
            int_input = local_storage_variable_2.get().isdigit()

            if (
                current_connection_details[5] != None
                and
                current_connection_details[6] != None
            ):
                list_of_table_name = [
                    data[1].lower()
                    for data in wwsdb.fetch_table_info(
                        current_connection_details
                    )
                ]
            else:
                list_of_table_name = [
                    data[1].lower()
                    for data in wwldb.fetch_table_info(file_path)
                ]

            if not int_input:
                messagebox.showwarning(
                    title='SQL Lab - Message Box',
                    message=(
                        'The entered number of column is not a number. '
                        'Please enter only number.'
                    )
                )
            else:
                number_of_column = int(local_storage_variable_2.get())

            if (
                number_of_column > maximum_no_of_column
                and
                int_input
            ):
                messagebox.showwarning(
                    title='SQL Lab - Message Box',
                    message=(
                        'The entered number of column cross miximum limit of '
                        f'{maximum_no_of_column} columns.\n'
                        'Note: Graphically you can create table with only '
                        f'{maximum_no_of_column} columns.'
                    )
                )
            elif local_storage_variable_1.get() == '':
                messagebox.showwarning(
                    title='SQL Lab - Message Box',
                    message=(
                        'The please enter all enteries'
                    )
                )
            elif local_storage_variable_1.get()[0].isdigit():
                messagebox.showwarning(
                    title='SQL Lab - Message Box',
                    message=(
                        'Table name should not start with digit. '
                        'Please enter a valid table name.'
                    )
                )
            elif (
                list_of_table_name.count(
                    local_storage_variable_1.get().replace(' ', '').lower()
                )
            ):
                messagebox.showwarning(
                    title='SQL Lab - Message Box',
                    message=(
                        'The entered table name already exists.'
                    )
                )
            else:
                top_level.destroy()
                create_table_top_level_window_b(
                    number_of_column,
                    local_storage_variable_1.get().replace(' ', '')
                )

        top_level = Toplevel(
            root, background=COLOUR_COLLECTION["Colour 00"]
        )

        top_level_windows.append(top_level)

        app_width = 350
        app_heigth = 115
        local_storage_variable_1 = StringVar()
        local_storage_variable_2 = StringVar()

        top_level.title("SQL Lab - Create Table")
        top_level.resizable(0, 0)
        top_level.geometry(
            f"{int(app_width)}x{int(app_heigth)}+"
            f"{int((screen_width - app_width)/2)}+"
            f"{int((screen_height - app_heigth)/5)}"
        )
        top_level.iconbitmap("Resources\\Images\\sqllablogo.ico")

        icon = LabelConfig(
            top_level, 15, 5, 25, "📅",
            colour=[COLOUR_COLLECTION["Colour 00"],
                    COLOUR_COLLECTION["Colour B1"]
                    ]
        )

        table_name = LabelConfig(
            top_level, 63, 18, 13, "Table Name :"
        )

        table_name_entry = EntryConfig(
            top_level, 170, 18, local_storage_variable_1, 20,
            font_size=12
        )
        local_storage_variable_1.set("table_name")

        no_of_column = LabelConfig(
            top_level, 15, 50, 13, "Number of column :"
        )

        no_of_column_entry = EntryConfig(
            top_level, 170, 50, local_storage_variable_2, 20,
            font_size=12
        )
        local_storage_variable_2.set("5")

        next_btn = ButtonConfig(
            top_level, 12, 7, place=[270, 80],
            button_text="Next ⏩", bg_less_btn=[True, False],
            command=verify_data
        )

    def create_table_top_level_window_b(no_of_column, new_table_name):

        def create_query_for_creating_table():
            error_not_found = False

            for i in range(1, int(no_of_column) + 1):

                if entry_a[f'{i}'].get() == '':
                    messagebox.showwarning(
                        title='SQL Lab - Message Box',
                        message=(
                            f'Please enter column name of column number {i}.'
                        )
                    )
                    break
                elif (
                    combo_a[f'{i}'].get() == ''
                    or
                    combo_a[f'{i}'].get() == "----"
                ):
                    messagebox.showwarning(
                        title='SQL Lab - Message Box',
                        message=(
                            'Please enter column datatype of column number '
                            f'{i}.'
                        )
                    )
                    break
            else:
                error_not_found = True

            primary_key_check_boxes_fetch_data = [
                check_a[f'{i}'].get()
                for i in range(1, int(no_of_column) + 1)
            ]

            if primary_key_check_boxes_fetch_data.count(1) > 1:
                error_not_found = False
                messagebox.showwarning(
                    title='SQL Lab - Message Box',
                    message=(
                        'Only single column can created as primary key.'
                    )
                )

            if error_not_found:

                executable_query = f'create table {new_table_name} ('
                raw_printable_query = f'CREATE TABLE {new_table_name} (\n'

                for i in range(1, int(no_of_column) + 1):
                    primary_key, not_null, unique = "", "", ""

                    if int(check_a[f'{i}'].get()):
                        primary_key = 'primary key'

                    if int(check_b[f'{i}'].get()):
                        not_null = 'not null'

                    if int(check_c[f'{i}'].get()):
                        unique = 'unique'

                    if entry_b[f'{i}'].get() == '':
                        executable_query += (
                            f"{entry_a[f'{i}'].get().replace(' ', '')} "
                            f"{combo_a[f'{i}'].get()}"
                            f" {primary_key} {not_null} {unique}"
                        )
                        raw_printable_query += (
                            f'''
                            {
                                entry_a[f'{i}'].get().replace(
                                ' ', ''
                                ).capitalize()
                            }
                            '''.split()[0] +
                            f"{combo_a[f'{i}'].get().upper()}"
                            f" {primary_key.upper()} {not_null.upper()} "
                            f"{unique.upper()}"
                        )
                    else:

                        if entry_b[f'{i}'].get().isdigit():
                            default = entry_b[f'{i}'].get()
                        else:
                            default = "'" + entry_b[f'{i}'].get() + "'"

                        executable_query += (
                            f"{entry_a[f'{i}'].get()} {combo_a[f'{i}'].get()} "
                            f"{primary_key} {not_null} {unique} "
                            f"default {default}"
                        )
                        raw_printable_query += (
                            f'''
                            {
                                entry_a[f'{i}'].get().replace(
                                    ' ', ''
                                ).capitalize()
                            }
                            '''.split()[0] +
                            f" {combo_a[f'{i}'].get().upper()} "
                            f"{primary_key.upper()} {not_null.upper()} "
                            f"{unique.upper()} "
                            f"DEFAULT {default}"
                        )

                    if i == int(no_of_column):
                        executable_query += ");"
                        raw_printable_query += "\n);"
                    else:
                        executable_query += ", "
                        raw_printable_query += ",\n"

                while(
                    executable_query.count('  ')
                ):
                    executable_query = executable_query.replace('  ', ' ')

                while(
                    executable_query.count(' , ')
                ):
                    executable_query = executable_query.replace(' , ', ', ')

                raw_printable_query = [
                    line
                    for line in raw_printable_query.split('\n')
                ]

                printable_query = ''

                for element in raw_printable_query:
                    real_element = element

                    while(
                        element.count('  ')
                    ):
                        element = element.replace('  ', ' ')

                    if element.endswith(' ,'):
                        element = element.replace(' ,', ',')

                    if (
                        raw_printable_query.index(real_element)
                        ==
                        len(raw_printable_query) - 1
                    ):
                        printable_query += element
                    elif (
                        raw_printable_query.index(real_element)
                        ==
                        len(raw_printable_query) - 2
                    ):
                        printable_query += element + "\n"
                    elif (
                        raw_printable_query.index(real_element)
                        ==
                        len(raw_printable_query) - 3
                    ):
                        printable_query += element + "\n└   "
                    else:
                        printable_query += element + "\n│   "

                ask_to_execute = messagebox.askyesno(
                    title='SQL Lab - Message Box',
                    message=(
                        'You want to execute this table creation query ?\n\n'
                        f'{printable_query}'
                    )
                )

                if ask_to_execute:

                    if (
                        current_connection_details[5] != None
                        and
                        current_connection_details[6] != None
                    ):
                        output = wwsdb.execute_query(
                            executable_query, current_connection_details
                        )
                    else:
                        output = wwldb.execute_query(
                            executable_query, file_path
                        )

                    list_of_outputs.append(output)
                    update_output_tree()
                    top_level.destroy()
                else:
                    messagebox.showinfo(
                        title='SQL Lab - Message Box',
                        message=(
                            'Table creation terminated.'
                        )
                    )
                    top_level.destroy()

        top_level = Toplevel(
            background=COLOUR_COLLECTION["Colour 00"]
        )

        top_level_windows.append(top_level)

        app_width = 650
        app_heigth = 60 + 25*(int(no_of_column) + 1)

        top_level.title("SQL Lab - Create Table")
        top_level.resizable(0, 0)
        top_level.geometry(
            f"{int(app_width)}x{int(app_heigth)}+"
            f"{int((screen_width - app_width)/2)}+"
            f"{int((screen_height - app_heigth)/5)}"
        )
        top_level.iconbitmap("Resources\\Images\\sqllablogo.ico")
        entry_a = {}
        combo_a = {}
        entry_b = {}
        check_a = {}
        check_b = {}
        check_c = {}

        for i in range(1, int(no_of_column) + 1):
            entry_a[f'{i}'] = StringVar()
            entry_a[f'{i}'].set(f"Column_{i}")
            combo_a[f'{i}'] = StringVar()
            combo_a[f'{i}'].set("VARCHAR(255)")
            entry_b[f'{i}'] = StringVar()
            check_a[f'{i}'] = IntVar()
            check_a[f'{i}'].set(0)
            check_b[f'{i}'] = IntVar()
            check_b[f'{i}'].set(0)
            check_c[f'{i}'] = IntVar()
            check_c[f'{i}'].set(0)

        icon = LabelConfig(
            top_level, 5, 5, 25, "📅",
            colour=[COLOUR_COLLECTION["Colour 00"],
                    COLOUR_COLLECTION["Colour B1"]
                    ]
        )

        table_name = LabelConfig(
            top_level, 200, 10, 19, "Column Details Form"
        )

        create_table = ButtonConfig(
            top_level, 15, 10, place=[525, 5],
            button_text="Create Table", bg_less_btn=[True, True],
            command=create_query_for_creating_table
        )

        column_detail_frame = Frame(
            top_level, background=COLOUR_COLLECTION["Colour 00"],
            highlightbackground=COLOUR_COLLECTION["Colour 05"],
            highlightthickness=1
        )
        column_detail_frame.place(
            x=5, y=45,
            width=635, height=25*(int(no_of_column) + 1)
        )

        i = 0

        for title in TITLES_LIST_OF_CREATE_TABLE_FORM:
            title = Label(
                column_detail_frame, text=title,
                background=COLOUR_COLLECTION["Colour 00"],
                font=(FONT_COLLECTION["Font 2 --> Times New Roman"], 10)
            ).grid(row=0, column=i)

            i += 1

        i = 1

        while(
            i < int(no_of_column) + 1
        ):
            column_name = Entry(
                column_detail_frame, bd=2, textvariable=entry_a[f'{i}'],
                font=(FONT_COLLECTION["Font 5 --> Bahnschrift"], 12)
            ).grid(row=i, column=0)

            datatype = ttk.Combobox(
                column_detail_frame, values=DATA_TYPE,
                textvariable=combo_a[f'{i}'],
                font=(FONT_COLLECTION["Font 5 --> Bahnschrift"], 11)
            ).grid(row=i, column=1)

            default_value = Entry(
                column_detail_frame, bd=2, textvariable=entry_b[f'{i}'],
                font=(FONT_COLLECTION["Font 5 --> Bahnschrift"], 12),
            ).grid(row=i, column=2)

            primary_check = Checkbutton(
                column_detail_frame, bd=1, cursor="hand2",
                background=COLOUR_COLLECTION["Colour 00"],
                activebackground=COLOUR_COLLECTION["Colour 00"],
                variable=check_a[f"{i}"]
            ).grid(row=i, column=3)

            unique_check = Checkbutton(
                column_detail_frame, bd=1, cursor="hand2",
                background=COLOUR_COLLECTION["Colour 00"],
                activebackground=COLOUR_COLLECTION["Colour 00"],
                variable=check_b[f"{i}"]
            ).grid(row=i, column=4)

            not_null_check = Checkbutton(
                column_detail_frame, bd=1, cursor="hand2",
                background=COLOUR_COLLECTION["Colour 00"],
                activebackground=COLOUR_COLLECTION["Colour 00"],
                variable=check_c[f"{i}"]
            ).grid(row=i, column=5)

            i += 1

    def open_sql_script():
        file_path = filedialog.askopenfilename(
            filetypes=[
                ('sql file', '*.sql')
            ]
        )

        data = ''
        if file_path != '':

            with open(file_path) as sql_script:

                for element in current_text_area.get('1.0', END).split("\n"):
                    data += element

                if data == '':
                    current_text_area.insert('1.0', sql_script.read())
                else:
                    add_data_in_current_text_area = messagebox.askyesno(
                        title='SQL Lab - Message Box',
                        message=(
                            'You want to open this sql query in current text '
                            'area.\nNote: All text removed from current text '
                            'area.'
                        )
                    )

                    if add_data_in_current_text_area:
                        current_text_area.delete('1.0', END)
                        current_text_area.insert('1.0', sql_script.read())
                    else:
                        new_query()
                        current_text_area.insert('1.0', sql_script.read())

    def save_sql_script():
        file_path = filedialog.asksaveasfile(
            initialfile='Sql_query.sql',
            defaultextension='.sql', mode='w',
            filetypes=[
                ('sql file', '*.sql')
            ]
        )

        if file_path != None:
            file_path.write(current_text_area.get('1.0', END))

            messagebox.showinfo(
                title='SQL Lab - Message Box',
                message=(
                    'File save successfully.'
                )
            )

    def close_connection():
        global current_user_details, current_connection_details

        ask_to_close_connection = messagebox.askyesno(
            title='SQL Lab - Message Box',
            message=(
                f'You want to close this connection?'
            )
        )

        if ask_to_close_connection:
            if (
                current_connection_details[5] != None
                and
                current_connection_details[6] != None
            ):
                add_user_action_info(
                    'Disconnect connection '
                    f'"{current_connection_details[0]}".',
                    'Action completed successfully.'
                )

            current_user_details = []
            current_connection_details = [
                None, None, None, None, None, None, None
            ]
            keys = ['Control-r', 'F5', 'Control-t', 'Control-n', 'Control-q']

            for key in keys:
                root.unbind(f'<{key}>')

            spu.top_level_window_destroyer()
            desktop_window()
        else:
            pass

    frame_destroyer(
        clone_connection_with_UACL_frame, clone_connect_with_db_frame
    )

    app_width = root.winfo_screenwidth()
    app_heigth = root.winfo_screenheight() - 83
    no_of_query_btn = 0

    root.title("SQL Lab - Connection Panel")
    root.resizable(1, 1)
    root.state('zoomed')
    root.geometry(
        f"{int(app_width)}x{int(app_heigth)}+"
        f"{int((screen_width - app_width)/2)}+"
        f"{int((screen_height - app_heigth)/5)}"
    )
    root.bind('<Control-r>', lambda event: refresh_connection())
    root.bind('<F5>', lambda event: query_processor_and_executer())
    root.bind('<Control-t>', lambda event: create_table_top_level_window())
    root.bind('<Control-n>', lambda event: new_query())
    root.bind('<Control-q>', lambda event: close_connection())

    list_of_outputs = []

    # ------------------------------ STATUS BAR ------------------------------

    status_bar_frame = Frame(
        root, background=COLOUR_COLLECTION["Colour 00"],
        highlightbackground="black", highlightthickness=1
    )
    status_bar_frame.place(
        x=0, y=0,
        width=app_width, height=app_heigth/24
    )

    clone_status_bar_frame = status_bar_frame

    new_query_btn = ButtonConfig(
        status_bar_frame, 11, 13, pack=["y", LEFT], command=new_query,
        button_text="❔ New Query", bg_less_btn=[True, True]
    )

    open_sql_script_btn = ButtonConfig(
        status_bar_frame, 11, 16, pack=["y", LEFT],
        button_text="📋 Save SQL Script", bg_less_btn=[True, True],
        command=save_sql_script
    )

    open_sql_script_btn = ButtonConfig(
        status_bar_frame, 11, 16, pack=["y", LEFT],
        button_text="📖 Open SQL Script", bg_less_btn=[True, True],
        command=open_sql_script
    )

    refresh_connection_btn = ButtonConfig(
        status_bar_frame, 11, 18, pack=["y", LEFT],
        button_text="🔃 Refresh Connection", bg_less_btn=[True, True],
        command=refresh_connection
    )

    create_table_btn = ButtonConfig(
        status_bar_frame, 11, 13, 8, pack=["y", LEFT],
        button_text="📅 Create Table", bg_less_btn=[True, True],
        command=create_table_top_level_window
    )

    execut_query_btn = ButtonConfig(
        status_bar_frame, 11, 15, pack=["y", LEFT],
        button_text="▶ Execute Query", bg_less_btn=[True, True],
        command=query_processor_and_executer
    )

    close_connection_btn = ButtonConfig(
        status_bar_frame, 11, 17, pack=["y", LEFT],
        button_text="❌ Close Connection", bg_less_btn=[True, True],
        command=close_connection
    )

    # ------------------------------- EXPLORER -------------------------------

    explorer_frame = Frame(
        root, background=COLOUR_COLLECTION["Colour 00"],
        highlightbackground="black", highlightthickness=1
    )
    explorer_frame.place(
        x=0, y=app_heigth/25,
        width=app_width/4, height=app_heigth - (app_heigth / 25)
    )

    clone_explorer_frame = explorer_frame

    table_detail_frame = Frame(
        explorer_frame, background=COLOUR_COLLECTION["Colour 00"],
        highlightbackground="black", highlightthickness=1
    )
    table_detail_frame.place(
        x=10, y=30,
        width=app_width/4 - 20, height=(app_heigth - (app_heigth / 25))/2.3
    )

    table = LabelConfig(
        explorer_frame, 5, 0, 15, "TABLE DETAIL"
    )

    table_info_tree = ttk.Treeview(
        table_detail_frame, columns=["c1", "c2", "c3"],
        show="headings", height=13
    )

    table_info_tree.column("c1", anchor=CENTER, width=10)
    table_info_tree.column("c2", anchor=W, width=60)
    table_info_tree.column("c3", anchor=W, width=30)

    table_info_tree.heading("c1", text="#")
    table_info_tree.heading("c2", text="Table Name")
    table_info_tree.heading("c3", text="No. of Column")

    scrollbar = Scrollbar(table_detail_frame)
    scrollbar.pack(side=RIGHT, fill=BOTH)
    table_info_tree.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=table_info_tree.yview)

    scrollbar1 = Scrollbar(table_detail_frame, orient=HORIZONTAL)
    scrollbar1.pack(side=BOTTOM, fill=BOTH)
    table_info_tree.config(xscrollcommand=scrollbar1.set)
    scrollbar1.config(command=table_info_tree.xview)

    table_info_tree.pack(fill=BOTH)

    connection = LabelConfig(
        explorer_frame, 5, (app_heigth - (app_heigth / 25))/2 - 10,
        15, "CONNECTION DETAIL"
    )

    connection_detail_frame = Frame(
        explorer_frame, background=COLOUR_COLLECTION["Colour 00"],
        highlightbackground="black", highlightthickness=1
    )
    connection_detail_frame.place(
        x=10, y=((app_heigth - (app_heigth / 25))/2) + 20,
        width=app_width/4 - 20,
        height=((app_heigth - (app_heigth / 25))/2.3)/2
    )

    connection_info_tree = ttk.Treeview(
        connection_detail_frame, columns=["c1", "c2"],
        show="headings", height=13
    )

    connection_info_tree.column("c1", anchor=W, width=30)
    connection_info_tree.column("c2", anchor=W, width=70)

    connection_info_tree.heading("c1", text="Detail Name")
    connection_info_tree.heading("c2", text="Detail")

    scrollbar1 = Scrollbar(connection_detail_frame, orient=HORIZONTAL)
    scrollbar1.pack(side=BOTTOM, fill=BOTH)
    connection_info_tree.config(xscrollcommand=scrollbar1.set)
    scrollbar1.config(command=connection_info_tree.xview)

    connection_info_tree.pack(fill=BOTH)

    schema = LabelConfig(
        explorer_frame, 5, (((app_heigth - (app_heigth / 25))/2))*1.5,
        15, "SCHEMA DETAIL"
    )

    schema_detail_frame = Frame(
        explorer_frame, background=COLOUR_COLLECTION["Colour 00"],
        highlightbackground="black", highlightthickness=1
    )
    schema_detail_frame.place(
        x=10, y=(((app_heigth - (app_heigth / 25))/2) + 20)*1.5,
        width=app_width/4 - 20,
        height=((app_heigth - (app_heigth / 25))/2.3)/2.3
    )

    schema_info_tree = ttk.Treeview(
        schema_detail_frame, columns=["c1", "c2"],
        show="headings", height=13
    )

    schema_info_tree.column("c1", anchor=W, width=30)
    schema_info_tree.column("c2", anchor=W, width=70)

    schema_info_tree.heading("c1", text="Detail Name")
    schema_info_tree.heading("c2", text="Detail")

    scrollbar1 = Scrollbar(schema_detail_frame, orient=HORIZONTAL)
    scrollbar1.pack(side=BOTTOM, fill=BOTH)
    schema_info_tree.config(xscrollcommand=scrollbar1.set)
    scrollbar1.config(command=schema_info_tree.xview)

    schema_info_tree.pack(fill=BOTH)

    # ------------------------- WORK AREA STATUS BAR -------------------------

    work_area_status_bar_frame = Frame(
        root, background=COLOUR_COLLECTION["Colour 00"],
        highlightbackground="black", highlightthickness=1
    )
    work_area_status_bar_frame.place(
        x=app_width/4, y=app_heigth/25,
        width=app_width*(3/4), height=app_heigth / 25
    )

    clone_work_area_status_bar_frame = work_area_status_bar_frame

    # ------------------------------ WORK AREA -------------------------------

    work_area_frame = Frame(
        root, background=COLOUR_COLLECTION["Colour 00"],
        highlightbackground="black", highlightthickness=1
    )
    work_area_frame.place(
        x=app_width/4, y=app_heigth*(2/25),
        width=app_width*(3/4), height=app_heigth*(17/25)
    )

    clone_work_area_frame = work_area_frame

    scrollbar_for_work_area = Scrollbar(work_area_frame)
    scrollbar_for_work_area.pack(side=RIGHT, fill=BOTH)

    # ------------------------ WORK AREA OUTPUT PANEL ------------------------

    work_area_output_panel = Frame(
        root, background=COLOUR_COLLECTION["Colour 00"],
        highlightbackground="black", highlightthickness=1
    )
    work_area_output_panel.place(
        x=app_width/4, y=app_heigth*(19/25),
        width=app_width*(3/4), height=app_heigth*(6/25)
    )

    clone_work_area_output_panel = work_area_output_panel

    output_tree = ttk.Treeview(
        work_area_output_panel, show="headings",
        columns=["c1", "c2", "c3", "c4", "c5"], height=7
    )

    output_tree.column("c1", anchor=CENTER, width=20)
    output_tree.column("c2", anchor=CENTER, width=25)
    output_tree.column("c3", anchor=W)
    output_tree.column("c4", anchor=W)
    output_tree.column("c5", anchor=CENTER)

    output_tree.heading("c1", text="#")
    output_tree.heading("c2", text="Time")
    output_tree.heading("c3", text="Action/Task")
    output_tree.heading("c4", text="Message")
    output_tree.heading("c5", text="Duration")

    scrollbar = Scrollbar(work_area_output_panel)
    scrollbar.pack(side=RIGHT, fill=BOTH)
    output_tree.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=output_tree.yview)

    scrollbar_1 = Scrollbar(work_area_output_panel, orient=HORIZONTAL)
    scrollbar_1.pack(side=BOTTOM, fill=BOTH)
    output_tree.config(xscrollcommand=scrollbar_1.set)
    scrollbar_1.config(command=output_tree.xview)

    output_tree.pack(fill=BOTH)

    tree_view = [
        connection_info_tree, table_info_tree, schema_info_tree, output_tree
    ]

    for tree in tree_view:
        tree.tag_configure(
            'evenrow', background=COLOUR_COLLECTION["Colour 00"]
        )

        tree.tag_configure(
            'oddrow', background=COLOUR_COLLECTION["Colour 03"],
        )

    new_query()
    refresh_connection()


# ------------------------------ U-Panel Window ------------------------------

def upanel_window():
    global clone_option_frame

    def create_database():

        def create_database_file(database_name):

            list_of_databases = [
                os.path.splitext(element)[0]
                for element in os.listdir(path)
            ]

            if (
                (
                    len(list_of_databases) == 100
                    and
                    current_user_details[2] == 'standard'
                )
                or
                (
                    len(list_of_databases) == 10
                    and
                    current_user_details[2] == 'guest'
                )
                or
                (
                    len(list_of_databases) == 2
                    and
                    current_user_details[2] == 'anonymous'
                )
            ):
                messagebox.showwarning(
                    title='SQL Lab - Message Box',
                    message=(
                        'Storage full, you create maximun number of databases'
                    )
                )
            elif len(database_name) > 15:
                messagebox.showwarning(
                    title='SQL Lab - Message Box',
                    message=(
                        'The entered database name cross the '
                        'maximum lenght of 15 words.'
                    )
                )
            elif punctuation_checker(database_name):
                messagebox.showwarning(
                    title='SQL Lab - Message Box',
                    message=(
                        'The entered database name contain puntuation marks '
                        'or special symbol which is not allowed.'
                    )
                )
            else:
                orignal_db_name = database_name
                database_name = de.convert_orignal_data_to_modifide_data(
                    database_name.lower().replace(' ', '')
                )

                if list_of_databases.count(database_name):
                    messagebox.showwarning(
                        title='SQL Lab - Message Box',
                        message=(
                            'The entered database name already exists.'
                        )
                    )
                else:

                    with open(f"{path}\\{database_name}.sqllab", "a"):
                        pass

                    messagebox.showinfo(
                        title='SQL Lab - Message Box',
                        message=(
                            f'Database "{orignal_db_name}" created '
                            'successfully.'
                        )
                    )

                    add_user_action_info(
                        f'Create new database "{orignal_db_name}".',
                        'Action completed successfully.'
                    )

                    create_database_window.destroy()

        local_storage_variable_1 = StringVar()

        create_database_window = Toplevel(
            root,
            background=COLOUR_COLLECTION["Colour 00"]
        )

        top_level_windows.append(create_database_window)

        app_width = 380
        app_heigth = 100

        create_database_window.title(
            "SQL Lab - Create Database Window"
        )
        create_database_window.resizable(0, 0)
        create_database_window.geometry(
            f"{int(app_width)}x{int(app_heigth)}+"
            f"{int((screen_width - app_width)/2)}+"
            f"{int((screen_height - app_heigth)/5)}"
        )

        create_database_window.iconbitmap(
            "Resources\\Images\\sqllablogo.ico")

        icon = LabelConfig(
            create_database_window, 5, -10, 65, "🛢",
            colour=[COLOUR_COLLECTION["Colour 00"],
                    COLOUR_COLLECTION["Colour B1"]
                    ]
        )

        db_name = LabelConfig(
            create_database_window, 70, 25, 13, "Database Name:"
        )

        db_name_entry = EntryConfig(
            create_database_window, 190, 25, local_storage_variable_1, 20,
            font_size=12
        )
        local_storage_variable_1.set("Database_name")

        next_btn = ButtonConfig(
            create_database_window, 10, 7, place=[160, 60],
            button_text="Next ⏩", border=2,
            command=lambda: create_database_file(
                local_storage_variable_1.get()
            )
        )

    def create_connection():
        fetch_data = {}

        databases_list = [
            de.convert_modifide_data_to_orignal_data(
                os.path.splitext(element)[0])
            for element in os.listdir(path)
        ]

        try:

            with open(
                f"{path_of_cre_folder}\\user_connections.json", "r"
            ) as file:
                fetch_data = json.load(file)

        except json.decoder.JSONDecodeError:
            pass

        def id_verifier(new_id):

            if list(fetch_data.keys()).count(de.ID):
                all_id = [de.convert_hashes_to_orignal_data(
                    i) for i in fetch_data[de.ID]]
                if all_id.count(new_id):
                    new_id = id_verifier(id_generator())
            else:
                pass

            return new_id

        def verification(
            connection_name, password, user, Id, schema, description
        ):
            connection_name = connection_name.strip().lower()
            connection_name = de.convert_orignal_data_to_hashes(
                connection_name)
            password = de.convert_orignal_data_to_hashes(password)
            user = current_user_details[0]
            Id = de.convert_orignal_data_to_hashes(Id)
            description = de.convert_orignal_data_to_hashes(description)

            entry_fill = [
                connection_name == '', password == '', Id == '',
                schema == ''
            ]

            try:
                id_exists = fetch_data[de.ID].count(Id)
            except KeyError:
                id_exists = 0

            if any(entry_fill):
                messagebox.showwarning(
                    title='SQL Lab - Message Box',
                    message=(
                        'Please, fill all entries.'
                    )
                )
            elif id_exists:
                messagebox.showwarning(
                    title='SQL Lab - Message Box',
                    message=(
                        'Entered Id already exists.'
                    )
                )
            elif not databases_list.count(schema):
                messagebox.showwarning(
                    title='SQL Lab - Message Box',
                    message=(
                        'Entered valid database name.'
                    )
                )
            else:

                if current_user_details[2] == 'anonymous':
                    connection_type = de.convert_orignal_data_to_hashes(
                        'Anonymous'
                    )
                else:
                    connection_type = de.convert_orignal_data_to_hashes(
                        'General'
                    )

                add_connection_details(
                    connection_name, password, connection_type, user, Id,
                    de.convert_orignal_data_to_hashes(schema), description
                )

        def add_connection_details(
            connection_name, password, connection_type, user, Id, schema,
            description
        ):
            uacl_orignal = (
                f'sqllab.system.{connection_type}.{current_user_details[0]}'
                f'.{connection_name}.{password}.uacl'
            )
            uacl = de.convert_orignal_data_to_hashes(uacl_orignal)

            if len(fetch_data):
                fetch_data[de.CONNECTION_NAME].append(connection_name)
                fetch_data[de.PASSWORD].append(password)
                fetch_data[de.CONNECTION_TYPE].append(connection_type)
                fetch_data[de.USER].append(user)
                fetch_data[de.ID].append(Id)
                fetch_data[de.SCHEMA].append(schema)
                fetch_data[de.DESCRIPTION].append(description)
                fetch_data[de.UACL].append(uacl)
            else:
                fetch_data[de.CONNECTION_NAME] = [connection_name]
                fetch_data[de.PASSWORD] = [password]
                fetch_data[de.CONNECTION_TYPE] = [connection_type]
                fetch_data[de.USER] = [user]
                fetch_data[de.ID] = [Id]
                fetch_data[de.SCHEMA] = [schema]
                fetch_data[de.DESCRIPTION] = [description]
                fetch_data[de.UACL] = [uacl]

            with open(
                f"{path_of_cre_folder}\\user_connections.json",
                "w"
            ) as file:
                json.dump(fetch_data, file)

            messagebox.showinfo(
                title='SQL Lab - Message Box',
                message=(
                    'Connection '
                    f'"{de.convert_hashes_to_orignal_data(connection_name)}"'
                    ' created successfully.'
                )
            )

            add_user_action_info(
                'Create new connection "'
                f'{de.convert_hashes_to_orignal_data(connection_name)}".',
                'Action completed successfully.'
            )

            root.clipboard_clear()
            root.clipboard_append(uacl_orignal)

            messagebox.showinfo(
                title='SQL Lab - Message Box',
                message=(
                    'Connection UACL copy to clipboard.'
                )
            )

            create_connection_window.destroy()

        app_width = 450
        app_heigth = 460

        local_storage_variable_1 = StringVar()
        local_storage_variable_2 = StringVar()
        local_storage_variable_3 = StringVar()
        local_storage_variable_4 = StringVar()
        local_storage_variable_5 = StringVar()

        create_connection_window = Toplevel(
            root,
            background=COLOUR_COLLECTION["Colour 00"]
        )

        top_level_windows.append(create_connection_window)

        create_connection_window.title(
            "SQL Lab - Create Connection Window"
        )
        create_connection_window.resizable(0, 0)
        create_connection_window.geometry(
            f"{int(app_width)}x{int(app_heigth)}+"
            f"{int((screen_width - app_width)/2)}+"
            f"{int((screen_height - app_heigth)/5)}"
        )
        create_connection_window.iconbitmap(
            "Resources\\Images\\sqllablogo.ico")

        icon = LabelConfig(
            create_connection_window, 105, -120, 200, "🔗",
            colour=[COLOUR_COLLECTION["Colour 00"],
                    COLOUR_COLLECTION["Colour B1"]
                    ]
        )

        connection_name = LabelConfig(
            create_connection_window, 20, 100, 16, "Connection Name:"
        )

        connection_name_entry = EntryConfig(
            create_connection_window, 190, 100, local_storage_variable_1, 20,
            font_size=16
        )
        local_storage_variable_1.set("Connection name")

        password = LabelConfig(
            create_connection_window, 20, 140, 16, "Password:"
        )

        password_entry = EntryConfig(
            create_connection_window, 190, 140, local_storage_variable_2, 20,
            font_size=16, hide_and_show_text=True,
            hide_and_show_btn_config=[420, 130]
        )
        local_storage_variable_2.set("Password")

        user = LabelConfig(
            create_connection_window, 20, 180, 16, "User:"
        )

        user_entry = EntryConfig(
            create_connection_window, 190, 180, local_storage_variable_3, 20,
            font_size=16
        )
        local_storage_variable_3.set(current_user_details[1])

        id_ = LabelConfig(
            create_connection_window, 20, 220, 16, "ID:"
        )

        id_entry = EntryConfig(
            create_connection_window, 190, 220, local_storage_variable_4, 20,
            font_size=16
        )
        local_storage_variable_4.set(id_verifier(id_generator()))

        refresh_id_btn = ButtonConfig(
            create_connection_window, 20, 1, place=[420, 210],
            button_text="🔃", bg_less_btn=[True, False],
            command=lambda: local_storage_variable_4.set(
                id_verifier(id_generator()))
        )

        schema = LabelConfig(
            create_connection_window, 20, 260, 16, "Schema:"
        )

        type_of_account = ttk.Combobox(
            create_connection_window, values=databases_list,
            textvariable=local_storage_variable_5, width=19,
            font=(FONT_COLLECTION["Font 2 --> Times New Roman"], 16)
        ).place(x=190, y=260)

        try:
            local_storage_variable_5.set(databases_list[0])
        except IndexError:
            pass

        description = LabelConfig(
            create_connection_window, 20, 300, 16, "Description:"
        )

        query_area = Text(
            create_connection_window,
            background=COLOUR_COLLECTION['Colour 01'],
            font=(FONT_COLLECTION["Font 2 --> Times New Roman"], 14)
        )
        query_area.place(
            x=20, y=330, width=400, height=80
        )
        query_area.insert(
            '1.0', 'Enter the basic description about this connection .....')

        create_connection_btn = ButtonConfig(
            create_connection_window, 10, 17, place=[150, 420],
            button_text="Create Connection", border=2,
            command=lambda: verification(
                local_storage_variable_1.get(),
                local_storage_variable_2.get(),
                local_storage_variable_3.get(),
                local_storage_variable_4.get(),
                local_storage_variable_5.get(),
                query_area.get('1.0', END)
            )
        )

    def dashboard():
        global clone_dashboard_frame

        def generate_user_report():

            def copy():
                text = (
                    f'User Name                         : '
                    f'{data[0].capitalize()}\n'
                    f'Password                          : {data[1]}\n'
                    f'Profile                           : '
                    f'{data[2].capitalize()}\n'
                    f'Date of account creation          : {data[3]}\n'
                    f'Time of account creation          : {data[4]}\n'
                    f'Storage used                      : {data[5]}\n'
                    f'Total number of database created  : {data[6]}\n'
                    f'Total number of connection created: {data[7]}'
                )
                root.clipboard_clear()
                root.clipboard_append(text)

            if current_user_details[2] == 'anonymous':

                with open(
                    f"{path_of_cre_folder}\\user_credential.json", 'r'
                ) as file:
                    credentials = json.load(file)

            else:

                with open(
                    f"{path_of_cre_folder}\\user_credential.json", 'r'
                ) as file:
                    credentials = json.load(file)

            data = []
            total_db_created = len(os.listdir(path))

            data.append(
                de.convert_modifide_data_to_orignal_data(
                    credentials[de.USER_NAME])
            )
            data.append(
                de.convert_hashes_to_orignal_data(credentials[de.PASSWORD])
            )
            data.append(
                de.convert_hashes_to_orignal_data(credentials[de.PROFILE])
            )
            if current_user_details[2] == 'anonymous':
                data.append("------")
                data.append("------")
                data.append(f'{(total_db_created/2)*100:.2f} %')
                data.append(f'{total_db_created} out of 2')
            else:
                data.append(credentials[de.DATE])
                data.append(credentials[de.TIME])

                if current_user_details[2] == 'guest':
                    data.append(f'{(total_db_created/10)*100:.2f} %')
                    data.append(f'{total_db_created} out of 10')
                elif current_user_details[2] == 'standard':
                    data.append(f'{(total_db_created):.2f} %')
                    data.append(f'{total_db_created} out of 100')

            try:

                if current_user_details[2] == 'anonymous':

                    with open(
                        f"{path_of_cre_folder}\\user_connections.json", 'r'
                    ) as file:
                        credentials = json.load(file)

                else:

                    with open(
                        f"{path_of_cre_folder}\\user_connections.json", 'r'
                    ) as file:
                        credentials = json.load(file)

                data.append(len(credentials[de.CONNECTION_NAME]))
            except json.decoder.JSONDecodeError:
                data.append('0')

            output_data = [
                ['User Name', data[0].capitalize()],
                ['Password', data[1]],
                ['Profile:', data[2].capitalize()],
                ['Date of account creation', data[3]],
                ['Time of account creation', data[4]],
                ['Storage used', data[5]],
                ['Total number of database created', data[6]],
                ['Total number of connection created', data[7]],
            ]

            database_report_window = Toplevel(
                root,
                background=COLOUR_COLLECTION["Colour 00"]
            )

            top_level_windows.append(database_report_window)

            app_width = 520
            app_heigth = 320

            database_report_window.title(
                "SQL Lab - User Report Window"
            )
            database_report_window.resizable(0, 0)
            database_report_window.geometry(
                f"{int(app_width)}x{int(app_heigth)}+"
                f"{int((screen_width - app_width)/2)}+"
                f"{int((screen_height - app_heigth)/5)}"
            )
            database_report_window.iconbitmap(
                "Resources\\Images\\sqllablogo.ico"
            )

            icon = LabelConfig(
                database_report_window, 90, 5, 44,
                '👤', colour=[COLOUR_COLLECTION["Colour 00"],
                             COLOUR_COLLECTION["Colour B1"]
                             ]
            )

            heading = LabelConfig(
                database_report_window, 150, 10, 33,
                'User Report', font_style='underline',
                font_name=FONT_COLLECTION["Font 1 --> Algerian"]
            )

            details_frame = Frame(
                database_report_window,
                background=COLOUR_COLLECTION["Colour 02"]
            )
            details_frame.place(x=10, y=80, height=200, width=500)

            user_report_tree = ttk.Treeview(
                details_frame, show="headings",
                columns=["c1", "c2"]
            )

            user_report_tree.heading("c1", text="Detail name")
            user_report_tree.heading("c2", text="Description")

            user_report_tree.column("c1", anchor=W)
            user_report_tree.column("c2", anchor=W)

            scrollbar1 = Scrollbar(details_frame, orient=HORIZONTAL)
            scrollbar1.pack(side=BOTTOM, fill=BOTH)
            user_report_tree.config(xscrollcommand=scrollbar1.set)
            scrollbar1.config(command=user_report_tree.xview)

            user_report_tree.tag_configure(
                'evenrow', background=COLOUR_COLLECTION["Colour 00"]
            )

            user_report_tree.tag_configure(
                'oddrow', background=COLOUR_COLLECTION["Colour 03"],
            )

            user_report_tree.pack(fill=BOTH)

            count = 1

            for element in output_data:
                value = [
                    element[0], element[1]
                ]

                if count % 2 != 0:
                    user_report_tree.insert(
                        "", "end", values=value, tags=('evenrow',)
                    )
                else:
                    user_report_tree.insert(
                        "", "end", values=value, tags=('oddrow',)
                    )

                count += 1

            copy_details_btn = ButtonConfig(
                database_report_window, 11, 12, place=[415, 290],
                button_text="📋 Copy Details", bg_less_btn=[True, True],
                command=copy
            )

        def show_action_info():
            action_tree.delete(*action_tree.get_children())

            if current_user_details[2] == 'anonymous':
                profile = "anonymous_"
            else:
                profile = ""

            try:

                with open(
                    f"{path_1}{profile}{current_user_details[0]}_folder\\"
                    "Upanel_folder\\user_actions.json"
                ) as file:
                    action_details = json.load(file)

            except json.decoder.JSONDecodeError:
                pass

            actions_list = [
                [
                    de.convert_hashes_to_orignal_data(data)
                    for data in action_details[de.DATE][::-1]
                ],
                [
                    de.convert_hashes_to_orignal_data(data)
                    for data in action_details[de.TIME][::-1]
                ],
                [
                    de.convert_hashes_to_orignal_data(data)
                    for data in action_details[de.ACTION][::-1]
                ],
                [
                    de.convert_hashes_to_orignal_data(data)
                    for data in action_details[de.MESSAGE][::-1]
                ]
            ]

            count = 0

            for date, time_, action, message in zip(
                actions_list[0], actions_list[1],
                actions_list[2], actions_list[3]
            ):
                value = [
                    len(actions_list[0]) - count, date, time_,
                    action, message
                ]

                if count % 2 == 0:
                    action_tree.insert(
                        "", "end", values=value, tags=('evenrow',)
                    )
                else:
                    action_tree.insert(
                        "", "end", values=value, tags=('oddrow',)
                    )

                count += 1

        frame_destroyer(
            clone_user_panel_login_frame, clone_connections_frame,
            clone_dashboard_frame, clone_database_frame
        )

        dashboard_frame = Frame(
            root, background=COLOUR_COLLECTION["Colour 00"],
            highlightbackground=COLOUR_COLLECTION["Colour 05"],
            highlightthickness=1
        )
        dashboard_frame.place(
            x=app_width/6, y=0,
            width=app_width*(5/6), height=app_heigth
        )

        clone_dashboard_frame = dashboard_frame

        quick_access_frame = Frame(
            dashboard_frame, background=COLOUR_COLLECTION["Colour 00"],
        )
        quick_access_frame.place(
            x=0, y=0,
            width=app_width*(5/6), height=app_heigth/6
        )

        QUICK_ACCESS_OPTION = [
            "CREATE\nDATABASE", "CREATE\nCONNECTION",
            "GENERATE\nUSER REPORT"
        ]

        quick_access = [
            create_database, create_connection,
            generate_user_report
        ]

        i = 0

        while(
            i < len(QUICK_ACCESS_OPTION)
        ):
            quick_access_btn = ButtonConfig(
                quick_access_frame, 20, 12, pack=[BOTH, LEFT, True],
                command=quick_access[i], bg_less_btn=[True, True], border=1,
                button_text=f"{QUICK_ACCESS_OPTION[i]}", padding=[5, 5]
            )
            i += 1

        general_detail = Frame(
            dashboard_frame, background=COLOUR_COLLECTION["Colour 00"],
        )
        general_detail.place(
            x=0, y=app_heigth/6,
            width=app_width*(5/6), height=app_heigth*(2.2/6)
        )

        total_db_created = len(os.listdir(path))

        if current_user_details[2] == 'standard':
            maximum_no_of_db = 100
        elif current_user_details[2] == 'guest':
            maximum_no_of_db = 10
        elif current_user_details[2] == 'anonymous':
            maximum_no_of_db = 2

        plt.style.use("seaborn-bright")

        figure_1 = plt.Figure(figsize=(2, 1), dpi=100, facecolor='white')
        graph_1 = figure_1.add_subplot(111)
        graph_1.pie(
            [maximum_no_of_db-total_db_created, total_db_created],
            explode=(0, 0.1), labels=['Free Space', 'Used Space'],
            colors=['#03C03C', '#E30022'], startangle=90,
            autopct='%1.1f%%'
        )
        graph_1.set_title('Storage Use')
        bar1 = FigureCanvasTkAgg(figure_1, general_detail)
        bar1.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True)

        figure_2 = plt.Figure(figsize=(5, 1), dpi=100, facecolor='white')
        graph_2 = figure_2.add_subplot(111)

        memory = [os.path.getsize(f"{path}\\{element}")
                  for element in os.listdir(path)]
        memory.sort(reverse=True)
        memory = memory[:4]

        db_details = [
            [
                os.path.getsize(f"{path}\\{element}"),
                de.convert_modifide_data_to_orignal_data(
                    os.path.splitext(element)[0])
            ]
            for element in os.listdir(path)
        ]

        db_name = []
        db_size = []

        while(
            len(memory)
        ):
            for file_size, file_name in db_details:

                if file_size == memory[0]:
                    db_name.append(file_name.capitalize())
                    db_size.append(file_size/1000)
                    db_details.pop(db_details.index([file_size, file_name]))
                    memory.pop(0)
                    break

        db_size.reverse(), db_name.reverse()

        graph_2.plot(
            db_name, db_size
        )
        graph_2.set_title('Database Vs Memory Consumption {Kb}')
        bar1 = FigureCanvasTkAgg(figure_2, general_detail)
        bar1.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True)

        current_actions = Frame(
            dashboard_frame, background=COLOUR_COLLECTION["Colour 00"],
        )
        current_actions.place(
            x=0, y=app_heigth*(3.2/6),
            width=app_width*(5/6), height=app_heigth*(2.8/6)
        )

        action_tree = ttk.Treeview(
            current_actions, show="headings",
            columns=["c1", "c2", "c3", "c4", "c5"], height=15
        )

        action_tree.column("c1", anchor=CENTER, width=25)
        action_tree.column("c2", anchor=CENTER, width=25)
        action_tree.column("c3", anchor=CENTER, width=25)
        action_tree.column("c4", anchor=W)
        action_tree.column("c5", anchor=CENTER, width=30)

        action_tree.heading(
            "c1", text="#", command=show_action_info
        )
        action_tree.heading(
            "c2", text="Date Of Execution", command=show_action_info
        )
        action_tree.heading(
            "c3", text="Time Of Execution", command=show_action_info
        )
        action_tree.heading(
            "c4", text="Action/Task", command=show_action_info
        )
        action_tree.heading(
            "c5", text="Message", command=show_action_info
        )

        scrollbar = Scrollbar(current_actions)
        scrollbar.pack(side=RIGHT, fill=BOTH)
        action_tree.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=action_tree.yview)

        scrollbar1 = Scrollbar(current_actions, orient=HORIZONTAL)
        scrollbar1.pack(side=BOTTOM, fill=BOTH)
        action_tree.config(xscrollcommand=scrollbar1.set)
        scrollbar1.config(command=action_tree.xview)

        action_tree.tag_configure(
            'evenrow', background=COLOUR_COLLECTION["Colour 00"]
        )

        action_tree.tag_configure(
            'oddrow', background=COLOUR_COLLECTION["Colour 03"],
        )

        action_tree.pack(fill=BOTH)

        show_action_info()

    def databases():
        global clone_database_frame

        def show_details_of_databases():
            database_details_tree.delete(
                *database_details_tree.get_children()
            )

            count = 1

            for element in databases_details:
                value = [
                    count, element[0].capitalize(), element[1], element[2],
                    element[3]
                ]

                if count % 2 != 0:
                    database_details_tree.insert(
                        "", "end", values=value, tags=('evenrow',)
                    )
                else:
                    database_details_tree.insert(
                        "", "end", values=value, tags=('oddrow',)
                    )

                count += 1

        def search(database_name):
            if database_name != '':
                database_name = database_name.strip().replace(' ', '').lower()

                database_details_tree.delete(
                    *database_details_tree.get_children()
                )

                count = 1

                for element in databases_details:

                    if element[0].strip().startswith(database_name):
                        value = [
                            count, element[0].capitalize(), element[1],
                            element[2], element[3]
                        ]

                        if count % 2 != 0:
                            database_details_tree.insert(
                                "", "end", values=value,
                                tags=('evenrow',)
                            )
                        else:
                            database_details_tree.insert(
                                "", "end", values=value,
                                tags=('oddrow',)
                            )

                        count += 1

                if not len(database_details_tree.get_children()):
                    value = [
                        'XXX', 'Database', 'Name', 'Not', 'Found'
                    ]
                    database_details_tree.insert(
                        "", "end", values=value, tags=('evenrow',)
                    )

            else:
                show_details_of_databases()

        def delete_database():

            def delete_database_file(database_name):
                orignal_db_name = database_name
                database_name = de.convert_orignal_data_to_modifide_data(
                    database_name.lower().replace(' ', '')
                )

                list_of_databases = [
                    os.path.splitext(element)[0]
                    for element in os.listdir(path)
                ]

                if not list_of_databases.count(database_name):
                    messagebox.showwarning(
                        title='SQL Lab - Message Box',
                        message=(
                            'The entered database name not exists.'
                        )
                    )
                else:
                    os.remove(f"{path}\\{database_name}.sqllab")
                    messagebox.showwarning(
                        title='SQL Lab - Message Box',
                        message=(
                            f'Database "{orignal_db_name}" deleted '
                            'successfully.'
                        )
                    )
                    add_user_action_info(
                        f'Delete database "{orignal_db_name}".',
                        'Action completed successfully.'
                    )
                    delete_database_window.destroy()

            local_storage_variable_1 = StringVar()

            delete_database_window = Toplevel(
                root,
                background=COLOUR_COLLECTION["Colour 00"]
            )

            top_level_windows.append(delete_database_window)

            app_width = 380
            app_heigth = 100

            delete_database_window.title(
                "SQL Lab - Delete Database Window"
            )
            delete_database_window.resizable(0, 0)
            delete_database_window.geometry(
                f"{int(app_width)}x{int(app_heigth)}+"
                f"{int((screen_width - app_width)/2)}+"
                f"{int((screen_height - app_heigth)/5)}"
            )
            delete_database_window.iconbitmap(
                "Resources\\Images\\sqllablogo.ico")

            icon = LabelConfig(
                delete_database_window, 5, -10, 65, "🛢",
                colour=[COLOUR_COLLECTION["Colour 00"],
                        COLOUR_COLLECTION["Colour B1"]
                        ]
            )

            table_name = LabelConfig(
                delete_database_window, 70, 25, 13, "Database Name:"
            )

            table_name_entry = EntryConfig(
                delete_database_window, 190, 25, local_storage_variable_1, 20,
                font_size=12
            )
            local_storage_variable_1.set("Database_name")

            next_btn = ButtonConfig(
                delete_database_window, 10, 7, place=[160, 60],
                button_text="Next ⏩", border=2,
                command=lambda: delete_database_file(
                    local_storage_variable_1.get()
                )
            )

        def generate_db_report():
            def search(database_name):
                database_report_tree.delete(
                    *database_report_tree.get_children()
                )
                database_name = database_name.replace(' ', '').lower()

                for data in databases_details:
                    if data[0] == database_name:

                        def copy():
                            text = (
                                'Database name     : '
                                f'{data[0].capitalize()}\n'
                                f'Date of creation  : {data[1]}\n'
                                f'User              : {data[2]}\n'
                                f'Storage consumption: {data[3]}'
                            )
                            root.clipboard_clear()
                            root.clipboard_append(text)

                        output_data = [
                            ['Database name', data[0].capitalize()],
                            ['Date of creation', data[1]],
                            ['User', data[2]],
                            ['Storage consumption', data[3]],
                        ]

                        count = 1

                        for element in output_data:
                            value = [
                                element[0], element[1]
                            ]

                            if count % 2 != 0:
                                database_report_tree.insert(
                                    "", "end", values=value, tags=('evenrow',)
                                )
                            else:
                                database_report_tree.insert(
                                    "", "end", values=value, tags=('oddrow',)
                                )

                            count += 1

                        widgets = database_report_window.winfo_children()

                        widgets[len(widgets) - 1].config(
                            command=copy
                        )
                        break
                else:
                    messagebox.showwarning(
                        title='SQL Lab - Message Box',
                        message=(
                            f'Database not found.'
                        )
                    )

            database_report_window = Toplevel(
                root,
                background=COLOUR_COLLECTION["Colour 00"]
            )

            top_level_windows.append(database_report_window)

            app_width = 520
            app_heigth = 270
            local_storage_variable_1 = StringVar()

            database_report_window.title(
                "SQL Lab - Generate Database Report Window"
            )
            database_report_window.resizable(0, 0)
            database_report_window.geometry(
                f"{int(app_width)}x{int(app_heigth)}+"
                f"{int((screen_width - app_width)/2)}+"
                f"{int((screen_height - app_heigth)/5)}"
            )
            database_report_window.iconbitmap(
                "Resources\\Images\\sqllablogo.ico"
            )

            heading = LabelConfig(
                database_report_window, 50, 10, 22,
                'Generate Database Report', font_style='underline',
                font_name=FONT_COLLECTION["Font 1 --> Algerian"]
            )

            database_name_ = LabelConfig(
                database_report_window, 15, 65, 18, "Database name:"
            )

            database_name_entry = EntryConfig(
                database_report_window, 180, 65,
                local_storage_variable_1, 25
            )

            search_btn = ButtonConfig(
                database_report_window, 25, 2, place=[460, 48],
                button_text="🔍", bg_less_btn=[True, False],
                command=lambda: search(local_storage_variable_1.get())
            )

            details_frame = Frame(
                database_report_window,
                background=COLOUR_COLLECTION["Colour 02"]
            )
            details_frame.place(x=10, y=110, height=120, width=500)

            database_report_tree = ttk.Treeview(
                details_frame, show="headings",
                columns=["c1", "c2"]
            )

            database_report_tree.heading("c1", text="Detail name")
            database_report_tree.heading("c2", text="Description")

            database_report_tree.column("c1", anchor=W)
            database_report_tree.column("c2", anchor=W)

            scrollbar1 = Scrollbar(details_frame, orient=HORIZONTAL)
            scrollbar1.pack(side=BOTTOM, fill=BOTH)
            database_report_tree.config(xscrollcommand=scrollbar1.set)
            scrollbar1.config(command=database_report_tree.xview)

            database_report_tree.tag_configure(
                'evenrow', background=COLOUR_COLLECTION["Colour 00"]
            )

            database_report_tree.tag_configure(
                'oddrow', background=COLOUR_COLLECTION["Colour 03"],
            )

            database_report_tree.pack(fill=BOTH)

            copy_details_btn = ButtonConfig(
                database_report_window, 11, 12, place=[415, 240],
                button_text="📋 Copy Details", bg_less_btn=[True, True]
            )

        frame_destroyer(
            clone_dashboard_frame, clone_database_frame,
            clone_connections_frame
        )

        database_frame = Frame(
            root, background=COLOUR_COLLECTION["Colour 00"],
            highlightbackground=COLOUR_COLLECTION["Colour 05"],
            highlightthickness=1
        )
        database_frame.place(
            x=app_width/6, y=0,
            width=app_width*(5/6), height=app_heigth
        )

        clone_database_frame = database_frame

        database_option_frame = Frame(
            database_frame, background=COLOUR_COLLECTION["Colour 00"],
        )
        database_option_frame.place(
            x=0, y=0,
            width=app_width*(1/6), height=app_heigth
        )

        QUICK_ACCESS_OPTION = [
            "CREATE\nDATABASE", "GENERATE\nDB REPORT",
            "DELETE\nDATABASE",
        ]

        command_for_btn = []

        quick_access = [
            create_database, generate_db_report,
            delete_database,
        ]

        local_storage_variable_1 = StringVar()

        i = 0

        while(
            i < len(QUICK_ACCESS_OPTION)
        ):
            quick_access_btn = ButtonConfig(
                database_option_frame, 20, 12, pack=[BOTH, TOP, True],
                command=quick_access[i], bg_less_btn=[True, True], border=1,
                button_text=f"{QUICK_ACCESS_OPTION[i]}", padding=[5, 5]
            )
            i += 1

        database_detail_frame = Frame(
            database_frame, background=COLOUR_COLLECTION["Colour 00"],
        )
        database_detail_frame.place(
            x=app_width*(1/6), y=0,
            width=app_width*(4/6), height=app_heigth
        )

        database_entry = EntryConfig(
            database_detail_frame, app_width*(4/6) - 670, 15,
            local_storage_variable_1, 55
        )
        local_storage_variable_1.set("Search for database name.....")

        search_btn = ButtonConfig(
            database_detail_frame, 25, 2, place=[app_width*(4/6) - 60, -3],
            button_text="🔍", bg_less_btn=[True, False],
            command=lambda: search(local_storage_variable_1.get())
        )

        list_of_db = Frame(
            database_detail_frame, background=COLOUR_COLLECTION["Colour 00"],
        )
        list_of_db.place(
            x=0, y=60,
            width=app_width*(4/6) - 5, height=app_heigth - 60
        )

        user = de.convert_modifide_data_to_orignal_data(
            current_user_details[0]
        ).capitalize()

        databases_details = [
            [
                f'''
                {
                    de.convert_modifide_data_to_orignal_data(
                        os.path.splitext(element)[0]
                    )
                }
                '''.split()[0],
                ' '.join(time.ctime(os.path.getctime(
                    f'{path}\\{element}')).split()[1:3])
                + "," +
                time.ctime(os.path.getctime(f'{path}\\{element}')).split()[4],
                user, f"{(os.path.getsize(f'{path}/{element}')/1000):.2f}" +
                " Kb"
            ]
            for element in os.listdir(path)
        ]

        database_details_tree = ttk.Treeview(
            list_of_db, show="headings",
            columns=["c1", "c2", "c3", "c4", "c5"], height=40
        )

        database_details_tree.column("c1", anchor=CENTER, width=40)
        database_details_tree.column("c2", anchor=W)
        database_details_tree.column("c3", anchor=CENTER)
        database_details_tree.column("c4", anchor=CENTER)
        database_details_tree.column("c5", anchor=CENTER)

        database_details_tree.heading("c1", text="#")
        database_details_tree.heading("c2", text="Database Name")
        database_details_tree.heading("c3", text="Date Of Creation")
        database_details_tree.heading("c4", text="User")
        database_details_tree.heading("c5", text="Size")

        scrollbar = Scrollbar(list_of_db)
        scrollbar.pack(side=RIGHT, fill=BOTH)
        database_details_tree.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=database_details_tree.yview)

        scrollbar1 = Scrollbar(list_of_db, orient=HORIZONTAL)
        scrollbar1.pack(side=BOTTOM, fill=BOTH)
        database_details_tree.config(xscrollcommand=scrollbar1.set)
        scrollbar1.config(command=database_details_tree.xview)

        database_details_tree.tag_configure(
            'evenrow', background=COLOUR_COLLECTION["Colour 00"]
        )

        database_details_tree.tag_configure(
            'oddrow', background=COLOUR_COLLECTION["Colour 03"],
        )

        database_details_tree.pack(fill=BOTH)
        show_details_of_databases()

    def connections():
        global clone_connections_frame

        def generate_connection_report():

            def search(connection_id):
                connection_details_tree.delete(
                    *connection_details_tree.get_children()
                )

                for data in connection_details:

                    if data[4] == connection_id:

                        def copy(number):

                            if number == 1:
                                text = data[6]
                            elif number == 2:
                                text = (
                                    'Connection name:'
                                    f' {data[0].capitalize()}\n'
                                    'Password       :'
                                    f' {data[1]}\n'
                                    'Type           :'
                                    f' {data[2]}\n'
                                    'User           :'
                                    f' {data[3]}\n'
                                    'ID             :'
                                    f' {data[4]}\n'
                                    'Schema         :'
                                    f' {data[5]}\n'
                                    'UACL           :'
                                    f' {data[6]}\n'
                                    'Description    :'
                                    f' {data[7]}'
                                )

                            root.clipboard_clear()
                            root.clipboard_append(text)

                        output_data = [
                            ['Connection name', data[0].capitalize()],
                            ['Password', data[1]],
                            ['Type', data[2]],
                            ['User', data[3]],
                            ['ID', data[4]],
                            ['Schema', data[5]],
                            ['UACL', data[6]],
                            ['Description', data[7]]
                        ]

                        count = 1

                        for element in output_data:
                            value = [
                                element[0], element[1]
                            ]

                            if count % 2 != 0:
                                connection_details_tree.insert(
                                    "", "end", values=value, tags=('evenrow',)
                                )
                            else:
                                connection_details_tree.insert(
                                    "", "end", values=value, tags=('oddrow',)
                                )

                            count += 1

                        widgets = connection_report_window.winfo_children()

                        widgets[len(widgets) - 1].config(
                            command=lambda: copy(1)
                        )

                        widgets[len(widgets) - 2].config(
                            command=lambda: copy(2)
                        )
                        break
                else:
                    messagebox.showwarning(
                        title='SQL Lab - Message Box',
                        message=(
                            f'Connection id not found.'
                        )
                    )

            connection_report_window = Toplevel(
                root,
                background=COLOUR_COLLECTION["Colour 00"]
            )

            top_level_windows.append(connection_report_window)

            app_width = 500
            app_heigth = 350
            local_storage_variable_1 = StringVar()

            connection_report_window.title(
                "SQL Lab - Generate Connection Report Window"
            )
            connection_report_window.resizable(0, 0)
            connection_report_window.geometry(
                f"{int(app_width)}x{int(app_heigth)}+"
                f"{int((screen_width - app_width)/2)}+"
                f"{int((screen_height - app_heigth)/5)}"
            )
            connection_report_window.iconbitmap(
                "Resources\\Images\\sqllablogo.ico"
            )

            heading = LabelConfig(
                connection_report_window, 30, 10, 22,
                'Generate Connection Report', font_style='underline',
                font_name=FONT_COLLECTION["Font 1 --> Algerian"]
            )

            id_symbol = LabelConfig(
                connection_report_window, 40, 60, 25, "🆔 :"
            )

            connection_id_entry = EntryConfig(
                connection_report_window, 100, 70,
                local_storage_variable_1, 30
            )

            search_btn = ButtonConfig(
                connection_report_window, 25, 2, place=[430, 52],
                button_text="🔍", bg_less_btn=[True, False],
                command=lambda: search(local_storage_variable_1.get())
            )

            details_frame = Frame(
                connection_report_window,
                background=COLOUR_COLLECTION["Colour 02"]
            )
            details_frame.place(x=10, y=110, height=200, width=480)

            connection_details_tree = ttk.Treeview(
                details_frame, show="headings",
                columns=["c1", "c2"]
            )

            connection_details_tree.heading("c1", text="Detail name")
            connection_details_tree.heading("c2", text="Description")

            connection_details_tree.column("c1", anchor=W, width=20)
            connection_details_tree.column("c2", anchor=W)

            scrollbar1 = Scrollbar(details_frame, orient=HORIZONTAL)
            scrollbar1.pack(side=BOTTOM, fill=BOTH)
            connection_details_tree.config(xscrollcommand=scrollbar1.set)
            scrollbar1.config(command=connection_details_tree.xview)

            connection_details_tree.tag_configure(
                'evenrow', background=COLOUR_COLLECTION["Colour 00"]
            )

            connection_details_tree.tag_configure(
                'oddrow', background=COLOUR_COLLECTION["Colour 03"],
            )

            connection_details_tree.pack(fill=BOTH)

            copy_details_btn = ButtonConfig(
                connection_report_window, 11, 12, place=[295, 320],
                button_text="📋 Copy Details", bg_less_btn=[True, True]
            )

            copy_uacl_btn = ButtonConfig(
                connection_report_window, 11, 12, place=[400, 320],
                button_text="📋 Copy UACL", bg_less_btn=[True, True]
            )

        def delete_connection():

            def delete(connection_id):

                if all_connection_id.count(connection_id):
                    yes_or_no = messagebox.askyesno(
                        title='SQL Lab - Message Box',
                        message=(
                            f'You really want to delete this connection?'
                        )
                    )

                    if yes_or_no:
                        index = fetch_connection_details[de.ID].index(
                            de.convert_orignal_data_to_hashes(connection_id)
                        )

                        for data in fetch_connection_details.keys():

                            if data == de.CONNECTION_NAME:
                                connection_name = (
                                    de.convert_hashes_to_orignal_data(
                                        fetch_connection_details[data][index]
                                    )
                                )
                            fetch_connection_details[data].pop(index)

                        if current_user_details[2] == 'anonymous':

                            with open(
                                f'{path_1}anonymous_{current_user_details[0]}'
                                '_folder\\user_connections.json', 'w'
                            ) as file:
                                json.dump(fetch_connection_details, file)

                        else:

                            with open(
                                f'{path_1}{current_user_details[0]}'
                                '_folder\\user_connections.json', 'w'
                            ) as file:
                                json.dump(fetch_connection_details, file)

                        messagebox.showinfo(
                            title='SQL Lab - Message Box',
                            message=(
                                f'Connection "{connection_name}" deleted '
                                'successfully.'
                            )
                        )
                        add_user_action_info(
                            'Delete connection "'
                            f'''
                            {
                                de.convert_hashes_to_orignal_data(
                                    connection_name
                                )
                            }".
                            '''.split()[0],
                            'Action completed successfully.'
                        )
                        delete_connection_window.destroy()
                    else:
                        messagebox.showinfo(
                            title='SQL Lab - Message Box',
                            message=(
                                'Deletation terminated.'
                            )
                        )
                        delete_connection_window.destroy()

                else:
                    messagebox.showwarning(
                        title='SQL Lab - Message Box',
                        message=(
                            'Connection id not found.'
                        )
                    )

            try:
                all_connection_id = [
                    de.convert_hashes_to_orignal_data(conn_id)
                    for conn_id in fetch_connection_details[de.ID]
                ]
            except KeyError:
                all_connection_id = []

            delete_connection_window = Toplevel(
                root,
                background=COLOUR_COLLECTION["Colour 00"]
            )

            top_level_windows.append(delete_connection_window)

            app_width = 470
            app_heigth = 120
            local_storage_variable_1 = StringVar()

            delete_connection_window.title(
                "SQL Lab - Delete Connection Window"
            )
            delete_connection_window.resizable(0, 0)
            delete_connection_window.geometry(
                f"{int(app_width)}x{int(app_heigth)}+"
                f"{int((screen_width - app_width)/2)}+"
                f"{int((screen_height - app_heigth)/5)}"
            )
            delete_connection_window.iconbitmap(
                "Resources\\Images\\sqllablogo.ico"
            )

            heading = LabelConfig(
                delete_connection_window, 90, 10, 22,
                'Delete Connection', font_style='underline',
                font_name=FONT_COLLECTION["Font 1 --> Algerian"]
            )

            id_symbol = LabelConfig(
                delete_connection_window, 10, 60, 25, "🆔 :"
            )

            connection_id_entry = EntryConfig(
                delete_connection_window, 60, 70,
                local_storage_variable_1, 30
            )
            local_storage_variable_1.set('Connection ID')

            delete_btn = ButtonConfig(
                delete_connection_window, 12, 5, place=[400, 65],
                button_text="Delete",
                command=lambda: delete(local_storage_variable_1.get())
            )

        def show_details_of_connection():
            connection_detail_tree.delete(
                *connection_detail_tree.get_children()
            )

            count = 1

            for element in connection_details:
                value = [
                    count, element[0].capitalize(), element[1], element[2],
                    element[3], element[4], element[5], element[6], element[7]
                ]

                if count % 2 != 0:
                    connection_detail_tree.insert(
                        "", "end", values=value, tags=('evenrow',)
                    )
                else:
                    connection_detail_tree.insert(
                        "", "end", values=value, tags=('oddrow',)
                    )

                count += 1

        def search(connection_name):
            if connection_name != '':
                connection_name = connection_name.strip().replace(
                    ' ', ''
                ).lower()
                connection_detail_tree.delete(
                    *connection_detail_tree.get_children()
                )
                count = 1

                for element in connection_details:

                    if element[0].strip().replace(
                        ' ', ''
                    ).startswith(connection_name):
                        value = [
                            count, element[0].capitalize(), element[1],
                            element[2], element[3], element[4], element[5],
                            element[6], element[7]
                        ]

                        if count % 2 != 0:
                            connection_detail_tree.insert(
                                "", "end", values=value,
                                tags=('evenrow',)
                            )
                        else:
                            connection_detail_tree.insert(
                                "", "end", values=value,
                                tags=('oddrow',)
                            )

                        count += 1

                if not len(connection_detail_tree.get_children()):
                    value = [
                        'XXX', 'Connection', 'Name', 'Not', 'Found',
                        'XXX', 'XXX', 'XXX', 'XXX'
                    ]
                    connection_detail_tree.insert(
                        "", "end", values=value, tags=('evenrow',)
                    )
            else:
                show_details_of_connection()

        local_storage_variable_1 = StringVar()

        frame_destroyer(
            clone_dashboard_frame, clone_database_frame,
            clone_connections_frame
        )

        connections_frame = Frame(
            root, background=COLOUR_COLLECTION["Colour 00"],
            highlightbackground=COLOUR_COLLECTION["Colour 05"],
            highlightthickness=1
        )
        connections_frame.place(
            x=app_width/6, y=0,
            width=app_width*(5/6), height=app_heigth
        )

        clone_connections_frame = connections_frame

        connection_option_frame = Frame(
            connections_frame, background=COLOUR_COLLECTION["Colour 00"],
        )
        connection_option_frame.place(
            x=0, y=0,
            width=app_width*(1/6), height=app_heigth
        )

        QUICK_ACCESS_OPTION = [
            "CREATE\nCONNECTION", "GENERATE\nCONNECTION\nREPORT",
            "DELETE\nCONNECTION"
        ]

        quick_access = [
            create_connection, generate_connection_report,
            delete_connection
        ]

        i = 0

        while(
            i < len(QUICK_ACCESS_OPTION)
        ):
            quick_access_btn = ButtonConfig(
                connection_option_frame, 20, 12, pack=[BOTH, TOP, True],
                command=quick_access[i], bg_less_btn=[True, True], border=1,
                button_text=f"{QUICK_ACCESS_OPTION[i]}", padding=[5, 5]
            )
            i += 1

        connection_detail_frame = Frame(
            connections_frame, background=COLOUR_COLLECTION["Colour 00"],
        )
        connection_detail_frame.place(
            x=app_width*(1/6), y=0,
            width=app_width*(4/6), height=app_heigth
        )

        connection_entry = EntryConfig(
            connection_detail_frame, app_width*(4/6) - 670, 15,
            local_storage_variable_1, 55
        )
        local_storage_variable_1.set("Search for connection name .....")

        scearch_btn = ButtonConfig(
            connection_detail_frame, 25, 2,
            place=[app_width*(4/6) - 60, -3],
            button_text="🔍", bg_less_btn=[True, False],
            command=lambda: search(local_storage_variable_1.get())
        )

        list_of_connection = Frame(
            connection_detail_frame,
            background=COLOUR_COLLECTION["Colour 00"],
        )
        list_of_connection.place(
            x=0, y=60,
            width=app_width*(4/6) - 5, height=app_heigth - 60
        )

        try:

            if current_user_details[2] == 'anonymous':

                with open(
                    f'{path_1}anonymous_{current_user_details[0]}_folder\\'
                    'user_connections.json'
                ) as file:
                    fetch_connection_details = json.load(file)

            else:

                with open(
                    f'{path_1}{current_user_details[0]}_folder\\'
                    'user_connections.json'
                ) as file:
                    fetch_connection_details = json.load(file)

            connection_details = [
                [
                    de.convert_hashes_to_orignal_data(
                        fetch_connection_details[de.CONNECTION_NAME][i]
                    ),
                    de.convert_hashes_to_orignal_data(
                        fetch_connection_details[de.PASSWORD][i]
                    ),
                    de.convert_hashes_to_orignal_data(
                        fetch_connection_details[de.CONNECTION_TYPE][i]
                    ),
                    de.convert_modifide_data_to_orignal_data(
                        fetch_connection_details[de.USER][i]
                    ).capitalize(),
                    de.convert_hashes_to_orignal_data(
                        fetch_connection_details[de.ID][i]
                    ),
                    de.convert_hashes_to_orignal_data(
                        fetch_connection_details[de.SCHEMA][i]
                    ),
                    de.convert_hashes_to_orignal_data(
                        fetch_connection_details[de.UACL][i]
                    ),
                    de.convert_hashes_to_orignal_data(
                        fetch_connection_details[de.DESCRIPTION][i]
                    ).replace('\n', ' ')
                ]
                for i in range(
                    len(fetch_connection_details[de.CONNECTION_NAME])
                )
            ]
        except json.decoder.JSONDecodeError:
            connection_details = []

        connection_detail_tree = ttk.Treeview(
            list_of_connection, show="headings",
            columns=["c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9"],
            height=40
        )

        connection_detail_tree.column("c1", anchor=CENTER, width=40)
        connection_detail_tree.column("c2", anchor=W)
        connection_detail_tree.column("c3", anchor=CENTER)
        connection_detail_tree.column("c4", anchor=CENTER)
        connection_detail_tree.column("c5", anchor=CENTER)
        connection_detail_tree.column("c6", anchor=CENTER)
        connection_detail_tree.column("c7", anchor=W)
        connection_detail_tree.column("c8", anchor=W, width=500)
        connection_detail_tree.column("c9", anchor=W, width=300)

        connection_detail_tree.heading("c1", text="#")
        connection_detail_tree.heading("c2", text="Connection Name")
        connection_detail_tree.heading("c3", text="Password")
        connection_detail_tree.heading("c4", text="Type")
        connection_detail_tree.heading("c5", text="User")
        connection_detail_tree.heading("c6", text="ID")
        connection_detail_tree.heading("c7", text="Database Name")
        connection_detail_tree.heading("c8", text="UACL")
        connection_detail_tree.heading("c9", text="Description")

        scrollbar = Scrollbar(list_of_connection)
        scrollbar.pack(side=RIGHT, fill=BOTH)
        connection_detail_tree.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=connection_detail_tree.yview)

        scrollbar1 = Scrollbar(list_of_connection, orient=HORIZONTAL)
        scrollbar1.pack(side=BOTTOM, fill=BOTH)
        connection_detail_tree.config(xscrollcommand=scrollbar1.set)
        scrollbar1.config(command=connection_detail_tree.xview)

        connection_detail_tree.tag_configure(
            'evenrow', background=COLOUR_COLLECTION["Colour 00"]
        )

        connection_detail_tree.tag_configure(
            'oddrow', background=COLOUR_COLLECTION["Colour 03"]
        )

        connection_detail_tree.pack(fill=BOTH)
        show_details_of_connection()

    def logout():
        global current_connection_details, current_user_details

        ask_to_logout = messagebox.askyesno(
            title='SQL Lab - Message Box',
            message=(
                f'You want to logout from user panel?'
            )
        )

        if ask_to_logout:
            add_user_action_info(
                'Logout from account.',
                'Action completed successfully.'
            )

            current_user_details = []
            current_connection_details = [
                None, None, None, None, None, None, None
            ]

            desktop_window()
        else:
            pass

    frame_destroyer(clone_user_panel_login_frame)

    if current_user_details[2] == 'anonymous':
        path = (
            f"{path_2}anonymous_{current_user_details[0]}_database_folder"
        )
    else:
        path = (
            f"{path_2}{current_user_details[0]}_database_folder"
        )

    if current_user_details[2] == 'anonymous':
        path_of_cre_folder = (
            f'{path_1}anonymous_{current_user_details[0]}_folder'
        )
    else:
        path_of_cre_folder = (
            f'{path_1}{current_user_details[0]}_folder'
        )

    app_width = root.winfo_screenwidth()
    app_heigth = root.winfo_screenheight() - 83

    root.title("SQL Lab - Connection Panel")
    root.resizable(1, 1)
    root.state('zoomed')
    root.geometry(
        f"{int(app_width)}x{int(app_heigth)}+"
        f"{int((screen_width - app_width)/2)}+"
        f"{int((screen_height - app_heigth)/5)}"
    )

    # ----------------------------- OPTION PANEL -----------------------------

    option_frame = Frame(
        root, background=COLOUR_COLLECTION["Colour 00"],
        highlightbackground=COLOUR_COLLECTION["Colour 05"],
        highlightthickness=1
    )
    option_frame.place(
        x=0, y=0,
        width=app_width/6, height=app_heigth
    )

    clone_option_frame = option_frame

    OPTION_NAME = [
        "    📊 Dashboard", "    🛢 Databases",
        "    🔗 Connections", "    🔒 Logout"

    ]

    COMMAND_FOR_BTN = {
        "    📊 Dashboard": dashboard,
        "    🛢 Databases": databases,
        "    🔗 Connections": connections,
        "    🔒 Logout": logout
    }

    i = 0

    while(
        i < len(OPTION_NAME)
    ):
        on_click_change = True

        if i == 0:
            state = "active"
        else:
            state = "deactive"

        if i == len(OPTION_NAME)-1:
            on_click_change = False

        options = ButtonConfig(
            option_frame, 16, 1, 2, button_text=f"{OPTION_NAME[i]}",
            bg_less_btn=[True, True], aling="w", padding=[1, 2],
            command=COMMAND_FOR_BTN[OPTION_NAME[i]], pack=['x', TOP],
            on_click_bg_change=on_click_change, on_click_state=state,
        )
        i += 1

    dashboard()


def redirect(function_name):
    for element in ['Create account', 'Admin panel']:
        account_menu.entryconfig(element, state="disable")

    function_name()


def frame_destroyer(*frames):
    for frame in frames:

        try:
            frame.destroy()
        except AttributeError:
            pass


def top_level_window_destroyer():
    global top_level_windows

    for win in top_level_windows:
        win.destroy()

    top_level_windows = []


def punctuation_checker(string):
    for element in string:

        if PUNCUATIONS.count(element):
            punctuation_found = True
            break

    else:
        punctuation_found = False

    return punctuation_found


def id_generator():
    id = (
        random.choice(de.VALUES[26:52]) +
        random.choice(de.VALUES[0:26]) +
        random.choice(de.VALUES[26:52]) +
        random.choice(de.VALUES[0:26]) +
        random.choice(de.VALUES[83:93]) +
        random.choice(de.VALUES[83:93]) +
        random.choice(de.VALUES[83:93]) +
        random.choice(de.VALUES[83:93]) +
        random.choice(['#', '$', '&', '@']) +
        random.choice(['#', '$', '&', '@'])
    )

    return id


def add_user_action_info(action, message):
    action_details = {}

    if current_user_details[2].lower() == "anonymous":
        profile = "anonymous_"
    else:
        profile = ""

    try:
        with open(
            f"{path_1}{profile}{current_user_details[0]}_folder\\"
            "Upanel_folder\\user_actions.json"
        ) as file:
            action_details = json.load(file)

    except json.decoder.JSONDecodeError:
        pass

    if not len(action_details):
        action_details[de.DATE] = [
            de.convert_orignal_data_to_hashes(
                datetime.now().strftime('%d %b, %Y')
            )
        ]
        action_details[de.TIME] = [
            de.convert_orignal_data_to_hashes(
                datetime.now().strftime('%X')
            )
        ]
        action_details[de.ACTION] = [
            de.convert_orignal_data_to_hashes(
                action
            )
        ]
        action_details[de.MESSAGE] = [
            de.convert_orignal_data_to_hashes(
                message
            )
        ]
    else:
        action_details[de.DATE].append(
            de.convert_orignal_data_to_hashes(
                datetime.now().strftime('%d %b, %Y')
            )
        )
        action_details[de.TIME].append(
            de.convert_orignal_data_to_hashes(
                datetime.now().strftime('%X')
            )
        )
        action_details[de.ACTION].append(
            de.convert_orignal_data_to_hashes(
                action
            )
        )
        action_details[de.MESSAGE].append(
            de.convert_orignal_data_to_hashes(
                message
            )
        )

    with open(
        f"{path_1}{profile}{current_user_details[0]}_folder\\"
        "Upanel_folder\\user_actions.json", 'w'
    ) as file:
        json.dump(action_details, file)


# --------------------- VARIABLE & CONSTANTS DECLERATION ---------------------
file_path = None
resizable = False
count = False
current_text_area = None
current_hovering_btn_bg = None
current_hovering_btn_fg = None
clone_option_bar_frame = None
clone_user_details_frame = None
clone_user_manager_frame = None
clone_change_pass_frame = None
clone_delete_user_frame = None
clone_clean_user_data_frame = None
clone_change_user_profile_frame = None
clone_activity_monitor_frame = None
clone_resource_monitor_frame = None
clone_desktop_frame = None
clone_create_user_account_frame = None
clone_user_panel_login_frame = None
clone_connection_frame = None
clone_connect_with_db_frame = None
clone_connection_with_UACL_frame = None
clone_status_bar_frame = None
clone_explorer_frame = None
clone_work_area_status_bar_frame = None
clone_work_area_frame = None
clone_work_area_output_panel = None
clone_option_frame = None
clone_dashboard_frame = None
clone_database_frame = None
clone_connections_frame = None
login_attempts = 0
no_of_query_btn = 0
path_1 = fbm.PATH_OF_CREDENTIALS_FOLDER_OF_USERS
path_2 = fbm.PATH_OF_USER_DATABASE_FOLDERS
path_3 = fbm.PATH_OF_CREDENTIALS_FOLDER_OF_ADMIN

top_level_windows = []

current_user_details = []

current_connection_details = [
    None, None, None, None, None, None, None
]

list_of_outputs = []

COLOUR_COLLECTION = {
    "Colour 00": "#ffffff",
    "Colour 01": "#f0f0f0",
    "Colour 02": "#E8EAE6",
    "Colour 03": "#CDD0CB",
    "Colour 04": "#555555",
    "Colour 05": "#000000",
    "Colour B1": "#0000FF",
    "Colour R1": "#FF0000",
}

FONT_COLLECTION = {
    "Font 1 --> Algerian": r"Algerian",
    "Font 2 --> Times New Roman": r"Times New Roman",
    "Font 3 --> Cooper Black": r"Cooper Black",
    "Font 4 --> Castellar": r"Castellar",
    "Font 5 --> Bahnschrift": r"Bahnschrift"
}

DATA_TYPE = [
    "INT", "INTEGER", "TINYINT", "SMALLINT", "MEDIUMINT", "BIGINT",
    "UNSIGNED BIG INT", "INT2", "INT8", "----", "CHARACTER(20)",
    "VARCHAR(255)", "VARYING CHARACTER(255)", "NCHAR(55)",
    "NATIVE CHARACTER(70)", "NVARCHAR(100)", "TEXT", "CLOB",
    "----", "BLOB", "----", "REAL", "DOUBLE", "DOUBLE PRECISION",
    "FLOAT", "----", "NUMERIC", "DECIMAL(10,5)", "BOOLEAN", "DATE", "DATETIME"
]

TITLES_LIST_OF_CREATE_TABLE_FORM = [
    "Colunm Name", "Datatype", "Default", "PK", "NN", "UQ"
]

TYPE_OF_ACCOUNT = [
    "Standard", "Guest", "Anonymous"
]

PUNCUATIONS = [
    '~', '}', '|', '{', '`', '^', ']', '[', '@', '?', '>', '=', '<',
    ';', ':', '/', '.', '-', ',', '+', '*', ')', '(', '"', "'",
    '&', '%', '$', '#', '!',
]

if __name__ == "__main__":
    desktop_window()
    root.mainloop()
