import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from mysql.connector import connect
import mysql, random
from datetime import datetime
from tkinter import ttk, messagebox
from tkcalendar import Calendar

primary_color = "#202d36"
secondary_color = "#2e3841"
tertiary_color = "#508ab2"
edit_color = "#30a27c"
white_font_color = "#bdc1c3"
faded_white = "#888888"

font_name = "Inder"

user = 'root'
host = '127.0.0.1'
database = 'logistics-management'
password = 'Siddhesh@54321'

connection = mysql.connector.connect(user=user, host=host, database=database, password=password)
cursor = connection.cursor()


def destroy_frame(fr):
    for widget in fr.winfo_children():
        widget.destroy()


def label(fr, txt, f_size, f_style, fg_c, bg_c, x, y):
    text_var = tk.StringVar()
    text_var.set(txt)
    lbl = tk.Label(fr, textvariable=text_var, font=(font_name, f_size, f_style), fg=fg_c, bg=bg_c)
    lbl.place(relx=x, rely=y)
    return lbl, text_var


def frame(fr, bg_c, border, x, y, x1, y1, width, height):
    frm = tk.Frame(fr, width=400, height=50, bg=bg_c, borderwidth=border, relief='solid')
    frm.place(relx=x, rely=y, x=x1, y=y1, width=width, height=height)
    return frm


def image(fr, icon_path, bg_c, x, y, x1, y1, width, height):
    icon = Image.open(icon_path).resize((width, height))
    fr.icon_image = ImageTk.PhotoImage(icon)
    icon_label = tk.Label(fr, image=fr.icon_image, text="", bg=bg_c)
    icon_label.icon = fr.icon_image
    icon_label.place(relx=x, rely=y, x=x1, y=y1)
    return fr.icon_image


def button(fr, x, y, x1, y1, width, height, txt, f_size, f_style, fg_c, bg_c, comm, img):
    btn = tk.Button(fr, text=txt, font=(font_name, f_size, f_style), fg=fg_c, borderwidth=0, cursor='hand2',
                    command=comm, bg=bg_c, image=img, compound=tk.LEFT, padx=15)
    btn.place(relx=x, rely=y, x=x1, y=y1, width=width, height=height)
    return btn


def entry(fr, txt, f_size, bg_c, fg_c, state, border, x, y, x1, y1, width, height):
    str_var = tk.StringVar()
    str_var.set(txt)
    ent = tk.Entry(fr, textvariable=str_var, font=(font_name, f_size), bg=bg_c, fg=fg_c, borderwidth=border, state=state)
    ent.place(relx=x, rely=y, x=x1, y=y1, width=width, height=height)
    return ent, str_var


def frame_entry(fr, txt, x, y, x1, y1, width, height):
    entry_frame = frame(fr, secondary_color, 1, x, y, x1, y1, width, height)
    user_entry, user_entry_var = entry(entry_frame, txt, 13, secondary_color, white_font_color, "normal", 0, 0, 0, 3, 0, width - 10, height - 3)
    return user_entry, user_entry_var, entry_frame


def show_password(password_entry):
    if password_entry.cget("show") == '●':
        password_entry.configure(show="")
    else:
        password_entry.configure(show="●")


def profile(fr, txt, file_path):
    f = open(file_path, 'r')
    index = f.read().strip()
    f.close()

    if index != '0':
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (index,))
        result = cursor.fetchone()

        profile_frame = frame(fr, secondary_color, 0, 0.6, 0.02, 0, 0, 400, 50)
        label(profile_frame, result[3], 14, "", white_font_color, secondary_color, 0.52, 0.05)
        label(profile_frame, result[4], 10, "", white_font_color, secondary_color, 0.52, 0.5)

        image(profile_frame, "icons/profile-icon.png", secondary_color, 0.43, 0.25, 0, 0, 24, 24)

        calendar_frame = frame(fr, secondary_color, 0, 0.03, 0.02, 0, 0, 310, 50)
        image(calendar_frame, "icons/calendar-icon.png", secondary_color, 0, 0, 5, 10, 24, 24)

        def get_current_time():
            today = datetime.today()
            current_date = today.strftime("%d %b, %Y %I:%M %p")
            time_label_var.set("Date - Time:{0}".format(current_date))
            time_label.after(1000, get_current_time)

        time_label, time_label_var = label(calendar_frame, "", 12, "", white_font_color, secondary_color, 0.14, 0.25)
        get_current_time()

        label(fr, f"{txt}", 20, "", white_font_color, secondary_color, 0.03, 0.1)


def menus(fr, icon_path, text, y, command, fg_c, flag):
    icon = Image.open(icon_path).resize((24, 24))
    photo_image = ImageTk.PhotoImage(icon)
    btn = tk.Button(fr, text=text, font=(font_name, 14), bg=primary_color, borderwidth=0, padx=30,
                    image=photo_image, compound=tk.LEFT, cursor="hand2", fg=fg_c, command=command,
                    anchor='w')
    btn.image = photo_image
    if flag:
        btn.bind("<Enter>", func=lambda e: btn.config(fg=tertiary_color))
    else:
        btn.bind("<Enter>", func=lambda e: btn.config(fg=tertiary_color))
        btn.bind("<Leave>", func=lambda e: btn.config(fg=white_font_color))
    btn.place(rely=y, width=288, height=40)


def canvas_text(window, fr, x, y, txt, bg_c, f_size, f_style, flag):

    def copy_to_clipboard(event, t):
        window.clipboard_clear()
        window.clipboard_append(t)
        window.update_idletasks()
        print(f"Copied to clipboard: {t}")

    def on_enter(frame_canvas, event, t):
        frame_canvas.itemconfig(t, fill=tertiary_color)

    def on_leave(frame_canvas, event, t):
        frame_canvas.itemconfig(t, fill=white_font_color)

    text = fr.create_text(x, y, text=txt, font=(font_name, f_size, f_style), fill=bg_c, anchor='nw')
    if flag:
        fr.tag_bind(text, "<Button-1>", lambda event: copy_to_clipboard(event, txt))
        fr.tag_bind(text, "<Enter>", lambda event: on_enter(fr, event, text))
        fr.tag_bind(text, "<Leave>", lambda event: on_leave(fr, event, text))
    return text


def canvas_frame(fr, border, bg_c, x, y, width, height):
    canvas_fr = tk.Canvas(fr, bg=bg_c, width=width, height=height, highlightthickness=border)
    canvas_fr.pack(padx=x, pady=y, anchor='nw')
    return canvas_fr


def get_current_date():
    today = datetime.today()
    current_date = today.strftime("%d %b, %Y")
    return current_date


def generate_id(rand_id):
    random_number = random.randint(1000, 9999)
    if random_number == rand_id:
        generate_id(rand_id)
    else:
        return random_number


def combobox(f, x, y, options):
    select = tk.StringVar()
    box = ttk.Combobox(f, values=options, textvariable=select, state='readonly')
    box.place(relx=x, rely=y)
    box.current(0)
    return select


def sign_out(file_path):
    request = messagebox.askquestion("Application", "Are you sure you want to sign out?")
    if request == 'yes':
        file = open(file_path, 'w')
        file.write('0')
        file.close()


def open_calendar(f, x, y):
    calendar_frame = frame(f, secondary_color, 1, x, y, 0, 0, 150, 26)
    date_label, date_label_var = label(calendar_frame, "Select Date", 11, "bold",
                                            white_font_color, secondary_color, 0, 0)
    calendar_image = image(calendar_frame, "icons/calendar-icon.png", secondary_color, 0.73, 0, 0,
                                0, 24, 24)

    def open_calendar(window):
        top = tk.Toplevel(window)
        cal = Calendar(top, selectmode='day', year=datetime.now().year, month=datetime.now().month,
                       day=datetime.now().day)
        cal.pack(pady=20)

        def grab_date():
            select_date = cal.get_date()
            date_label_var.set(select_date)
            top.destroy()

        tk.Button(top, text="Select", command=grab_date).pack()

    button(calendar_frame, 0.73, 0, 0, 0, 30, 22, "", 11, "bold", secondary_color,
                secondary_color, lambda: open_calendar(f), calendar_image)
    return date_label_var
