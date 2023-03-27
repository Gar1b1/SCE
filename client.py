from tkinter import *
from tkinter import ttk
import re, socket, platform, time, json
from PIL import Image, ImageTk
from threading import Thread
from cryptography.fernet import Fernet
from plyer import notification as nt
import ctypes
from win11toast import toast
import win11toast
# from winotify import Notification
from windows_toasts import WindowsToaster,InteractableWindowsToaster, ToastInputTextBox, ToastText1, ToastButton
import windows_toasts



# encrypt
fkey = open("key.txt", "rb")
key = fkey.read()
cipher = Fernet(key)
fkey.close()

# graphic
global winHeight, winWidth, resulations, current_res, homeButton
imgPath = "images/"
backgroundColor = "#040030"
secondColor = "#76E6CB"
user32 = ctypes.windll.user32
maxResulation = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

window = Tk()

#sizes
global titlesFontSize, appTextFontSize, titleWidth, mainEntrysWidth, titleX, titleY

global isUser

#connection
ip = "127.0.0.1"
port = 3339
global sock

#origin images
XOriginImage = Image.open(f"{imgPath}xButton.png")
homeOriginImage = Image.open(f"{imgPath}homeButton.png")
registerOriginImage = Image.open(f"{imgPath}registerButton.png")
loginOriginImage = Image.open(f"{imgPath}loginButton.png")
dmOriginImage = Image.open(f"{imgPath}dmButton.png")
settingsOriginImage = Image.open(f"{imgPath}settings.png")
joinServerOriginImage = Image.open(f"{imgPath}joinServer.png")
joinOriginImage = Image.open(f"{imgPath}joinButton.png")
newServerOriginImage = Image.open(f"{imgPath}createServer.png")
createOriginImage = Image.open(f"{imgPath}createButton.png")
addFriendOriginImage = Image.open(f"{imgPath}addFriend.png")
addOriginImage = Image.open(f"{imgPath}addButton.png")
changeOriginImage = Image.open(f"{imgPath}changeButton.png")

# XImage = Image.open(f"{imgPath}xButton.png")
# homeImage = Image.open(f"{imgPath}homeButton.png")
# registerImage = Image.open(f"{imgPath}registerButton.png")
# loginImage = Image.open(f"{imgPath}loginButton.png")
# dmImage = Image.open(f"{imgPath}dmButton.png")
# settingsImage = Image.open(f"{imgPath}settings.png")
# joinServerImage = Image.open(f"{imgPath}joinServer.png")
# joinImage = Image.open(f"{imgPath}joinButton.png")
# XBTNImage = ImageTk.PhotoImage(XImage)
# homeBTNImage = ImageTk.PhotoImage(homeImage)
# registerBTNImage = ImageTk.PhotoImage(registerImage)
# loginBTNImage = ImageTk.PhotoImage(loginImage)
# smallLoginBTNImage
# smallRegisterBTNImage
# dmBTNImage = ImageTk.PhotoImage(dmImage)
# settingsBTNImage = ImageTk.PhotoImage(settingsImage)
# joinServerBTNImage = ImageTk.PhotoImage(joinServerImage)
# joinBTNImage = ImageTk.PhotoImage(joinImage)

#changeable images
global XImage, homeImage, registerImage, loginImage, smallLoginImage, smallRegisterImage, dmImage, settingsImage, joinServerImage, joinImage, newServerImage, createImage, addFriendImage, addImage, changeImage

#buttons images
global XBTNImage, homeBTNImage, registerBTNImage, loginBTNImage, smallLoginBTNImage, smallRegisterBTNImage, dmBTNImage, settingsBTNImage, joinServerBTNImage, joinBTNImage, newServerBTNImage, createBTNImage, addFriendBTNImage, addBTNImage, changeBTNImage

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
        

def register(email: str, password: str, username: str):
    if "|" in password or "&" in password:
        print(password)
        notify("register failed", "password is not valid")
        return
    print(f"{email=} {username=} {password=}")
    data = handle_sends("register", username, email, password).split("|")
    successfully = data[1] == "successfully"
        
    if successfully:
        notify("sent verification code", "check you email box for your verification code")
        loadScreen("email validation")

    else:
        data = " ".join(data[1:])
        print(f"{data}")
        notify("register failed", data)

def finish_register(verificationCode):
    global isUser
    data = handle_sends("finish register", verificationCode).split("|")
    successfully = data[1] == "successfully"
    if successfully:
        isUser = True
        notify("registered successfully", "welcome to SCE")
        loadScreen("Home")


def login(email: str, password: str):
    global isUser
    print(f"{email=}, {password=}")
    userData = f"email: {email} password: {password}"
    successfully = handle_sends("login", email, password).split("|")[1] == "successfully"
    print(f"{successfully=}")

    if successfully:
        isUser=True
        loadScreen("Home")
        notify("login successfully", "welcome back")
    else:
        notify("login failed","user params are inncorect")
    print(userData)
    print('login')

def notify(title1, message1):
    global current_res
    print(title1, message1)
    try:
        # win11toast.ToastNotificationManager.create_toast_notifier("Python")
        winToaster = WindowsToaster("SCE")
        winToaster2 = InteractableWindowsToaster("SCE")
        newToast = ToastText1()
        newToast.SetBody(message1)
        newToast.AddInput(ToastInputTextBox("name", "your name", "Alon Garibi"))
        newToast.AddAction(ToastButton("Submit", "submit"))
        winToaster2.show_toast(newToast)
    except:
        pass

    

def handle_sends(*arguments):
    toSend ="|".join(arguments) + "&"
    print(f"{toSend=}")
    encrypted_message = cipher.encrypt(toSend.encode())
    sock.send(encrypted_message)
    # print(f'{encrypted_message =}')
    tr = waitToConfim()
    print(tr)
    # return waitToConfim()
    return tr

def waitToConfim():
    enc_message = sock.recv(1024)
    message = cipher.decrypt(enc_message).decode()
    return message

def clearScreen():
    for widget in window.winfo_children():
        widget.destroy()

def show_password(passwordEntry):
    if passwordEntry.cget('show') == '*':
        passwordEntry.config(show='')
    else:
        passwordEntry.config(show='*')

def loadServer(server):
    loadScreen("server")
    # dataOfMessages = handle_sends("loadServer", server)
    print(server)

def temp(a):
    return a

def homeSceen():
    dmY = int(winHeight/6.5)
    serversY = int(winHeight/3.5)
    lefSideX = int(winWidth/50)
    dm = Button(window, image=dmBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("dm"))
    dm.place(x=lefSideX, y=dmY)
    
    joinServer = Button(window, image=joinServerBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("Join Server"))
    joinServer.place(x=winWidth-joinServerImage.size[0], y=winHeight-settingsImage.size[1] - joinServerImage.size[1] - winHeight/30)

    joinServer.update()

    servers = handle_sends("getServers").split("|")[1]
    print("-----------------------------------------------")
    servers = dict(json.loads(servers))
    print(f"{servers=}")
    serversButtons = []
    keys = list(servers.keys())
    first = True
    for server in keys:
        print(server)
        sb = Button(window, text=servers[server], bg=backgroundColor, fg=secondColor, font=("Assistant", int(appTextFontSize * 0.8), "bold"), command=lambda a=server: loadServer(a))
        y = serversY
        if not first:
            y = serversButtons[-1].winfo_y() + serversButtons[-1].winfo_height() + int(winHeight/100)
        first = False
        
        sb.place(x=lefSideX, y= y)
        sb.update()
        print(f"{winHeight=}")
        serversButtons.append(sb)
    window.update()
    

def resize_screen():
    global registerImage, registerBTNImage
    global loginImage, loginBTNImage
    global joinImage, joinBTNImage
    global joinServerImage, joinServerBTNImage
    global smallLoginImage, smallLoginBTNImage
    global smallRegisterImage, smallRegisterBTNImage
    global homeImage, homeBTNImage
    global XImage, XBTNImage
    global dmImage, dmBTNImage
    global settingsImage, settingsBTNImage
    global newServerImage, newServerBTNImage
    global createImage, createBTNImage
    global addFriendImage, addFriendBTNImage
    global addImage, addBTNImage
    global changeImage, changeBTNImage

    global titlesFontSize, appTextFontSize, titleWidth, titleX, titleY, mainEntrysWidth
    #texts data
    titlesFontSize  = int(winWidth/25)
    appTextFontSize = int(winWidth/65)

    titleWidth = int(winWidth / 1.25)

    titleX = int(winWidth / 2) - int(titleWidth / 2)
    titleY = int(winHeight / 28)

    mainEntrysWidth = int(winWidth/3)

    #submit buttons
    proportion = 4
    newWidth = int(winWidth/proportion)

    # register button
    originalSize = registerOriginImage.size
    registerImage = registerOriginImage.resize(get_new_size(originalSize, newWidth))
    registerBTNImage = ImageTk.PhotoImage(registerImage)

    # login button
    originalSize = loginOriginImage.size
    loginImage = loginOriginImage.resize(get_new_size(originalSize, newWidth))
    loginBTNImage = ImageTk.PhotoImage(loginImage)

    # join button
    originalSize = joinOriginImage.size
    joinImage = joinOriginImage.resize(get_new_size(originalSize, newWidth))
    joinBTNImage = ImageTk.PhotoImage(joinImage)

    # create button
    originalSize = createOriginImage.size
    createImage = createOriginImage.resize(get_new_size(originalSize, newWidth))
    createBTNImage = ImageTk.PhotoImage(createImage)

    # add button
    originalSize = addOriginImage.size
    addImage = addOriginImage.resize(get_new_size(originalSize, newWidth))
    addBTNImage = ImageTk.PhotoImage(addImage)

    # change button
    originalSize = changeOriginImage.size
    changeImage = changeOriginImage.resize(get_new_size(originalSize, newWidth))
    changeBTNImage = ImageTk.PhotoImage(changeImage)

    # #small submit buttons
    proportion = 5
    newWidth = int(winWidth/proportion)
    
    #small login button
    originalSize = loginOriginImage.size
    smallLoginImage = loginOriginImage.resize(get_new_size(originalSize, newWidth))
    smallLoginBTNImage = ImageTk.PhotoImage(smallLoginImage)

    #small register button
    originalSize = registerOriginImage.size
    smallRegisterImage = registerOriginImage.resize(get_new_size(originalSize, newWidth))
    smallRegisterBTNImage = ImageTk.PhotoImage(smallRegisterImage)

    #home buttons
    proportion = 12.8
    newWidth = int(winWidth/proportion)

    #home button
    originalSize = homeOriginImage.size
    homeImage = homeOriginImage.resize(get_new_size(originalSize, newWidth))
    homeBTNImage = ImageTk.PhotoImage(homeImage)

    #x button
    originalSize = XOriginImage.size
    XImage = XOriginImage.resize(get_new_size(originalSize, newWidth))
    XBTNImage = ImageTk.PhotoImage(XImage)

    #settings button
    originalSize = settingsOriginImage.size
    settingsImage = settingsOriginImage.resize(get_new_size(originalSize, newWidth))
    settingsBTNImage = ImageTk.PhotoImage(settingsImage)

    #dm button
    proportion = 17
    newWidth = int(winWidth/proportion)

    originalSize = dmOriginImage.size
    dmImage = dmOriginImage.resize(get_new_size(originalSize, newWidth))
    dmBTNImage = ImageTk.PhotoImage(dmImage)

    #move to join/create server screen buttons
    proportion = 8.5
    newWidth = int(winWidth/proportion)
    
    #join server button
    originalSize = joinServerOriginImage.size
    joinServerImage = joinServerOriginImage.resize(get_new_size(originalSize, newWidth))
    joinServerBTNImage = ImageTk.PhotoImage(joinServerImage)

    #create server button
    originalSize = newServerOriginImage.size
    newServerImage = newServerOriginImage.resize(get_new_size(originalSize, newWidth))
    newServerBTNImage = ImageTk.PhotoImage(newServerImage)

    #add friend button
    originalSize = addFriendOriginImage.size
    addFriendImage = addFriendOriginImage.resize(get_new_size(originalSize, newWidth))
    addFriendBTNImage = ImageTk.PhotoImage(addFriendImage)


def get_new_size(originalSize: tuple, newWidth: int):
    return (newWidth, int(originalSize[1] * newWidth/originalSize[0]))

def loginRegisterScreens(screen):
    global emailEntry, usernameEntry, passwordEntry
    global winHeight, winWidth
    global titlesFontSize, appTextFontSize, titleWidth

    emailY = int(winHeight/3.5)
    labelX = int(winWidth / 4)
    
    if screen == "Register":
        usernameY = emailY + int(winHeight/7)
        passwordY = emailY + int(winHeight/3.5)
        usernameEntry = Entry(window, bg=secondColor, font=("Assistant", int(appTextFontSize), "bold"))
        usernameEntry.place(x=labelX, y=usernameY, width=mainEntrysWidth)
        usernameLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", appTextFontSize, "bold"),
                              text="Username:")
        usernameLabel.place(x=labelX, y=usernameY - int(winHeight/17))
        
        getOtherLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", int(appTextFontSize * 0.8), "bold"),
                              text="Already have account?")
        getOtherButton = Button(window, image=smallLoginBTNImage, bd=0, highlightthickness=0,
                                activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("login"))
        submitWidth = registerImage.size[0]
        submitX = int(mainEntrysWidth/2) + labelX - (submitWidth)/2
        

    else:
        passwordY = emailY + int(winHeight/7)

        getOtherLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", int(appTextFontSize * 0.8), "bold"),
                              text="Still don't have account?")
        getOtherButton = Button(window, image=smallRegisterBTNImage, bd=0, highlightthickness=0,
                                activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("Register"))
        
        submitWidth = loginImage.size[0]
        submitX = int(mainEntrysWidth/2) + labelX - (submitWidth)/2

        # forgotPassword = Button(window, text="Logout", bg=backgroundColor, fg=secondColor, font=("Assistant", appTextFontSize, "bold"), command=logout_user)
        # forgotPassword.place(x=LabelX, y= max + rb.winfo_height() + int(winHeight/25))


    submitY = passwordY + int(winWidth/12)

    emailLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", appTextFontSize, "bold"), text="Email:")
    emailLabel.place(x=labelX, y=emailY - (winHeight/17))

    emailEntry = Entry(window, bg=secondColor, font=("Assistant", appTextFontSize, "bold"))
    emailEntry.place(x=labelX, y=emailY, width=mainEntrysWidth)

    passwordLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", appTextFontSize, "bold"), text="Password:")
    passwordLabel.place(x=labelX, y=passwordY - int(winHeight/17))

    passwordEntry = Entry(window, bg=secondColor, font=("Assistant", appTextFontSize, "bold"), show="*")
    passwordEntry.place(x=labelX, y=passwordY, width=mainEntrysWidth)

    showPasswordButton = Checkbutton(window, text="show password", bg=backgroundColor, fg=secondColor,
                                     highlightthickness=0, activebackground=backgroundColor, bd=0,
                                     font=("Assistant", int(0.7 * appTextFontSize), "bold"), command= lambda: show_password(passwordEntry))
    showPasswordButton.place(x=labelX, y=passwordY + int(winHeight/13))

    if screen == "Register":
        submitButton = Button(window, image=registerBTNImage, bd=0, highlightthickness=0,
                activebackground=backgroundColor, bg=backgroundColor, command= lambda: register(emailEntry.get(), passwordEntry.get(), usernameEntry.get()))
    else:
        submitButton = Button(window, image=loginBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor,
                bg=backgroundColor, command= lambda: login(emailEntry.get(), passwordEntry.get()))

    #print(submitX)
    submitButton.place(x=submitX, y=submitY)
    getOtherLabel.place(x=submitX + int(winWidth / 2.5), y=submitY - (winHeight/24))
    getOtherButton.place(x=submitX + int(winWidth / 2.5) - int(winWidth/60), y=submitY)

def settingsScreen():
    global window, resulations, isUser

    global titlesFontSize, appTextFontSize, titleWidth, titleX

    LabelX = int(winWidth/10)
    resulationLabelY = int(winHeight/5.5)
    resulationLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", appTextFontSize, "bold"), text="Resulation:")
    resulationLabel.place(x=LabelX, y=resulationLabelY)
    resulationButtons = []

    for i, resulation in enumerate(resulations):
        print(f"{i=}")
        print(resulation)
        rb = Button(window, text=resulations[i], bg=backgroundColor, fg=secondColor, font=("Assistant", int(appTextFontSize * 0.9), "bold"), command=lambda a=resulation: change_screen_resulation("settings", a))
        rb.pack(anchor=N)
        rb.update()
        bh = rb.winfo_height()
        max = ((resulationLabelY + resulationLabel.winfo_height() + int(winHeight/50)) + (int(winHeight/50) + rb.winfo_height()) * i)
        rb.place(x=LabelX + int (winWidth/ 50), y = max)
        rb.update()
        resulationButtons.append(rb)
        print(f"{bh=}")
    if isUser:
        logout = Button(window, text="Logout", bg=backgroundColor, fg=secondColor, font=("Assistant", appTextFontSize, "bold"), command=logout_user)
        logout.place(x=LabelX, y= max + rb.winfo_height() + int(winHeight/25))

        window.update()
        print(f"{logout.winfo_y()=}")
        chnageUser = Button(window, text="change user data", bg=backgroundColor, fg=secondColor, font=("Assistant", appTextFontSize, "bold"), command = lambda: loadScreen("change user"))
        chnageUser.place(x=LabelX, y = logout.winfo_y() + logout.winfo_height() + int(winHeight/25))

    # resulation.place(x=0, y=0)
    
def logout_user():
    global isUser, homeButton
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
        window.overrideredirect(True)
        window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")
    else:
        window.overrideredirect(False)
        window.geometry(res)
    window.update()
    loadScreen(screen)

def loadScreen(screen):
    global window, emailEntry, passwordEntry, usernameEntry
    global winHeight, winWidth, homeButton

    clearScreen()

    winWidth = window.winfo_width()
    winHeight = window.winfo_height()

    window.update()

    resize_screen()

    loadBasicScreen(window, screen)

    window.update()


    print(screen)
    
    match screen:
        case "Register":
            loginRegisterScreens(screen)
        case "login":
            loginRegisterScreens(screen)
        case "Home":
            homeSceen()
        case "settings":
            settingsScreen()
        case "Create Server":
            createServerScreen()
        case "change user":
            changeUserDataScreen()
        case "dm":
            DMScreen()
        case "server":
            serverScreen()
        case _:
            defualt_screen(screen)

def serverScreen():
    clearScreen()
    serverCanvas = Canvas(window, bg=backgroundColor, bd=0, highlightthickness=0, highlightcolor=backgroundColor, width=winWidth, height=winHeight)
    serverCanvas['background'] = backgroundColor,
    scrollBar = ttk.Scrollbar 

    serverCanvas.pack(fill= BOTH, expand= True)
    loadBasicScreen(serverCanvas, "server")

def loadBasicScreen(window2, screen):

    xButton = Button(window2, image=XBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=close)
    xButton.pack(anchor=NE)
    
    titleLabel = Label(window2, bg=backgroundColor, fg=secondColor, font=("Assistant", titlesFontSize, "bold"), text=screen.upper())
    titleLabel.place(x=titleX, y=int(winHeight/29), width=titleWidth)

    homeButton = Button(window2, image=homeBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("Home"))
    if not isUser:
        homeButton.config(command=lambda: loadScreen("login"))        
    homeButton.place(x=0, y=0)
    
    if screen != "settings":
        settings = Button(window2, image=settingsBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("settings"))
        settings.place(x=winWidth-settingsImage.size[0], y=winHeight-settingsImage.size[1])
        settings.update()

    

def changeUserDataScreen():
    usernameY = int(1.7 * winHeight / 4)
    passwordY = usernameY + int(winHeight/7)
    labelX = int(winWidth / 4)

    submitX = mainEntrysWidth - 100
    submitY = passwordY + int(winWidth/12)

    changeUsernameLabelText = "New Username:"
    changePasswordLabelText = "New Password:"
    explainText = "not all required".title()
    explainLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("assitant", appTextFontSize, "bold"), text=explainText)
    explainLabel.place(x=0, y=usernameY - int(winHeight/7), width=winWidth)

    changeUsernameLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", appTextFontSize, "bold"),
                         text=changeUsernameLabelText)
    changeUsernameLabel.place(x=labelX, y=usernameY - int(winHeight/17))
    
    changeUsernameEntry = Entry(window, bg=secondColor, font=("Assistant", int(appTextFontSize), "bold"))
    changeUsernameEntry.place(x=labelX, y=usernameY, width=mainEntrysWidth)

    ChangePasswordLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", appTextFontSize, "bold"), text=changePasswordLabelText)
    ChangePasswordLabel.place(x=labelX, y=passwordY - int(winHeight/17))
    
    ChangePasswordEntry = Entry(window, bg=secondColor, font=("Assistant", appTextFontSize, "bold"), show="*")
    ChangePasswordEntry.place(x=labelX, y=passwordY, width=mainEntrysWidth)

    showPasswordButton = Checkbutton(window, text="show password", bg=backgroundColor, fg=secondColor,
                                     highlightthickness=0, activebackground=backgroundColor, bd=0,
                                     font=("Assistant", int(0.7 * appTextFontSize), "bold"), command=lambda: show_password(ChangePasswordEntry))
    showPasswordButton.place(x=labelX, y=passwordY + int(winHeight/13))

    submitButton = Button(window, image=changeBTNImage, bd=0, highlightthickness=0,
                              activebackground=backgroundColor, bg=backgroundColor, command=lambda: manage_update(changeUsernameEntry.get(), ChangePasswordEntry.get()))
    submitButton.place(x=submitX, y=submitY)

def manage_update(username, password):
    changed = False
    if username != "":
        data = handle_sends("change username", username).split('|')
        print(f"{data=}")
        changed = data[1] == "successfully"
        if changed:
            notify("username changed", "username changed successfully")
        else:
            notify("username didnt changed", "username changed failed")
    if password != "":
        if "|" in password or "&" in password:
            print(password)
            notify("password didnt changed", "password is not valid")
            changed = False
        else:
            data = handle_sends("change password", password).split("|")
            changed = data[1] == "successfully"
            if changed:
                notify("password changed", "password changed successfully")
            else:
                data = " ".join(data[1:])
                notify("password didnt changed", data)
    print(changed)
    if changed:
        loadScreen("Home")

    
def DMScreen():
    friendsY = int(winHeight/5)
    lefSideX = int(winWidth/50)
        
    addFriend = Button(window, image=addFriendBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("Add friend"))
    addFriend.place(x=winWidth-joinServerImage.size[0], y=winHeight-settingsImage.size[1] - joinServerImage.size[1] - winHeight/30)

    friends = handle_sends("getFriends").split("|")[1]
    print("-----------------------------------------------")
    friends = dict(json.loads(friends))
    print(f"{friends=}")
    friendsButtons = []
    keys = list(friends.keys())
    for i, frined in enumerate(keys):
        print(friends)
        sb = Button(window, text=friends[frined], bg=backgroundColor, fg=secondColor, font=("Assistant", int(appTextFontSize * 0.8), "bold"), command=lambda a=frined: loadDMChat(a))
        sb.pack(anchor=N)
        sb.update()
        sb.place(x=lefSideX, y=(friendsY + (int(winHeight/50) + sb.winfo_height()) * i))
        window.update()
        print(f"{winHeight=}")
        friendsButtons.append(sb)

def loadDMChat(id):
    pass

def createServerScreen():
    global winHeight, winWidth
    global titlesFontSize, appTextFontSize, titleWidth

    nameY = int(1.7 * winHeight / 4)
    isGhostRoomsY = nameY + int(winHeight/7)
    labelX = int(winWidth / 4)
    ghostRooms = False

    submitX = mainEntrysWidth - 100
    submitY = isGhostRoomsY + int(winWidth/20)

    nameLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", appTextFontSize, "bold"), text="Server Name:")
    nameLabel.place(x=labelX, y=nameY - (winHeight/17))

    nameEntry = Entry(window, bg=secondColor, font=("Assistant", appTextFontSize, "bold"))
    nameEntry.place(x=labelX, y=nameY, width=mainEntrysWidth)

    ghostRoomButton = Checkbutton(window, text="ghost room", bg=backgroundColor, fg=secondColor,
                                     highlightthickness=0, activebackground=backgroundColor, bd=0, font=("Assistant", int(0.7 * appTextFontSize), "bold"), variable=ghostRooms, offvalue=False, onvalue=True)
    ghostRoomButton.place(x=labelX, y=nameY + int(winHeight/13))
    window.update()

    submitButton = Button(window, image=createBTNImage, bd=0, highlightthickness=0,
                              activebackground=backgroundColor, bg=backgroundColor, command=lambda: createServer(nameEntry.get(), ghostRooms))

    submitButton.place(x=int(winWidth/2) - int(joinImage.size[0]/2), y=submitY)

def createServer(name, isGhost):
    data = handle_sends("createServer", name, str(isGhost)).split("|")
    successfully = data[1] != "later"
    if successfully:
        notify("create server", "server created successfully")
        loadScreen("Home")
    


def defualt_screen(screen):    
    print(f"{screen=}")

    labelX = int(winWidth / 4)
    idEntryWidth = int(winWidth / 4)
    labelY = int(1.2 * winHeight / 4)
    submitY = labelY + int(winHeight / 7)
    
    match screen:
        case "Add friend":
            labelText = "Friend Email:"
            submitButtonImage = addBTNImage
            submitX = int(winWidth/2) - int(addImage.size[0]/2)
        case "Join Server":
            labelText = "Server ID:"
            submitButtonImage = joinBTNImage
            submitX = int(winWidth/2) - int(joinImage.size[0]/2)
        case "email validation":
            print("here")
            labelText = "Verify Code:"
            submitButtonImage = registerBTNImage
            submitX = int(winWidth/2) - int(addImage.size[0]/2)
            backToRegister = Button(window, text="back to register".title(), bd=0, highlightthickness=0,
                              activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("register"))
            backToRegister.place(x=submitX, y=submitY + registerImage.size[1] + int(winHeight/14))
        case _:
            return

    label = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", appTextFontSize, "bold"), text=labelText)
    label.place(x=labelX, y=labelY)

    label.update()
    len = idEntryWidth + int(label.winfo_width())
    labelX = int(winWidth/2)-int(len/2)

    label.place(x=labelX, y=labelY)
    label.update()
    entry = Entry(window, bg=secondColor, font=("Assistant", appTextFontSize, "bold"))
    entry.place(x=labelX + label.winfo_width(), y=labelY, width=idEntryWidth)
    entry.update()


    submitButton = Button(window, image=submitButtonImage, bd=0, highlightthickness=0,
                              activebackground=backgroundColor, bg=backgroundColor, command=lambda: addFriend(entry.get()))
    if screen == "Join Server":
        newButton =  Button(window, image=newServerBTNImage, bd=0, highlightthickness=0,
                                activebackground=backgroundColor, bg=backgroundColor, command=lambda: loadScreen("Create Server"))
        newButton.place(x=0, y= winHeight - newServerImage.size[1])
        submitButton.config(command=lambda: joinServer(entry.get()))
    if screen == "email validation":
        submitButton.config(command=lambda: finish_register(entry.get()))
    

    submitButton.place(x=submitX, y=submitY)

def addFriend(a):
    pass
    
def joinServer(id: Entry):
    print(f"{id=}")
    data = handle_sends("joinServer", id).split("|")
    print(data)
    successfully = data[1] == "successfully"
    if successfully:
        notify("joined server", "joined successfully to server")
        loadScreen("Home")
    else:
        notify("joined failed", data[1])


def close():
    global window
    # handle_client("close")
    window.destroy()

def mainG():
    global window, sock, resulations, isUser, current_res

    isUser = False
    sock = socket.socket()
    sock.connect((ip, port))

    # window.attributes('-fullscreen', False)
    current_res = "fullscreen"
    # window.attributes('-fullscreen', True)
    
    window.resizable(False, False)
    # print(str(window.winfo_width()) + " " + str(window.winfo_height()))

    window['background'] = backgroundColor
    # window.attributes('-fullscreen', False)
    change_screen_resulation("login", "fullscreen")

    resulations = getResulations(maxResulation)

    # graphic_t = Thread(target=loadScreen, args=("Register",))
    # graphic_t.start()

    window.mainloop()
    # graphic_t.join()

if __name__ == '__main__':
    mainG()

