from tkinter import *
import re, socket
from threading import Thread
from cryptography.fernet import Fernet

# encrypt
fkey = open("key.txt", "rb")
key = fkey.read()
cipher = Fernet(key)
fkey.close()

# graphic
imgPath = "images/"
backgroundColor = "#040030"
secondColor = "#76E6CB"
screenSize = (800, 600)

servers = {"a": "aaaaaaaa", "b": "baaaaaaa", "c": "caaaaaaa"}

window = Tk()

#connection
ip = "127.0.0.1"
port = 3339
global sock

#images
XBTNImage = PhotoImage(file=f"{imgPath}xButton.png")
homeBTNImage = PhotoImage(file=f"{imgPath}homeButton.png")
registerBTNImage = PhotoImage(file=f"{imgPath}registerButton.png")
loginBTNImage = PhotoImage(file=f"{imgPath}loginButton.png")
smallLoginImage = PhotoImage(file=f"{imgPath}smallLogin.png")
smallRegisterImage = PhotoImage(file=f"{imgPath}smallRegister.png")
dmButtonImage = PhotoImage(file=f"{imgPath}dmButton.png")

global emailEntry, passwordEntry, usernameEntry

def register():
    global emailEntry, passwordEntry, usernameEntry, f
    username = usernameEntry.get()
    email = emailEntry.get()
    password = passwordEntry.get()
    passwordValidate = checkPassword(password)
    print('register')
    if passwordValidate == "valid":
        loadScreen("login")
        userData = f"username: {username} email: {email} password: {password}"
        print(userData)
        handle_sends("register", username, email, password)
    else:
        print(f"password: {password} is not valid because it is {passwordValidate}")

def checkPassword(password):
    if len(password) < 6:
        return "tooShort"
    elif re.search('[0-9]', password) is None:
        return "noDigits"
    elif re.search('[a-z]', password) is None and re.search('[A-Z]', password) is None:
        return "noLetters"
    else:
        return "valid"

def login():
    global emailEntry, passwordEntry, cipher
    email = emailEntry.get()
    password = passwordEntry.get()
    userData = f"email: {email} password: {password}"
    handle_sends("login", email, password)
    print(userData)
    print('login')

def handle_sends(*arguments):
    print("-----------------------------------------------")
    toSend ="|".join(arguments) + "&"
    print(toSend)
    encrypted_message = cipher.encrypt(toSend.encode())
    sock.send(encrypted_message)
    print(f'{encrypted_message =}')
    # waitToConfim()

def waitToConfim():
    enc_message = sock.recv(1024)
    message = cipher.decrypt(enc_message).decode()
    print(f"the message is {message}")

def clearScreen():
    for widget in window.winfo_children():
        widget.destroy()

def show_password():
    global passwordEntry
    if passwordEntry.cget('show') == '*':
        passwordEntry.config(show='')
    else:
        passwordEntry.config(show='*')

def loadServer(server):
    print(server)

def temp(a):
    return a

def home_screen():
    dmY = 250
    serversY = 450
    lefSideX = 50
    i = 0
    dm = Button(window, image=dmButtonImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("dm"))
    dm.place(x=lefSideX, y=dmY)
    serversButtons = []
    for server in servers:
        serversButtons.append(Button(window, text=servers[server], bg=backgroundColor, fg=secondColor, font=("Assistant", 25, "bold"), command=lambda a=server: loadServer(a)))
        serversButtons[i].place(x=lefSideX, y=serversY + 100 * i)
        i += 1
        print(server)

    print(serversButtons)

def login_register_screens(screen):
    global emailEntry, usernameEntry, passwordEntry
    winWidth = window.winfo_width()
    winHeight = window.winfo_height()
    titleWidth = 1000

    titleX = winWidth / 2 - titleWidth / 2
    emailY = 1.7 * winHeight / 4
    passwordY = emailY + 200
    labelX = winWidth / 4

    submitX = winWidth / 3 - 100
    submitY = passwordY + 150

    emailLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", 45, "bold"), text="Email:")
    emailLabel.place(x=labelX, y=emailY - 75)

    emailEntry = Entry(window, bg=secondColor, font=("Assistant", 45, "bold"))
    emailEntry.place(x=labelX, y=emailY, width=int(winWidth / 3))

    passwordLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", 45, "bold"), text="Password:")
    passwordLabel.place(x=labelX, y=passwordY - 75)

    passwordEntry = Entry(window, bg=secondColor, font=("Assistant", 45, "bold"), show="*")
    passwordEntry.place(x=labelX, y=passwordY, width=int(winWidth / 3))

    showPasswordButton = Checkbutton(window, text="show password", bg=backgroundColor, fg=secondColor,
                                     highlightthickness=0, activebackground=backgroundColor, bd=0,
                                     font=("Assistant", 20, "bold"), command=show_password)
    showPasswordButton.place(x=labelX, y=passwordY + 100)

    if screen == "register":
        usernameEntry = Entry(window, bg=secondColor, font=("Assistant", 45, "bold"))
        usernameEntry.place(x=labelX, y=emailY - 200, width=int(winWidth / 3))
        usernameLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", 45, "bold"),
                              text="Username:")
        usernameLabel.place(x=labelX, y=emailY - 200 - 75)
        titleLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", 125, "bold"), text="register")
        submitButton = Button(window, image=registerBTNImage, bd=0, highlightthickness=0,
                              activebackground=backgroundColor, bg=backgroundColor, command=register)
        getOtherLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", 35, "bold"),
                              text="Already have account?")
        getOtherButton = Button(window, image=smallLoginImage, bd=0, highlightthickness=0,
                                activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("login"))

    else:
        titleLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", 125, "bold"), text="login")
        submitButton = Button(window, image=loginBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor,
                              bg=backgroundColor, command=login)
        getOtherLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", 35, "bold"),
                              text="Still don't have account?")
        getOtherButton = Button(window, image=smallRegisterImage, bd=0, highlightthickness=0,
                                activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("register"))

    print(submitX)
    submitButton.place(x=submitX, y=submitY)
    titleLabel.place(x=titleX, y=50, width=titleWidth)
    getOtherLabel.place(x=submitX + int(winWidth / 2.5), y=submitY - 60)
    getOtherButton.place(x=submitX + int(winWidth / 2.5), y=submitY)


def loadScreen(screen):
    global window, emailEntry, passwordEntry, usernameEntry

    clearScreen()

    homeButton = Button(window, image=homeBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("home"))
    homeButton.place(x=0, y=0)

    xButton = Button(window, image=XBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=close)
    xButton.pack(anchor=NE)

    if screen == "register" or screen == "login":
        login_register_screens(screen)
    elif screen == "home":
        home_screen()
    print('here')
    window.update()

def updateSize():
    global screenSize
    close()
    screenSize = (screenSize[0] + 100, screenSize[1] + 100)
    mainG()

def close():
    global window
    # handle_client("close")
    window.destroy()

def mainG():
    global screenSize
    global window, f, sock

    sock = socket.socket()
    sock.connect((ip, port))

    window.resizable(False, False)
    window.attributes('-fullscreen', True)
    # window.geometry("1280x720")
    window.update()
    print(str(window.winfo_width()) + " " + str(window.winfo_height()))

    window['background'] = backgroundColor

    loadScreen("register")

    window.mainloop()

if __name__ == '__main__':
    mainG()

