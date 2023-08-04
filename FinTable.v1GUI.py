import os
import tkinter
from tkinter import filedialog
import tkinter.messagebox
import customtkinter as ctk
from FinTable import AnnualReport

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

def bank_bool():
    if bank_value.get() == 1:
        return True
    else:
        return False
    
def report_code(type):
    report_dict = {
        "Profit or Loss": "SOPL",
        "Financial Position": "SOFP",
        "Cash Flows": "SOCF"
    }
    return report_dict[type]

def clear_frame():
    for widget in display_screen.winfo_children():
        widget.destroy()

filepath_var = []
def upload_button_callback():
    clear_frame()
    filepath_var.clear()

    filepath = filedialog.askopenfilename()
    filepath_var.append(filepath)
    if len(filepath_var) > 0:
        file = filepath_var[0]
        filename = file.split("/")[-1]

        upload_button.pack_forget()
        display_msg = ctk.CTkLabel(
            display_screen,
            text=f"File Uploaded\n\n{filename}"
        )
        display_msg.pack(side="top", expand=True)

def download_button_callback():

    file = filepath_var[0]
    bank = bank_bool()
    type = report_code(report_type.get())
    
    comp = AnnualReport(file, bank)
    filename = comp.save_report(type)
    
    clear_frame()
    saved_msg = ctk.CTkLabel(
        display_screen,
        text=f"File Saved!\n\n{filename}"
    )
    saved_msg.pack(side="top", expand=True)

    new_upload_button = ctk.CTkButton(
        display_screen,
        text="New Upload",
        command=upload_button_callback
    )
    new_upload_button.pack(side="bottom", expand=True)
    try:
        os.system(f'start excel.exe "{filename}"')
    except FileNotFoundError:
        print("Working on it...")

window = ctk.CTk()

window.title("FinTable.v1")
window.geometry("720x480")
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

display_screen = ctk.CTkFrame(master=window)
display_screen.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsew", rowspan=3)

bank_value = ctk.IntVar(window)
bank_toggle = ctk.CTkSwitch(
    window,
    text="Bank",
    onvalue=1,
    offvalue=0,
    variable=bank_value,
    command=bank_bool
)
bank_toggle.grid(column=1, row=0, sticky="ne", padx=10, pady=10)

report_type = ctk.StringVar(window, value="Profit or Loss")
report_box = ctk.CTkComboBox(
    window,
    values=["Profit or Loss", "Financial Position", "Cash Flows"],
    variable=report_type,
    command=report_code
    )
report_box.grid(row=1, column=1, padx=10, pady=10, sticky="ne")

upload_button = ctk.CTkButton(
    display_screen,
    text="Upload File",
    command=upload_button_callback,
)
upload_button.pack(side="top", expand=True)

download_button = ctk.CTkButton(
    window,
    text="Download CSV",
    command=download_button_callback,
)
download_button.grid(row=2, column=1, padx=10, pady=10, sticky="se")

window.mainloop()