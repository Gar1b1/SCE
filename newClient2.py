from tkinter import *
import re, socket, platform, time, json
from PIL import Image, ImageTk
from threading import Thread
from cryptography.fernet import Fernet
from plyer import notification as nt
import ctypes
# from win11toast import toast
# import win11toast
from winotify import Notification

# encrypt
fkey = open("key.txt", "rb")
key = fkey.read()
cipher = Fernet(key)
fkey.close()

# graphic
global winHeight, winWidth, resulations, current_res
imgPath = "images/"
backgroundColor = "#040030"
secondColor = "#76E6CB"
user32 = ctypes.windll.user32
maxResulation = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

window = Tk()

#fonts sizes
global titlesFontSize, appTextFontSize, titleWidth

#connection
ip = "127.0.0.1"
port = 3339
global sock

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

global emailEntry, passwordEntry, usernameEntry, isUser, titleX


def getResulations(maxResulation):
    allRes = {2560: "2560x1440", 1920: "1920x1080", 1280: "1280x720"}
    possiableRes = allRes.copy()
    maxWidht = maxResulation[0]
    print(f"{maxWidht=}")
    keys = allRes.keys()
    for key in keys:
        if maxWidht <= key:
            print(f"{key=}")
            del possiableRes[key]
    possiableRes = list(possiableRes.values())
    possiableRes.insert(0, "fullscreen")
    print(f"{possiableRes=}")
    return possiableRes
        

def register():
    global emailEntry, passwordEntry, usernameEntry, isUser
    username = usernameEntry.get()
    email = emailEntry.get()
    password = passwordEntry.get()
    data = handle_sends("register", username, email, password).split("|")
    successfully = data[1]
    if successfully:
        isUser = True
        loadScreen("home")
        notify("register successfully", "thank you for register")
    elif data[2] == "password":
        notify("register failed", "password is not valid")
    elif not bool(data[3]):
        notify("register failed", "email is already used")

    # passwordValidate = checkPassword(password)
    # print('register')
    # if passwordValidate == "valid":
    #     loadScreen("login")
    #     userData = f"username: {username} email: {email} password: {password}"
    #     # print(userData)
    #     handle_sends("register", username, email, password)
    # else:
    #     print(f"password: {password} is not valid because it is {passwordValidate}")

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
    global emailEntry, passwordEntry, cipher, isUser
    email = emailEntry.get()
    password = passwordEntry.get()
    print(f"{email=}, {password=}")
    userData = f"email: {email} password: {password}"
    successfully = handle_sends("login", email, password).split("|")[1] == "successfully"
    print(f"{successfully=}")

    if successfully:
        isUser=True
        loadScreen("home")
        notify("login successfully", "welcome back")
    else:
        notify("login failed","user params are inncorect")
    print(userData)
    print('login')

def notify(title1, message1):
    global current_res
    if current_res != "fullscreen":
        nt.notify(
            title=title1,
            message=message1,
            timeout=2
        )
    else:
        emailEntry 
    

def handle_sends(*arguments):
    toSend ="|".join(arguments) + "&"
    print(f"{toSend=}")
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
    dmY = int(winHeight/6.5)
    serversY = int(winHeight/3.5)
    lefSideX = int(winWidth/50)
    dm = Button(window, image=dmBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("dm"))
    dm.place(x=lefSideX, y=dmY)
    
    joinServer = Button(window, image=dmBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("dm"))
    joinServer.place()

    servers = handle_sends("getServers").split("|")[1]
    print("-----------------------------------------------")
    servers = dict(json.loads(servers))
    print(f"{servers=}")
    serversButtons = []
    keys = list(servers.keys())
    for i, server in enumerate(keys):
        print(server)
        sb = Button(window, text=servers[server], bg=backgroundColor, fg=secondColor, font=("Assistant", int(appTextFontSize * 0.8), "bold"), command=lambda a=server: loadServer(a))
        sb.pack(anchor=N)
        sb.update()
        sb.place(x=lefSideX, y=(serversY + (int(winHeight/50) + sb.winfo_height()) * i))
        window.update()
        print(f"{winHeight=}")
        serversButtons.append(sb)

def resize_screen(winWidth):
    global registerImage, registerBTNImage
    global loginImage, loginBTNImage
    global smallLoginImage, smallLoginBTNImage
    global smallRegisterImage, smallRegisterBTNImage
    global homeImage, homeBTNImage
    global XImage, XBTNImage
    global dmImage, dmBTNImage
    global settingsImage, settingsBTNImage

    global titlesFontSize, appTextFontSize, titleWidth, titleX
    #texts data
    titlesFontSize  = int(winWidth/25)
    appTextFontSize = int(winWidth/65)

    titleWidth = int(winWidth / 4)

    titleX = winWidth / 2 - titleWidth / 2

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
    global titlesFontSize, appTextFontSize, titleWidth

    emailY = 1.7 * winHeight / 4
    passwordY = emailY + int(winHeight/7)
    labelX = winWidth / 4

    submitX = winWidth / 3 - 100
    submitY = passwordY + int(winWidth/12)

    emailLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", appTextFontSize, "bold"), text="Email:")
    emailLabel.place(x=labelX, y=emailY - (winHeight/17))

    emailEntry = Entry(window, bg=secondColor, font=("Assistant", appTextFontSize, "bold"))
    emailEntry.place(x=labelX, y=emailY, width=int(winWidth / 3))

    passwordLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", appTextFontSize, "bold"), text="Password:")
    passwordLabel.place(x=labelX, y=passwordY - int(winHeight/17))

    passwordEntry = Entry(window, bg=secondColor, font=("Assistant", appTextFontSize, "bold"), show="*")
    passwordEntry.place(x=labelX, y=passwordY, width=int(winWidth / 3))

    showPasswordButton = Checkbutton(window, text="show password", bg=backgroundColor, fg=secondColor,
                                     highlightthickness=0, activebackground=backgroundColor, bd=0,
                                     font=("Assistant", int(0.7 * appTextFontSize), "bold"), command=show_password)
    showPasswordButton.place(x=labelX, y=passwordY + int(winHeight/13))

    titleLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", titlesFontSize, "bold"), text=screen)
    titleLabel.place(x=titleX, y=50, width=titleWidth)

    if screen == "register":
        usernameY = emailY - int(winHeight/7)
        usernameEntry = Entry(window, bg=secondColor, font=("Assistant", int(appTextFontSize), "bold"))
        usernameEntry.place(x=labelX, y=usernameY, width=int(winWidth / 3))
        usernameLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", appTextFontSize, "bold"),
                              text="Username:")
        usernameLabel.place(x=labelX, y=usernameY - int(winHeight/17))
        
        submitButton = Button(window, image=registerBTNImage, bd=0, highlightthickness=0,
                              activebackground=backgroundColor, bg=backgroundColor, command=register)
        
        getOtherLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", int(appTextFontSize * 0.8), "bold"),
                              text="Already have account?")
        getOtherButton = Button(window, image=smallLoginBTNImage, bd=0, highlightthickness=0,
                                activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("login"))

    else:
        submitButton = Button(window, image=loginBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor,
                              bg=backgroundColor, command= login)
        getOtherLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", int(appTextFontSize * 0.8), "bold"),
                              text="Still don't have account?")
        getOtherButton = Button(window, image=smallRegisterBTNImage, bd=0, highlightthickness=0,
                                activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("register"))

    #print(submitX)
    submitButton.place(x=submitX, y=submitY)
    titleLabel.place(x=titleX, y=50, width=titleWidth)
    getOtherLabel.place(x=submitX + int(winWidth / 2.5), y=submitY - 60)
    getOtherButton.place(x=submitX + int(winWidth / 2.5), y=submitY)


def settingsScreen():
    global window, resulations, isUser

    global titlesFontSize, appTextFontSize, titleWidth, titleX


    # scrollbar = Scrollbar(window, orient=VERTICAL, command=window.yview)
    # scrollbar.pack(side=RIGHT, fill=Y)
    # window.configure(yscrollcommand=scrollbar.set)
    # window.bind("<configure>", lambda a: window.configure(scrollregion=window.bbox("all")))
    resulationLabelX = 250
    resulationLabelY = 250
    resulationLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", appTextFontSize, "bold"), text="Resulation:")
    resulationLabel.place(x=resulationLabelX, y=resulationLabelY)
    resulationButtons = []

    titleLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", titlesFontSize, "bold"), text="settings")
    titleLabel.place(x=titleX, y=50, width=titleWidth)

    for i, resulation in enumerate(resulations):
        print(f"{i=}")
        print(resulation)
        rb = Button(window, text=resulations[i], bg=backgroundColor, fg=secondColor, font=("Assistant", int(appTextFontSize * 0.9), "bold"), command=lambda a=resulation: change_screen_resulation("settings", a))
        rb.pack(anchor=N)
        rb.update()
        bh = rb.winfo_height()
        max = ((resulationLabelY + resulationLabel.winfo_height() + int(winHeight/50)) + (int(winHeight/50) + rb.winfo_height()) * i)
        rb.place(x=resulationLabelX + int (winWidth/ 50), y = max)
        rb.update()
        resulationButtons.append(rb)
        print(f"{bh=}")
    if isUser:
        logout = Button(window, text="Logout", bg=backgroundColor, fg=secondColor, font=("Assistant", appTextFontSize, "bold"), command=logout_user)
        logout.place(x=resulationLabelX, y= max + rb.winfo_height() + int(winHeight/25))

    # resulation.place(x=0, y=0)
    
def logout_user():
    global isUser
    isUser = False
    successfully = handle_sends("logout").split("|")[1] == "successfully"
    if successfully:
        loadScreen("login")
        print("logout")
    else:
        print("error")

def change_screen_resulation(screen, res):
    global window, current_res
    print(f"{res=}")
    current_res = res
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

    resize_screen(winWidth)

    xButton = Button(window, image=XBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=close)
    xButton.pack(anchor=NE)
    
    homeButton = Button(window, image=homeBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("home"))
    if not isUser:
        homeButton.config(command=lambda: loadScreen("login"))        
    homeButton.place(x=0, y=0)


    settings = Button(window, image=settingsBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("settings"))
    settings.place(x=winWidth-settingsImage.size[0], y=winHeight-settingsImage.size[1])

    if screen == "register" or screen == "login":
        login_register_screens(screen)
    else:

        if screen == "home":
            home_screen()
        elif screen == "settings":
            settingsScreen()

def close():
    global window
    # handle_client("close")
    window.destroy()

def mainG():
    global window, sock, resulations, isUser, current_res

    isUser = False
    sock = socket.socket()
    sock.connect((ip, port))

    window.attributes('-fullscreen', True)
    current_res = "fullscreen"
    
    window.resizable(False, False)
    window.update()
    # print(str(window.winfo_width()) + " " + str(window.winfo_height()))

    window['background'] = backgroundColor
    loadScreen("register")


    resulations = getResulations(maxResulation)

    # graphic_t = Thread(target=loadScreen, args=("register",))
    # graphic_t.start()

    window.mainloop()
    # graphic_t.join()

if __name__ == '__main__':
    mainG()

