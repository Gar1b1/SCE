from tkinter import *
import re, socket, platform, time, json
from PIL import Image, ImageTk
from threading import Thread
from cryptography.fernet import Fernet
from plyer import notification

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
global winHeight, winWidth


servers = {"a": "aaaaaaaa", "b": "baaaaaaa", "c": "caaaaaaa"}

window = Tk()

#connection
ip = "127.0.0.1"
port = 3339
global sock

#images
global newImage

#origin images
XOriginImage = Image.open(f"{imgPath}xButton.png")
homeOriginImage = Image.open(f"{imgPath}homeButton.png")
registerOriginImage = Image.open(f"{imgPath}registerButton.png")
loginOriginImage = Image.open(f"{imgPath}loginButton.png")
smallLoginOriginImage = Image.open(f"{imgPath}smallLogin.png")
smallRegisterOriginImage = Image.open(f"{imgPath}smallRegister.png")
dmOriginImage = Image.open(f"{imgPath}dmButton.png")
settingsOriginImage = Image.open(f"{imgPath}settings.png")

#changeable images
XImage = Image.open(f"{imgPath}xButton.png")
homeImage = Image.open(f"{imgPath}homeButton.png")
registerImage = Image.open(f"{imgPath}registerButton.png")
loginImage = Image.open(f"{imgPath}loginButton.png")
smallLoginImage = Image.open(f"{imgPath}smallLogin.png")
smallRegisterImage = Image.open(f"{imgPath}smallRegister.png")
dmImage = Image.open(f"{imgPath}dmButton.png")
settingsImage = Image.open(f"{imgPath}settings.png")

#buttons images
XBTNImage = ImageTk.PhotoImage(XImage)
homeBTNImage = ImageTk.PhotoImage(homeImage)
registerBTNImage = ImageTk.PhotoImage(registerImage)
loginBTNImage = ImageTk.PhotoImage(loginImage)
smallLoginBTNImage = ImageTk.PhotoImage(smallLoginImage)
smallRegisterBTNImage = ImageTk.PhotoImage(smallRegisterImage)
dmBTNImage = ImageTk.PhotoImage(dmImage)
settingsBTNImage = ImageTk.PhotoImage(settingsImage)

global emailEntry, passwordEntry, usernameEntry

def register():
    global emailEntry, passwordEntry, usernameEntry, f
    username = usernameEntry.get()
    email = emailEntry.get()
    password = passwordEntry.get()
    passwordValidate = checkPassword(password)
    # print('register')
    if passwordValidate == "valid":
        loadScreen("login")
        userData = f"username: {username} email: {email} password: {password}"
        # print(userData)
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
    sec = handle_sends("login", email, password).split("|")[1] == "successfully"
    print(f"{sec=}")

    if sec:
        loadScreen("home")
        notify("login successfully", "loged in successfully")
    else:
        notify("login failed","user params are inncorect")
    print(userData)
    print('login')

def notify(title1, message1):
    notification.notify(
        title=title1,
        message=message1,
        timeout=10,
        app_icon="images/app_logo.ico"
    )
    time.sleep(0.2)
    

def handle_sends(*arguments):
    toSend ="|".join(arguments) + "&"
    print(toSend)
    encrypted_message = cipher.encrypt(toSend.encode())
    sock.send(encrypted_message)
    # print(f'{encrypted_message =}')
    return waitToConfim()

def waitToConfim():
    enc_message = sock.recv(1024)
    message = cipher.decrypt(enc_message).decode()
    return message

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
    dataOfMessages = handle_sends("loadServer", server)

def temp(a):
    return a

def home_screen():
    window.update()
    dmY = 250
    serversY = 450
    lefSideX = 50
    i = 0
    dm = Button(window, image=dmBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("dm"))
    dm.place(x=lefSideX, y=dmY)

    servers = handle_sends("getServers").split("|")[1]
    print("-----------------------------------------------")
    servers = json.loads(servers)
    print(f"{servers=}")
    serversButtons = []
    for server in servers:
        print(server)
        serversButtons.append(Button(window, text=servers[server], bg=backgroundColor, fg=secondColor, font=("Assistant", 25, "bold"), command=lambda a=server: loadServer(a)))
        serversButtons[i].place(x=lefSideX, y=serversY + 100 * i)
        i += 1

def resize_images(winWidth):
    global registerImage, registerBTNImage
    global loginImage, loginBTNImage
    global smallLoginImage, smallLoginBTNImage
    global smallRegisterImage, smallRegisterBTNImage
    global homeImage, homeBTNImage
    global XImage, XBTNImage
    global dmImage, dmBTNImage
    global settingsImage, settingsBTNImage

    #submin buttons
    proportion = 4

    # register button
    originalSize = registerOriginImage.size
    newWidth = int(winWidth/proportion)
    registerImage = registerOriginImage.resize(get_new_size(originalSize, newWidth))
    registerBTNImage = ImageTk.PhotoImage(registerImage)

    #login button
    originalSize = loginOriginImage.size
    newWidth = int(winWidth/proportion)
    loginImage = loginOriginImage.resize(get_new_size(originalSize, newWidth))
    loginBTNImage = ImageTk.PhotoImage(loginImage)


    #small submit buttons
    proportion = 5
    
    #small login button
    originalSize = smallLoginOriginImage.size
    newWidth = int(winWidth/proportion)
    smallLoginImage = loginOriginImage.resize(get_new_size(originalSize, newWidth))
    smallLoginBTNImage = ImageTk.PhotoImage(smallLoginImage)

    #small register button
    originalSize = smallRegisterOriginImage.size
    newWidth = int(winWidth/proportion)
    smallRegisterImage = registerOriginImage.resize(get_new_size(originalSize, newWidth))
    smallRegisterBTNImage = ImageTk.PhotoImage(smallRegisterImage)

    #home buttons
    proportion = 12.8

    #home button
    originalSize = homeOriginImage.size
    print(f"{originalSize=}")
    newWidth = int(winWidth/proportion)
    print(f"{winWidth=}")
    print(f"{newWidth=}")
    homeImage = homeOriginImage.resize(get_new_size(originalSize, newWidth))
    print(f"{homeImage.size=}")
    homeBTNImage = ImageTk.PhotoImage(homeImage)

    #x button
    originalSize = XOriginImage.size
    newWidth = int(winWidth/proportion)
    XImage = XOriginImage.resize(get_new_size(originalSize, newWidth))
    XBTNImage = ImageTk.PhotoImage(XImage)

    #settings button
    originalSize = settingsOriginImage.size
    newWidth = int(winWidth/proportion)
    settingsImage = settingsOriginImage.resize(get_new_size(originalSize, newWidth))
    settingsBTNImage = ImageTk.PhotoImage(settingsImage)

    #dm button
    proportion = 17
    originalSize = dmImage.size
    newWidth = int(winWidth/proportion)
    dmImage = dmOriginImage.resize(get_new_size(originalSize, newWidth))
    dmBTNImage = ImageTk.PhotoImage(dmImage)

def get_new_size(originalSize: tuple, newWidth: int):
    return (newWidth, int(originalSize[1] * newWidth/originalSize[0]))

def login_register_screens(screen):
    global emailEntry, usernameEntry, passwordEntry
    global winHeight, winWidth

    titleWidth = int(winWidth / 4)
    titleFontSize = int(winWidth/20)
    print(f"{titleFontSize=}")

    entrysTitlesFontSize = int(winWidth/57)
    titleX = winWidth / 2 - titleWidth / 2
    emailY = 1.7 * winHeight / 4
    passwordY = emailY + int(winHeight/7)
    labelX = winWidth / 4

    submitX = winWidth / 3 - 100
    submitY = passwordY + int(winWidth/12)

    emailLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", entrysTitlesFontSize, "bold"), text="Email:")
    emailLabel.place(x=labelX, y=emailY - (winHeight/17))

    emailEntry = Entry(window, bg=secondColor, font=("Assistant", entrysTitlesFontSize, "bold"))
    emailEntry.place(x=labelX, y=emailY, width=int(winWidth / 3))

    passwordLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", entrysTitlesFontSize, "bold"), text="Password:")
    passwordLabel.place(x=labelX, y=passwordY - int(winHeight/17))

    passwordEntry = Entry(window, bg=secondColor, font=("Assistant", entrysTitlesFontSize, "bold"), show="*")
    passwordEntry.place(x=labelX, y=passwordY, width=int(winWidth / 3))

    showPasswordButton = Checkbutton(window, text="show password", bg=backgroundColor, fg=secondColor,
                                     highlightthickness=0, activebackground=backgroundColor, bd=0,
                                     font=("Assistant", int(0.7 * entrysTitlesFontSize), "bold"), command=show_password)
    showPasswordButton.place(x=labelX, y=passwordY + int(winHeight/13))

    if screen == "register":
        usernameY = emailY - int(winHeight/7)
        usernameEntry = Entry(window, bg=secondColor, font=("Assistant", int(entrysTitlesFontSize * 0.8), "bold"))
        usernameEntry.place(x=labelX, y=usernameY, width=int(winWidth / 3))
        usernameLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", entrysTitlesFontSize, "bold"),
                              text="Username:")
        usernameLabel.place(x=labelX, y=usernameY - int(winHeight/17))
        titleLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", titleFontSize, "bold"), text="register")
        
        submitButton = Button(window, image=registerBTNImage, bd=0, highlightthickness=0,
                              activebackground=backgroundColor, bg=backgroundColor, command=register)
        
        getOtherLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", int(entrysTitlesFontSize * 0.8), "bold"),
                              text="Already have account?")
        getOtherButton = Button(window, image=smallLoginBTNImage, bd=0, highlightthickness=0,
                                activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("login"))

    else:
        titleLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", titleFontSize, "bold"), text="login")
        submitButton = Button(window, image=loginBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor,
                              bg=backgroundColor, command=login)
        getOtherLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", int(entrysTitlesFontSize * 0.8), "bold"),
                              text="Still don't have account?")
        getOtherButton = Button(window, image=smallRegisterBTNImage, bd=0, highlightthickness=0,
                                activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("register"))

    #print(submitX)
    submitButton.place(x=submitX, y=submitY)
    titleLabel.place(x=titleX, y=50, width=titleWidth)
    getOtherLabel.place(x=submitX + int(winWidth / 2.5), y=submitY - 60)
    getOtherButton.place(x=submitX + int(winWidth / 2.5), y=submitY)


def settingsScreen():
    global window

    # scrollbar = Scrollbar(window, orient=VERTICAL, command=window.yview)
    # scrollbar.pack(side=RIGHT, fill=Y)
    # window.configure(yscrollcommand=scrollbar.set)
    # window.bind("<configure>", lambda a: window.configure(scrollregion=window.bbox("all")))

    ResulationLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", 25, "bold"), text="Resulation:")
    ResulationLabel.place(x=200, y=225)
    resulationButtons = []
    resulations = ["fullscreen" ,"2560x1440", "1920x1080", "1280x720"]
    for i, resulation in enumerate(resulations):
        print(f"{i=}")
        print(resulation)
        resulationButtons.append(Button(window, text=resulations[i], bg=backgroundColor, fg=secondColor, font=("Assistant", 25, "bold"), command=lambda a=resulation: change_screen_resulation("settings", a)))
        resulationButtons[i].place(x=300, y =300 + 75 * i)
        max = 300 + 75 * i
    logout = Button(window, text="Logout", bg=backgroundColor, fg=secondColor, font=("Assistant", 25, "bold"), command=logout_user)
    logout.place(x=300, y= max+ 200)

    # resulation.place(x=0, y=0)
    
def logout_user():
    loadScreen("login")
    print("logout")


def change_screen_resulation(screen, res):
    global window
    print(f"{res=}")
    if res == "fullscreen":
        window.attributes('-fullscreen', True)
    else:
        window.attributes('-fullscreen', False)
        window.geometry(res)
    loadScreen(screen)

def loadScreen(screen):
    global window, emailEntry, passwordEntry, usernameEntry
    global winHeight, winWidth

    clearScreen()

    window.update()

    winWidth = window.winfo_width()
    winHeight = window.winfo_height()

    resize_images(winWidth)

    homeButton = Button(window, image=homeBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("home"))
    homeButton.place(x=0, y=0)

    xButton = Button(window, image=XBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=close)
    xButton.pack(anchor=NE)

    settings = Button(window, image=settingsBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("settings"))
    settings.place(x=winWidth-settingsImage.size[0], y=winHeight-settingsImage.size[1])

    if screen == "register" or screen == "login":
        login_register_screens(screen)
    elif screen == "home":
        home_screen()
    if screen == "settings":
        settingsScreen()

def close():
    global window
    # handle_client("close")
    window.destroy()

def mainG():
    global screenSize
    global window, f, sock

    sock = socket.socket()
    sock.connect((ip, port))

    window.attributes('-fullscreen', True)
    window.resizable(False, False)
    window.update()
    # print(str(window.winfo_width()) + " " + str(window.winfo_height()))

    window['background'] = backgroundColor
    loadScreen("register")
    # graphic_t = Thread(target=loadScreen, args=("register",))
    # graphic_t.start()

    window.mainloop()
    # graphic_t.join()

if __name__ == '__main__':
    mainG()

