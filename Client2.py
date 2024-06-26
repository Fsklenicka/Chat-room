import functools
import random
import socket
import threading

import customtkinter
import pywinstyles
import requests
from customtkinter import *
from plyer import notification as n

import AuthGate
import EmailHandler
import verification

baseurl = 'http://89.203.249.186:5000'
notifs = False
app = CTk()
set_appearance_mode('dark')
app.geometry('720x600')
app.title('Chat Room')


def setuser(username):
    global NameSender
    NameSender = username


def receive_messages(client_socket, chat):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                if notifs and not app.focus_get():
                    n.notify(title='ChatRoom', message=message, ticker='r')
                    pass
                else:
                    pass
                chat.configure(state='normal')
                chat.insert("end", message + '\n')
                chat.yview("end")
                chat.configure(state='disabled')
            else:
                break
        except:
            print("An error occurred! recv")
            client_socket.close()
            break


def ThemeToggle():
    mode = customtkinter.get_appearance_mode()
    if mode == "Light":
        customtkinter.set_appearance_mode('Dark')
    else:
        customtkinter.set_appearance_mode('Light')


def sendMsg(client_socket, message_entry, chat):
    msg = f'{NameSender}: {message_entry}'
    if msg:
        try:
            chat.configure(state='normal')
            chat.insert("end", f'{msg} \n')
            chat.yview("end")
            chat.configure(state='disabled')

            client_socket.send(msg.encode('utf-8'))
        except:
            client_socket.close()


def forgotpassfun(userID):
    response = requests.get(f'{baseurl}/emails/get/{userID}')

    if response.status_code == 200:
        useremail = response.text
        vercode = verification.verify(useremail)

        dialog = CTkInputDialog(text="Enter verification code", title='Verification')
        user_vercode = dialog.get_input()

        if user_vercode is not None and user_vercode == str(vercode):
            dialog2 = CTkInputDialog(text="Enter new password", title='Password reset')
            newpass = dialog2.get_input()
            if newpass:
                # Call the API to change the password
                change_pass_response = requests.get(f'{baseurl}/changepassword/{userID}/{newpass}')

                if change_pass_response.status_code == 200:
                    print("Password changed successfully.")
                else:
                    print("Failed to change password.")
            else:
                print("Password reset was cancelled.")
        else:
            errlbl = CTkLabel(master=window, text='Invalid verification code', text_color='red')
            errlbl.pack(padx=5, pady=5)
    else:
        print("Error: Failed to retrieve user email.")

def forgoted_pass():
    forgotwin = CTkToplevel(window)
    forgotwin.title('Forgotten Password')

    forgotuser = CTkEntry(forgotwin, placeholder_text='Enter Your Username')
    forgotuser.pack(padx=5, pady=5)

    submitbtn = CTkButton(forgotwin, text='Submit', command=lambda: [forgotpassfun(forgotuser.get())])
    submitbtn.pack(padx=5, pady=5)

    pass

def enter_l(username, password):
    authstat = requests.get(f'{baseurl}/get-user/{username}/{password}')
    if authstat.status_code == 200:
        setuser(username)
        window.withdraw()
        app.deiconify()
        showuserlist(userlistbox)
    else:
        label = CTkLabel(window, text="login unsuccessful", text_color='red')
        label.pack(pady=5, padx=5)
        button1 = CTkButton(window, text="Forgoted Password", corner_radius=10, command=forgoted_pass)
        button1.pack(pady=5, padx=5)
        window.after(1000, functools.partial(button1.destroy))
        window.after(1000, functools.partial(label.destroy))


def registeruser(username, password, email):
    regstat = requests.get(f'{baseurl}/chkusr/{username}')
    print(regstat)

    if regstat.status_code == 200:
        label2 = CTkLabel(master=window, text='registration success. enter ver code', text_color='green')
        label2.pack(pady=5, padx=5)
        ver_code = random.randint(10000, 999999)
        dialog = CTkInputDialog(text="Enter ver code from your email.")
        EmailHandler.SendEmail(email, "Ověřovací kód pro ChatRoom", f"Váš jednorázový kód: {ver_code} | Na tento email neodpovídejte !")
        if int(dialog.get_input()) == ver_code:
            window.after(1000, functools.partial(label2.destroy))
            registr = requests.get(f'{baseurl}/reg-user/{username}/{password}')
            emailreg = requests.get(f'{baseurl}/emails/save/{username}/{email}')
            pass
        else:
            label3 = CTkLabel(master=window, text='registration :(. Try again', text_color='red')
            label3.pack(pady=5, padx=5)
    else:
        label1 = CTkLabel(master=window, text='Username already exists', text_color='red')
        label1.pack(pady=5, padx=5)
        window.after(1000, functools.partial(label1.destroy))


def toplogin():
    global window
    window = CTk()
    pywinstyles.apply_style(window, "normal")
    window.attributes('-topmost', True)  # Ensure the window is always on top
    set_appearance_mode('dark')
    CTkFont('Roboto')
    app.geometry('720x600')
    window.title('login')

    tabs1 = CTkTabview(window)
    tablogin = tabs1.add("Login")
    tabreg = tabs1.add("Register")

    tabs1.pack(pady=5)

    global entry_login_username
    global entry_login_password
    entry_login_username = CTkEntry(master=tablogin, placeholder_text="Enter username", corner_radius=10)
    entry_login_username.pack(padx=5, pady=5)

    entry_login_password = CTkEntry(master=tablogin, placeholder_text="Enter password", corner_radius=10, show='*')
    entry_login_password.pack(padx=5, pady=5)

    entry_login_email = CTkEntry(master=tabreg, placeholder_text="Enter Email", corner_radius=10)
    entry_login_email.pack(padx=5, pady=5)

    button_login = CTkButton(master=tablogin, text="Enter", corner_radius=10,
                             command=lambda: [enter_l(entry_login_username.get(), entry_login_password.get())])
    button_login.pack(padx=5, pady=5)

    entryuser = CTkEntry(master=tabreg, placeholder_text='Enter username', corner_radius=10)
    entryclass = CTkEntry(master=tabreg, placeholder_text='Enter your class', corner_radius=10)
    entrypass = CTkEntry(master=tabreg, corner_radius=10, placeholder_text='Enter password', show='*')
    entryuser.pack(pady=5, padx=5)
    entryclass.pack(padx=5, pady=5)
    entrypass.pack(pady=5, padx=5)

    regbtn = CTkButton(master=tabreg, text='register', corner_radius=10,
                       command=lambda: [registeruser(entryuser.get(), entrypass.get(), entry_login_email.get())])
    regbtn.pack(pady=5, padx=5)


def changestyle(value):
    pywinstyles.apply_style(app, 'normal')
    pywinstyles.apply_style(app, value)

def showuserlist(chat):
    usersreq = requests.get(f'{baseurl}/userlist/get')
    if usersreq.status_code ==200:
        users = usersreq.json()
        chat.configure(state='normal')
        for user in users:
            chat.insert('end', f'{user}\n')

    chat.configure(state='disabled')

def NotifControl():
    global notifs
    if notifs:
        notifs = False
    else:
        notifs = True

def mainapp():
    global app
    app = CTkToplevel(window)
    pywinstyles.apply_style(app, 'mica')
    set_appearance_mode('dark')
    app.geometry('720x600')
    app.title('Chat Room')

    tabs = CTkTabview(master=app, height=585, width=720)
    tabs.pack()

    tab1 = tabs.add('Chat')
    tab2 = tabs.add('Uživatelé')
    tab3 = tabs.add('Nastavení')

    global Textbox
    Textbox = CTkTextbox(master=tab1, corner_radius=18, border_width=2, width=550, height=450, font=('roboto', 20),
                         scrollbar_button_hover_color="blue")
    Textbox.configure(state='disabled')
    Textbox.place(relx=0.5, rely=0.45, anchor="center")

    MsgEntry = CTkEntry(master=tab1, corner_radius=18, border_width=2, border_color='blue', width=480)
    MsgEntry.place(relx=0.45, rely=0.93, anchor='center')

    SendBtn = CTkButton(master=tab1, corner_radius=45, width=20, height=25, text='Send', hover_color='black',
                        font=('Segoe UI Semibold', 14),
                        command=lambda: [sendMsg(client_socket, MsgEntry.get(), Textbox), MsgEntry.delete(0, "end")])
    SendBtn.place(relx=0.84, rely=0.93, anchor='center')

    ThemeLabel = CTkLabel(master=tab3, text='Select Theme', anchor="center").pack(pady=5, padx=5)
    Themepicker = CTkOptionMenu(master=tab3,
                                values=['normal', 'acrylic', 'transparent', 'aero', 'optimised', 'inverse', 'mica'],
                                command=changestyle).pack()

    NotifSwitch = CTkSwitch(master=tab3, text='Notifications', command=NotifControl)
    NotifSwitch.pack(pady=5,padx=5)

    userframe = CTkFrame(tab3)
    userframe.pack(pady=20, padx=20, fill="both", expand=True)

    global userlistbox
    userlistbox = CTkTextbox(master=tab2, state='disabled', font=('roboto', 20))
    userlistbox.pack(pady=10,padx=10,fill='both', expand=True)
def client_program():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('89.203.249.186', 5555))

    toplogin()
    mainapp()
    app.withdraw()

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, Textbox))
    receive_thread.daemon = True
    receive_thread.start()

    window.mainloop()


if __name__ == "__main__":
    client_program()