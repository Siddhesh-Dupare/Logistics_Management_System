import tkinter as tk
from tkinter import messagebox, ttk

import utility as util
import mysql
from mysql.connector import errorcode


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("931x700")
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Reports, Invoice, Tracking, Shipments, Warehouse, Transport, Users, Orders, Quotation, Dashboard, Main):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        def check_status():
            f = open("login_status/status.txt", 'r')
            index = f.read().strip()
            f.close()
            return index

        if check_status() == '0':
            self.show_frame(Main)
        else:
            self.show_frame(Dashboard)

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()

        if controller == Main:
            self.geometry("931x700")
            self.title("Logistics Management System")
        elif controller == Dashboard:
            self.geometry("1440x830")
            frame.connection.commit()
            frame.display_summary_frames()
            frame.display_active_quotes()
            util.profile(frame.main, "Dashboard", "login_status/status.txt")
        elif controller == Quotation:
            frame.connection.commit()
            frame.display_quotation()
            util.profile(frame.main, "Quotation", "login_status/status.txt")
        elif controller == Orders:
            frame.connection.commit()
            frame.display_orders()
            util.profile(frame.main, "Orders", "login_status/status.txt")
        elif controller == Users:
            frame.connection.commit()
            frame.display_driver()
            frame.display_users()
            util.profile(frame.main, "Users", "login_status/status.txt")
        elif controller == Transport:
            frame.connection.commit()
            frame.display_transport()
            util.profile(frame.main, "Transport", "login_status/status.txt")
        elif controller == Warehouse:
            frame.connection.commit()
            frame.display_warehouse_commodities()
            util.profile(frame.main, "Warehouse", "login_status/status.txt")
        elif controller == Shipments:
            frame.connection.commit()
            frame.display_shipments()
            util.profile(frame.main, "Shipments", "login_status/status.txt")
        elif controller == Tracking:
            frame.connection.commit()
            frame.display_tracking()
            util.profile(frame.main, "Tracking", "login_status/status.txt")
        elif controller == Invoice:
            frame.connection.commit()
            frame.display_invoice()
            util.profile(frame.main, "Invoice", "login_status/status.txt")
        elif controller == Reports:
            frame.connection.commit()
            util.profile(frame.main, "Reports", "login_status/status.txt")


class Main(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=util.secondary_color)
        self.controller = controller
        util.destroy_frame(self)

        self.connection = mysql.connector.connect(user=util.user, host=util.host, database=util.database,
                                                  password=util.password)
        self.cursor = self.connection.cursor()

        util.label(self, "Login", 28, "bold", util.white_font_color, util.secondary_color, 0.3, 0.1)
        util.label(self, "Please, login to your account", 14, "", util.white_font_color, util.secondary_color,
                   0.3, 0.17)

        util.label(self, "Username", 14, "", util.white_font_color, util.secondary_color, 0.3, 0.26)
        username_frame = util.frame(self, util.secondary_color, 1, 0.31, 0.3, -10, 5, 400, 50)
        util.image(username_frame, "icons/email-icon.png", util.secondary_color, 0, 0, 5, 10, 24, 24)
        username_entry = util.entry(username_frame, "", 14, util.secondary_color, util.white_font_color, "normal", 0, 0, 0,
                                    40, 8,
                                    350, 30)
        username_label, username_label_var = util.label(self, "", 10, "", "#e42510", util.secondary_color, 0.3, 0.378)

        util.label(self, "Password", 14, "", util.white_font_color, util.secondary_color, 0.3, 0.41)
        password_frame = util.frame(self, util.secondary_color, 1, 0.31, 0.45, -10, 5, 400, 50)
        util.image(password_frame, "icons/key-icon.png", util.secondary_color, 0, 0, 7, 10, 24, 24)
        password_entry = util.entry(password_frame, "", 14, util.secondary_color, util.white_font_color, "normal", 0, 0, 0,
                                    40, 8,
                                    350, 30)
        eye_icon = util.image(password_frame, "icons/eye-icon.png", util.secondary_color, 0.9, 0, 7, 5, 24, 24)
        util.button(password_frame, 0.9, 0, 5, 10, 30, 20, "", 0, "", None, util.secondary_color,
                    lambda: util.show_password(password_entry), eye_icon)
        password_label, password_label_var = util.label(self, "", 10, "", "#e42510", util.secondary_color, 0.3, 0.53)

        def login_command():
            username_placeholder = "Username"
            password_placeholder = "Password"

            username = username_entry.get()
            password = password_entry.get()

            if (not username or password == username_placeholder) \
                    and (not password or password == password_placeholder):
                username_label.configure(text="Username field should not empty")
                password_label.configure(text="Password field should not empty")
            elif not username or username == username_placeholder:
                username_label.configure(text="Username field should not empty")
                password_label.configure(text="")
            elif not password or password == password_placeholder:
                password_label.configure(text="Password field should not empty")
                username_label.configure(text="")
            else:
                password_label.configure(text="")
                username_label.configure(text="")

                try:
                    query = "SELECT * FROM users WHERE username = %s AND password = %s"
                    value = (username, password)
                    self.cursor.execute(query, value)
                    result = self.cursor.fetchall()

                    if result:
                        for i in result:
                            f = open("login_status/status.txt", 'w')
                            f.write(str(i[0]))
                            f.close()
                            messagebox.showinfo("Database", "Sign In Successful")
                            self.controller.show_frame(Dashboard)
                    else:
                        messagebox.showerror("Database", "Sign In Failed")

                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_DUP_ENTRY:
                        messagebox.showerror("Database Error 1",
                                             "Username already exists. Please choose a different username.")
                    elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                        messagebox.showerror("Database Error 2", "Something is wrong with your username or password.")
                    elif err.errno == errorcode.ER_BAD_DB_ERROR:
                        messagebox.showerror("Database Error 3", "Database does not exist.")
                    else:
                        messagebox.showerror("Database Error 4", f"An error occurred: {err}")

        util.button(self, 0.29, 0.63, 10, 5, 400, 50, "Login", 16, "bold", util.white_font_color, util.tertiary_color,
                    login_command, "")


class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=util.secondary_color)
        self.controller = controller
        util.destroy_frame(self)

        self.connection = mysql.connector.connect(user=util.user, host=util.host, database=util.database,
                                                  password=util.password)
        self.cursor = self.connection.cursor()

        menu_frame = tk.Frame(self, bg=util.primary_color)
        menu_frame.place(relx=0, rely=0, width=290, height=900)

        self.main = util.frame(self, util.secondary_color, 0, 0.2, 0, 0, 0, 1170, 830)

        util.profile(self.main, "Dashboard", "login_status/status.txt")

        util.menus(self, "icons/dashboard-menu-icon.png", "Dashboard", 0.2, lambda: self.controller.show_frame(Dashboard),
                   util.tertiary_color, True)
        util.menus(self, "icons/quotation-menu-icon.png", "Quotation", 0.25, lambda: self.controller.show_frame(Quotation),
                   util.white_font_color, False)
        util.menus(self, "icons/orders-menu-icon.png", "Orders", 0.3, lambda: self.controller.show_frame(Orders),
                   util.white_font_color, False)
        util.menus(self, "icons/user-menu-icon.png", "Users", 0.35, lambda: self.controller.show_frame(Users),
                   util.white_font_color, False)
        util.menus(self, "icons/transport-menu-icon.png", "Transport", 0.4,
                   lambda: self.controller.show_frame(Transport),
                   util.white_font_color, False)
        util.menus(self, "icons/warehouse-menu-icon.png", "Warehouse", 0.45,
                   lambda: self.controller.show_frame(Warehouse),
                   util.white_font_color, False)
        util.menus(self, "icons/shipment-menu-icon.png", "Shipments", 0.5,
                   lambda: self.controller.show_frame(Shipments),
                   util.white_font_color, False)
        util.menus(self, "icons/tracking-menu-icon.png", "Tracking", 0.55,
                   lambda: self.controller.show_frame(Tracking),
                   util.white_font_color, False)
        util.menus(self, "icons/invoice-menu-icon.png", "Invoice", 0.6, lambda: self.controller.show_frame(Invoice),
                   util.white_font_color, False)
        util.menus(self, "icons/reports-menu-icon.png", "Reports", 0.65, lambda: self.controller.show_frame(Reports),
                   util.white_font_color, False)

        def sign_out_button():
            util.sign_out("login_status/status.txt")
            self.controller.show_frame(Main)

        util.menus(self, "icons/exit-menu-icon.png", "Sign Out", 0.8, sign_out_button,
                   util.white_font_color, False)

        active_quotation_frame = util.frame(self.main, util.primary_color, 0, 0.55, 0.3, 0, 0, 500, 550)

        util.label(active_quotation_frame, "Active Quotations", 15, "bold", util.white_font_color, util.primary_color, 0.03, 0.02)

        self.scrollbar_window = util.frame(active_quotation_frame, util.primary_color, 1, 0, 0.1, 0, 0, 500, 540)

        self.display_summary_frames()
        self.display_active_quotes()

    def display_summary_frames(self):
        def create_frames(frame_text, values, x, y):
            orders_frame = util.frame(self.main, util.primary_color, 1, x, y, 0, 0, 200, 100)
            util.label(orders_frame, frame_text, 12, "bold", util.white_font_color, util.primary_color, 0.03, 0.06)
            data_frame = util.frame(orders_frame, util.white_font_color, 0, 0, 0.4, 0, 0, 200, 60)
            util.label(data_frame, values, 20, "bold", util.secondary_color, util.white_font_color, 0.4, 0.2)

        def count_query(search_query):
            self.cursor.execute(search_query)
            result = self.cursor.fetchall()
            return result[0]

        create_frames("Total Orders", count_query("SELECT COUNT(*) FROM orders"), 0.03, 0.16)
        create_frames("Total Shipped", count_query("SELECT COUNT(*) FROM transport"), 0.25, 0.16)
        create_frames("Delivered", count_query("SELECT COUNT(*) FROM orders WHERE delivery_status = 'DELIVERED'"), 0.47, 0.16)
        create_frames("In Progress", count_query("SELECT COUNT(*) FROM orders"), 0.69, 0.16)

    def display_active_quotes(self):
        util.destroy_frame(self.scrollbar_window)

        query = "SELECT quotation.client_name, invoice.status, orders.delivery_status FROM ((quotation INNER JOIN invoice ON quotation.quotation_id = invoice.user_id) INNER JOIN orders ON quotation.quotation_id = orders.user_id)"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if results:
            header_canvas = util.canvas_frame(self.scrollbar_window, 1, util.primary_color, 0.03, 0, 1100, 30)

            canvas = tk.Canvas(self.scrollbar_window, bg=util.primary_color, highlightthickness=0,
                               scrollregion=(0, 0, 2000, 5000))
            canvas.pack(expand=True, fill='both')

            vertical_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='vertical', command=canvas.yview)
            horizontal_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='horizontal', command=canvas.xview)

            canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
            vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
            horizontal_scrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')

            canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-int(event.delta / 120), "units"))
            canvas.bind("<Control MouseWheel>", lambda event: canvas.xview_scroll(-int(event.delta / 120), "units"))

            def sync_scroll(*args):
                canvas.xview(*args)
                header_canvas.xview(*args)

            canvas.bind("<Configure>", lambda event: header_canvas.configure(scrollregion=(0, 0, 2000, 5000)))

            header_canvas.configure(xscrollcommand=lambda *args: sync_scroll('moveto', args[0]))
            canvas.configure(xscrollcommand=lambda *args: sync_scroll('moveto', args[0]))

            util.canvas_text(self.main, header_canvas, 20, 6, "Name", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 200, 6, "Amount", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 350, 6, "Status", util.white_font_color, 13, "bold", False)

            frame = tk.Frame(canvas, bg=util.secondary_color, borderwidth=1, relief='solid')
            canvas.create_window(0, 0, window=frame, anchor='nw')

            for index, result in enumerate(results):
                frame_canvas = util.canvas_frame(frame, 1, util.primary_color, 0, 4, 2000, 40)

                util.canvas_text(self.main, frame_canvas, 20, 12, result[0], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 200, 12, result[1], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 350, 12, result[2], util.white_font_color, 13, "", True)


class Quotation(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=util.secondary_color)
        self.controller = controller
        util.destroy_frame(self)

        self.connection = mysql.connector.connect(user=util.user, host=util.host, database=util.database,
                                                  password=util.password)
        self.cursor = self.connection.cursor()

        menu_frame = tk.Frame(self, bg=util.primary_color)
        menu_frame.place(relx=0, rely=0, width=290, height=900)

        self.main = util.frame(self, util.secondary_color, 0, 0.2, 0, 0, 0, 1170, 830)

        util.profile(self.main, "Quotation", "login_status/status.txt")

        util.menus(self, "icons/dashboard-menu-icon.png", "Dashboard", 0.2, lambda: self.controller.show_frame(Dashboard),
                   util.white_font_color, False)
        util.menus(self, "icons/quotation-menu-icon.png", "Quotation", 0.25, lambda: self.controller.show_frame(Quotation),
                   util.tertiary_color, True)
        util.menus(self, "icons/orders-menu-icon.png", "Orders", 0.3, lambda: self.controller.show_frame(Orders),
                   util.white_font_color, False)
        util.menus(self, "icons/user-menu-icon.png", "Users", 0.35, lambda: self.controller.show_frame(Users),
                   util.white_font_color, False)
        util.menus(self, "icons/transport-menu-icon.png", "Transport", 0.4,
                   lambda: self.controller.show_frame(Transport),
                   util.white_font_color, False)
        util.menus(self, "icons/warehouse-menu-icon.png", "Warehouse", 0.45,
                   lambda: self.controller.show_frame(Warehouse),
                   util.white_font_color, False)
        util.menus(self, "icons/shipment-menu-icon.png", "Shipments", 0.5,
                   lambda: self.controller.show_frame(Shipments),
                   util.white_font_color, False)
        util.menus(self, "icons/tracking-menu-icon.png", "Tracking", 0.55,
                   lambda: self.controller.show_frame(Tracking),
                   util.white_font_color, False)
        util.menus(self, "icons/invoice-menu-icon.png", "Invoice", 0.6, lambda: self.controller.show_frame(Invoice),
                   util.white_font_color, False)
        util.menus(self, "icons/reports-menu-icon.png", "Reports", 0.65, lambda: self.controller.show_frame(Reports),
                   util.white_font_color, False)

        def sign_out_button():
            util.sign_out("login_status/status.txt")
            self.controller.show_frame(Main)

        util.menus(self, "icons/exit-menu-icon.png", "Sign Out", 0.8, sign_out_button,
                   util.white_font_color, False)

        create_btn = util.image(self.main, "icons/add-customer-icon.png", util.tertiary_color, 0.75, 0.1, 0, 0, 20, 20)

        def create_quotation():
            top_level = tk.Toplevel()
            top_level.title("Request Quotation")
            top_level.geometry("500x400")
            top_level.config(bg=util.secondary_color)
            util.destroy_frame(top_level)

            util.label(top_level, "Client Name", 13, "bold", util.white_font_color, util.secondary_color, 0.17, 0.1)
            client_name, client_name_var, client_name_frame = util.frame_entry(top_level, "", 0.4, 0.1, 0, 0, 220, 30)

            util.label(top_level, "Company Name", 13, "bold", util.white_font_color, util.secondary_color, 0.11, 0.2)
            company_name, company_name_var, company_name_frame = util.frame_entry(top_level, "", 0.4, 0.2, 0, 0, 220, 30)

            util.label(top_level, "Company Website", 13, "bold", util.white_font_color, util.secondary_color, 0.07, 0.3)
            company_website, company_website_var, company_website_frame = util.frame_entry(top_level, "", 0.4, 0.3, 0, 0, 220, 30)

            util.label(top_level, "Client Email", 13, "bold", util.white_font_color, util.secondary_color, 0.17, 0.4)
            email, email_var, email_frame = util.frame_entry(top_level, "", 0.4, 0.4, 0, 0, 220, 30)

            util.label(top_level, "Contact No.", 13, "bold", util.white_font_color, util.secondary_color, 0.17, 0.5)
            contact_no, contact_no_var, contact_no_frame = util.frame_entry(top_level, "", 0.4, 0.5, 0, 0, 220, 30)

            def send_quotation_button():
                search_query = "SELECT id FROM quotation"
                self.cursor.execute(search_query)
                result = self.cursor.fetchall()

                query = "INSERT INTO quotation (quotation_id, user_id, client_name, company_name, company_website, client_email," \
                        "contact_no, status, created_on) VALUES (%s, %s, %s, %s, %s, %s, %s, 'ACTIVE', %s)"
                values = (f"ID-{util.generate_id(result)}", f"{util.generate_id(result)}", client_name_var.get(), company_name_var.get(),
                          company_website_var.get(), email_var.get(), contact_no_var.get(), util.get_current_date())
                self.cursor.execute(query, values)
                self.connection.commit()

                result_button = messagebox.showinfo("Application", "Quotation created!")
                if result_button == 'ok':
                    top_level.destroy()
                    self.display_quotation()

            util.button(top_level, 0.25, 0.8, 0, 0, 100, 35, "Send", 15, "bold", util.secondary_color, util.edit_color,
                        send_quotation_button, "")

            def back_button():
                top_level.destroy()

            util.button(top_level, 0.55, 0.8, 0, 0, 100, 35, "Cancel", 15, "bold", util.secondary_color, "red",
                        back_button, "")

            top_level.resizable(False, False)
            top_level.mainloop()

        def update_quotation():
            top_level = tk.Toplevel()
            top_level.title("Create Booking")
            top_level.geometry("500x400")
            top_level.config(bg=util.secondary_color)

            util.label(top_level, "Quotation Id", 12, "bold", util.white_font_color, util.secondary_color, 0.07, 0.03)
            request_id, request_id_var, request_id_frame = util.frame_entry(top_level, "", 0.33, 0.03, 0, 0, 200, 30)

            def search_quotation_id():
                search_query = f"SELECT * FROM quotation WHERE quotation_id = '{request_id_var.get()}'"
                self.cursor.execute(search_query)
                result = self.cursor.fetchone()

                client_name_var.set(result[3])
                company_name_var.set(result[4])
                company_website_var.set(result[5])
                email_var.set(result[6])
                contact_no_var.set(result[7])

            util.button(top_level, 0.77, 0.03, 0, 0, 80, 30, "Search", 12, "bold", util.white_font_color,
                        util.primary_color, search_quotation_id, "")

            util.label(top_level, "Client Name", 13, "bold", util.white_font_color, util.secondary_color, 0.17,
                       0.18)
            client_name, client_name_var, client_name_frame = util.frame_entry(top_level, "", 0.4, 0.18, 0, 0, 220, 30)

            util.label(top_level, "Company Name", 13, "bold", util.white_font_color, util.secondary_color, 0.11,
                       0.28)
            company_name, company_name_var, company_name_frame = util.frame_entry(top_level, "", 0.4, 0.28, 0, 0, 220, 30)

            util.label(top_level, "Company Website", 13, "bold", util.white_font_color, util.secondary_color,
                       0.07, 0.38)
            company_website, company_website_var, company_website_frame = util.frame_entry(top_level, "", 0.4, 0.38, 0, 0, 220, 30)

            util.label(top_level, "Client Email", 13, "bold", util.white_font_color, util.secondary_color, 0.17,
                       0.48)
            email, email_var, email_frame = util.frame_entry(top_level, "", 0.4, 0.48, 0, 0, 220, 30)

            util.label(top_level, "Contact No.", 13, "bold", util.white_font_color, util.secondary_color, 0.17,
                       0.58)
            contact_no, contact_no_var, contact_no_frame = util.frame_entry(top_level, "", 0.4, 0.58, 0, 0, 220, 30)

            def update_quotation_button():
                update_query = "UPDATE quotation SET client_name = %s, company_name = %s, company_website = %s, client_email = %s, contact_no = %s WHERE quotation_id = %s"
                values = (client_name_var.get(), company_name_var.get(), company_website_var.get(), email_var.get(), contact_no_var.get(), request_id_var.get())
                self.cursor.execute(update_query, values)
                self.connection.commit()
                result = messagebox.showinfo("Application", "Quotation updated")
                if result == 'ok':
                    top_level.destroy()
                    self.display_quotation()

            util.button(top_level, 0.25, 0.8, 0, 0, 100, 35, "Update", 15, "bold", util.secondary_color,
                        util.edit_color,
                        update_quotation_button, "")

            def back_button():
                top_level.destroy()

            util.button(top_level, 0.55, 0.8, 0, 0, 100, 35, "Cancel", 15, "bold", util.secondary_color, "red",
                        back_button, "")

        util.button(self.main, 0.55, 0.1, 0, 0, 210, 50, "Update Quotation", 13, "bold", util.tertiary_color,
                    util.primary_color, update_quotation, create_btn)

        util.button(self.main, 0.75, 0.1, 0, 0, 210, 50, "Create Quotation", 13, "bold", util.tertiary_color,
                    util.primary_color, create_quotation, create_btn)

        self.scrollbar_window = util.frame(self.main, util.primary_color, 1, 0.03, 0.2, 0, 0, 1090, 650)

        self.display_quotation()

    def display_quotation(self):
        util.destroy_frame(self.scrollbar_window)

        query = "SELECT * FROM quotation"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if results:
            header_canvas = util.canvas_frame(self.scrollbar_window, 1, util.primary_color, 0.03, 0, 1100, 30)

            canvas = tk.Canvas(self.scrollbar_window, bg=util.primary_color, highlightthickness=0,
                               scrollregion=(0, 0, 2000, 5000))
            canvas.pack(expand=True, fill='both')

            vertical_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='vertical', command=canvas.yview)
            horizontal_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='horizontal', command=canvas.xview)

            canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
            vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
            horizontal_scrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')

            canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-int(event.delta / 120), "units"))
            canvas.bind("<Control MouseWheel>", lambda event: canvas.xview_scroll(-int(event.delta / 120), "units"))

            def sync_scroll(*args):
                canvas.xview(*args)
                header_canvas.xview(*args)

            canvas.bind("<Configure>", lambda event: header_canvas.configure(scrollregion=(0, 0, 2000, 5000)))

            header_canvas.configure(xscrollcommand=lambda *args: sync_scroll('moveto', args[0]))
            canvas.configure(xscrollcommand=lambda *args: sync_scroll('moveto', args[0]))

            util.canvas_text(self.main, header_canvas, 30, 6, "ID", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 160, 6, "Name", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 450, 6, "Company Name", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 700, 6, "Company Website", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 1000, 6, "Email", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 1300, 6, "Contact Number", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 1500, 6, "Created On", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 1650, 6, "Status", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 1800, 6, "Action", util.white_font_color, 13, "bold", False)

            frame = tk.Frame(canvas, bg=util.secondary_color, borderwidth=1, relief='solid')
            canvas.create_window(0, 0, window=frame, anchor='nw')

            for index, result in enumerate(results):
                frame_canvas = util.canvas_frame(frame, 1, util.primary_color, 0, 4, 2000, 40)

                util.canvas_text(self.main, frame_canvas, 30, 12, result[1], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 160, 12, result[3], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 450, 12, result[4], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 700, 12, result[5], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1000, 12, result[6], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1300, 12, result[7], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1500, 12, result[9], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1650, 12, result[8], util.white_font_color, 13, "", True)

                def recycle_command(res):
                    def command():
                        question = messagebox.askquestion("Application", "Are you sure you want to delete")
                        if question == 'yes':
                            delete_query = f"DELETE FROM quotation WHERE id = {res[0]}"
                            self.cursor.execute(delete_query)
                            self.connection.commit()
                            self.display_quotation()

                    return command

                recycle_callback = recycle_command(result)
                recycle_button = util.image(frame_canvas, "icons/recycle-bin-icon.png", util.primary_color, 0.89, 0.22, 10, 0,
                                           20, 20)
                util.button(frame_canvas, 0.89, 0.22, 12, 2, 20, 20, "", 12, "", util.primary_color, util.primary_color,
                            recycle_callback, recycle_button)
        else:
            util.label(self.scrollbar_window, "No Quotation", 20, "bold", util.white_font_color,
                       util.primary_color, 0.4, 0.45)


class Orders(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=util.secondary_color)
        self.controller = controller
        util.destroy_frame(self)

        self.connection = mysql.connector.connect(user=util.user, host=util.host, database=util.database,
                                                  password=util.password)
        self.cursor = self.connection.cursor()

        menu_frame = tk.Frame(self, bg=util.primary_color)
        menu_frame.place(relx=0, rely=0, width=290, height=900)

        self.main = util.frame(self, util.secondary_color, 0, 0.2, 0, 0, 0, 1170, 830)

        util.profile(self.main, "Orders", "login_status/status.txt")

        util.menus(self, "icons/dashboard-menu-icon.png", "Dashboard", 0.2, lambda: self.controller.show_frame(Dashboard),
                   util.white_font_color, False)
        util.menus(self, "icons/quotation-menu-icon.png", "Quotation", 0.25, lambda: self.controller.show_frame(Quotation),
                   util.white_font_color, False)
        util.menus(self, "icons/orders-menu-icon.png", "Orders", 0.3, lambda: self.controller.show_frame(Orders),
                   util.tertiary_color, True)
        util.menus(self, "icons/user-menu-icon.png", "Users", 0.35, lambda: self.controller.show_frame(Users),
                   util.white_font_color, False)
        util.menus(self, "icons/transport-menu-icon.png", "Transport", 0.4,
                   lambda: self.controller.show_frame(Transport),
                   util.white_font_color, False)
        util.menus(self, "icons/warehouse-menu-icon.png", "Warehouse", 0.45,
                   lambda: self.controller.show_frame(Warehouse),
                   util.white_font_color, False)
        util.menus(self, "icons/shipment-menu-icon.png", "Shipments", 0.5,
                   lambda: self.controller.show_frame(Shipments),
                   util.white_font_color, False)
        util.menus(self, "icons/tracking-menu-icon.png", "Tracking", 0.55,
                   lambda: self.controller.show_frame(Tracking),
                   util.white_font_color, False)
        util.menus(self, "icons/invoice-menu-icon.png", "Invoice", 0.6, lambda: self.controller.show_frame(Invoice),
                   util.white_font_color, False)
        util.menus(self, "icons/reports-menu-icon.png", "Reports", 0.65, lambda: self.controller.show_frame(Reports),
                   util.white_font_color, False)

        def sign_out_button():
            util.sign_out("login_status/status.txt")
            self.controller.show_frame(Main)

        util.menus(self, "icons/exit-menu-icon.png", "Sign Out", 0.8, sign_out_button,
                   util.white_font_color, False)
        self.scrollbar_window = util.frame(self.main, util.primary_color, 1, 0.03, 0.2, 0, 0, 1090, 650)

        def create_order():
            top_level = tk.Toplevel()
            top_level.title("Create Booking")
            top_level.geometry("900x600")
            top_level.config(bg=util.secondary_color)

            util.label(top_level, "Quotation ID", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.035)
            quotation_id, quotation_id_var, quotation_id_frame = util.frame_entry(top_level, "", 0.33, 0.03, 0, 0, 200, 30)

            def search_quotation_id():
                search_query = f"SELECT quotation.client_name FROM quotation WHERE quotation_id = '{quotation_id_var.get()}'"
                self.cursor.execute(search_query)
                result = self.cursor.fetchone()

                client_name_var.set(result[0])

            util.button(top_level, 0.77, 0.03, 0, 0, 80, 30, "Search", 12, "bold", util.white_font_color,
                        util.primary_color, search_quotation_id, "")

            driver_details_frame = util.frame(top_level, util.tertiary_color, 1, 0.02, 0.1, 0, 0, 850, 30)
            util.label(driver_details_frame, "Personal Details", 13, "bold", util.white_font_color,
                       util.tertiary_color, 0.03, 0.02)

            util.label(top_level, "Client Name", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.18)
            client_name, client_name_var, client_name_frame = util.frame_entry(top_level, "", 0.22, 0.18, 0, 0, 200, 30)

            order_details_frame = util.frame(top_level, util.tertiary_color, 1, 0.02, 0.25, 0, 0, 850, 30)
            util.label(order_details_frame, "Order Details", 13, "bold", util.white_font_color,
                       util.tertiary_color, 0.03, 0.02)

            util.label(top_level, "Product Description", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.32)
            product_description, product_description_var, product_description_frame = util.frame_entry(top_level, "", 0.25, 0.32, 0, 0, 200, 30)

            util.label(top_level, "Departure Date", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.39)
            departure_date = util.open_calendar(top_level, 0.25, 0.39)

            util.label(top_level, "Arrival Date", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.46)
            arrival_date = util.open_calendar(top_level, 0.25, 0.46)

            util.label(top_level, "Departure Location", 12, "bold", util.white_font_color, util.secondary_color, 0.5, 0.32)
            departure_location, departure_location_var, departure_location_frame = util.frame_entry(top_level, "", 0.7, 0.32, 0, 0, 200, 30)

            util.label(top_level, "Arrival Location", 12, "bold", util.white_font_color, util.secondary_color, 0.5, 0.39)
            arrival_location, arrival_location_var, arrival_location_frame = util.frame_entry(top_level, "", 0.7, 0.39, 0, 0, 200, 30)

            util.label(top_level, "Specification", 12, "bold", util.white_font_color, util.secondary_color, 0.5, 0.46)
            specificaiton, specificaiton_var, specificaiton_frame = util.frame_entry(top_level, "", 0.7, 0.46, 0, 0, 200, 30)

            def create_order_button():
                insert_query = "INSERT INTO orders (order_id, user_id, order_status, product_category, departure_date, arrival_date, departure_location, arrival_location, specification) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (f"OR-{util.generate_id('9893')}", quotation_id_var.get(), 'ACTIVE', product_description_var.get(), departure_date.get(), arrival_date.get(), departure_location_var.get(), arrival_location_var.get(), specificaiton_var.get())
                self.cursor.execute(insert_query, values)
                self.connection.commit()
                result = messagebox.showinfo("Application", "Order created successfully")
                if result == 'ok':
                    top_level.destroy()
                    self.display_orders()

            util.button(top_level, 0.25, 0.8, 0, 0, 100, 35, "Create", 15, "bold", util.secondary_color,
                        util.edit_color,
                        create_order_button, "")

            def back_button():
                top_level.destroy()

            util.button(top_level, 0.55, 0.8, 0, 0, 100, 35, "Cancel", 15, "bold", util.secondary_color, "red",
                        back_button, "")

            top_level.resizable(False, False)
            top_level.mainloop()

        create_btn = util.image(self.main, "icons/add-customer-icon.png", util.tertiary_color, 0.83, 0.1, 0, 0, 20, 20)
        util.button(self.main, 0.77, 0.1, 0, 0, 180, 50, "Create Order", 13, "bold", util.tertiary_color,
                    util.primary_color, create_order, create_btn)

        def update_order():
            top_level = tk.Toplevel()
            top_level.title("Update Order")
            top_level.geometry("900x600")
            top_level.config(bg=util.secondary_color)

            util.label(top_level, "Quotation ID", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.035)
            order_id, order_id_var, order_id_frame = util.frame_entry(top_level, "", 0.33, 0.03, 0, 0, 200,
                                                                                  30)

            def search_order_id():
                search_query = f"SELECT * FROM order WHERE order_id = '{order_id_var.get()}'"
                self.cursor.execute(search_query)
                result = self.cursor.fetchone()

                product_description_var.set(result[4])
                departure_date.set(result[5])
                arrival_date.set(result[6])
                departure_location_var.set(result[7])
                arrival_location_var.set(result[8])
                specification_var.set(result[9])

            util.button(top_level, 0.77, 0.03, 0, 0, 80, 30, "Search", 12, "bold", util.white_font_color,
                        util.primary_color, search_order_id, "")

            order_details_frame = util.frame(top_level, util.tertiary_color, 1, 0.02, 0.25, 0, 0, 850, 30)
            util.label(order_details_frame, "Order Details", 13, "bold", util.white_font_color,
                       util.tertiary_color, 0.03, 0.02)

            util.label(top_level, "Product Description", 12, "bold", util.white_font_color, util.secondary_color, 0.03,
                       0.32)
            product_description, product_description_var, product_description_frame = util.frame_entry(top_level, "",
                                                                                                       0.25, 0.32, 0, 0,
                                                                                                       200, 30)

            util.label(top_level, "Departure Date", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.39)
            departure_date = util.open_calendar(top_level, 0.25, 0.39)

            util.label(top_level, "Arrival Date", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.46)
            arrival_date = util.open_calendar(top_level, 0.25, 0.46)

            util.label(top_level, "Departure Location", 12, "bold", util.white_font_color, util.secondary_color, 0.5,
                       0.32)
            departure_location, departure_location_var, departure_location_frame = util.frame_entry(top_level, "", 0.7,
                                                                                                    0.32, 0, 0, 200, 30)

            util.label(top_level, "Arrival Location", 12, "bold", util.white_font_color, util.secondary_color, 0.5,
                       0.39)
            arrival_location, arrival_location_var, arrival_location_frame = util.frame_entry(top_level, "", 0.7, 0.39,
                                                                                              0, 0, 200, 30)

            util.label(top_level, "Specification", 12, "bold", util.white_font_color, util.secondary_color, 0.5, 0.46)
            specification, specification_var, specification_frame = util.frame_entry(top_level, "", 0.7, 0.46, 0, 0,
                                                                                     200, 30)

            def update_order_button():
                update_query = "UPDATE orders SET product_category = %s, departure_date = %s, arrival_date = %s, departure_location = %s, arrival_location = %s, specification = %s, delivery_status = %s"
                values = (product_description_var.get(), departure_date.get(), arrival_date.get(), departure_location_var.get(), arrival_location_var.get(), specification_var.get(), 'NOT DELIVERED')
                self.cursor.execute(update_query, values)
                result = messagebox.askquestion("Application", "Order updated successfully")
                if result == 'ok':
                    top_level.destroy()
                    self.display_orders()

            util.button(top_level, 0.25, 0.8, 0, 0, 100, 35, "Update", 15, "bold", util.secondary_color,
                        util.edit_color,
                        update_order_button, "")

            def back_button():
                top_level.destroy()

            util.button(top_level, 0.55, 0.8, 0, 0, 100, 35, "Cancel", 15, "bold", util.secondary_color, "red",
                        back_button, "")

            top_level.resizable(False, False)
            top_level.mainloop()

        update_btn = util.image(self.main, "icons/add-customer-icon.png", util.tertiary_color, 0.6, 0.1, 0, 0, 20, 20)
        util.button(self.main, 0.6, 0.1, 0, 0, 180, 50, "Update Order", 13, "bold", util.tertiary_color,
                    util.primary_color, update_order, update_btn)

        self.display_orders()

    def display_orders(self):
        util.destroy_frame(self.scrollbar_window)

        query = "SELECT orders.order_id, orders.order_status, orders.product_category, orders.departure_date, orders.arrival_date, orders.departure_location, orders.arrival_location, orders.specification, invoice.total_amount, invoice.payment_type, quotation.client_name FROM ((orders INNER JOIN invoice ON invoice.user_id = orders.user_id) INNER JOIN quotation ON quotation.quotation_id = orders.user_id)"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if results:
            canvas = tk.Canvas(self.scrollbar_window, bg=util.primary_color, highlightthickness=0,
                               scrollregion=(0, 0, 1700, 5000))
            canvas.pack(expand=True, fill='both')

            vertical_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='vertical', command=canvas.yview)
            horizontal_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='horizontal', command=canvas.xview)

            canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
            vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
            horizontal_scrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')

            canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-int(event.delta / 120), "units"))
            canvas.bind("<Control MouseWheel>", lambda event: canvas.xview_scroll(-int(event.delta / 120), "units"))

            frame = tk.Frame(canvas, bg=util.secondary_color, borderwidth=1, relief='solid')
            canvas.create_window(0, 0, window=frame, anchor='nw')

            for index, result in enumerate(results):
                frame_canvas = util.canvas_frame(frame, 1, util.primary_color, 0, 4, 1350, 160)

                util.canvas_text(self.main, frame_canvas, 30, 12, f"{result[0]}", util.white_font_color, 12, "bold",
                                 False)
                frame_canvas.create_rectangle(30, 40, 170, 70, fill='green', outline=util.secondary_color)
                util.canvas_text(self.main, frame_canvas, 75, 47, f"{result[1]}", util.white_font_color, 12, "bold",
                                 False)
                util.canvas_text(self.main, frame_canvas, 30, 100, "Category", util.faded_white, 11, "bold", False)
                util.canvas_text(self.main, frame_canvas, 30, 120, f"{result[2]}", util.white_font_color, 12,
                                 "bold", False)

                util.canvas_text(self.main, frame_canvas, 250, 12, "Departure Date", util.faded_white, 11, "bold",
                                 False)
                util.canvas_text(self.main, frame_canvas, 250, 35, f"{result[3]}", util.white_font_color, 12,
                                 "bold", False)
                util.canvas_text(self.main, frame_canvas, 250, 100, "Arrival Date", util.faded_white, 11, "bold", False)
                util.canvas_text(self.main, frame_canvas, 250, 120, f"{result[4]}", util.white_font_color, 11, "bold",
                                 False)

                util.image(frame_canvas, "icons/location-icon.png", util.secondary_color, 0.35, 0.1, 0, 0, 24, 120)
                util.canvas_text(self.main, frame_canvas, 540, 18, f"{result[5]}", util.white_font_color, 11,
                                 "bold", False)
                util.canvas_text(self.main, frame_canvas, 540, 110, f"{result[6]}", util.white_font_color, 11,
                                 "bold", False)

                util.canvas_text(self.main, frame_canvas, 920, 12, "Specification", util.faded_white, 11, "bold", False)
                util.canvas_text(self.main, frame_canvas, 920, 35, f"{result[7]}", util.white_font_color, 12,
                                 "bold", False)
                util.canvas_text(self.main, frame_canvas, 920, 80, "Transport", util.faded_white, 11, "bold", False)
                util.canvas_text(self.main, frame_canvas, 920, 100, "{result[8]}", util.white_font_color, 12, "bold",
                                 False)
                util.canvas_text(self.main, frame_canvas, 920, 120, "Straight Engine", util.white_font_color, 12,
                                 "bold", False)

                util.canvas_text(self.main, frame_canvas, 1150, 12, f"{result[8]}", util.white_font_color, 15, "bold",
                                 False)
                util.canvas_text(self.main, frame_canvas, 1150, 50, "Payment Type", util.faded_white, 11, "bold", False)
                util.canvas_text(self.main, frame_canvas, 1150, 70, f"{result[9]}", util.white_font_color, 12, "bold",
                                 False)
                util.canvas_text(self.main, frame_canvas, 1150, 100, "Client Name", util.faded_white, 11, "bold", False)
                util.canvas_text(self.main, frame_canvas, 1150, 120, f"{result[10]}", util.white_font_color, 12,
                                 "bold", False)


class Users(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=util.secondary_color)
        self.controller = controller
        util.destroy_frame(self)

        self.connection = mysql.connector.connect(user=util.user, host=util.host, database=util.database,
                                                  password=util.password)
        self.cursor = self.connection.cursor()

        menu_frame = tk.Frame(self, bg=util.primary_color)
        menu_frame.place(relx=0, rely=0, width=290, height=900)

        self.main = util.frame(self, util.secondary_color, 0, 0.2, 0, 0, 0, 1170, 830)

        util.profile(self.main, "Users", "login_status/status.txt")

        util.menus(self, "icons/dashboard-menu-icon.png", "Dashboard", 0.2, lambda: self.controller.show_frame(Dashboard),
                   util.white_font_color, False)
        util.menus(self, "icons/quotation-menu-icon.png", "Quotation", 0.25, lambda: self.controller.show_frame(Quotation),
                   util.white_font_color, False)
        util.menus(self, "icons/orders-menu-icon.png", "Orders", 0.3, lambda: self.controller.show_frame(Orders),
                   util.white_font_color, False)
        util.menus(self, "icons/user-menu-icon.png", "Users", 0.35, lambda: self.controller.show_frame(Users),
                   util.tertiary_color, True)
        util.menus(self, "icons/transport-menu-icon.png", "Transport", 0.4,
                   lambda: self.controller.show_frame(Transport),
                   util.white_font_color, False)
        util.menus(self, "icons/warehouse-menu-icon.png", "Warehouse", 0.45,
                   lambda: self.controller.show_frame(Warehouse),
                   util.white_font_color, False)
        util.menus(self, "icons/shipment-menu-icon.png", "Shipments", 0.5,
                   lambda: self.controller.show_frame(Shipments),
                   util.white_font_color, False)
        util.menus(self, "icons/tracking-menu-icon.png", "Tracking", 0.55,
                   lambda: self.controller.show_frame(Tracking),
                   util.white_font_color, False)
        util.menus(self, "icons/invoice-menu-icon.png", "Invoice", 0.6, lambda: self.controller.show_frame(Invoice),
                   util.white_font_color, False)
        util.menus(self, "icons/reports-menu-icon.png", "Reports", 0.65, lambda: self.controller.show_frame(Reports),
                   util.white_font_color, False)

        def sign_out_button():
            util.sign_out("login_status/status.txt")
            self.controller.show_frame(Main)

        util.menus(self, "icons/exit-menu-icon.png", "Sign Out", 0.8, sign_out_button,
                   util.white_font_color, False)

        switch_frame = util.frame(self.main, util.secondary_color, 0, 0.03, 0.15, 0, 0, 600, 30)
        self.scrollbar_window = util.frame(self.main, util.primary_color, 1, 0.03, 0.2, 0, 0, 1090, 650)

        def users():
            util.destroy_frame(switch_frame)

            util.button(switch_frame, 0, 0, 0, 0, 70, 25, "Users", 12, "bold", util.tertiary_color,
                        util.secondary_color, users, "")
            util.button(switch_frame, 0.12, 0, 0, 0, 100, 25, "Drivers", 12, "bold", util.white_font_color,
                        util.secondary_color, drivers, "")

            self.display_users()

        def drivers():
            util.destroy_frame(switch_frame)

            util.button(switch_frame, 0, 0, 0, 0, 70, 25, "Users", 12, "bold", util.white_font_color,
                        util.secondary_color, users, "")
            util.button(switch_frame, 0.12, 0, 0, 0, 100, 25, "Drivers", 12, "bold", util.tertiary_color,
                        util.secondary_color, drivers, "")

            def create_driver():
                top_level = tk.Toplevel()
                top_level.title("Create Booking")
                top_level.geometry("900x600")
                top_level.config(bg=util.secondary_color)

                driver_details_frame = util.frame(top_level, util.tertiary_color, 1, 0.02, 0.03, 0, 0, 850, 30)
                util.label(driver_details_frame, "Driver Details", 13, "bold", util.white_font_color,
                           util.tertiary_color, 0.03, 0.02)

                util.label(top_level, "Driver Name", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.11)
                driver_name, driver_name_var, driver_name_frame = util.frame_entry(top_level, "", 0.22, 0.11, 0, 0, 200, 30)
                util.label(top_level, "Vehicle Category", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.18)
                vehicle_category, vehicle_category_var, vehicle_category_frame = util.frame_entry(top_level, "", 0.22, 0.18, 0, 0, 200, 30)
                util.label(top_level, "Vehicle Number", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.25)
                vehicle_number, vehicle_number_var, vehicle_number_frame = util.frame_entry(top_level, "", 0.22, 0.25, 0, 0, 200, 30)
                util.label(top_level, "Vehicle Model", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.32)
                vehicle_model, vehicle_model_var, vehicle_model_frame = util.frame_entry(top_level, "", 0.22, 0.32, 0, 0, 200, 30)
                util.label(top_level, "Issue Date", 12, "bold", util.white_font_color, util.secondary_color, 0.5, 0.11)

                date_label_var = util.open_calendar(top_level, 0.68, 0.11)

                util.label(top_level, "Contact Number", 12, "bold", util.white_font_color, util.secondary_color, 0.5,
                           0.18)
                contact_no, contact_no_var, contact_no_frame = util.frame_entry(top_level, "", 0.68, 0.18, 0,
                                                                                         0, 200, 30)
                util.label(top_level, "Driver License", 12, "bold", util.white_font_color, util.secondary_color, 0.5,
                           0.25)
                driver_license, driver_license_var, driver_license_frame = util.frame_entry(top_level, "", 0.68, 0.25, 0,
                                                                                         0, 200, 30)

                def create_driver_button():
                    insert_query = "INSERT INTO driver (driver_id, driver_name, vehicle_category, vehicle_number, vehicle_model, issue_date, contact_no, driver_license, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    values = (f"DR-{util.generate_id('8983')}", driver_name_var.get(), vehicle_category_var.get(), vehicle_number_var.get(), vehicle_model_var.get(), date_label_var.get(), contact_no_var.get(), driver_license_var.get(), 'AVAILABLE')
                    self.cursor.execute(insert_query, values)
                    self.connection.commit()
                    result = messagebox.showinfo("Application", "Driver created")
                    if result == 'ok':
                        self.display_driver()

                util.button(top_level, 0.25, 0.8, 0, 0, 100, 35, "Create", 15, "bold", util.secondary_color,
                            util.edit_color,
                            create_driver_button, "")

                def back_button():
                    top_level.destroy()

                util.button(top_level, 0.55, 0.8, 0, 0, 100, 35, "Cancel", 15, "bold", util.secondary_color, "red",
                            back_button, "")

                top_level.resizable(False, False)
                top_level.mainloop()

            create_btn = util.image(self.main, "icons/add-customer-icon.png", util.tertiary_color, 0.83, 0.1, 0, 0, 20,
                                    20)

            def update_driver():
                top_level = tk.Toplevel()
                top_level.title("Create Booking")
                top_level.geometry("900x600")
                top_level.config(bg=util.secondary_color)

                util.label(top_level, "Driver Id", 12, "bold", util.white_font_color, util.secondary_color, 0.07,
                           0.03)
                driver_id, driver_id_var, driver_id_frame = util.frame_entry(top_level, "", 0.33, 0.03, 0, 0, 200,
                                                                                30)

                def search_driver_id():
                    search_query = f"SELECT * FROM driver WHERE driver_id = '{driver_id_var.get()}'"
                    self.cursor.execute(search_query)
                    result = self.cursor.fetchone()

                    driver_name_var.set(result[2])
                    vehicle_category_var.set(result[3])
                    vehicle_number_var.set(result[4])
                    vehicle_model_var.set(result[5])
                    date_label_var.set(result[6])
                    contact_no_var.set(result[7])
                    driver_license_var.set(result[8])

                util.button(top_level, 0.77, 0.03, 0, 0, 80, 30, "Search", 12, "bold", util.white_font_color,
                            util.primary_color, search_driver_id, "")

                driver_details_frame = util.frame(top_level, util.tertiary_color, 1, 0.02, 0.1, 0, 0, 850, 30)
                util.label(driver_details_frame, "Driver Details", 13, "bold", util.white_font_color,
                           util.tertiary_color, 0.03, 0.02)

                util.label(top_level, "Driver Name", 12, "bold", util.white_font_color, util.secondary_color, 0.03,
                           0.18)
                driver_name, driver_name_var, driver_name_frame = util.frame_entry(top_level, "", 0.22, 0.18, 0, 0, 200,
                                                                                   30)
                util.label(top_level, "Vehicle Category", 12, "bold", util.white_font_color, util.secondary_color, 0.03,
                           0.25)
                vehicle_category, vehicle_category_var, vehicle_category_frame = util.frame_entry(top_level, "", 0.22,
                                                                                                  0.25, 0, 0, 200, 30)
                util.label(top_level, "Vehicle Number", 12, "bold", util.white_font_color, util.secondary_color, 0.03,
                           0.32)
                vehicle_number, vehicle_number_var, vehicle_number_frame = util.frame_entry(top_level, "", 0.22, 0.32,
                                                                                            0, 0, 200, 30)
                util.label(top_level, "Vehicle Model", 12, "bold", util.white_font_color, util.secondary_color, 0.03,
                           0.39)
                vehicle_model, vehicle_model_var, vehicle_model_frame = util.frame_entry(top_level, "", 0.22, 0.39, 0,
                                                                                         0, 200, 30)
                util.label(top_level, "Issue Date", 12, "bold", util.white_font_color, util.secondary_color, 0.5, 0.18)

                date_label_var = util.open_calendar(top_level, 0.68, 0.18)
                #
                util.label(top_level, "Contact Number", 12, "bold", util.white_font_color, util.secondary_color, 0.5,
                           0.25)
                contact_no, contact_no_var, contact_no_frame = util.frame_entry(top_level, "", 0.68, 0.25, 0,
                                                                                0, 200, 30)
                util.label(top_level, "Driver License", 12, "bold", util.white_font_color, util.secondary_color, 0.5,
                           0.32)
                driver_license, driver_license_var, driver_license_frame = util.frame_entry(top_level, "", 0.68, 0.32, 0, 0, 200, 30)

                def update_driver_button():
                    update_query = "UPDATE driver SET driver_name = %s, vehicle_category = %s, vehicle_number = %s, vehicle_model = %s, issue_date = %s, contact_no = %s, driver_license = %s"
                    values = (driver_name_var.get(), vehicle_category_var.get(), vehicle_number_var.get(), vehicle_model_var.get(), date_label_var.get(), contact_no_var.get(), driver_license_var.get())
                    self.cursor.execute(update_query, values)
                    self.connection.commit()
                    result = messagebox.showinfo("Application", "Driver details updated")
                    if result == 'ok':
                        self.display_driver()
                        top_level.destroy()

                util.button(top_level, 0.25, 0.8, 0, 0, 100, 35, "Update", 15, "bold", util.secondary_color,
                            util.edit_color,
                            update_driver_button, "")

                def back_button():
                    top_level.destroy()

                util.button(top_level, 0.55, 0.8, 0, 0, 100, 35, "Cancel", 15, "bold", util.secondary_color, "red",
                            back_button, "")

                top_level.resizable(False, False)
                top_level.mainloop()

            util.button(self.main, 0.55, 0.1, 0, 0, 210, 50, "Update Driver", 13, "bold", util.tertiary_color,
                        util.primary_color, update_driver, create_btn)
            util.button(self.main, 0.77, 0.1, 0, 0, 180, 50, "Create Driver", 13, "bold", util.tertiary_color,
                        util.primary_color, create_driver, create_btn)

            self.display_driver()

        users()

    def display_users(self):
        util.destroy_frame(self.scrollbar_window)

        query = "SELECT * FROM quotation"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if results:
            header_canvas = util.canvas_frame(self.scrollbar_window, 1, util.primary_color, 0.03, 0, 1100, 30)

            canvas = tk.Canvas(self.scrollbar_window, bg=util.primary_color, highlightthickness=0,
                               scrollregion=(0, 0, 1700, 5000))
            canvas.pack(expand=True, fill='both')

            vertical_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='vertical', command=canvas.yview)
            horizontal_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='horizontal', command=canvas.xview)

            canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
            vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
            horizontal_scrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')

            canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-int(event.delta / 120), "units"))
            canvas.bind("<Control MouseWheel>", lambda event: canvas.xview_scroll(-int(event.delta / 120), "units"))

            def sync_scroll(*args):
                canvas.xview(*args)
                header_canvas.xview(*args)

            canvas.bind("<Configure>", lambda event: header_canvas.configure(scrollregion=(0, 0, 1700, 5000)))

            header_canvas.configure(xscrollcommand=lambda *args: sync_scroll('moveto', args[0]))
            canvas.configure(xscrollcommand=lambda *args: sync_scroll('moveto', args[0]))

            util.canvas_text(self.main, header_canvas, 30, 6, "ID", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 160, 6, "Name", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 450, 6, "Company Name", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 700, 6, "Company Website", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 1000, 6, "Email", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 1300, 6, "Contact Number", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 1500, 6, "Created On", util.white_font_color, 13, "bold", False)

            frame = tk.Frame(canvas, bg=util.secondary_color, borderwidth=1, relief='solid')
            canvas.create_window(0, 0, window=frame, anchor='nw')

            for index, result in enumerate(results):
                frame_canvas = util.canvas_frame(frame, 1, util.primary_color, 0, 4, 1700, 40)

                util.canvas_text(self.main, frame_canvas, 30, 12, result[1], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 160, 12, result[3], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 450, 12, result[4], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 700, 12, result[5], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1000, 12, result[6], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1300, 12, result[7], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1500, 12, result[9], util.white_font_color, 13, "", True)

    def display_driver(self):
        util.destroy_frame(self.scrollbar_window)

        query = "SELECT * FROM driver"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if results:
            header_canvas = util.canvas_frame(self.scrollbar_window, 1, util.primary_color, 0.03, 0, 1100, 30)

            canvas = tk.Canvas(self.scrollbar_window, bg=util.primary_color, highlightthickness=0,
                               scrollregion=(0, 0, 2150, 5000))
            canvas.pack(expand=True, fill='both')

            vertical_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='vertical', command=canvas.yview)
            horizontal_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='horizontal', command=canvas.xview)

            canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
            vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
            horizontal_scrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')

            canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-int(event.delta / 120), "units"))
            canvas.bind("<Control MouseWheel>", lambda event: canvas.xview_scroll(-int(event.delta / 120), "units"))

            def sync_scroll(*args):
                canvas.xview(*args)
                header_canvas.xview(*args)

            canvas.bind("<Configure>", lambda event: header_canvas.configure(scrollregion=(0, 0, 2150, 5000)))

            header_canvas.configure(xscrollcommand=lambda *args: sync_scroll('moveto', args[0]))
            canvas.configure(xscrollcommand=lambda *args: sync_scroll('moveto', args[0]))

            util.canvas_text(self.main, header_canvas, 30, 6, "ID", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 160, 6, "Name", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 450, 6, "Vehicle Category", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 700, 6, "Vehicle Number", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 1000, 6, "Vehicle Model", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 1300, 6, "Issue Date", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 1500, 6, "Contact Number", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 1700, 6, "Driver License", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 1900, 6, "Status", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 2030, 6, "Action", util.white_font_color, 13, "bold",
                             False)

            frame = tk.Frame(canvas, bg=util.secondary_color, borderwidth=1, relief='solid')
            canvas.create_window(0, 0, window=frame, anchor='nw')

            for index, result in enumerate(results):
                frame_canvas = util.canvas_frame(frame, 1, util.primary_color, 0, 4, 2150, 40)

                util.canvas_text(self.main, frame_canvas, 30, 12, result[1], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 160, 12, result[2], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 450, 12, result[3], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 700, 12, result[4], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1000, 12, result[5], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1300, 12, result[6], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1500, 12, result[7], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1700, 12, result[8], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1900, 12, result[9], util.white_font_color, 13, "", True)

                def recycle_command(res):
                    def command():
                        question = messagebox.askquestion("Application", "Are you sure you want to delete")
                        if question == 'yes':
                            delete_query = f"DELETE FROM driver WHERE id = {res[0]}"
                            self.cursor.execute(delete_query)
                            self.connection.commit()
                            self.display_driver()

                    return command

                recycle_callback = recycle_command(result)
                recycle_button = util.image(frame_canvas, "icons/recycle-bin-icon.png", util.primary_color, 0.94, 0.22, 10, 0,
                                           20, 20)
                util.button(frame_canvas, 0.94, 0.22, 12, 2, 20, 20, "", 12, "", util.primary_color, util.primary_color,
                            recycle_callback, recycle_button)


class Transport(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=util.secondary_color)
        self.controller = controller
        util.destroy_frame(self)

        self.connection = mysql.connector.connect(user=util.user, host=util.host, database=util.database,
                                                  password=util.password)
        self.cursor = self.connection.cursor()

        menu_frame = tk.Frame(self, bg=util.primary_color)
        menu_frame.place(relx=0, rely=0, width=290, height=900)

        self.main = util.frame(self, util.secondary_color, 0, 0.2, 0, 0, 0, 1170, 830)

        util.profile(self.main, "Users", "login_status/status.txt")

        util.menus(self, "icons/dashboard-menu-icon.png", "Dashboard", 0.2, lambda: self.controller.show_frame(Dashboard),
                   util.white_font_color, False)
        util.menus(self, "icons/quotation-menu-icon.png", "Quotation", 0.25, lambda: self.controller.show_frame(Quotation),
                   util.white_font_color, False)
        util.menus(self, "icons/orders-menu-icon.png", "Orders", 0.3, lambda: self.controller.show_frame(Orders),
                   util.white_font_color, False)
        util.menus(self, "icons/user-menu-icon.png", "Users", 0.35, lambda: self.controller.show_frame(Users),
                   util.white_font_color, False)
        util.menus(self, "icons/transport-menu-icon.png", "Transport", 0.4,
                   lambda: self.controller.show_frame(Transport),
                   util.tertiary_color, True)
        util.menus(self, "icons/warehouse-menu-icon.png", "Warehouse", 0.45,
                   lambda: self.controller.show_frame(Warehouse),
                   util.white_font_color, False)
        util.menus(self, "icons/shipment-menu-icon.png", "Shipments", 0.5,
                   lambda: self.controller.show_frame(Shipments),
                   util.white_font_color, False)
        util.menus(self, "icons/tracking-menu-icon.png", "Tracking", 0.55,
                   lambda: self.controller.show_frame(Tracking),
                   util.white_font_color, False)
        util.menus(self, "icons/invoice-menu-icon.png", "Invoice", 0.6, lambda: self.controller.show_frame(Invoice),
                   util.white_font_color, False)
        util.menus(self, "icons/reports-menu-icon.png", "Reports", 0.65, lambda: self.controller.show_frame(Reports),
                   util.white_font_color, False)

        def sign_out_button():
            util.sign_out("login_status/status.txt")
            self.controller.show_frame(Main)

        util.menus(self, "icons/exit-menu-icon.png", "Sign Out", 0.8, sign_out_button,
                   util.white_font_color, False)

        def create_transport():
            top_level = tk.Toplevel()
            top_level.title("Request Quotation")
            top_level.geometry("900x600")
            top_level.config(bg=util.secondary_color)
            util.destroy_frame(top_level)

            util.label(top_level, "Quotation Id", 12, "bold", util.white_font_color, util.secondary_color, 0.07, 0.03)
            quotation_id, quotation_id_var, quotation_id_frame = util.frame_entry(top_level, "", 0.33, 0.03, 0, 0, 200,
                                                                                  30)

            def search_quotation_id():
                search_query = f"SELECT quotation.client_name FROM quotation WHERE quotation_id = '{quotation_id_var.get()}'"
                self.cursor.execute(search_query)
                result = self.cursor.fetchone()

                client_name_var.set(result[0])

            util.button(top_level, 0.77, 0.03, 0, 0, 80, 30, "Search", 12, "bold", util.white_font_color,
                        util.primary_color, search_quotation_id, "")

            driver_details_frame = util.frame(top_level, util.tertiary_color, 1, 0.02, 0.1, 0, 0, 850, 30)
            util.label(driver_details_frame, "Personal Details", 13, "bold", util.white_font_color,
                       util.tertiary_color, 0.03, 0.02)

            util.label(top_level, "Client Name", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.18)
            client_name, client_name_var, client_name_frame = util.frame_entry(top_level, "", 0.22, 0.18, 0, 0, 200, 30)

            order_details_frame = util.frame(top_level, util.tertiary_color, 1, 0.02, 0.25, 0, 0, 850, 30)
            util.label(order_details_frame, "Driver Details", 13, "bold", util.white_font_color,
                       util.tertiary_color, 0.03, 0.02)

            util.label(top_level, "Driver Id", 12, "bold", util.white_font_color, util.secondary_color, 0.07, 0.32)
            driver_id, driver_id_var, driver_id_frame = util.frame_entry(top_level, "", 0.33, 0.32, 0, 0, 200,
                                                                                  30)

            def search_driver_id():
                search_query = f"SELECT * FROM driver WHERE driver_id = '{driver_id.get()}' AND status = 'AVAILABLE'"
                self.cursor.execute(search_query)
                result = self.cursor.fetchone()

                driver_name_var.set(result[2])
                category_var.set(result[3])
                number_var.set(result[4])
                model_var.set(result[5])
                issue_date_var.set(result[6])
                contact_var.set(result[7])
                license_var.set(result[8])

            util.button(top_level, 0.77, 0.32, 0, 0, 80, 30, "Search", 12, "bold", util.white_font_color,
                        util.primary_color, search_driver_id, "")

            util.label(top_level, "Driver Name", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.4)
            driver_name, driver_name_var = util.label(top_level, "", 11, "", util.white_font_color, util.secondary_color, 0.25, 0.4)

            util.label(top_level, "Category", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.47)
            category, category_var = util.label(top_level, "", 11, "", util.white_font_color,
                                                      util.secondary_color, 0.25, 0.47)

            util.label(top_level, "Number", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.54)
            number, number_var = util.label(top_level, "", 11, "", util.white_font_color,
                                                util.secondary_color, 0.25, 0.54)

            util.label(top_level, "Model", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.61)
            model, model_var = util.label(top_level, "", 11, "", util.white_font_color,
                                                util.secondary_color, 0.25, 0.61)

            util.label(top_level, "Issue Date", 12, "bold", util.white_font_color, util.secondary_color, 0.5, 0.4)
            issue_date, issue_date_var = util.label(top_level, "", 11, "", util.white_font_color,
                                                util.secondary_color, 0.65, 0.4)

            util.label(top_level, "Contact", 12, "bold", util.white_font_color, util.secondary_color, 0.5, 0.47)
            contact, contact_var = util.label(top_level, "", 11, "", util.white_font_color,
                                                util.secondary_color, 0.65, 0.47)

            util.label(top_level, "License", 12, "bold", util.white_font_color, util.secondary_color, 0.5, 0.54)
            license, license_var = util.label(top_level, "", 11, "", util.white_font_color,
                                                util.secondary_color, 0.65, 0.54)

            def create_invoice_button():
                insert_query = "INSERT INTO transport (user_id, driver_id) VALUES (%s, %s)"
                values = (quotation_id_var.get(), driver_id_var.get())
                self.cursor.execute(insert_query, values)
                self.connection.commit()
                result = messagebox.showinfo("Application", "Transport created successfully")
                if result == 'ok':
                    top_level.destroy()
                    self.display_transport()

            util.button(top_level, 0.25, 0.8, 0, 0, 100, 35, "Create", 15, "bold", util.secondary_color, util.edit_color,
                        create_invoice_button, "")

            def back_button():
                top_level.destroy()

            util.button(top_level, 0.55, 0.8, 0, 0, 100, 35, "Cancel", 15, "bold", util.secondary_color, "red",
                        back_button, "")

            top_level.resizable(False, False)
            top_level.mainloop()

        create_btn = util.image(self.main, "icons/add-customer-icon.png", util.tertiary_color, 0.83, 0.1, 0, 0, 20, 20)
        util.button(self.main, 0.77, 0.1, 0, 0, 200, 50, "Create Transport", 13, "bold", util.tertiary_color,
                    util.primary_color, create_transport, create_btn)

        def update_transport():
            top_level = tk.Toplevel()
            top_level.title("Request Quotation")
            top_level.geometry("900x600")
            top_level.config(bg=util.secondary_color)
            util.destroy_frame(top_level)

            util.label(top_level, "Quotation Id", 12, "bold", util.white_font_color, util.secondary_color, 0.07, 0.03)
            quotation_id, quotation_id_var, quotation_id_frame = util.frame_entry(top_level, "", 0.33, 0.03, 0, 0, 200,
                                                                                  30)

            def search_quotation_id():
                search_query = f"SELECT quotation.client_name FROM quotation WHERE quotation_id = '{quotation_id_var.get()}'"
                self.cursor.execute(search_query)
                result = self.cursor.fetchone()

                client_name_var.set(result[0])

            util.button(top_level, 0.77, 0.03, 0, 0, 80, 30, "Search", 12, "bold", util.white_font_color,
                        util.primary_color, search_quotation_id, "")

            driver_details_frame = util.frame(top_level, util.tertiary_color, 1, 0.02, 0.1, 0, 0, 850, 30)
            util.label(driver_details_frame, "Personal Details", 13, "bold", util.white_font_color,
                       util.tertiary_color, 0.03, 0.02)

            util.label(top_level, "Client Name", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.18)
            client_name, client_name_var, client_name_frame = util.frame_entry(top_level, "", 0.22, 0.18, 0, 0, 200, 30)

            order_details_frame = util.frame(top_level, util.tertiary_color, 1, 0.02, 0.25, 0, 0, 850, 30)
            util.label(order_details_frame, "Driver Details", 13, "bold", util.white_font_color,
                       util.tertiary_color, 0.03, 0.02)

            util.label(top_level, "Driver Id", 12, "bold", util.white_font_color, util.secondary_color, 0.07, 0.32)
            driver_id, driver_id_var, driver_id_frame = util.frame_entry(top_level, "", 0.33, 0.32, 0, 0, 200,
                                                                         30)

            def search_driver_id():
                search_query = f"SELECT * FROM driver WHERE driver_id = '{driver_id.get()}' AND status = 'AVAILABLE'"
                self.cursor.execute(search_query)
                result = self.cursor.fetchone()

                driver_name_var.set(result[2])
                category_var.set(result[3])
                number_var.set(result[4])
                model_var.set(result[5])
                issue_date_var.set(result[6])
                contact_var.set(result[7])
                license_var.set(result[8])

            util.button(top_level, 0.77, 0.32, 0, 0, 80, 30, "Search", 12, "bold", util.white_font_color,
                        util.primary_color, search_driver_id, "")

            util.label(top_level, "Driver Name", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.4)
            driver_name, driver_name_var = util.label(top_level, "", 11, "", util.white_font_color,
                                                      util.secondary_color, 0.25, 0.4)

            util.label(top_level, "Category", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.47)
            category, category_var = util.label(top_level, "", 11, "", util.white_font_color,
                                                util.secondary_color, 0.25, 0.47)

            util.label(top_level, "Number", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.54)
            number, number_var = util.label(top_level, "", 11, "", util.white_font_color,
                                            util.secondary_color, 0.25, 0.54)

            util.label(top_level, "Model", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.61)
            model, model_var = util.label(top_level, "", 11, "", util.white_font_color,
                                          util.secondary_color, 0.25, 0.61)

            util.label(top_level, "Issue Date", 12, "bold", util.white_font_color, util.secondary_color, 0.5, 0.4)
            issue_date, issue_date_var = util.label(top_level, "", 11, "", util.white_font_color,
                                                    util.secondary_color, 0.65, 0.4)

            util.label(top_level, "Contact", 12, "bold", util.white_font_color, util.secondary_color, 0.5, 0.47)
            contact, contact_var = util.label(top_level, "", 11, "", util.white_font_color,
                                              util.secondary_color, 0.65, 0.47)

            util.label(top_level, "License", 12, "bold", util.white_font_color, util.secondary_color, 0.5, 0.54)
            license, license_var = util.label(top_level, "", 11, "", util.white_font_color,
                                              util.secondary_color, 0.65, 0.54)

            def create_invoice_button():
                update_query = "UPDATE transport SET user_id = %s, driver_id = %s WHERE user_id = %s ANDs driver_id = %s"
                values = (quotation_id_var.get(), driver_id_var.get(), quotation_id_var.get(), driver_id_var.get())
                self.cursor.execute(update_query, values)
                self.connection.commit()
                result = messagebox.showinfo("Application", "Transport updated successfully")
                if result == 'ok':
                    top_level.destroy()
                    self.display_transport()

            util.button(top_level, 0.25, 0.8, 0, 0, 100, 35, "Update", 15, "bold", util.secondary_color,
                        util.edit_color,
                        create_invoice_button, "")

            def back_button():
                top_level.destroy()

            util.button(top_level, 0.55, 0.8, 0, 0, 100, 35, "Cancel", 15, "bold", util.secondary_color, "red",
                        back_button, "")

            top_level.resizable(False, False)
            top_level.mainloop()

        update_btn = util.image(self.main, "icons/add-customer-icon.png", util.tertiary_color, 0.6, 0.1, 0, 0, 20, 20)
        util.button(self.main, 0.57, 0.1, 0, 0, 200, 50, "Update Transport", 13, "bold", util.tertiary_color,
                    util.primary_color, update_transport, update_btn)

        self.scrollbar_window = util.frame(self.main, util.primary_color, 1, 0.03, 0.2, 0, 0, 1090, 650)
        self.display_transport()

    def display_transport(self):
        util.destroy_frame(self.scrollbar_window)

        query = "SELECT quotation.quotation_id, orders.order_status, driver.vehicle_category, driver.vehicle_number, driver.vehicle_model, driver.issue_date, driver.driver_name, driver.contact_no, driver.driver_license FROM (((transport INNER JOIN quotation ON transport.user_id = quotation.quotation_id) INNER JOIN driver ON transport.driver_id = driver.driver_id) INNER JOIN orders ON orders.user_id = transport.user_id)"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if results:
            canvas = tk.Canvas(self.scrollbar_window, bg=util.primary_color, highlightthickness=0,
                               scrollregion=(0, 0, 1700, 5000))
            canvas.pack(expand=True, fill='both')

            vertical_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='vertical', command=canvas.yview)
            horizontal_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='horizontal', command=canvas.xview)

            canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
            vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
            horizontal_scrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')

            canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-int(event.delta / 120), "units"))
            canvas.bind("<Control MouseWheel>", lambda event: canvas.xview_scroll(-int(event.delta / 120), "units"))

            frame = tk.Frame(canvas, bg=util.secondary_color, borderwidth=1, relief='solid')
            canvas.create_window(0, 0, window=frame, anchor='nw')

            for index, result in enumerate(results):
                frame_canvas = util.canvas_frame(frame, 1, util.primary_color, 0, 4, 1350, 160)

                util.canvas_text(self.main, frame_canvas, 30, 40, f"{result[0]}", util.white_font_color, 12, "bold",
                                 False)
                frame_canvas.create_rectangle(30, 93, 170, 125, fill='green', outline=util.secondary_color)
                util.canvas_text(self.main, frame_canvas, 70, 100, f"{result[1]}", util.white_font_color, 12, "bold",
                                 False)
                util.canvas_text(self.main, frame_canvas, 250, 12, "Category", util.faded_white, 11, "bold", False)
                util.canvas_text(self.main, frame_canvas, 250, 35, f"{result[2]}", util.white_font_color, 12,
                                 "bold", False)

                util.canvas_text(self.main, frame_canvas, 250, 100, "Number", util.faded_white, 11, "bold", False)
                util.canvas_text(self.main, frame_canvas, 250, 120, f"{result[3]}", util.white_font_color, 11, "bold",
                                 False)

                util.canvas_text(self.main, frame_canvas, 500, 18, "Vehicle Model", util.faded_white, 11,
                                 "bold", False)
                util.canvas_text(self.main, frame_canvas, 500, 40, f"{result[4]}", util.white_font_color, 11,
                                 "bold", False)

                util.canvas_text(self.main, frame_canvas, 500, 110, "Year of Issue", util.faded_white, 11, "bold", False)
                util.canvas_text(self.main, frame_canvas, 500, 130, f"{result[5]}", util.white_font_color, 12,
                                 "bold", False)
                util.canvas_text(self.main, frame_canvas, 750, 60, "Driver Name", util.faded_white, 11, "bold", False)
                util.canvas_text(self.main, frame_canvas, 750, 80, f"{result[6]}", util.white_font_color, 12, "bold",
                                 False)
                util.canvas_text(self.main, frame_canvas, 920, 12, "Phone Number", util.faded_white, 12,
                                 "bold", False)
                util.canvas_text(self.main, frame_canvas, 920, 35, f"{result[7]}", util.white_font_color, 15, "bold",
                                 False)

                util.canvas_text(self.main, frame_canvas, 920, 100, "License", util.faded_white, 11, "bold", False)
                util.canvas_text(self.main, frame_canvas, 920, 120, f"{result[8]}", util.white_font_color, 12, "bold",
                                 False)


class Warehouse(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=util.secondary_color)
        self.controller = controller
        util.destroy_frame(self)

        self.connection = mysql.connector.connect(user=util.user, host=util.host, database=util.database,
                                                  password=util.password)
        self.cursor = self.connection.cursor()

        menu_frame = tk.Frame(self, bg=util.primary_color)
        menu_frame.place(relx=0, rely=0, width=290, height=900)

        self.main = util.frame(self, util.secondary_color, 0, 0.2, 0, 0, 0, 1170, 830)

        util.profile(self.main, "Warehouse", "login_status/status.txt")

        util.menus(self, "icons/dashboard-menu-icon.png", "Dashboard", 0.2, lambda: self.controller.show_frame(Dashboard),
                   util.white_font_color, False)
        util.menus(self, "icons/quotation-menu-icon.png", "Quotation", 0.25, lambda: self.controller.show_frame(Quotation),
                   util.white_font_color, False)
        util.menus(self, "icons/orders-menu-icon.png", "Orders", 0.3, lambda: self.controller.show_frame(Orders),
                   util.white_font_color, False)
        util.menus(self, "icons/user-menu-icon.png", "Users", 0.35, lambda: self.controller.show_frame(Users),
                   util.white_font_color, False)
        util.menus(self, "icons/transport-menu-icon.png", "Transport", 0.4,
                   lambda: self.controller.show_frame(Transport),
                   util.white_font_color, False)
        util.menus(self, "icons/warehouse-menu-icon.png", "Warehouse", 0.45,
                   lambda: self.controller.show_frame(Warehouse),
                   util.tertiary_color, True)
        util.menus(self, "icons/shipment-menu-icon.png", "Shipments", 0.5,
                   lambda: self.controller.show_frame(Shipments),
                   util.white_font_color, False)
        util.menus(self, "icons/tracking-menu-icon.png", "Tracking", 0.55,
                   lambda: self.controller.show_frame(Tracking),
                   util.white_font_color, False)
        util.menus(self, "icons/invoice-menu-icon.png", "Invoice", 0.6, lambda: self.controller.show_frame(Invoice),
                   util.white_font_color, False)
        util.menus(self, "icons/reports-menu-icon.png", "Reports", 0.65, lambda: self.controller.show_frame(Reports),
                   util.white_font_color, False)

        def sign_out_button():
            util.sign_out("login_status/status.txt")
            self.controller.show_frame(Main)

        util.menus(self, "icons/exit-menu-icon.png", "Sign Out", 0.8, sign_out_button,
                   util.white_font_color, False)

        def create_commodity():
            top_level = tk.Toplevel()
            top_level.title("Request Quotation")
            top_level.geometry("900x600")
            top_level.config(bg=util.secondary_color)
            util.destroy_frame(top_level)

            driver_details_frame = util.frame(top_level, util.tertiary_color, 1, 0.02, 0.1, 0, 0, 850, 30)
            util.label(driver_details_frame, "Commodity Details", 13, "bold", util.white_font_color,
                       util.tertiary_color, 0.03, 0.02)

            util.label(top_level, "Product Name", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.18)
            product_name, product_name_var, product_name_frame = util.frame_entry(top_level, "", 0.22, 0.18, 0, 0, 200, 30)

            util.label(top_level, "Quantity", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.25)
            product_quantity, product_quantity_var, product_quantity_frame = util.frame_entry(top_level, "", 0.22, 0.25, 0, 0, 200,
                                                                                  30)

            util.label(top_level, "Package Type", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.32)
            get_package_type = util.combobox(top_level, 0.22, 0.32, ('Primary Packaging', 'Secondary Packaging', 'Tertiary Packaging'))

            util.label(top_level, "Specification", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.39)
            specification, specification_var, specification_frame = util.frame_entry(top_level, "", 0.22, 0.39, 0, 0, 200,
                                                                                  30)

            util.label(top_level, "Total Weight", 12, "bold", util.white_font_color, util.secondary_color, 0.5, 0.18)
            total_weight, total_weight_var, total_weight_frame = util.frame_entry(top_level, "", 0.66, 0.18, 0, 0, 200, 30)

            util.label(top_level, "Rate", 12, "bold", util.white_font_color, util.secondary_color, 0.5, 0.25)
            rate, rate_var, rate_frame = util.frame_entry(top_level, "", 0.66, 0.25, 0, 0, 200, 30)

            def calculate_amount():
                total = float(product_quantity_var.get()) * float(rate_var.get())
                total_amount_var.set(total)

            util.button(top_level, 0.7, 0.32, 0, 0, 100, 30, "Calculate", 12, "bold", util.white_font_color,
                        util.primary_color, calculate_amount, "")

            util.label(top_level, "Total Amount", 12, "bold", util.white_font_color, util.secondary_color, 0.5, 0.39)
            total_amount, total_amount_var, total_amount_frame = util.frame_entry(top_level, "", 0.66, 0.39, 0, 0, 200, 30)

            util.label(top_level, "NOTE: Primary Package - This is the first level of packaging that protects individual products from damage.", 11, "bold", util.white_font_color, util.secondary_color, 0.03, 0.5)
            util.label(top_level, "NOTE: Secondary Package - This is used to transport commodities in primary packages.", 11, "bold", util.white_font_color, util.secondary_color, 0.03, 0.55)
            util.label(top_level, "NOTE: Tertiary Package - This is used by warehouses when shipping products in secondary packaging.", 11, "bold", util.white_font_color, util.secondary_color, 0.03, 0.6)

            def create_button():
                query = "INSERT INTO warehouse (warehouse_id, product_name, quantity, package_type, specification, total_weight, total_value) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (f"WR-{util.generate_id('4849')}", product_name_var.get(), product_quantity_var.get(), get_package_type.get(), specification_var.get(), total_weight_var.get(), total_amount_var.get())
                self.cursor.execute(query, values)
                self.connection.commit()
                result = messagebox.showinfo("Application", "Commodities created successfully")
                if result == 'ok':
                    top_level.destroy()
                    self.display_warehouse_commodities()

            util.button(top_level, 0.25, 0.8, 0, 0, 100, 35, "Create", 15, "bold", util.secondary_color, util.edit_color,
                        create_button, "")

            def back_button():
                top_level.destroy()

            util.button(top_level, 0.55, 0.8, 0, 0, 100, 35, "Cancel", 15, "bold", util.secondary_color, "red",
                        back_button, "")

            top_level.resizable(False, False)
            top_level.mainloop()

        create_btn = util.image(self.main, "icons/add-customer-icon.png", util.tertiary_color, 0.83, 0.1, 0, 0, 20, 20)
        util.button(self.main, 0.77, 0.1, 0, 0, 210, 50, "Create Commodity", 13, "bold", util.tertiary_color,
                    util.primary_color, create_commodity, create_btn)

        self.scrollbar_window = util.frame(self.main, util.primary_color, 1, 0.03, 0.2, 0, 0, 600, 630)
        self.display_warehouse_commodities()

    def display_warehouse_commodities(self):
        util.destroy_frame(self.scrollbar_window)

        query = "SELECT * FROM warehouse"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if results:
            header_canvas = util.canvas_frame(self.scrollbar_window, 1, util.primary_color, 0.03, 0, 1100, 30)

            canvas = tk.Canvas(self.scrollbar_window, bg=util.primary_color, highlightthickness=0,
                               scrollregion=(0, 0, 2150, 5000))
            canvas.pack(expand=True, fill='both')

            vertical_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='vertical', command=canvas.yview)
            horizontal_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='horizontal', command=canvas.xview)

            canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
            vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
            horizontal_scrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')

            canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-int(event.delta / 120), "units"))
            canvas.bind("<Control MouseWheel>", lambda event: canvas.xview_scroll(-int(event.delta / 120), "units"))

            def sync_scroll(*args):
                canvas.xview(*args)
                header_canvas.xview(*args)

            canvas.bind("<Configure>", lambda event: header_canvas.configure(scrollregion=(0, 0, 2150, 5000)))

            header_canvas.configure(xscrollcommand=lambda *args: sync_scroll('moveto', args[0]))
            canvas.configure(xscrollcommand=lambda *args: sync_scroll('moveto', args[0]))

            util.canvas_text(self.main, header_canvas, 30, 6, "ID", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 160, 6, "Product Name", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 450, 6, "Quantity", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 700, 6, "Package Type", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 1000, 6, "Specification", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 1300, 6, "Total Weight", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 1500, 6, "Total Value", util.white_font_color, 13, "bold",
                             False)

            frame = tk.Frame(canvas, bg=util.secondary_color, borderwidth=1, relief='solid')
            canvas.create_window(0, 0, window=frame, anchor='nw')

            for index, result in enumerate(results):
                frame_canvas = util.canvas_frame(frame, 1, util.primary_color, 0, 4, 2150, 40)

                util.canvas_text(self.main, frame_canvas, 30, 12, result[1], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 160, 12, result[2], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 450, 12, result[3], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 700, 12, result[4], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1000, 12, result[5], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1300, 12, result[6], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1500, 12, result[7], util.white_font_color, 13, "", True)


class Shipments(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=util.secondary_color)
        self.controller = controller
        util.destroy_frame(self)

        self.connection = mysql.connector.connect(user=util.user, host=util.host, database=util.database,
                                                  password=util.password)
        self.cursor = self.connection.cursor()

        menu_frame = tk.Frame(self, bg=util.primary_color)
        menu_frame.place(relx=0, rely=0, width=290, height=900)

        self.main = util.frame(self, util.secondary_color, 0, 0.2, 0, 0, 0, 1170, 830)

        util.profile(self.main, "Shipments", "login_status/status.txt")

        util.menus(self, "icons/dashboard-menu-icon.png", "Dashboard", 0.2, lambda: self.controller.show_frame(Dashboard),
                   util.white_font_color, False)
        util.menus(self, "icons/quotation-menu-icon.png", "Quotation", 0.25, lambda: self.controller.show_frame(Quotation),
                   util.white_font_color, False)
        util.menus(self, "icons/orders-menu-icon.png", "Orders", 0.3, lambda: self.controller.show_frame(Orders),
                   util.white_font_color, False)
        util.menus(self, "icons/user-menu-icon.png", "Users", 0.35, lambda: self.controller.show_frame(Users),
                   util.white_font_color, False)
        util.menus(self, "icons/transport-menu-icon.png", "Transport", 0.4,
                   lambda: self.controller.show_frame(Transport),
                   util.white_font_color, False)
        util.menus(self, "icons/warehouse-menu-icon.png", "Warehouse", 0.45,
                   lambda: self.controller.show_frame(Warehouse),
                   util.white_font_color, False)
        util.menus(self, "icons/shipment-menu-icon.png", "Shipments", 0.5,
                   lambda: self.controller.show_frame(Shipments),
                   util.tertiary_color, True)
        util.menus(self, "icons/tracking-menu-icon.png", "Tracking", 0.55,
                   lambda: self.controller.show_frame(Tracking),
                   util.white_font_color, False)
        util.menus(self, "icons/invoice-menu-icon.png", "Invoice", 0.6, lambda: self.controller.show_frame(Invoice),
                   util.white_font_color, False)
        util.menus(self, "icons/reports-menu-icon.png", "Reports", 0.65, lambda: self.controller.show_frame(Reports),
                   util.white_font_color, False)

        def sign_out_button():
            util.sign_out("login_status/status.txt")
            self.controller.show_frame(Main)

        util.menus(self, "icons/exit-menu-icon.png", "Sign Out", 0.8, sign_out_button,
                   util.white_font_color, False)

        self.scrollbar_window = util.frame(self.main, util.primary_color, 1, 0.03, 0.2, 0, 0, 1090, 650)
        self.display_shipments()

    def display_shipments(self):
        util.destroy_frame(self.scrollbar_window)

        query = "SELECT orders.order_id, quotation.client_name, orders.departure_location, orders.arrival_location, quotation.created_on, invoice.shipping_charges, orders.order_status FROM ((orders INNER JOIN quotation ON quotation.quotation_id = orders.user_id) INNER JOIN invoice ON invoice.user_id = orders.user_id)"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if results:
            header_canvas = util.canvas_frame(self.scrollbar_window, 1, util.primary_color, 0.03, 0, 1100, 30)

            canvas = tk.Canvas(self.scrollbar_window, bg=util.primary_color, highlightthickness=0,
                               scrollregion=(0, 0, 2150, 5000))
            canvas.pack(expand=True, fill='both')

            vertical_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='vertical', command=canvas.yview)
            horizontal_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='horizontal', command=canvas.xview)

            canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
            vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
            horizontal_scrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')

            canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-int(event.delta / 120), "units"))
            canvas.bind("<Control MouseWheel>", lambda event: canvas.xview_scroll(-int(event.delta / 120), "units"))

            def sync_scroll(*args):
                canvas.xview(*args)
                header_canvas.xview(*args)

            canvas.bind("<Configure>", lambda event: header_canvas.configure(scrollregion=(0, 0, 2150, 5000)))

            header_canvas.configure(xscrollcommand=lambda *args: sync_scroll('moveto', args[0]))
            canvas.configure(xscrollcommand=lambda *args: sync_scroll('moveto', args[0]))

            util.canvas_text(self.main, header_canvas, 30, 6, "ID", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 160, 6, "Receiver Name", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 450, 6, "Origin", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 700, 6, "Destination", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 1000, 6, "Created On", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 1300, 6, "Charges", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 1500, 6, "Status", util.white_font_color, 13, "bold",
                             False)

            frame = tk.Frame(canvas, bg=util.secondary_color, borderwidth=1, relief='solid')
            canvas.create_window(0, 0, window=frame, anchor='nw')

            for index, result in enumerate(results):
                frame_canvas = util.canvas_frame(frame, 1, util.primary_color, 0, 4, 2150, 40)

                util.canvas_text(self.main, frame_canvas, 30, 12, result[0], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 160, 12, result[1], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 450, 12, result[2], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 700, 12, result[3], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1000, 12, result[4], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1300, 12, result[5], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1500, 12, result[6], util.white_font_color, 13, "", True)


class Tracking(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=util.secondary_color)
        self.controller = controller
        util.destroy_frame(self)

        self.connection = mysql.connector.connect(user=util.user, host=util.host, database=util.database,
                                                  password=util.password)
        self.cursor = self.connection.cursor()

        menu_frame = tk.Frame(self, bg=util.primary_color)
        menu_frame.place(relx=0, rely=0, width=290, height=900)

        self.main = util.frame(self, util.secondary_color, 0, 0.2, 0, 0, 0, 1170, 830)

        util.profile(self.main, "Tracking", "login_status/status.txt")

        util.menus(self, "icons/dashboard-menu-icon.png", "Dashboard", 0.2, lambda: self.controller.show_frame(Dashboard),
                   util.white_font_color, False)
        util.menus(self, "icons/quotation-menu-icon.png", "Quotation", 0.25, lambda: self.controller.show_frame(Quotation),
                   util.white_font_color, False)
        util.menus(self, "icons/orders-menu-icon.png", "Orders", 0.3, lambda: self.controller.show_frame(Orders),
                   util.white_font_color, False)
        util.menus(self, "icons/user-menu-icon.png", "Users", 0.35, lambda: self.controller.show_frame(Users),
                   util.white_font_color, False)
        util.menus(self, "icons/transport-menu-icon.png", "Transport", 0.4,
                   lambda: self.controller.show_frame(Transport),
                   util.white_font_color, False)
        util.menus(self, "icons/warehouse-menu-icon.png", "Warehouse", 0.45,
                   lambda: self.controller.show_frame(Warehouse),
                   util.white_font_color, False)
        util.menus(self, "icons/shipment-menu-icon.png", "Shipments", 0.5,
                   lambda: self.controller.show_frame(Shipments),
                   util.white_font_color, False)
        util.menus(self, "icons/tracking-menu-icon.png", "Tracking", 0.55,
                   lambda: self.controller.show_frame(Tracking),
                   util.tertiary_color, True)
        util.menus(self, "icons/invoice-menu-icon.png", "Invoice", 0.6, lambda: self.controller.show_frame(Invoice),
                   util.white_font_color, False)
        util.menus(self, "icons/reports-menu-icon.png", "Reports", 0.65, lambda: self.controller.show_frame(Reports),
                   util.white_font_color, False)

        def sign_out_button():
            util.sign_out("login_status/status.txt")
            self.controller.show_frame(Main)

        util.menus(self, "icons/exit-menu-icon.png", "Sign Out", 0.8, sign_out_button,
                   util.white_font_color, False)

        self.scrollbar_window = util.frame(self.main, util.primary_color, 1, 0.03, 0.2, 0, 0, 1090, 650)
        self.display_tracking()

    def display_tracking(self):
        util.destroy_frame(self.scrollbar_window)

        query = "SELECT orders.order_id, quotation.client_name, orders.departure_location, orders.arrival_location, orders.arrival_date, orders.delivery_status FROM orders JOIN quotation ON quotation.quotation_id = orders.user_id"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if results:
            header_canvas = util.canvas_frame(self.scrollbar_window, 1, util.primary_color, 0.03, 0, 1100, 30)

            canvas = tk.Canvas(self.scrollbar_window, bg=util.primary_color, highlightthickness=0,
                               scrollregion=(0, 0, 2150, 5000))
            canvas.pack(expand=True, fill='both')

            vertical_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='vertical', command=canvas.yview)
            horizontal_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='horizontal', command=canvas.xview)

            canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
            vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
            horizontal_scrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')

            canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-int(event.delta / 120), "units"))
            canvas.bind("<Control MouseWheel>", lambda event: canvas.xview_scroll(-int(event.delta / 120), "units"))

            def sync_scroll(*args):
                canvas.xview(*args)
                header_canvas.xview(*args)

            canvas.bind("<Configure>", lambda event: header_canvas.configure(scrollregion=(0, 0, 2150, 5000)))

            header_canvas.configure(xscrollcommand=lambda *args: sync_scroll('moveto', args[0]))
            canvas.configure(xscrollcommand=lambda *args: sync_scroll('moveto', args[0]))

            util.canvas_text(self.main, header_canvas, 30, 6, "ID", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 160, 6, "Receiver Name", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 450, 6, "Origin", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 700, 6, "Destination", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 1000, 6, "Delivery Date", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 1300, 6, "Activity", util.white_font_color, 13, "bold",
                             False)

            frame = tk.Frame(canvas, bg=util.secondary_color, borderwidth=1, relief='solid')
            canvas.create_window(0, 0, window=frame, anchor='nw')

            for index, result in enumerate(results):
                frame_canvas = util.canvas_frame(frame, 1, util.primary_color, 0, 4, 2150, 40)

                util.canvas_text(self.main, frame_canvas, 30, 12, result[0], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 160, 12, result[1], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 450, 12, result[2], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 700, 12, result[3], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1000, 12, result[4], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1300, 12, result[5], util.white_font_color, 13, "", True)


class Invoice(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=util.secondary_color)
        self.controller = controller
        util.destroy_frame(self)
        self.shipping_amount = None

        self.connection = mysql.connector.connect(user=util.user, host=util.host, database=util.database,
                                                  password=util.password)
        self.cursor = self.connection.cursor()

        menu_frame = tk.Frame(self, bg=util.primary_color)
        menu_frame.place(relx=0, rely=0, width=290, height=900)

        self.main = util.frame(self, util.secondary_color, 0, 0.2, 0, 0, 0, 1170, 830)

        util.profile(self.main, "Invoice", "login_status/status.txt")

        util.menus(self, "icons/dashboard-menu-icon.png", "Dashboard", 0.2, lambda: self.controller.show_frame(Dashboard),
                   util.white_font_color, False)
        util.menus(self, "icons/quotation-menu-icon.png", "Quotation", 0.25, lambda: self.controller.show_frame(Quotation),
                   util.white_font_color, False)
        util.menus(self, "icons/orders-menu-icon.png", "Orders", 0.3, lambda: self.controller.show_frame(Orders),
                   util.white_font_color, False)
        util.menus(self, "icons/user-menu-icon.png", "Users", 0.35, lambda: self.controller.show_frame(Users),
                   util.white_font_color, False)
        util.menus(self, "icons/transport-menu-icon.png", "Transport", 0.4,
                   lambda: self.controller.show_frame(Transport),
                   util.white_font_color, False)
        util.menus(self, "icons/warehouse-menu-icon.png", "Warehouse", 0.45,
                   lambda: self.controller.show_frame(Warehouse),
                   util.white_font_color, False)
        util.menus(self, "icons/shipment-menu-icon.png", "Shipments", 0.5,
                   lambda: self.controller.show_frame(Shipments),
                   util.white_font_color, False)
        util.menus(self, "icons/tracking-menu-icon.png", "Tracking", 0.55,
                   lambda: self.controller.show_frame(Tracking),
                   util.white_font_color, False)
        util.menus(self, "icons/invoice-menu-icon.png", "Invoice", 0.6, lambda: self.controller.show_frame(Invoice),
                   util.tertiary_color, True)
        util.menus(self, "icons/reports-menu-icon.png", "Reports", 0.65, lambda: self.controller.show_frame(Reports),
                   util.white_font_color, False)

        def sign_out_button():
            util.sign_out("login_status/status.txt")
            self.controller.show_frame(Main)

        util.menus(self, "icons/exit-menu-icon.png", "Sign Out", 0.8, sign_out_button,
                   util.white_font_color, False)

        def create_invoice():
            top_level = tk.Toplevel()
            top_level.title("Request Quotation")
            top_level.geometry("900x600")
            top_level.config(bg=util.secondary_color)
            util.destroy_frame(top_level)

            util.label(top_level, "Quotation Id", 12, "bold", util.white_font_color, util.secondary_color, 0.07, 0.03)
            quotation_id, quotation_id_var, quotation_id_frame = util.frame_entry(top_level, "", 0.33, 0.03, 0, 0, 200, 30)

            def search_quotation_id():
                search_query = f"SELECT quotation.client_name FROM quotation WHERE quotation_id = '{quotation_id_var.get()}'"
                self.cursor.execute(search_query)
                result = self.cursor.fetchone()

                client_name_var.set(result[0])

            util.button(top_level, 0.77, 0.03, 0, 0, 80, 30, "Search", 12, "bold", util.white_font_color,
                        util.primary_color, search_quotation_id, "")

            driver_details_frame = util.frame(top_level, util.tertiary_color, 1, 0.02, 0.1, 0, 0, 850, 30)
            util.label(driver_details_frame, "Personal Details", 13, "bold", util.white_font_color,
                       util.tertiary_color, 0.03, 0.02)

            util.label(top_level, "Client Name", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.18)
            client_name, client_name_var, client_name_frame = util.frame_entry(top_level, "", 0.22, 0.18, 0, 0, 200, 30)

            order_details_frame = util.frame(top_level, util.tertiary_color, 1, 0.02, 0.25, 0, 0, 850, 30)
            util.label(order_details_frame, "Invoice Details", 13, "bold", util.white_font_color,
                       util.tertiary_color, 0.03, 0.02)

            util.label(top_level, "Invoice Type", 12, "bold", util.white_font_color, util.secondary_color, 0.03,
                       0.32)
            get_invoice_type = util.combobox(top_level, 0.25, 0.32, ('Receivable', 'Payable'))

            util.label(top_level, "Payment Type", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.39)
            get_payment_type = util.combobox(top_level, 0.25, 0.39, ('Cash', 'Credit Card', 'Debit Card'))

            util.label(top_level, "Quantity", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.46)
            quantity, quantity_var, quantity_frame = util.frame_entry(top_level, "", 0.25,
                                                                                                    0.46, 0, 0, 200, 30)

            util.label(top_level, "Rate", 12, "bold", util.white_font_color, util.secondary_color, 0.5,
                       0.32)
            rate, rate_var, rate_frame = util.frame_entry(top_level, "", 0.7,
                                                                                                    0.32, 0, 0, 200, 30)

            util.label(top_level, "GST (%)", 12, "bold", util.white_font_color, util.secondary_color, 0.5,
                       0.39)
            gst, gst_var, gst_frame = util.frame_entry(top_level, "", 0.7, 0.39,
                                                                                              0, 0, 200, 30)

            util.label(top_level, "Total Amount", 12, "bold", util.white_font_color, util.secondary_color, 0.5, 0.46)
            total_amount, total_amount_var = util.label(top_level, "", 12, "bold", util.white_font_color, util.secondary_color, 0.7, 0.46)

            def calculate_amount():
                total = float(quantity_var.get()) * float(rate_var.get())
                total_gst = (float(gst_var.get()) / 100) * total
                total_shipping = (5 / 100) * (total * total_gst)
                total_amount_label = total + total_gst + total_shipping
                total_amount_var.set("{:.2f}".format(total_amount_label))
                self.shipping_amount = total_shipping

            util.button(top_level, 0.45, 0.55, 0, 0, 100, 30, "Calculate", 12, "bold", util.white_font_color,
                        util.primary_color, calculate_amount, "")

            def create_invoice_button():
                insert_query = "INSERT INTO invoice (invoice_id, user_id, invoice_type, payment_type, quantity, rate, gst, total_amount, status, shipping_charges) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (f"IN-{util.generate_id('4849')}", quotation_id_var.get(), get_invoice_type.get(), get_payment_type.get(), quantity_var.get(), rate_var.get(), gst_var.get(), total_amount_var.get(), 'Unpaid', self.shipping_amount)
                self.cursor.execute(insert_query, values)
                self.connection.commit()
                result = messagebox.showinfo("Application", "Invoice created successfully")
                if result == 'ok':
                    top_level.destroy()
                    self.display_invoice()

            util.button(top_level, 0.25, 0.8, 0, 0, 100, 35, "Create", 15, "bold", util.secondary_color, util.edit_color,
                        create_invoice_button, "")

            def back_button():
                top_level.destroy()

            util.button(top_level, 0.55, 0.8, 0, 0, 100, 35, "Cancel", 15, "bold", util.secondary_color, "red",
                        back_button, "")

            top_level.resizable(False, False)
            top_level.mainloop()

        create_btn = util.image(self.main, "icons/add-customer-icon.png", util.tertiary_color, 0.83, 0.1, 0, 0, 20, 20)
        util.button(self.main, 0.77, 0.1, 0, 0, 180, 50, "Create Invoice", 13, "bold", util.tertiary_color,
                    util.primary_color, create_invoice, create_btn)

        def update_invoice():
            top_level = tk.Toplevel()
            top_level.title("Request Quotation")
            top_level.geometry("900x600")
            top_level.config(bg=util.secondary_color)
            util.destroy_frame(top_level)

            util.label(top_level, "Invoice Id", 12, "bold", util.white_font_color, util.secondary_color, 0.07, 0.03)
            invoice_id, invoice_id_var, invoice_id_frame = util.frame_entry(top_level, "", 0.33, 0.03, 0, 0, 200, 30)

            def search_quotation_id():
                search_query = f"SELECT * FROM invoice WHERE quotation_id = '{invoice_id_var.get()}'"
                self.cursor.execute(search_query)
                result = self.cursor.fetchone()

                get_invoice_type.set(result[3])
                get_payment_type.set(result[4])
                quantity_var.set(result[5])
                rate_var.set(result[6])
                gst_var.set(result[7])
                total_amount_var.set(result[8])

            util.button(top_level, 0.77, 0.03, 0, 0, 80, 30, "Search", 12, "bold", util.white_font_color,
                        util.primary_color, search_quotation_id, "")

            order_details_frame = util.frame(top_level, util.tertiary_color, 1, 0.02, 0.25, 0, 0, 850, 30)
            util.label(order_details_frame, "Invoice Details", 13, "bold", util.white_font_color,
                       util.tertiary_color, 0.03, 0.02)

            util.label(top_level, "Invoice Type", 12, "bold", util.white_font_color, util.secondary_color, 0.03,
                       0.32)
            get_invoice_type = util.combobox(top_level, 0.25, 0.32, ('Receivable', 'Payable'))

            util.label(top_level, "Payment Type", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.39)
            get_payment_type = util.combobox(top_level, 0.25, 0.39, ('Cash', 'Credit Card', 'Debit Card'))

            util.label(top_level, "Quantity", 12, "bold", util.white_font_color, util.secondary_color, 0.03, 0.46)
            quantity, quantity_var, quantity_frame = util.frame_entry(top_level, "", 0.25,
                                                                      0.46, 0, 0, 200, 30)

            util.label(top_level, "Rate", 12, "bold", util.white_font_color, util.secondary_color, 0.5,
                       0.32)
            rate, rate_var, rate_frame = util.frame_entry(top_level, "", 0.7,
                                                          0.32, 0, 0, 200, 30)

            util.label(top_level, "GST (%)", 12, "bold", util.white_font_color, util.secondary_color, 0.5,
                       0.39)
            gst, gst_var, gst_frame = util.frame_entry(top_level, "", 0.7, 0.39,
                                                       0, 0, 200, 30)

            util.label(top_level, "Total Amount", 12, "bold", util.white_font_color, util.secondary_color, 0.5, 0.46)
            total_amount, total_amount_var = util.label(top_level, "", 12, "bold", util.white_font_color,
                                                        util.secondary_color, 0.7, 0.46)

            def calculate_amount():
                total = float(quantity_var.get()) * float(rate_var.get())
                total_gst = (float(gst_var.get()) / 100) * total
                total_shipping = (5 / 100) * (total * total_gst)
                total_amount_label = total + total_gst + total_shipping
                total_amount_var.set("{:.2f}".format(total_amount_label))
                self.shipping_amount = total_shipping

            util.button(top_level, 0.45, 0.55, 0, 0, 100, 30, "Calculate", 12, "bold", util.white_font_color,
                        util.primary_color, calculate_amount, "")

            def update_quotation_button():
                update_query = "UPDATE invoice SET invoice_type = %s, payment_type = %s, quantity = %s, rate = %s, gst = %s, total_amount = %s, shipping_charges = %s"
                values = (get_invoice_type.get(), get_payment_type.get(), quantity_var.get(), rate_var.get(), gst_var.get(), total_amount_var.get(), self.shipping_amount)
                self.cursor.execute(update_query, values)
                self.connection.commit()
                result = messagebox.showinfo("Application", "Quotation updated")
                if result == 'ok':
                    top_level.destroy()
                    self.display_invoice()

            util.button(top_level, 0.25, 0.8, 0, 0, 100, 35, "Update", 15, "bold", util.secondary_color,
                        util.edit_color,
                        update_quotation_button, "")

            def back_button():
                top_level.destroy()

            util.button(top_level, 0.55, 0.8, 0, 0, 100, 35, "Cancel", 15, "bold", util.secondary_color, "red",
                        back_button, "")

            top_level.resizable(False, False)
            top_level.mainloop()

        update_btn = util.image(self.main, "icons/add-customer-icon.png", util.tertiary_color, 0.6, 0.1, 0, 0, 20, 20)
        util.button(self.main, 0.6, 0.1, 0, 0, 180, 50, "Update Invoice", 13, "bold", util.tertiary_color,
                    util.primary_color, update_invoice, update_btn)

        self.scrollbar_window = util.frame(self.main, util.primary_color, 1, 0.03, 0.2, 0, 0, 1090, 650)
        self.display_invoice()

    def display_invoice(self):
        util.destroy_frame(self.scrollbar_window)

        query = "SELECT invoice.invoice_id, quotation.client_name, invoice.invoice_type, orders.departure_date, orders.arrival_date, invoice.total_amount, invoice.status FROM ((invoice INNER JOIN quotation ON invoice.user_id = quotation.quotation_id) INNER JOIN orders ON invoice.user_id = orders.user_id)"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        if results:
            header_canvas = util.canvas_frame(self.scrollbar_window, 1, util.primary_color, 0.03, 0, 1100, 30)

            canvas = tk.Canvas(self.scrollbar_window, bg=util.primary_color, highlightthickness=0,
                               scrollregion=(0, 0, 1650, 5000))
            canvas.pack(expand=True, fill='both')

            vertical_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='vertical', command=canvas.yview)
            horizontal_scrollbar = ttk.Scrollbar(self.scrollbar_window, orient='horizontal', command=canvas.xview)

            canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
            vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
            horizontal_scrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')

            canvas.bind("<MouseWheel>", lambda event: canvas.yview_scroll(-int(event.delta / 120), "units"))
            canvas.bind("<Control MouseWheel>", lambda event: canvas.xview_scroll(-int(event.delta / 120), "units"))

            def sync_scroll(*args):
                canvas.xview(*args)
                header_canvas.xview(*args)

            canvas.bind("<Configure>", lambda event: header_canvas.configure(scrollregion=(0, 0, 1650, 5000)))

            header_canvas.configure(xscrollcommand=lambda *args: sync_scroll('moveto', args[0]))
            canvas.configure(xscrollcommand=lambda *args: sync_scroll('moveto', args[0]))

            util.canvas_text(self.main, header_canvas, 30, 6, "ID", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 160, 6, "Client Name", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 450, 6, "Type", util.white_font_color, 13, "bold", False)
            util.canvas_text(self.main, header_canvas, 700, 6, "Date", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 1000, 6, "Due Date", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 1300, 6, "Total Amount", util.white_font_color, 13, "bold",
                             False)
            util.canvas_text(self.main, header_canvas, 1500, 6, "Status", util.white_font_color, 13, "bold", False)

            frame = tk.Frame(canvas, bg=util.secondary_color, borderwidth=1, relief='solid')
            canvas.create_window(0, 0, window=frame, anchor='nw')

            for index, result in enumerate(results):
                frame_canvas = util.canvas_frame(frame, 1, util.primary_color, 0, 4, 1650, 40)

                util.canvas_text(self.main, frame_canvas, 30, 12, result[0], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 160, 12, result[1], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 450, 12, result[2], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 700, 12, result[3], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1000, 12, result[4], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1300, 12, result[5], util.white_font_color, 13, "", True)
                util.canvas_text(self.main, frame_canvas, 1500, 12, result[6], util.white_font_color, 13, "", True)
        else:
            util.label(self.scrollbar_window, "No Invoice", 20, "bold", util.white_font_color,
                       util.primary_color, 0.4, 0.45)


class Reports(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=util.secondary_color)
        self.controller = controller
        util.destroy_frame(self)

        self.connection = mysql.connector.connect(user=util.user, host=util.host, database=util.database,
                                                  password=util.password)
        self.cursor = self.connection.cursor()

        menu_frame = tk.Frame(self, bg=util.primary_color)
        menu_frame.place(relx=0, rely=0, width=290, height=900)

        self.main = util.frame(self, util.secondary_color, 0, 0.2, 0, 0, 0, 1170, 830)

        util.profile(self.main, "Reports", "login_status/status.txt")

        util.menus(self, "icons/dashboard-menu-icon.png", "Dashboard", 0.2, lambda: self.controller.show_frame(Dashboard),
                   util.white_font_color, False)
        util.menus(self, "icons/quotation-menu-icon.png", "Quotation", 0.25, lambda: self.controller.show_frame(Quotation),
                   util.white_font_color, False)
        util.menus(self, "icons/orders-menu-icon.png", "Orders", 0.3, lambda: self.controller.show_frame(Orders),
                   util.white_font_color, False)
        util.menus(self, "icons/user-menu-icon.png", "Users", 0.35, lambda: self.controller.show_frame(Users),
                   util.white_font_color, False)
        util.menus(self, "icons/transport-menu-icon.png", "Transport", 0.4,
                   lambda: self.controller.show_frame(Transport),
                   util.white_font_color, False)
        util.menus(self, "icons/warehouse-menu-icon.png", "Warehouse", 0.45,
                   lambda: self.controller.show_frame(Warehouse),
                   util.white_font_color, False)
        util.menus(self, "icons/shipment-menu-icon.png", "Shipments", 0.5,
                   lambda: self.controller.show_frame(Shipments),
                   util.white_font_color, False)
        util.menus(self, "icons/tracking-menu-icon.png", "Tracking", 0.55,
                   lambda: self.controller.show_frame(Tracking),
                   util.white_font_color, False)
        util.menus(self, "icons/invoice-menu-icon.png", "Invoice", 0.6, lambda: self.controller.show_frame(Invoice),
                   util.white_font_color, False)
        util.menus(self, "icons/reports-menu-icon.png", "Reports", 0.65, lambda: self.controller.show_frame(Reports),
                   util.tertiary_color, True)

        def sign_out_button():
            util.sign_out("login_status/status.txt")
            self.controller.show_frame(Main)

        util.menus(self, "icons/exit-menu-icon.png", "Sign Out", 0.8, sign_out_button,
                   util.white_font_color, False)


app = Application()
app.mainloop()
