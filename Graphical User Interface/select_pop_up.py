from tkinter import *
from tkinter import ttk


def select_output(column_name_list=[], data=()):
    window = Toplevel()

    app_width = 400
    app_heigth = 350

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    top_level_windows.append(window)

    window.geometry(
        f"{int(app_width)}x{int(app_heigth)}+"
        f"{int((screen_width - app_width)/2)}+"
        f"{int((screen_height - app_heigth)/5)}"
    )
    window.config(background="white")
    window.iconbitmap('Resources\\Images\\sqllablogo.ico')
    window.title(
        "SQL Lab - Output Window"
    )

    tree = ttk.Treeview(window, columns=column_name_list,
                        show="headings", height=100)

    for column in column_name_list:
        tree.column(f"{column}", anchor=CENTER, width=20)
        tree.heading(f"{column}", text=f"{str(column).strip().capitalize()}")

    tree.tag_configure(
        'evenrow', background='#FFFFFF'
    )

    tree.tag_configure(
        'oddrow', background='#CDD0CB',
    )

    count = 0

    for element in data:

        if count % 2 == 0:
            tree.insert("", "end", values=element, tags=('evenrow',))
        else:
            tree.insert("", "end", values=element, tags=('oddrow',))
        count += 1

    scrollbar = Scrollbar(window)
    scrollbar.pack(side=RIGHT, fill=BOTH)
    tree.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=tree.yview)

    scrollbar_1 = Scrollbar(window, orient=HORIZONTAL)
    scrollbar_1.pack(side=BOTTOM, fill=BOTH)
    tree.config(xscrollcommand=scrollbar_1.set)
    scrollbar_1.config(command=tree.xview)

    tree.pack(fill=BOTH)


def top_level_window_destroyer():
    global top_level_windows

    for win in top_level_windows:
        win.destroy()

    top_level_windows = []


top_level_windows = []
