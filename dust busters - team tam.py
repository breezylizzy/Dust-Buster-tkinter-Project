import re
import csv
import tkinter as tk
from tkinter import messagebox, PhotoImage, Entry, Button, Canvas, Checkbutton, Label, Listbox, Frame, OptionMenu, END, StringVar
from PIL import Image, ImageTk
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./")


class DustBusters:
    def __init__(self, master):
        self.profile_window_open = None
        self.profile_window = None
        self.cart_window = None
        self.order_window = None
        self.homecare_window = None
        self.laundry_window = None
        self.clothes_window = None
        self.confirm_window = None
        self.payment_var = StringVar()
        self.delivery_var = StringVar()
        self.master = master
        master.title("Dust Busters")
        master.geometry("1430x835")

        self.splash_bg = Image.open("splash.png").resize((1430, 835))
        self.splash_bg = ImageTk.PhotoImage(self.splash_bg)

        self.create_bg = Image.open("image_bg_signup.png").resize((1430, 835))
        self.create_bg = ImageTk.PhotoImage(self.create_bg)

        self.new_username_entry = None
        self.new_email_entry = None
        self.new_password_entry = None

        self.delivery_cost = 0
        self.price_dict = {}
        self.item_data = {}

    def show_splash_and_start(self):
        splash_window = tk.Toplevel(self.master)
        splash_window.title("Dust Busters")
        splash_window.geometry("1430x835")

        splash_label = tk.Label(
            splash_window,
            image=self.splash_bg
        )
        splash_label.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        splash_window.after(1000, lambda: self.close_splash_and_start(splash_window))

    def close_splash_and_start(self, window):
        window.destroy()
        self.show_login()

    def show_login(self):  # Login Page
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        self.login_window = tk.Toplevel(self.master)
        self.login_window.title("Dust Busters")
        self.login_window.geometry("1430x835")

        self.canvas1 = Canvas(
            self.login_window,
            bg="#FFFFFF",
            height=835,
            width=1430,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas1.place(x=0, y=0)

        self.image_login_1 = PhotoImage(file=relative_to_assets("image_login.png"))
        self.login_1 = self.canvas1.create_image(
            715.0,
            417.0,
            image=self.image_login_1
        )

        self.canvas1.create_rectangle(
            710.0,
            0.0,
            1430.0,
            835.0,
            fill="#B2CBDE",
            outline=""
        )

        self.image_login_2 = PhotoImage(file=relative_to_assets("image_logintext.png"))
        self.login_2 = self.canvas1.create_image(
            1071.0,
            210.0,
            image=self.image_login_2
        )

        self.canvas1.create_text(
            838.0,
            313.0,
            anchor="nw",
            text="USERNAME / EMAIL",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.entry_login_1 = PhotoImage(file=relative_to_assets("entry_1_login.png"))
        self.login_bg_1 = self.canvas1.create_image(
            1070.0,
            377.5,
            image=self.entry_login_1
        )

        self.username = Entry(
            self.login_window,
            bd=0, bg="#D9D9D9",
            fg="#000716",
            font=("Inter", 20 * -1),
            highlightthickness=0
        )
        self.username.place(
            x=848.0,
            y=347.0,
            width=444.0,
            height=59.0
        )

        self.canvas1.create_text(
            838.0,
            429.0,
            anchor="nw",
            text="PASSWORD",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.entry_login_2 = PhotoImage(file=relative_to_assets("entry_2_login.png"))
        self.login_bg_2 = self.canvas1.create_image(
            1070.0,
            493.0,
            image=self.entry_login_2
        )

        self.password = Entry(
            self.login_window,
            bd=0, bg="#D9D9D9",
            fg="#000716",
            font=("Inter", 20 * -1),
            highlightthickness=0,
            show="*")
        self.password.place(
            x=848.0,
            y=463.0,
            width=444.0,
            height=58.0
        )

        self.button_login_1 = PhotoImage(file=relative_to_assets("button_login.png"))
        self.bt_login_1 = Button(
            self.login_window,
            image=self.button_login_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,
            relief="flat"
        )
        self.bt_login_1.place(
            x=838.0,
            y=596.0,
            width=464.0,
            height=60.0
        )

        self.canvas1.create_text(
            841.0,
            677.0,
            anchor="nw",
            text="Don't have an account?",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.button_login_2 = PhotoImage(file=relative_to_assets("button_signin.png"))
        self.bt_login_2 = Button(
            self.login_window,
            image=self.button_login_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_create_account,
            relief="flat"
        )
        self.bt_login_2.place(
            x=1211.0,
            y=671.0,
            width=94.0,
            height=35.0
        )

        def toggle_password():
            if self.show_password.get():
                self.password.config(show="")
            else:
                self.password.config(show="*")

        self.show_password = tk.BooleanVar()
        self.checkbox = Checkbutton(
            self.login_window,
            text="Show Password",
            variable=self.show_password,
            command=toggle_password,
            bg="#B2CBDE",
            fg="black"
        )
        self.checkbox.place(x=848.0, y=528.0)

    def open_login(self):
        if not self.login_window or not self.login_window.winfo_exists():
            self.show_login()
        else:
            self.login_window.deiconify()
            if hasattr(self, 'create_account_window') and self.create_account_window:
                self.create_account_window.destroy()

    def hide_login(self):
        if self.login_window:
            self.login_window.withdraw()

    def write_to_csv(self, name, email, password):
        with open('accounts.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, email, password])

    def login(self):  # Methods for login to existing account
        global session
        user_input = self.username.get()
        password = self.password.get()

        with open('accounts.csv', mode='r') as file:
            reader = csv.reader(file)
            accounts = {row[0]: (row[1], row[2]) for row in reader}

        for username, data in accounts.items():
            stored_email = data[0]
            stored_password = data[1]

            if user_input in [username, stored_email] and stored_password == password:
                messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                session = [username, stored_email, stored_password]
                self.hide_login()
                self.home()
                return

        messagebox.showerror("Login Failed", "Invalid username or password.\nPlease create an account first.")

    def create_account(self):  # Create New Account Page
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        self.create_account_window = tk.Toplevel(self.master)
        self.create_account_window.title("Dust Busters")
        self.create_account_window.geometry("1430x835")

        self.canvas2 = Canvas(
            self.create_account_window,
            bg="#FFFFFF",
            height=835,
            width=1430,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas2.place(x=0, y=0)

        self.image_signup_1 = PhotoImage(file=relative_to_assets("image_bg_signup.png"))
        self.signup_1 = self.canvas2.create_image(
            715.0,
            417.0,
            image=self.image_signup_1
        )

        self.button_signup_1 = PhotoImage(file=relative_to_assets("button_signup.png"))
        self.bt_su_1 = Button(
            self.create_account_window,
            image=self.button_signup_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.create_success,
            relief="flat"
        )
        self.bt_su_1.place(x=108.0, y=635.0, width=464.0, height=60.0)

        self.image_signup_2 = PhotoImage(file=relative_to_assets("image_signuptext.png"))
        self.signup_2 = self.canvas2.create_image(
            1244.0,
            112.0,
            image=self.image_signup_2
        )

        self.image_signup_3 = PhotoImage(file=relative_to_assets("image_createacctext.png"))
        self.signup_3 = self.canvas2.create_image(
            336.0,
            154.0,
            image=self.image_signup_3
        )

        self.button_signup_2 = PhotoImage(file=relative_to_assets("button_login2.png"))
        self.bt_su_2 = Button(
            self.create_account_window,
            image=self.button_signup_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_login,
            relief="flat"
        )
        self.bt_su_2.place(
            x=393.0,
            y=708.0,
            width=94.0,
            height=35.0
        )

        self.canvas2.create_text(
            193.0, 714.0,
            anchor="nw",
            text="Already Registered?",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.entry_signup_1 = PhotoImage(file=relative_to_assets("entry_1_signup.png"))
        self.signup_bg_1 = self.canvas2.create_image(
            340.0,
            306.5,
            image=self.entry_signup_1
        )

        self.new_username_entry = Entry(
            self.create_account_window,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            font=("Inter", 20 * -1),
            highlightthickness=0
        )
        self.new_username_entry.place(x=118.0, y=276.0, width=444.0, height=59.0)

        self.canvas2.create_text(
            108.0, 242.0,
            anchor="nw",
            text="USERNAME",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.entry_signup_2 = PhotoImage(file=relative_to_assets("entry_2_signup.png"))
        self.signup_bg_2 = self.canvas2.create_image(
            340.0,
            423.0,
            image=self.entry_signup_2
        )

        self.new_email_entry = Entry(
            self.create_account_window,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            font=("Inter", 20 * -1),
            highlightthickness=0
        )
        self.new_email_entry.place(
            x=118.0,
            y=393.0,
            width=444.0,
            height=58.0
        )

        self.canvas2.create_text(
            108.0, 364.0,
            anchor="nw",
            text="EMAIL",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.entry_signup_3 = PhotoImage(file=relative_to_assets("entry_3_signup.png"))
        self.signup_bg_3 = self.canvas2.create_image(
            340.0,
            540.0,
            image=self.entry_signup_3
        )

        self.new_password_entry = Entry(
            self.create_account_window,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            font=("Inter", 20 * -1),
            highlightthickness=0,
            show="*"
        )
        self.new_password_entry.place(
            x=118.0,
            y=510.0,
            width=444.0,
            height=58.0
        )

        self.canvas2.create_text(
            108.0, 481.0,
            anchor="nw",
            text="PASSWORD",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        def toggle_new_password():
            if self.show_new_password.get():
                self.new_password_entry.config(show="")
            else:
                self.new_password_entry.config(show="*")

        self.show_new_password = tk.BooleanVar()
        self.checkbox_new = Checkbutton(
            self.create_account_window,
            text="Show Password",
            variable=self.show_new_password,
            command=toggle_new_password,
            bg="white",
            fg="black"
        )
        self.checkbox_new.place(x=118.0, y=580.0)

    def open_create_account(self):
        self.hide_login()
        self.show_create_account()

    def show_create_account(self):
        if hasattr(self, 'create_account_window'):
            self.create_account_window.destroy()

        self.create_account()
        self.hide_login()

    def hide_create_account(self):
        if hasattr(self, 'create_account_window') and self.create_account_window:
            self.create_account_window.destroy()
            self.show_login()

    def check_existing_email(self, email):
        with open('accounts.csv', mode='r') as file:
            reader = csv.reader(file)
            existing_emails = [row[1] for row in reader]

        return email in existing_emails

    def update_profile_labels(self):
        self.username_pf.config(text=self.new_name if self.new_name else session[0])
        self.email_pf.config(text=self.new_email if self.new_email else session[1])
        self.pass_pf.config(text=self.new_password if self.new_password else session[2])

    def create_success(self):  # Methods for validating input and creating account
        global session
        name = self.new_username_entry.get()
        email = self.new_email_entry.get()
        new_password = self.new_password_entry.get()

        if self.check_existing_email(email):
            messagebox.showerror("Existing Email", "Email already exists. Please use a different email.")
            return

        # Validasi password
        if not (4 <= len(new_password) <= 10):
            messagebox.showerror("Invalid Password Length", "Password must be between 4 and 10 characters.")
            return

        if not re.search("[a-z]", new_password):
            messagebox.showerror("Invalid Password", "Password must contain at least one lowercase letter.")
            return

        if not re.search("[A-Z]", new_password):
            messagebox.showerror("Invalid Password", "Password must contain at least one uppercase letter.")
            return

        if not re.search("[0-9]", new_password):
            messagebox.showerror("Invalid Password", "Password must contain at least one digit.")
            return

        # Validasi alamat email
        if not (email.endswith('@gmail.com')):
            messagebox.showerror("Invalid Email", "Please enter a valid email address ending with @gmail.com")
            return

        if not all((name, email, new_password)):
            messagebox.showerror("Incomplete Information", "Please fill in all fields to create an account.")
            return

        self.new_name = name
        self.new_email = email
        self.new_password = new_password

        self.write_to_csv(name, email, new_password)
        messagebox.showinfo("Account Created", "Account created successfully!")
        session = [name, email, new_password]

        self.master.withdraw()
        self.create_account_window.destroy()
        self.home()
        self.update_profile_labels()

    def home(self):  # Dashboard Page
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        self.home_window = tk.Toplevel(self.master)
        self.home_window.title("Dust Busters")
        self.home_window.geometry("1430x835")

        self.canvas3 = Canvas(
            self.home_window,
            bg="#FFFFFF",
            height="835",
            width="1430",
            bd="0",
            highlightthickness="0",
            relief="ridge"
        )
        self.canvas3.place(x=0, y=0)

        self.canvas3.create_rectangle(
            0.0,
            0.0,
            337.0,
            835.0,
            fill="#B2CBDE",
            outline=""
        )

        self.image_home_1 = PhotoImage(file=relative_to_assets("image_logo.png"))
        self.home_1 = self.canvas3.create_image(
            79.0,
            84.0,
            image=self.image_home_1
        )

        self.image_home_2 = PhotoImage(file=relative_to_assets("image_dbtext.png"))
        self.home_2 = self.canvas3.create_image(
            218.0,
            94.0,
            image=self.image_home_2
        )

        self.canvas3.create_rectangle(
            336.0,
            122.0,
            1429.9998779296875,
            123.03045654296875,
            fill="#000000",
            outline=""
        )

        self.image_home_3 = PhotoImage(file=relative_to_assets("image_logo2.png"))
        self.home_3 = self.canvas3.create_image(
            1361.0,
            55.0,
            image=self.image_home_3
        )

        self.image_home_4 = PhotoImage(file=relative_to_assets("image_dashboard.png"))
        self.home_4 = self.canvas3.create_image(
            873.0,
            272.0,
            image=self.image_home_4
        )

        self.button_home_1 = PhotoImage(file=relative_to_assets("button_dashboard.png"))
        self.bt_home_1 = Button(
            self.home_window,
            image=self.button_home_1,
            borderwidth='0',
            highlightthickness='0',
            relief="flat"
        )
        self.bt_home_1.place(
            x=53.0,
            y=180.0,
            width=232.0,
            height=63.0
        )

        self.button_home_2 = PhotoImage(file=relative_to_assets("button_profile.png"))
        self.bt_home_2 = Button(
            self.home_window,
            image=self.button_home_2,
            borderwidth='0',
            highlightthickness='0',
            command=self.open_profile,
            relief="flat"
        )
        self.bt_home_2.place(
            x=53.0,
            y=270.0,
            width=232.0,
            height=63.0
        )

        self.button_home_3 = PhotoImage(file=relative_to_assets("button_cart.png"))
        self.bt_home_3 = Button(
            self.home_window,
            image=self.button_home_3,
            borderwidth='0',
            highlightthickness='0',
            command=self.open_cart,
            relief="flat"
        )
        self.bt_home_3.place(
            x=53.0,
            y=360.0,
            width=232.0,
            height=63.0
        )

        self.button_home_4 = PhotoImage(file=relative_to_assets("button_orders.png"))
        self.bt_home_4 = Button(
            self.home_window,
            image=self.button_home_4,
            borderwidth='0',
            highlightthickness='0',
            command=self.open_order,
            relief="flat"
        )
        self.bt_home_4.place(
            x=53.0,
            y=450.0,
            width=232.0,
            height=63.0
        )

        self.button_home_5 = PhotoImage(file=relative_to_assets("button_exit.png"))
        self.bt_home_5 = Button(
            self.home_window,
            image=self.button_home_5,
            borderwidth='0',
            highlightthickness='0',
            command=self.exit,
            relief="flat"
        )
        self.bt_home_5.place(
            x=53.0,
            y=720.0,
            width=232.0,
            height=63.0
        )

        self.image_home_5 = PhotoImage(file=relative_to_assets("image_db_greetings.png"))
        self.home_5 = self.canvas3.create_image(
            541.0,
            454.0,
            image=self.image_home_5
        )

        self.button_home_6 = PhotoImage(file=relative_to_assets("button_homecare.png"))
        self.bt_home_6 = Button(
            self.home_window,
            image=self.button_home_6,
            borderwidth=0,
            highlightthickness=0,
            command=self.homecare,
            relief="flat"
        )
        self.bt_home_6.place(
            x=415.0,
            y=560.0,
            width=407.0,
            height=218.0
        )

        self.button_home_7 = PhotoImage(file=relative_to_assets("button_laundry.png"))
        self.bt_home_7 = Button(
            self.home_window,
            image=self.button_home_7,
            borderwidth=0,
            highlightthickness=0,
            command=self.laundry,
            relief="flat"
        )
        self.bt_home_7.place(
            x=900.0,
            y=560.0,
            width=407.0,
            height=218.0
        )

        self.image_home_6 = PhotoImage(file=relative_to_assets("image_db_design.png"))
        self.home_6 = self.canvas3.create_image(
            1305.0,
            457.0,
            image=self.image_home_6
        )

        self.canvas3.create_rectangle(
            336.0,
            527.0,
            715.0,
            529.0,
            fill="#000000",
            outline=""
        )

        self.image_home_7 = PhotoImage(file=relative_to_assets("image_dashboardtext.png"))
        self.home_7 = self.canvas3.create_image(
            492.0,
            57.0,
            image=self.image_home_7
        )

    def open_home(self):
        if hasattr(self, "homecare_window"):
            self.hide_homecare()
        elif hasattr(self, "profile_window"):
            self.hide_profile()
        elif hasattr(self, "laundry_window"):
            self.hide_laundry()
        elif hasattr(self, "cart_window"):
            self.hide_cart()
        elif hasattr(self, "order_window"):
            self.hide_order()
        elif hasattr(self, "confirm_window"):
            self.hide_confirm()
        elif hasattr(self, "clothes_window"):
            self.hide_clothes()

        self.show_home()

    def show_home(self):
        if hasattr(self, 'home_window'):
            self.home_window.destroy()

        self.home()
        self.hide_profile()
        self.hide_cart()
        # self.hide_laundry()
        self.hide_clothes()
        self.hide_order()
        self.hide_confirm()

    def hide_home(self):
        if hasattr(self, 'home_window') and self.home_window and self.home_window.winfo_exists():
            self.home_window.withdraw()
        elif hasattr(self, 'laundry_window') and self.laundry_window and self.laundry_window.winfo_exists():
            self.laundry_window.withdraw()
        elif hasattr(self, 'homecare_window') and self.homecare_window and self.homecare_window.winfo_exists():
            self.homecare_window.withdraw()
        elif hasattr(self, 'profile_window') and self.profile_window and self.profile_window.winfo_exists():
            self.profile_window.withdraw()
        elif hasattr(self, 'order_window') and self.order_window and self.order_window.winfo_exists():
            self.order_window.withdraw()
        elif hasattr(self, 'confirm_window') and self.confirm_window and self.confirm_window.winfo_exists():
            self.confirm_window.withdraw()
        elif hasattr(self, 'clothes_window') and self.clothes_window and self.clothes_window.winfo_exists():
            self.clothes_window.withdraw()

    def profile_content(self):  # Profile Page
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        self.profile_window = tk.Toplevel(self.master)
        self.profile_window.title("Dust Busters")
        self.profile_window.geometry("1430x835")

        self.canvas4 = Canvas(
            self.profile_window,
            bg="#FFFFFF",
            height=835,
            width=1430,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas4.place(x=0, y=0)

        self.canvas4.create_rectangle(
            0.0,
            0.0,
            337.0,
            835.0,
            fill="#B2CBDE",
            outline=""
        )

        self.image_pf_1 = PhotoImage(file=relative_to_assets("image_accountinfo.png"))
        self.pf_1 = self.canvas4.create_image(
            699.0,
            104.0,
            image=self.image_pf_1
        )

        self.image_pf_2 = PhotoImage(file=relative_to_assets("image_iconprofile.png"))
        self.pf_2 = self.canvas4.create_image(
            829.0,
            281.0,
            image=self.image_pf_2
        )

        self.entry_pf_1 = PhotoImage(file=relative_to_assets("entry_1_profile.png"))
        self.pf_bg_1 = self.canvas4.create_image(
            829.0,
            473.5,
            image=self.entry_pf_1
        )

        self.username_pf = Label(
            self.profile_window,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            font=("Inter", 20 * -1),
            highlightthickness=0
        )
        self.username_pf.place(
            x=607.0,
            y=443.0,
            width=444.0,
            height=59.0
        )

        self.canvas4.create_text(
            597.0,
            409.0,
            anchor="nw",
            text="USERNAME",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.entry_pf_2 = PhotoImage(file=relative_to_assets("entry_2_profile.png"))
        self.pf_bg_2 = self.canvas4.create_image(
            829.0,
            590.0,
            image=self.entry_pf_2
        )

        self.email_pf = Label(
            self.profile_window,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            font=("Inter", 20 * -1),
            highlightthickness=0
        )
        self.email_pf.place(
            x=607.0,
            y=560.0,
            width=444.0,
            height=58.0
        )

        self.canvas4.create_text(
            597.0,
            531.0,
            anchor="nw",
            text="EMAIL",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.entry_pf_3 = PhotoImage(file=relative_to_assets("entry_3_profile.png"))
        self.pf_bg_3 = self.canvas4.create_image(
            829.0,
            707.0,
            image=self.entry_pf_3
        )

        self.pass_pf = Label(
            self.profile_window,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            font=("Inter", 20 * -1),
            highlightthickness=0
        )
        self.pass_pf.place(
            x=607.0,
            y=677.0,
            width=444.0,
            height=58.0
        )

        self.canvas4.create_text(
            597.0,
            648.0,
            anchor="nw",
            text="PASSWORD",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.button_pf_1 = PhotoImage(file=relative_to_assets("button_logout.png"))
        self.bt_pf_1 = Button(
            self.profile_window,
            image=self.button_pf_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.logout,
            relief="flat"
        )
        self.bt_pf_1.place(
            x=1210.0,
            y=765.0,
            width=204.0,
            height=37.0
        )

        self.image_pf_4 = PhotoImage(file=relative_to_assets("image_logo.png"))
        self.pf_4 = self.canvas4.create_image(
            79.0,
            84.0,
            image=self.image_pf_4
        )

        self.image_pf_5 = PhotoImage(file=relative_to_assets("image_dbtext.png"))
        self.pf_5 = self.canvas4.create_image(
            218.0,
            94.0,
            image=self.image_pf_5
        )

        self.button_pf_2 = PhotoImage(file=relative_to_assets("button_dashboard.png"))
        self.bt_pf_2 = Button(
            self.profile_window,
            image=self.button_pf_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_home,
            relief="flat"
        )
        self.bt_pf_2.place(
            x=53.0,
            y=180.0,
            width=232.0,
            height=63.0
        )

        self.button_pf_3 = PhotoImage(file=relative_to_assets("button_profile.png"))
        self.bt_pf_3 = Button(
            self.profile_window,
            image=self.button_pf_3,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.bt_pf_3.place(
            x=53.0,
            y=270.0,
            width=232.0,
            height=63.0
        )

        self.button_pf_4 = PhotoImage(file=relative_to_assets("button_cart.png"))
        self.bt_pf_4 = Button(
            self.profile_window,
            image=self.button_pf_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_cart,
            relief="flat"
        )
        self.bt_pf_4.place(
            x=53.0,
            y=360.0,
            width=232.0,
            height=63.0
        )

        self.button_pf_5 = PhotoImage(file=relative_to_assets("button_orders.png"))
        self.bt_pf_5 = Button(
            self.profile_window,
            image=self.button_pf_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_order,
            relief="flat"
        )
        self.bt_pf_5.place(
            x=53.0,
            y=450.0,
            width=232.0,
            height=63.0
        )

        self.button_pf_6 = PhotoImage(file=relative_to_assets("button_exit.png"))
        self.bt_pf_6 = Button(
            self.profile_window,
            image=self.button_pf_6,
            borderwidth=0,
            highlightthickness=0,
            command=self.exit,
            relief="flat"
        )
        self.bt_pf_6.place(
            x=53.0,
        
            y=720.0,
            width=232.0,
            height=63.0
        )

        self.username_pf.config(text=session[0])
        self.email_pf.config(text=session[1])
        self.pass_pf.config(text=session[2])

    def open_profile(self):
        if hasattr(self, "homecare_window"):
            self.hide_homecare()
        elif hasattr(self, "home_window"):
            self.hide_home()
        elif hasattr(self, "laundry_window"):
            self.hide_laundry()
        elif hasattr(self, "cart_window"):
            self.hide_cart()
        elif hasattr(self, "order_window"):
            self.hide_order()
        elif hasattr(self, "confirm_window"):
            self.hide_confirm()
        elif hasattr(self, "clothes_window"):
            self.hide_clothes()

        self.show_profile()

    def show_profile(self):
        if hasattr(self, 'profile_window') and self.profile_window is not None:
            self.profile_window.destroy()

        self.profile_content()
        self.hide_home()
        self.hide_cart()
        self.hide_laundry()
        self.hide_clothes()
        self.hide_order()
        self.hide_confirm()

    def hide_profile(self):
        if self.profile_window:
            self.profile_window.withdraw()

    def homecare(self):  # Homecare Page
        if hasattr(self, 'home_window'):
            self.home_window.destroy()

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        # cart = []

        def write_to_cart(data):
            csv_columns = ['categories', 'qty', 'total_price']

            # Jika file belum ada, tulis header kolom
            if not Path('cart_content.csv').is_file():
                with open('cart_content.csv', mode='w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                    writer.writeheader()

            # Tambahkan data baru ke file CSV
            with open('cart_content.csv', mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writerow(data)

        def add_to_cart(categories, qty, price_dict):
            data = {'categories': categories, 'qty': qty}

            # Mendapatkan harga dari dictionary price_dict
            price = price_dict.get(categories, 0)  # Mengambil harga dari dictionary, default 0 jika tidak ada

            # Mengalikan harga dengan kuantitas
            total_price = price * qty

            # Menambahkan informasi harga ke data
            data['total_price'] = total_price  # Menambahkan total harga ke data

            # Tulis ke file CSV
            write_to_cart(data)

            messagebox.showinfo("Info", f"{categories} has been added to cart!")

        self.homecare_window = tk.Toplevel(self.master)
        self.homecare_window.title("Dust Busters")
        self.homecare_window.geometry("1430x835")

        self.canvas5 = Canvas(
            self.homecare_window,
            bg="#FFFFFF",
            height=835,
            width=1430,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas5.place(x=0, y=0)

        self.canvas5.create_rectangle(
            0.0,
            0.0,
            337.0,
            835.0,
            fill="#B2CBDE",
            outline=""
        )

        self.image_hc_1 = PhotoImage(file=relative_to_assets("image_logo.png"))
        self.hc_1 = self.canvas5.create_image(
            79.0,
            84.0,
            image=self.image_hc_1
        )

        self.image_hc_2 = PhotoImage(file=relative_to_assets("image_dbtext.png"))
        self.hc_2 = self.canvas5.create_image(
            218.0,
            94.0,
            image=self.image_hc_2
        )

        self.canvas5.create_rectangle(
            336.0,
            122.0,
            1429.9998779296875,
            123.03045654296875,
            fill="#000000",
            outline=""
        )

        self.image_hc_3 = PhotoImage(file=relative_to_assets("image_logo2.png"))
        self.hc_3 = self.canvas5.create_image(
            1361.0,
            55.0,
            image=self.image_hc_3
        )

        self.image_hc_4 = PhotoImage(file=relative_to_assets("image_categories.png"))
        self.hc_4 = self.canvas5.create_image(
            1004.0,
            343.0,
            image=self.image_hc_4
        )

        self.button_hc_1 = PhotoImage(file=relative_to_assets("button_dashboard.png"))
        self.bt_hc_1 = Button(
            self.homecare_window,
            image=self.button_hc_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_home,
            relief="flat"
        )
        self.bt_hc_1.place(
            x=53.0,
            y=180.0,
            width=232.0,
            height=63.0
        )

        self.button_hc_2 = PhotoImage(file=relative_to_assets("button_profile.png"))
        self.bt_hc_2 = Button(
            self.homecare_window,
            image=self.button_hc_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_profile,
            relief="flat")
        self.bt_hc_2.place(
            x=53.0,
            y=270.0,
            width=232.0,
            height=63.0
        )

        self.button_hc_3 = PhotoImage(file=relative_to_assets("button_cart.png"))
        self.bt_hc_3 = Button(
            self.homecare_window,
            image=self.button_hc_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_cart,
            relief="flat"
        )
        self.bt_hc_3.place(
            x=53.0,
            y=360.0,
            width=232.0,
            height=63.0
        )

        self.button_hc_4 = PhotoImage(file=relative_to_assets("button_orders.png"))
        self.bt_hc_4 = Button(
            self.homecare_window,
            image=self.button_hc_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_order,
            relief="flat"
        )
        self.bt_hc_4.place(
            x=53.0,
            y=450.0,
            width=232.0,
            height=63.0
        )

        self.button_hc_5 = PhotoImage(file=relative_to_assets("button_exit.png"))
        self.bt_hc_5 = Button(
            self.homecare_window,
            image=self.button_hc_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.exit,
            relief="flat"
        )
        self.bt_hc_5.place(
            x=53.0,
            y=720.0,
            width=232.0,
            height=63.0
        )

        self.image_hc_5 = PhotoImage(file=relative_to_assets("image_homecare.png"))
        self.hc_5 = self.canvas5.create_image(
            580.0,
            456.0,
            image=self.image_hc_5
        )

        self.button_hc_6 = PhotoImage(file=relative_to_assets("button_mitee.png"))
        self.bt_hc_6 = Button(
            self.homecare_window,
            image=self.button_hc_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: add_to_cart('Mitee Vacum', 1, self.price_dict),
            relief="flat"
        )
        self.bt_hc_6.place(
            x=831.0,
            y=478.0,
            width=253.81915283203125,
            height=238.0
        )

        self.button_hc_7 = PhotoImage(file=relative_to_assets("button_area.png"))
        self.bt_hc_7 = Button(
            self.homecare_window,
            image=self.button_hc_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: add_to_cart('Spesific Area Cleaning', 1, self.price_dict),
            relief="flat"
        )
        self.bt_hc_7.place(
            x=1135.0,
            y=482.0,
            width=249.251220703125,
            height=237.0
        )

        self.button_hc_8 = PhotoImage(file=relative_to_assets("button_house.png"))
        self.bt_hc_8 = Button(
            self.homecare_window,
            image=self.button_hc_8,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: add_to_cart('Whole House Cleaning', 1, self.price_dict),
            relief="flat"
        )
        self.bt_hc_8.place(
            x=1128.0,
            y=198.6053009033203,
            width=243.5880126953125,
            height=240.19467163085938
        )

        self.image_hc_6 = PhotoImage(file=relative_to_assets("image_homecaretext.png"))
        self.hc_6 = self.canvas5.create_image(
            492.0,
            57.0,
            image=self.image_hc_6
        )

    def show_homecare(self):
        if hasattr(self, 'homecare_window') and self.homecare_window is not None:
            self.homecare_window.destroy()

        self.homecare()
        self.hide_profile()
        self.hide_home()
        self.hide_cart()
        self.hide_order()

    def homecare_content(self):
        self.button_homecare_cart = Button(
            self.homecare_window,
            text="Open Cart",
            command=self.open_cart_from_homecare,
            relief="flat"
        )
        self.button_homecare_cart.place(x=200, y=200, width=100, height=30)

    def hide_homecare(self):
        if self.homecare_window:
            self.homecare_window.withdraw()

    def open_cart_from_homecare(self):
        if hasattr(self, "home_window"):
            self.hide_home()
        elif hasattr(self, "laundry_window"):
            self.hide_laundry()
        elif hasattr(self, "homecare_window"):
            self.hide_homecare()
        elif hasattr(self, "profile_window"):
            self.hide_profile()
        elif hasattr(self, "order_window"):
            self.hide_order()

        self.show_cart()

    def laundry(self):  # Laundry Page
        if hasattr(self, 'home_window'):
            self.home_window.destroy()

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        cart = []

        def write_to_cart(data):
            csv_columns = ['categories', 'qty', 'total_price']

            # Jika file belum ada, tulis header kolom
            if not Path('cart_content.csv').is_file():
                with open('cart_content.csv', mode='w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                    writer.writeheader()

            # Tambahkan data baru ke file CSV
            with open('cart_content.csv', mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writerow(data)

        def add_to_cart(categories, qty, price_dict):
            data = {'categories': categories, 'qty': qty}

            # Mendapatkan harga dari dictionary price_dict
            price = price_dict.get(categories, 0)  # Mengambil harga dari dictionary, default 0 jika tidak ada

            # Mengalikan harga dengan kuantitas
            total_price = price * qty

            # Menambahkan informasi harga ke data
            data['total_price'] = total_price  # Menambahkan total harga ke data

            # Tulis ke file CSV
            write_to_cart(data)

            messagebox.showinfo("Info", f"{categories} has been added to cart!")

        self.laundry_window = tk.Toplevel(self.master)
        self.laundry_window.title("Dust Busters")
        self.laundry_window.geometry("1430x835")

        self.canvas6 = Canvas(
            self.laundry_window,
            bg="#FFFFFF",
            height=835,
            width=1430,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas6.place(x=0, y=0)

        self.canvas6.create_rectangle(
            0.0,
            0.0,
            337.0,
            835.0,
            fill="#B2CBDE",
            outline=""
        )

        self.image_ld_1 = PhotoImage(file=relative_to_assets("image_logo.png"))
        self.ld_1 = self.canvas6.create_image(
            79.0,
            84.0,
            image=self.image_ld_1
        )

        self.image_ld_2 = PhotoImage(file=relative_to_assets("image_dbtext.png"))
        self.ld_2 = self.canvas6.create_image(
            218.0,
            94.0,
            image=self.image_ld_2
        )

        self.canvas6.create_rectangle(
            336.0,
            122.0,
            1429.9998779296875,
            123.03045654296875,
            fill="#000000",
            outline=""
        )

        self.image_ld_3 = PhotoImage(file=relative_to_assets("image_logo2.png"))
        self.ld_3 = self.canvas6.create_image(
            1361.0,
            55.0,
            image=self.image_ld_3
        )

        self.button_ld_1 = PhotoImage(file=relative_to_assets("button_dashboard.png"))
        self.bt_ld_1 = Button(
            self.laundry_window,
            image=self.button_ld_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_home,
            relief="flat"
        )
        self.bt_ld_1.place(
            x=53.0,
            y=180.0,
            width=232.0,
            height=63.0
        )

        self.button_ld_2 = PhotoImage(file=relative_to_assets("button_profile.png"))
        self.bt_ld_2 = Button(
            self.laundry_window,
            image=self.button_ld_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_profile,
            relief="flat"
        )
        self.bt_ld_2.place(
            x=53.0,
            y=270.0,
            width=232.0,
            height=63.0
        )

        self.button_ld_3 = PhotoImage(file=relative_to_assets("button_cart.png"))
        self.bt_ld_3 = Button(
            self.laundry_window,
            image=self.button_ld_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_cart,
            relief="flat"
        )
        self.bt_ld_3.place(
            x=53.0,
            y=360.0,
            width=232.0,
            height=63.0
        )

        self.button_ld_4 = PhotoImage(file=relative_to_assets("button_orders.png"))
        self.bt_ld_4 = Button(
            self.laundry_window,
            image=self.button_ld_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_order,
            relief="flat"
        )
        self.bt_ld_4.place(
            x=53.0,
            y=450.0,
            width=232.0,
            height=63.0
        )

        self.button_ld_5 = PhotoImage(file=relative_to_assets("button_exit.png"))
        self.bt_ld_5 = Button(
            self.laundry_window,
            image=self.button_ld_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.exit,
            relief="flat"
        )
        self.bt_ld_5.place(
            x=53.0,
            y=720.0,
            width=232.0,
            height=63.0
        )

        self.image_ld_4 = PhotoImage(file=relative_to_assets("image_laundry.png"))
        self.ld_4 = self.canvas6.create_image(
            910.0,
            332.0,
            image=self.image_ld_4
        )

        self.button_ld_6 = PhotoImage(file=relative_to_assets("button_clothes.png"))
        self.bt_ld_6 = Button(
            self.laundry_window,
            image=self.button_ld_6,
            borderwidth=0,
            highlightthickness=0,
            command=self.clothes,
            relief="flat"
        )
        self.bt_ld_6.place(
            x=405.0,
            y=474.0,
            width=459.0,
            height=318.0
        )

        self.button_ld_7 = PhotoImage(file=relative_to_assets("button_shoes.png"))
        self.bt_ld_7 = Button(
            self.laundry_window,
            image=self.button_ld_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: add_to_cart('Shoes Cleaning', 1, self.price_dict),
            relief="flat"
        )
        self.bt_ld_7.place(
            x=913.0,
            y=474.0,
            width=459.0,
            height=318.0
        )

        self.image_ld_5 = PhotoImage(file=relative_to_assets("image_laundrytext.png"))
        self.ld_5 = self.canvas6.create_image(
            536.0,
            57.0,
            image=self.image_ld_5
        )

    def open_laundry(self):
        if hasattr(self, "home_window"):
            self.hide_home()
        elif hasattr(self, "cart_window"):
            self.hide_cart()
        elif hasattr(self, "profile_window"):
            self.hide_profile()
        elif hasattr(self, "order_window"):
            self.hide_order()

        self.show_laundry()

    def show_laundry(self):
        if hasattr(self, 'laundry_window') and self.laundry_window is not None:
            self.laundry_window.destroy()

        self.laundry()
        self.hide_profile()
        self.hide_home()
        self.hide_cart()
        self.hide_order()

    def hide_laundry(self):
        if hasattr(self, 'laundry_window') and self.laundry_window.winfo_exists():
            self.laundry_window.withdraw()
        elif hasattr(self, 'clothes_window') and self.clothes_window:
            self.clothes_window.withdraw()

    def clothes(self):  # Clothes Page
        if hasattr(self, 'laundry_window'):
            self.laundry_window.destroy()

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        cart = []

        def write_to_cart(data):
            csv_columns = ['categories', 'qty', 'total_price']

            # Jika file belum ada, tulis header kolom
            if not Path('cart_content.csv').is_file():
                with open('cart_content.csv', mode='w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                    writer.writeheader()

            # Tambahkan data baru ke file CSV
            with open('cart_content.csv', mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writerow(data)

        def add_to_cart(categories, qty, price_dict):
            data = {'categories': categories, 'qty': qty}

            # Mendapatkan harga dari dictionary price_dict
            price = price_dict.get(categories, 0)  # Mengambil harga dari dictionary, default 0 jika tidak ada

            # Mengalikan harga dengan kuantitas
            total_price = price * qty

            # Menambahkan informasi harga ke data
            data['total_price'] = total_price  # Menambahkan total harga ke data

            # Tulis ke file CSV
            write_to_cart(data)

            messagebox.showinfo("Info", f"{categories} has been added to cart!")

        self.clothes_window = tk.Toplevel(self.master)
        self.clothes_window.title("Dust Busters")
        self.clothes_window.geometry("1430x835")

        self.canvas7 = Canvas(
            self.clothes_window,
            bg="#FFFFFF",
            height=835,
            width=1430,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas7.place(x=0, y=0)

        self.canvas7.create_rectangle(
            0.0,
            0.0,
            337.0,
            835.0,
            fill="#B2CBDE",
            outline=""
        )

        self.image_c_1 = PhotoImage(file=relative_to_assets("image_logo.png"))
        self.c_1 = self.canvas7.create_image(
            79.0,
            84.0,
            image=self.image_c_1
        )

        self.image_c_2 = PhotoImage(file=relative_to_assets("image_dbtext.png"))
        self.c_2 = self.canvas7.create_image(
            218.0,
            94.0,
            image=self.image_c_2
        )

        self.canvas7.create_rectangle(
            336.0,
            122.0,
            1429.9998779296875,
            123.03044700622559,
            fill="#000000",
            outline=""
        )

        self.image_c_3 = PhotoImage(file=relative_to_assets("image_logo2.png"))
        self.c_3 = self.canvas7.create_image(
            1361.0,
            55.0,
            image=self.image_c_3
        )

        self.button_c_1 = PhotoImage(file=relative_to_assets("button_dashboard.png"))
        self.bt_c_1 = Button(
            self.clothes_window,
            image=self.button_c_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_home,
            relief="flat"
        )
        self.bt_c_1.place(
            x=53.0,
            y=180.0,
            width=232.0,
            height=63.0
        )

        self.button_c_2 = PhotoImage(file=relative_to_assets("button_profile.png"))
        self.c_2 = Button(
            self.clothes_window,
            image=self.button_c_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_profile,
            relief="flat"
        )
        self.c_2.place(
            x=53.0,
            y=270.0,
            width=232.0,
            height=63.0
        )

        self.button_c_3 = PhotoImage(file=relative_to_assets("button_cart.png"))
        self.bt_c_3 = Button(
            self.clothes_window,
            image=self.button_c_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_cart,
            relief="flat"
        )
        self.bt_c_3.place(
            x=53.0,
            y=360.0,
            width=232.0,
            height=63.0
        )

        self.button_c_4 = PhotoImage(file=relative_to_assets("button_orders.png"))
        self.bt_c_4 = Button(
            self.clothes_window,
            image=self.button_c_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_order,
            relief="flat"
        )
        self.bt_c_4.place(
            x=53.0,
            y=450.0,
            width=232.0,
            height=63.0
        )

        self.button_c_5 = PhotoImage(file=relative_to_assets("button_exit.png"))
        self.bt_c_5 = Button(
            self.clothes_window,
            image=self.button_c_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.exit,
            relief="flat"
        )
        self.bt_c_5.place(
            x=53.0,
            y=720.0,
            width=232.0,
            height=63.0
        )

        self.image_c_4 = PhotoImage(file=relative_to_assets("image_clothesmenu.png"))
        self.c_4 = self.canvas7.create_image(
            894.0,
            772.0,
            image=self.image_c_4
        )

        self.image_c_5 = PhotoImage(file=relative_to_assets("image_clothes.png"))
        self.c_5 = self.canvas7.create_image(
            918.0,
            317.0,
            image=self.image_c_5
        )

        self.button_c_6 = PhotoImage(file=relative_to_assets("button_w&i.png"))
        self.bt_c_6 = Button(
            self.clothes_window,
            image=self.button_c_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: add_to_cart('Wash & Fold', 1, self.price_dict),
            relief="flat"
        )
        self.bt_c_6.place(
            x=375.0,
            y=477.0,
            width=235.0,
            height=240.0
        )

        self.button_c_7 = PhotoImage(file=relative_to_assets("button_w&f.png"))
        self.bt_c_7 = Button(
            self.clothes_window,
            image=self.button_c_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: add_to_cart('Wash & Iron', 1, self.price_dict),
            relief="flat"
        )
        self.bt_c_7.place(
            x=639.0,
            y=477.0,
            width=235.0,
            height=240.0
        )

        self.button_c_8 = PhotoImage(file=relative_to_assets("button_iron.png"))
        self.bt_c_8 = Button(
            self.clothes_window,
            image=self.button_c_8,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: add_to_cart('Ironing', 1, self.price_dict),
            relief="flat"
        )
        self.bt_c_8.place(
            x=903.0,
            y=477.0,
            width=235.0,
            height=240.0
        )

        self.button_c_9 = PhotoImage(file=relative_to_assets("button_dryclean.png"))
        self.bt_c_9 = Button(
            self.clothes_window,
            image=self.button_c_9,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: add_to_cart('Dry Clean', 1, self.price_dict),
            relief="flat"
        )
        self.bt_c_9.place(
            x=1165.0,
            y=479.0,
            width=235.0,
            height=240.0
        )

        self.image_c_6 = PhotoImage(file=relative_to_assets("image_clothestext.png"))
        self.c_6 = self.canvas7.create_image(
            622.0,
            57.0,
            image=self.image_c_6
        )

    def open_clothes(self):
        if hasattr(self, "home_window"):
            self.hide_home()
        elif hasattr(self, "cart_window"):
            self.hide_cart()
        elif hasattr(self, "laundry_window"):
            self.hide_laundry()
        elif hasattr(self, "profile_window"):
            self.hide_profile()
        elif hasattr(self, "order_window"):
            self.hide_order()

        self.show_clothes()

    def show_clothes(self):
        if hasattr(self, 'clothes_window') and self.clothes_window is not None:
            self.clothes_window.destroy()

        self.clothes()
        self.hide_home()
        self.hide_profile()
        self.hide_cart()
        self.hide_laundry()
        self.hide_order()

    def hide_clothes(self):
        if self.clothes_window:
            self.clothes_window.withdraw()

    def cart_content(self):  # Cart Page
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        self.cart_window = tk.Toplevel(self.master)
        self.cart_window.title("Dust Busters")
        self.cart_window.geometry("1430x835")

        self.canvas8 = Canvas(
            self.cart_window,
            bg="#FFFFFF",
            height=835,
            width=1430,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas8.place(x=0, y=0)

        self.canvas8.create_rectangle(
            0.0,
            0.0,
            337.0,
            835.0,
            fill="#B2CBDE",
            outline=""
        )

        self.image_cart_1 = PhotoImage(file=relative_to_assets("image_logo.png"))
        self.cart_1 = self.canvas8.create_image(
            79.0,
            84.0,
            image=self.image_cart_1
        )

        self.image_cart_2 = PhotoImage(file=relative_to_assets("image_dbtext.png"))
        self.cart_2 = self.canvas8.create_image(
            218.0,
            94.0,
            image=self.image_cart_2
        )

        self.canvas8.create_rectangle(
            338.0,
            122.0,
            1431.9998779296875,
            123.03044703016093,
            fill="#000000",
            outline=""
        )

        self.button_cart_1 = PhotoImage(file=relative_to_assets("button_dashboard.png"))
        self.bt_cart_1 = Button(
            self.cart_window,
            image=self.button_cart_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_home,
            relief="flat"
        )
        self.bt_cart_1.place(
            x=53.0,
            y=180.0,
            width=232.0,
            height=63.0
        )

        self.button_cart_2 = PhotoImage(file=relative_to_assets("button_profile.png"))
        self.bt_cart_2 = Button(
            self.cart_window,
            image=self.button_cart_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_profile,
            relief="flat"
        )
        self.bt_cart_2.place(
            x=53.0,
            y=270.0,
            width=232.0,
            height=63.0
        )

        self.button_cart_3 = PhotoImage(file=relative_to_assets("button_cart.png"))
        self.bt_cart_3 = Button(
            self.cart_window,
            image=self.button_cart_3,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.bt_cart_3.place(
            x=53.0,
            y=360.0,
            width=232.0,
            height=63.0
        )

        self.button_cart_4 = PhotoImage(file=relative_to_assets("button_orders.png"))
        self.bt_cart_4 = Button(
            self.cart_window,
            image=self.button_cart_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_order,
            relief="flat"
        )
        self.bt_cart_4.place(
            x=53.0,
            y=450.0,
            width=232.0,
            height=63.0
        )

        self.button_cart_5 = PhotoImage(file=relative_to_assets("button_exit.png"))
        self.bt_cart_5 = Button(
            self.cart_window,
            image=self.button_cart_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.exit,
            relief="flat"
        )
        self.bt_cart_5.place(
            x=53.0,
            y=720.0,
            width=232.0,
            height=63.0
        )

        self.image_cart_3 = PhotoImage(file=relative_to_assets("image_carttext.png"))
        self.cart_3 = self.canvas8.create_image(
            492.0,
            57.0,
            image=self.image_cart_3
        )

        self.image_cart_4 = PhotoImage(file=relative_to_assets("image_logo2.png"))
        self.cart_4 = self.canvas8.create_image(
            1361.0,
            55.0,
            image=self.image_cart_4
        )

        self.button_cart_6 = PhotoImage(file=relative_to_assets("button_checkout.png"))
        self.bt_cart_6 = Button(
            self.cart_window,
            image=self.button_cart_6,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_confirm,
            relief="flat"
        )
        self.bt_cart_6.place(
            x=426.0,
            y=761.0,
            width=920.0,
            height=48.0
        )

        self.item_listbox = Listbox(self.cart_window, height=37, width=102, font=('Arial', 2))
        self.item_listbox.place(x=426, y=170)

        with open('cart_content.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # Check if the row is not empty
                    item_name = row[0]
                    quantity = int(row[1])
                    self.item_data[item_name] = quantity

        self.refresh_listbox()

    def check_cart_and_checkout(self):
        if not self.item_data:
            messagebox.showinfo("Empty Cart", "You haven't selected a service yet. Please return to the dashboard.")
        else:
            self.open_confirm()

    def refresh_listbox(self):
        for widget in self.item_listbox.winfo_children():
            widget.destroy()

        for item, count in self.item_data.items():
            if count > 0:
                cart_list_item = f"{item}: {count}"
                frame = Frame(self.item_listbox, bd=2)
                frame.pack(fill='x')

                label = Label(frame, text=cart_list_item, width=68, font=('Arial', 20))
                label.pack(side='left')

                button_add = Button(frame, text="+", command=lambda item=item: self.add_product(item))
                button_add.pack(side='left')

                button_remove = Button(frame, text="-", command=lambda item=item: self.remove_product(item))
                button_remove.pack(side='left')

    def refresh_order_listbox(self):
        self.order_listbox.delete(0, 'end')

        for item_name, quantity in self.item_data.items():
            if quantity > 0:
                display_text = f"{item_name}: {quantity}"
                self.order_listbox.insert("end", display_text)

    def add_product(self, item):
        if item in self.item_data:
            self.item_data[item] += 1  # Increase the quantity by 1
        else:
            self.item_data[item] = 1  # If the item is not in the dictionary, set quantity to 1

        self.update_csv()
        self.refresh_listbox()
        self.refresh_order_listbox()

    def remove_product(self, item):
        if item in self.item_data and self.item_data[item] > 0:
            self.item_data[item] -= 1  # Decrease the quantity by 1

            if self.item_data[item] == 0:
                del self.item_data[item]  # If quantity becomes 0, remove the item from the dictionary

        self.update_csv()
        self.refresh_listbox()
        self.refresh_order_listbox()

    def update_csv(self):
        with open('cart_content.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for item, count in self.item_data.items():
                writer.writerow([item, count])

    def open_cart(self):
        if hasattr(self, "home_window"):
            self.hide_home()
        elif hasattr(self, "laundry_window"):
            self.hide_laundry()
        elif hasattr(self, "homecare_window"):
            self.hide_homecare()
        elif hasattr(self, "profile_window"):
            self.hide_profile()
        elif hasattr(self, "order_window"):
            self.hide_order()
        elif hasattr(self, "confirm_window"):
            self.hide_confirm()

        self.show_cart()

    def show_cart(self):
        if hasattr(self, 'cart_window') and self.cart_window is not None:
            self.cart_window.destroy()

        self.hide_home()
        self.hide_profile()
        # self.hide_laundry()
        self.hide_homecare()
        self.hide_clothes()
        self.hide_order()
        self.hide_confirm()
        self.cart_content()

    def hide_cart(self):
        if self.cart_window and self.cart_window.winfo_exists():
            self.cart_window.withdraw()

    def load_prices_from_csv(self):
        with open('pricelistdb.csv', newline='') as file:
            reader = csv.DictReader(file)
            self.price_dict = {row['item_name']: int(row['price']) for row in reader}

    def calculate_total_price(self):
        total_price = 0
        self.load_prices_from_csv()

        for item_name, quantity in self.item_data.items():
            if item_name in self.price_dict:
                item_price = self.price_dict[item_name]
                total_price += item_price * quantity

        return total_price

    def order_confirmation(self, master, item_data):  # Order Confirmation Page
        self.master = master
        self.item_data = item_data

        if hasattr(self, 'cart_window'):
            self.cart_window.destroy()

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        self.confirm_window = tk.Toplevel(self.master)
        self.confirm_window.title("Dust Busters")
        self.confirm_window.geometry("1430x835")

        self.canvas9 = Canvas(
            self.confirm_window,
            bg="#FFFFFF",
            height=835,
            width=1430,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas9.place(x=0, y=0)

        self.canvas9.create_rectangle(
            0.0,
            0.0,
            337.0,
            835.0,
            fill="#B2CBDE",
            outline=""
        )

        self.image_cf_1 = PhotoImage(file=relative_to_assets("image_logo.png"))
        self.cf_1 = self.canvas9.create_image(
            79.0,
            84.0,
            image=self.image_cf_1
        )

        self.image_cf_2 = PhotoImage(file=relative_to_assets("image_dbtext.png"))
        self.cf_2 = self.canvas9.create_image(
            218.0,
            94.0,
            image=self.image_cf_2
        )

        self.canvas9.create_rectangle(
            338.0,
            122.0,
            1431.9998779296875,
            123.03044703016093,
            fill="#000000",
            outline=""
        )

        self.button_cf_1 = PhotoImage(file=relative_to_assets("button_dashboard.png"))
        self.bt_cf_1 = Button(
            self.confirm_window,
            image=self.button_cf_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_home,
            relief="flat"
        )
        self.bt_cf_1.place(
            x=53.0,
            y=180.0,
            width=232.0,
            height=63.0
        )

        self.button_cf_2 = PhotoImage(file=relative_to_assets("button_profile.png"))
        self.bt_cf_2 = Button(
            self.confirm_window,
            image=self.button_cf_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_profile,
            relief="flat"
        )
        self.bt_cf_2.place(
            x=53.0,
            y=270.0,
            width=232.0,
            height=63.0
        )

        self.button_cf_3 = PhotoImage(file=relative_to_assets("button_cart.png"))
        self.bt_cf_3 = Button(
            self.confirm_window,
            image=self.button_cf_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_cart,
            relief="flat"
        )
        self.bt_cf_3.place(
            x=53.0,
            y=360.0,
            width=232.0,
            height=63.0
        )

        self.button_cf_4 = PhotoImage(file=relative_to_assets("button_orders.png"))
        self.bt_cf_4 = Button(
            self.confirm_window,
            image=self.button_cf_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_order,
            relief="flat"
        )
        self.bt_cf_4.place(
            x=53.0,
            y=450.0,
            width=232.0,
            height=63.0
        )

        self.button_cf_5 = PhotoImage(file=relative_to_assets("button_exit.png"))
        self.bt_cf_5 = Button(
            self.confirm_window,
            image=self.button_cf_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.exit,
            relief="flat"
        )
        self.bt_cf_5.place(
            x=53.0,
            y=720.0,
            width=232.0,
            height=63.0
        )

        self.button_cf_6 = PhotoImage(file=relative_to_assets("button_placeorder.png"))
        self.bt_cf_6 = Button(
            self.confirm_window,
            image=self.button_cf_6,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_summary,
            relief="flat"
        )
        self.bt_cf_6.place(
            x=426.0,
            y=761.0,
            width=920.0,
            height=48.0
        )
        self.bt_cf_6.config(state="disabled")

        self.image_cf_3 = PhotoImage(
            file=relative_to_assets("image_cftext.png"))
        self.cf_3 = self.canvas9.create_image(
            603.0,
            57.0,
            image=self.image_cf_3
        )

        self.image_cf_4 = PhotoImage(
            file=relative_to_assets("image_logo2.png"))
        self.cf_4 = self.canvas9.create_image(
            1361.0,
            55.0,
            image=self.image_cf_4
        )

        self.canvas9.create_text(
            426.0,
            135.0,
            anchor="nw",
            text="Service Chosen List",
            fill="#000000",
            font=("Fraunces Regular", 24 * -1)
        )

        self.canvas9.create_text(
            426.0,
            455.0,
            anchor="nw",
            text="Payment Methods",
            fill="#000000",
            font=("Fraunces Regular", 24 * -1)
        )

        self.canvas9.create_text(
            426.0,
            535.0,
            anchor="nw",
            text="Delivery Methods",
            fill="#000000",
            font=("Fraunces Regular", 24 * -1)
        )

        self.canvas9.create_text(
            426.0,
            615.0,
            anchor="nw",
            text="Total Price",
            fill="#000000",
            font=("Fraunces Regular", 24 * -1)
        )

        self.label_total_price = Label(
            self.confirm_window,
            text=f"Rp {self.calculate_total_price()}",  # Initial value, will be updated
            font=("Fraunces Regular", 20),
            fg="#000000",
            width=70,
            height=3
        )
        self.label_total_price.place(x=426, y=655)

        self.payment_options = ["Choose Payment Method", "Credit/Debit Card", "Bank Transfer", "QRIS"]
        self.delivery_options = ["Choose Delivery Method", "Delivery", "Pickup"]

        self.payment_var = StringVar(self.confirm_window)
        self.payment_var.set(self.payment_options[0])

        self.delivery_var = StringVar(self.confirm_window)
        self.delivery_var.set(self.delivery_options[0])

        payment_menu = OptionMenu(self.confirm_window, self.payment_var, *self.payment_options)
        payment_menu.config(font=("Fraunces Regular", 16), width=20)
        payment_menu.place(x=426, y=495)
        payment_menu.bind("<ButtonRelease-1>", lambda event: self.check_order_validity())

        delivery_menu = OptionMenu(self.confirm_window, self.delivery_var, *self.delivery_options)
        delivery_menu.config(font=("Fraunces Regular", 16), width=20)
        delivery_menu.place(x=426, y=575)
        delivery_menu.bind("<ButtonRelease-1>", lambda event: self.check_order_validity())

        self.create_order_listbox()
        self.populate_order_listbox()

    def create_order_listbox(self):
        self.order_listbox = Listbox(self.confirm_window, height=37, width=102, font=('Arial', 2))
        self.order_listbox.place(x=426, y=170)

    def populate_order_listbox(self):
        for item_name, quantity in self.item_data.items():
            frame = Frame(self.order_listbox, bd=2)
            frame.pack(fill="x")

            display_text = f"{item_name}: {quantity}"
            label = Label(frame, text=display_text, width=76, font=('Arial', 20))
            label.pack(side="left")

    def check_order_validity(self):
        selected_payment = self.payment_var.get()
        selected_delivery = self.delivery_var.get()

        if selected_payment != "Choose Payment Method" and selected_delivery != "Choose Delivery Method":
            self.bt_cf_6.config(state="normal")
        else:
            self.bt_cf_6.config(state="disabled")

    def open_confirm(self):
        if hasattr(self, "home_window"):
            self.hide_home()
        elif hasattr(self, "cart_window"):
            self.hide_cart()
        elif hasattr(self, "profile_window"):
            self.hide_profile()
        elif hasattr(self, "order_window"):
            self.hide_order()

        self.show_confirm()

    def show_confirm(self):
        if hasattr(self, 'confirm_window') and self.confirm_window is not None:
            self.confirm_window.destroy()

        self.order_confirmation(self.master, self.item_data)
        self.hide_clothes()
        self.hide_profile()
        self.hide_home()
        self.hide_cart()
        # self.hide_laundry()
        self.hide_order()

    def hide_confirm(self):
        if self.confirm_window:
            self.confirm_window.withdraw()

    def order_content(self):  # Order Page
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        self.order_window = tk.Toplevel(self.master)
        self.order_window.title("Dust Busters")
        self.order_window.geometry("1430x835")

        self.canvas10 = Canvas(
            self.order_window,
            bg="#FFFFFF",
            height=835,
            width=1430,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas10.place(x=0, y=0)

        self.canvas10.create_rectangle(
            0.0,
            0.0,
            337.0,
            835.0,
            fill="#B2CBDE",
            outline=""
        )

        self.image_order_1 = PhotoImage(file=relative_to_assets("image_logo.png"))
        self.order_1 = self.canvas10.create_image(
            79.0,
            84.0,
            image=self.image_order_1
        )

        self.image_order_2 = PhotoImage(file=relative_to_assets("image_dbtext.png"))
        self.order_2 = self.canvas10.create_image(
            218.0,
            94.0,
            image=self.image_order_2
        )

        self.canvas10.create_rectangle(
            338.0,
            122.0,
            1431.9998779296875,
            123.03044703016093,
            fill="#000000",
            outline=""
        )

        self.button_order_1 = PhotoImage(file=relative_to_assets("button_dashboard.png"))
        self.bt_order_1 = Button(
            self.order_window,
            image=self.button_order_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_home,
            relief="flat"
        )
        self.bt_order_1.place(
            x=53.0,
            y=180.0,
            width=232.0,
            height=63.0
        )

        self.button_order_2 = PhotoImage(file=relative_to_assets("button_profile.png"))
        self.bt_order_2 = Button(
            self.order_window,
            image=self.button_order_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_profile,
            relief="flat"
        )
        self.bt_order_2.place(
            x=53.0,
            y=270.0,
            width=232.0,
            height=63.0
        )

        self.button_order_3 = PhotoImage(file=relative_to_assets("button_cart.png"))
        self.bt_order_3 = Button(
            self.order_window,
            image=self.button_order_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_cart,
            relief="flat"
        )
        self.bt_order_3.place(
            x=53.0,
            y=360.0,
            width=232.0,
            height=63.0
        )

        self.button_order_4 = PhotoImage(file=relative_to_assets("button_orders.png"))
        self.bt_order_4 = Button(
            self.order_window,
            image=self.button_order_4,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.bt_order_4.place(
            x=53.0,
            y=450.0,
            width=232.0,
            height=63.0
        )

        self.button_order_5 = PhotoImage(file=relative_to_assets("button_exit.png"))
        self.bt_order_5 = Button(
            self.order_window,
            image=self.button_order_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.exit,
            relief="flat"
        )
        self.bt_order_5.place(
            x=53.0,
            y=720.0,
            width=232.0,
            height=63.0
        )

        self.button_show_receipt = Button(
            self.order_window,
            text="Show Order Receipt",
            command=self.open_summary,
            width=103,
            height=40
        )
        self.button_show_receipt.place(x=400, y=135)


    def open_order(self):
        if hasattr(self, "home_window"):
            self.hide_home()
        elif hasattr(self, "laundry_window"):
            self.hide_laundry()
        elif hasattr(self, "homecare_window"):
            self.hide_homecare()
        elif hasattr(self, "profile_window"):
            self.hide_profile()
        elif hasattr(self, "cart_window"):
            self.hide_cart()
        elif hasattr(self, "confirm_window"):
            self.hide_confirm()
        elif hasattr(self, "clothes_window"):
            self.hide_clothes()

        self.show_order()

    def show_order(self):
        if hasattr(self, 'order_window') and self.order_window is not None:
            self.order_window.destroy()

        self.order_content()
        self.hide_home()
        self.hide_profile()
        self.hide_cart()
        self.hide_confirm()
        self.hide_homecare()
        self.hide_laundry()
        self.hide_clothes()
        self.hide_summary()

    def hide_order(self):
        if self.order_window:
            self.order_window.withdraw()

    def order_summary(self):
        if hasattr(self, 'cart_window'):
            self.cart_window.destroy()

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        self.summary_window = tk.Toplevel(self.master)
        self.summary_window.title("Dust Busters")
        self.summary_window.geometry("1430x835")

        self.canvas11 = Canvas(
            self.summary_window,
            bg="#FFFFFF",
            height=835,
            width=1430,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas11.place(x=0, y=0)

        self.canvas11.create_rectangle(
            0.0,
            0.0,
            337.0,
            835.0,
            fill="#B2CBDE",
            outline=""
        )

        self.image_sum_1 = PhotoImage(file=relative_to_assets("image_logo.png"))
        self.sum_1 = self.canvas11.create_image(
            79.0,
            84.0,
            image=self.image_sum_1
        )

        self.image_sum_2 = PhotoImage(file=relative_to_assets("image_dbtext.png"))
        self.sum_2 = self.canvas11.create_image(
            218.0,
            94.0,
            image=self.image_sum_2
        )

        self.canvas11.create_rectangle(
            338.0,
            122.0,
            1431.9998779296875,
            123.03044703016093,
            fill="#000000",
            outline=""
        )

        self.button_sum_1 = PhotoImage(file=relative_to_assets("button_dashboard.png"))
        self.bt_sum_1 = Button(
            self.summary_window,
            image=self.button_sum_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_home,
            relief="flat"
        )
        self.bt_sum_1.place(
            x=53.0,
            y=180.0,
            width=232.0,
            height=63.0
        )

        self.button_sum_2 = PhotoImage(file=relative_to_assets("button_profile.png"))
        self.bt_sum_2 = Button(
            self.summary_window,
            image=self.button_sum_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_profile,
            relief="flat"
        )
        self.bt_sum_2.place(
            x=53.0,
            y=270.0,
            width=232.0,
            height=63.0
        )

        self.button_sum_3 = PhotoImage(file=relative_to_assets("button_cart.png"))
        self.bt_sum_3 = Button(
            self.summary_window,
            image=self.button_sum_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_cart,
            relief="flat"
        )
        self.bt_sum_3.place(
            x=53.0,
            y=360.0,
            width=232.0,
            height=63.0
        )

        self.button_sum_4 = PhotoImage(file=relative_to_assets("button_orders.png"))
        self.bt_sum_4 = Button(
            self.summary_window,
            image=self.button_sum_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_order, 
            relief="flat"
        )
        self.bt_sum_4.place(
            x=53.0,
            y=450.0,
            width=232.0,
            height=63.0
        )

        self.button_sum_5 = PhotoImage(file=relative_to_assets("button_exit.png"))
        self.bt_sum_5 = Button(
            self.summary_window,
            image=self.button_sum_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.exit,
            relief="flat"
        )
        self.bt_sum_5.place(
            x=53.0,
            y=720.0,
            width=232.0,
            height=63.0
        )

        self.image_sum_3 = PhotoImage(
            file=relative_to_assets("image_3.png"))
        self.sum_3 = self.canvas11.create_image(
            884.0,
            89.0,
            image=self.image_sum_3
        )

        self.image_sum_4 = PhotoImage(
            file=relative_to_assets("image_4.png"))
        self.sum_4 = self.canvas11.create_image(
            397.0,
            200.0,
            image=self.image_sum_4
        )

        self.image_sum_5 = PhotoImage(
            file=relative_to_assets("image_5.png"))
        self.sum_5 = self.canvas11.create_image(
            549.0,
            274.0,
            image=self.image_sum_5
        )

        self.image_sum_6 = PhotoImage(
            file=relative_to_assets("image_6.png"))
        self.sum_6 = self.canvas11.create_image(
            1072.0,
            305.0,
            image=self.image_sum_6
        )

        self.image_sum_7 = PhotoImage(
            file=relative_to_assets("image_7.png"))
        self.sum_7 = self.canvas11.create_image(
            1120.0,
            789.0,
            image=self.image_sum_7
        )

        self.image_sum_8 = PhotoImage(
            file=relative_to_assets("image_8.png"))
        self.sum_8 = self.canvas11.create_image(
            502.0,
            412.0,
            image=self.image_sum_8
        )

        self.usn_label = Label(self.summary_window, text=session[0], font=("Fraunces Regular", 25), bg='white')
        self.usn_label.place(x=427, y=179)
        
        selected_payment = self.payment_var.get()
        selected_delivery = self.delivery_var.get()

        # Menampilkan metode pembayaran yang dipilih
        payment_label = Label(self.summary_window, text=f"{selected_payment}", font=("Fraunces Regular", 25), bg='white')
        payment_label.place(x=960, y=320)  # Sesuaikan posisi label sesuai kebutuhan

        # Menampilkan metode pengiriman yang dipilih
        delivery_label = Label(self.summary_window, text=f"{selected_delivery}", font=("Fraunces Regular", 25), bg='white')
        delivery_label.place(x=395, y=320)

        with open('cart_content.csv', mode='r') as file:
            reader = csv.reader(file)
            cart_content = [row for row in reader]

        # Menampilkan isi file CSV pada Listbox
        self.sum_listbox = Listbox(self.summary_window, height=13, width=80, font=('Arial', 20))
        self.sum_listbox.place(x=390, y=435)

        for item in cart_content:
            # Menggabungkan setiap item dalam satu string
            display_text = ', '.join(item)  # Sesuaikan dengan cara penampilan yang diinginkan
            self.sum_listbox.insert(END, display_text)

        self.total_label = Label(self.summary_window, text=f"{self.calculate_total_price()}", font=("Fraunces Regular", 25), bg='white')
        self.total_label.place(x=1170, y=770)

    def open_summary(self):
        if hasattr(self, "home_window"):
            self.hide_home()
        elif hasattr(self, "laundry_window"):
            self.hide_laundry()
        elif hasattr(self, "homecare_window"):
            self.hide_homecare()
        elif hasattr(self, "profile_window"):
            self.hide_profile()
        elif hasattr(self, "cart_window"):
            self.hide_cart()
        elif hasattr(self, "confirm_window"):
            self.hide_confirm()
        elif hasattr(self, "clothes_window"):
            self.hide_clothes()
        elif hasattr(self, "order_window"):
            self.hide_order()

        self.show_summary()

    def show_summary(self):
        if hasattr(self, 'summary_window') and self.summary_window is not None:
            self.summary_window.destroy()

        self.order_summary()
        self.hide_home()
        self.hide_profile()
        self.hide_cart()
        self.hide_confirm()
        self.hide_homecare()
        self.hide_laundry()
        self.hide_clothes()
        self.hide_confirm()
        self.hide_order()

    def hide_summary(self):
        if self.summary_window:
            self.summary_window.withdraw()

    def logout(self):
        self.hide_profile()
        self.open_login()

    def start(self):
        self.master.withdraw()
        self.master.mainloop()

    def exit(self):
        self.master.destroy()


def main():
    root = tk.Tk()
    app = DustBusters(root)
    app.show_splash_and_start()
    app.start()


main() 