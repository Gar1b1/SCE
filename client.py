from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import re, socket, platform, time, json
from PIL import Image, ImageTk
from threading import Thread
from cryptography.fernet import Fernet
import ctypes, os
from windows_toasts import WindowsToaster, ToastDisplayImage, ToastImageAndText1
import random, string, math


curPath = os.getcwd()

print(curPath)
# encrypt
fkey = open(curPath+"/key.txt", "rb")
key = fkey.read()
cipher = Fernet(key)
fkey.close()

# notification
winToaster = WindowsToaster("SCE")
msgbox = messagebox

# graphic
global resulations, screenManager
window = Tk()

global isUser, current_server, toRemember

#connection
ip = "127.0.0.1"
port = 3339
global sock

#origin images


class screen_manager():
    def __init__(self, window, current_res):
        self.imgPath = curPath+"/images/"
        self.backgroundColor = "#040030"
        self.secondColor = "#76E6CB"
        self.thirdColor = "#001830"

        self.window = window
        self.winWidth = self.window.winfo_width()
        self.winHeight = self.window.winfo_height()
  
        self.XOriginImage = Image.open(f"{self.imgPath}xButton.png")
        self.homeOriginImage = Image.open(f"{self.imgPath}homeButton.png")
        self.registerOriginImage = Image.open(f"{self.imgPath}registerButton.png")
        self.loginOriginImage = Image.open(f"{self.imgPath}loginButton.png")
        self.dmOriginImage = Image.open(f"{self.imgPath}dmButton.png")
        self.settingsOriginImage = Image.open(f"{self.imgPath}settings.png")
        self.joinServerOriginImage = Image.open(f"{self.imgPath}joinServer.png")
        self.joinOriginImage = Image.open(f"{self.imgPath}joinButton.png")
        self.newServerOriginImage = Image.open(f"{self.imgPath}createServer.png")
        self.createOriginImage = Image.open(f"{self.imgPath}createButton.png")
        self.addFriendOriginImage = Image.open(f"{self.imgPath}addFriend.png")
        self.addOriginImage = Image.open(f"{self.imgPath}addButton.png")
        self.changeOriginImage = Image.open(f"{self.imgPath}changeButton.png")
        self.sendOriginImage = Image.open(f"{self.imgPath}sendButton.png")
        self.verifyOriginImage = Image.open(f"{self.imgPath}verify.png")
        self.tOriginImage = Image.open(f"{self.imgPath}T.png")
        self.vOriginImage = Image.open(f"{self.imgPath}V.png")
        self.sendIconOriginImage = Image.open(f"{self.imgPath}sendIconButton.png")

        user32 = ctypes.windll.user32
        self.maxResulation = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

        self.current_res = current_res

        self.resize_screen()

    def resize_screen(self):
        self.winWidth = self.window.winfo_width()
        self.winHeight = self.window.winfo_height()
        # texts data
        self.titlesFontSize  = int(self.winWidth/25)
        self.appTextFontSize = int(self.winWidth/65)
        self.roomsNamesTextSize = int(self.winWidth/125)
        self.messagesFontSize = int(self.winWidth/140)
        self.participantsFontSize = int(self.winWidth/ 93)

        self.titleWidth = int(self.winWidth / 1.25)

        self.titleX = int(self.winWidth / 2) - int(self.titleWidth / 2)
        self.titleY = int(self.winHeight / 28)

        self.mainEntrysWidth = int(self.winWidth/3)

        #submit buttons
        proportion = 4
        newWidth = int(self.winWidth/proportion)

        # register button
        originalSize = self.registerOriginImage.size
        self.registerImage = self.registerOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.registerBTNImage = ImageTk.PhotoImage(self.registerImage)

        # login button
        originalSize = self.loginOriginImage.size
        self.loginImage = self.loginOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.loginBTNImage = ImageTk.PhotoImage(self.loginImage)

        # join button
        originalSize = self.joinOriginImage.size
        self.joinImage = self.joinOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.joinBTNImage = ImageTk.PhotoImage(self.joinImage)

        # create button
        originalSize = self.createOriginImage.size
        self.createImage = self.createOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.createBTNImage = ImageTk.PhotoImage(self.createImage)

        # add button
        originalSize = self.addOriginImage.size
        self.addImage = self.addOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.addBTNImage = ImageTk.PhotoImage(self.addImage)

        # change button
        originalSize = self.changeOriginImage.size
        self.changeImage = self.changeOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.changeBTNImage = ImageTk.PhotoImage(self.changeImage)

        # send button
        originalSize = self.sendOriginImage.size
        self.sendImage = self.sendOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.sendBTNImage = ImageTk.PhotoImage(self.sendImage)

        # verify button
        originalSize = self.verifyOriginImage.size
        self.verifyImage = self.verifyOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.verifyBTNImage = ImageTk.PhotoImage(self.verifyImage)

        # small submit buttons
        proportion = 5
        newWidth = int(self.winWidth/proportion)
        
        # small login button
        originalSize = self.loginOriginImage.size
        self.smallLoginImage = self.loginOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.smallLoginBTNImage = ImageTk.PhotoImage(self.smallLoginImage)

        # small register button
        originalSize = self.registerOriginImage.size
        self.smallRegisterImage = self.registerOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.smallRegisterBTNImage = ImageTk.PhotoImage(self.smallRegisterImage)

        # home buttons
        proportion = 12.8
        newWidth = int(self.winWidth/proportion)

        # home button
        originalSize = self.homeOriginImage.size
        self.homeImage = self.homeOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.homeBTNImage = ImageTk.PhotoImage(self.homeImage)

        # x button
        originalSize = self.XOriginImage.size
        self.XImage = self.XOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.XBTNImage = ImageTk.PhotoImage(self.XImage)

        # settings button
        originalSize = self.settingsOriginImage.size
        self.settingsImage = self.settingsOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.settingsBTNImage = ImageTk.PhotoImage(self.settingsImage)

        # dm button
        proportion = 17
        newWidth = int(self.winWidth/proportion)

        originalSize = self.dmOriginImage.size
        self.dmImage = self.dmOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.dmBTNImage = ImageTk.PhotoImage(self.dmImage)

        # move to join/create server screen buttons
        proportion = 8.5
        newWidth = int(self.winWidth/proportion)
        
        # join server button
        originalSize = self.joinServerOriginImage.size
        self.joinServerImage = self.joinServerOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.joinServerBTNImage = ImageTk.PhotoImage(self.joinServerImage)

        # create server button
        originalSize = self.newServerOriginImage.size
        self.newServerImage = self.newServerOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.newServerBTNImage = ImageTk.PhotoImage(self.newServerImage)

        # add friend button
        originalSize = self.addFriendOriginImage.size
        self.addFriendImage = self.addFriendOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.addFriendBTNImage = ImageTk.PhotoImage(self.addFriendImage)

        # rooms button
        proportion = 51
        newWidth = int(self.winHeight/proportion)

        # t button
        originalSize = self.tOriginImage.size
        self.tImage = self.tOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.tBTNImage = ImageTk.PhotoImage(self.tImage)

        #v button
        originalSize = self.vOriginImage.size
        self.vImage = self.vOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.vBTNImage = ImageTk.PhotoImage(self.vImage)

        # send icon button
        proportion = 34
        newWidth = int(self.winWidth/proportion)
        
        originalSize = self.sendIconOriginImage.size
        self.sendIconImage = self.sendIconOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.sendIconBTNImage = ImageTk.PhotoImage(self.sendIconImage)

        
    def _get_new_size(self, originalSize: tuple, newWidth: int):
        return (newWidth, int(originalSize[1] * newWidth/originalSize[0]))


    def setTitleLowestY(self, titleLowestY):
        self.titleLowestY = titleLowestY

    def setCurrentRes(self, res):
        self.currentRes = res


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
    return possiableRes
        

def register(email: str, password: str, username: str):
    if "|" in password or "&" in password:
        notify("register failed", "password is not valid")
        return
    if "|" in email or "&" in email:
        notify("register failed", "email is not valid")
        return
    if "|" in username or "&" in username:
        notify("register failed", "username is not valid")
        return
    
    data = handle_sends("register", username, email, password)
    successfully = data == "S"
        
    if successfully:
        notify("sent verification code", "check you email box for your verification code")
        loadScreen("email validation")

    else:
        notify("register failed", data)

def finish_register(verificationCode):
    global isUser
    data = handle_sends("finish register", verificationCode).split("|")
    successfully = data == "S"
    if successfully:
        isUser = True
        notify("registered successfully", "welcome to SCE")
        loadScreen("Home")


def login(email: str, password: str):
    global toRemember
    global isUser
    if "|" in password or "&" in password or "|" in email or "&" in email:
        notify("login failed","user params are inncorect")
        return

    successfully = handle_sends("login", email, password) == "S"

    if successfully:
        isUser=True
        loadScreen("Home")
        notify("login successfully", "welcome back")
        if toRemember:
            location = os.getcwd()+"/user.txt"
            encrypted_email = cipher.encrypt(email.encode())
            encrypted_password = cipher.encrypt(password.encode())
            data = [encrypted_email, encrypted_password]
            with open(location, "+ab") as encrypted_user_file:
                encrypted_user_file.write(encrypted_email+"\n".encode())
                encrypted_user_file.write(encrypted_password)
    else:
        notify("login failed","user params are inncorect")

def notify(title1, message1):
    try:
        # win11toast.ToastNotificationManager.create_toast_notifier("Python")
        # winToaster2 = InteractableWindowsToaster("SCE")
        newToast = ToastImageAndText1()
        newToast.SetBody(title1 + " | " + message1)
        # newToast.SetHeadline(title1)
        newToast.AddImage(ToastDisplayImage.fromPath(f"{os.getcwd()}/{screenManager.imgPath}sce_logo.png"))
        winToaster.show_toast(newToast)
        # newToast.AddInput(ToastInputTextBox("name", "your name", "Alon Garibi"))
        # newToast.AddAction(ToastButton("Submit", "submit"))
        # winToaster2.show_toast(newToast)
    except Exception as e:
        print(e)

    try:
       print("here!!!")
       msgbox.showinfo(title=title1, message=message1)
    except Exception as e:
        print(e)

    

def handle_sends(*arguments):
    toSend ="|".join(arguments) + "&"
    print(f"{toSend=}")
    encrypted_message = cipher.encrypt(toSend.encode())
    sock.send(encrypted_message)

    return decrypt_message()

def decrypt_message():
    return cipher.decrypt(waitToConfim()).decode()

def waitToConfim():
    message = sock.recv(9001)
    print(message)
    isFirst = message[:1].decode() == "`"
    isMiddle = message[-1:].decode() == "/"
    isEnd = message[-1:].decode() == "~"
    
    if isMiddle:
        if isFirst:
            message=message[1:]
        message = message[:-1]
        return message + waitToConfim()
    elif isEnd:
        if isFirst:
            message=message[1:]
        message = message[:-1]
        message = message
        return message
    else:
        notify("message", "didnt went clear")
        return "error"

def clearScreen():
    for widget in screenManager.window.winfo_children():
        widget.destroy()

def show_password(passwordEntry):
    if passwordEntry.cget('show') == '*':
        passwordEntry.config(show='')
    else:
        passwordEntry.config(show='*')

def loadServer(server):
    global current_server
    current_server = server
    loadScreen("server")
    # dataOfMessages = handle_sends("loadServer", server)

def temp(a):
    return a

def homeSceen():
    global toRemember
    dmY = int(screenManager.winHeight/6.5)
    serversY = int(screenManager.winHeight/3.5)
    lefSideX = int(screenManager.winWidth/50)
    dm = Button(screenManager.window, image=screenManager.dmBTNImage, bd=0, highlightthickness=0, activebackground=screenManager.backgroundColor, bg=screenManager.backgroundColor, command=lambda: loadScreen("dm"))
    dm.place(x=lefSideX, y=dmY)
    
    joinServer = Button(screenManager.window, image=screenManager.joinServerBTNImage, bd=0, highlightthickness=0, activebackground=screenManager.backgroundColor, bg=screenManager.backgroundColor, command=lambda: loadScreen("Join Server"))
    joinServer.place(x=screenManager.winWidth-screenManager.joinServerImage.size[0], y=screenManager.winHeight-screenManager.settingsImage.size[1] - screenManager.joinServerImage.size[1] - screenManager.winHeight/30)

    joinServer.update()

    servers = handle_sends("getServers").split("|")[0]
    servers = dict(json.loads(servers))
    serversButtons = []
    keys = list(servers.keys())
    first = True
    for server in keys:
        sb = Button(screenManager.window, text=servers[server], bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", int(screenManager.appTextFontSize * 0.8), "bold"), command=lambda a=server: loadServer(a))
        y = serversY
        if not first:
            y = serversButtons[-1].winfo_y() + serversButtons[-1].winfo_height() + int(screenManager.winHeight/100)
        first = False
        
        sb.place(x=lefSideX, y= y)
        sb.update()
        serversButtons.append(sb)
    screenManager.window.update()

def loginRegisterScreens(screen):
    global toRemember
    screenManager.window.update()

    emailY = int(screenManager.winHeight/3.5)
    labelX = int(screenManager.winWidth / 4)
    getOtherLabel = 0
    
    if screen == "Register":
        usernameY = emailY + int(screenManager.winHeight/7)
        passwordY = emailY + int(screenManager.winHeight/3.5)
        usernameEntry = Entry(screenManager.window, bg=screenManager.secondColor, font=("Airal", int(screenManager.appTextFontSize), "bold"))
        usernameEntry.place(x=labelX, y=usernameY, width=screenManager.mainEntrysWidth)
        usernameLabel = Label(screenManager.window, bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"),
                              text="Username:")
        usernameLabel.place(x=labelX, y=usernameY - int(screenManager.winHeight/17))
        
        getOtherLabel = Label(screenManager.window, bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", int(screenManager.appTextFontSize * 0.8), "bold"),
                              text="Already have account?")
        getOtherButton = Button(screenManager.window, image=screenManager.smallLoginBTNImage, bd=0, highlightthickness=0,
                                activebackground=screenManager.backgroundColor, bg=screenManager.backgroundColor, command=lambda: loadScreen("login"))
        submitWidth = screenManager.registerImage.size[0]
        submitX = int(screenManager.mainEntrysWidth/2) + labelX - (submitWidth)/2
        

    else:
        passwordY = emailY + int(screenManager.winHeight/7)

        getOtherLabel = Label(screenManager.window, bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", int(screenManager.appTextFontSize * 0.8), "bold"),
                              text="Still don't have account?")
        getOtherButton = Button(screenManager.window, image=screenManager.smallRegisterBTNImage, bd=0, highlightthickness=0,
                                activebackground=screenManager.backgroundColor, bg=screenManager.backgroundColor, command=lambda: loadScreen("Register"))
        
        submitWidth = screenManager.loginImage.size[0]
        submitX = int(screenManager.mainEntrysWidth/2) + labelX - (submitWidth)/2

    emailLabel = Label(screenManager.window, bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"), text="Email:")
    emailLabel.place(x=labelX, y=emailY - (screenManager.winHeight/17))

    emailEntry = Entry(screenManager.window, bg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"))
    emailEntry.place(x=labelX, y=emailY, width=screenManager.mainEntrysWidth)

    passwordLabel = Label(screenManager.window, bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"), text="Password:")
    passwordLabel.place(x=labelX, y=passwordY - int(screenManager.winHeight/17))

    passwordEntry = Entry(screenManager.window, bg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"), show="*")
    passwordEntry.place(x=labelX, y=passwordY, width=screenManager.mainEntrysWidth)

    showPasswordButton = Checkbutton(screenManager.window, text="show password", bg=screenManager.backgroundColor, fg=screenManager.secondColor,
                                     highlightthickness=0, activebackground=screenManager.backgroundColor, bd=0,
                                     font=("Airal", int(0.7 * screenManager.appTextFontSize), "bold"), command= lambda: show_password(passwordEntry))
    showPasswordButton.place(x=labelX, y=passwordY + int(screenManager.winHeight/13))
    screenManager.window.update()

    if screen == "Register":
        submitY = showPasswordButton.winfo_y() + showPasswordButton.winfo_height() + int(screenManager.winHeight/40)

        submitButton = Button(screenManager.window, image=screenManager.registerBTNImage, bd=0, highlightthickness=0,
                activebackground=screenManager.backgroundColor, bg=screenManager.backgroundColor, command= lambda: register(emailEntry.get(), passwordEntry.get(), usernameEntry.get()))
        submitButton.place(x=submitX, y=submitY)
    else:
        toRemember = False
        remmeberMeButton = Checkbutton(screenManager.window, text="remmeber me", bg=screenManager.backgroundColor, fg=screenManager.secondColor, highlightthickness=0, activebackground=screenManager.backgroundColor, bd=0,
                                       font=("Airal", int(0.7 * screenManager.appTextFontSize), "bold"), command=toggleToRemember)

        remmeberMeButton.place(x=labelX, y=showPasswordButton.winfo_y() + showPasswordButton.winfo_height() + int(screenManager.winHeight/40))
    
        screenManager.window.update()
        
        submitY = remmeberMeButton.winfo_y() + remmeberMeButton.winfo_height() + int(screenManager.winHeight/40)

        submitButton = Button(screenManager.window, image=screenManager.loginBTNImage, bd=0, highlightthickness=0, activebackground=screenManager.backgroundColor,
                              bg=screenManager.backgroundColor, command= lambda: login(emailEntry.get(), passwordEntry.get()))
        submitButton.place(x=submitX, y=submitY)
        screenManager.window.update()

        width = int(screenManager.winWidth/5)
        forgotPassword = Button(screenManager.window, text="Forgot Password", bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"), command= lambda: loadScreen("forgot password"))
        forgotPassword.place(x = submitButton.winfo_x() + int(submitButton.winfo_width()/2) - int(width/2), y= submitButton.winfo_y() + submitButton.winfo_height() + int(screenManager.winHeight/20), width=width)

    gobx = submitX + int(screenManager.winWidth / 2.5)
    getOtherLabel.place(x= gobx, y=(submitY - (screenManager.winHeight/24)))
    getOtherButton.place(x=gobx - int(screenManager.winWidth/60), y=submitY)
    screenManager.window.update()

    if screen == "login":
        location = os.getcwd()+"/user.txt"
        if os.path.getsize(location) > 0:
            with open(location, 'rb') as encrypted_user_file:
                lines = encrypted_user_file.readlines()
                encryptedEmail = lines[0][:-1]
                encryptedPassword = lines[1]
                login(cipher.decrypt(encryptedEmail).decode(), cipher.decrypt(encryptedPassword).decode())

def toggleToRemember():
    global toRemember
    toRemember = not toRemember

def settingsScreen():
    global resulations, isUser

    LabelX = int(screenManager.winWidth/10)
    resulationLabelY = int(screenManager.winHeight/5.5)
    resulationLabel = Label(screenManager.window, bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"), text="Resulation:")
    resulationLabel.place(x=LabelX, y=resulationLabelY)
    resulationButtons = []

    for i, resulation in enumerate(resulations):
        rb = Button(screenManager.window, text=resulations[i], bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", int(screenManager.appTextFontSize * 0.9), "bold"), command=lambda a=resulation: change_screen_resulation("settings", a))
        rb.pack(anchor=N)
        rb.update()
        bh = rb.winfo_height()
        max = ((resulationLabelY + resulationLabel.winfo_height() + int(screenManager.winHeight/50)) + (int(screenManager.winHeight/50) + rb.winfo_height()) * i)
        rb.place(x=LabelX + int (screenManager.winWidth/ 50), y = max)
        rb.update()
        resulationButtons.append(rb)
    if isUser:
        logout = Button(screenManager.window, text="Logout", bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"), command=logout_user)
        logout.place(x=LabelX, y= max + rb.winfo_height() + int(screenManager.winHeight/25))

        screenManager.window.update()
        chnageUser = Button(screenManager.window, text="change user data", bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"), command = lambda: loadScreen("change user"))
        chnageUser.place(x=LabelX, y = logout.winfo_y() + logout.winfo_height() + int(screenManager.winHeight/25))

    # resulation.place(x=0, y=0)
    
def logout_user():
    global isUser, homeButton
    isUser = False
    successfully = handle_sends("logout").split("|")[0] == "S"
    if successfully:
        location = os.getcwd()+"/user.txt"
        with open(location,'r+') as file:
            file.truncate(0)
        loadScreen("login")
    else:
        print("error")

def change_screen_resulation(screen, res):
    screenManager.setCurrentRes(res)

    if res == "fullscreen":
        screenManager.window.attributes('-fullscreen', True)       
    else:
        screenManager.window.attributes('-fullscreen', False)       
        screenManager.window.geometry(res)

    screenManager.window.update()
    loadScreen(screen)

def loadScreen(screen):
    clearScreen()



    screenManager.window.update()

    screenManager.resize_screen()

    loadBasicScreen(screenManager.window, screen)

    screenManager.window.update()

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
            server_screen()
        case "forgot password":
            forgotPasswordScreen()
        case _:
            defualt_screen(screen)

def forgotPasswordScreen():
    emailY = int(screenManager.winHeight/3.75)

    labelsX = int((screenManager.winWidth - screenManager.mainEntrysWidth)/2)
    
    emailEntry = Entry(screenManager.window, bg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"))
    emailEntry.place(x= labelsX, y=emailY, width=screenManager.mainEntrysWidth)
    emailEntry.update()
    emailLabel = Label(screenManager.window, bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"), text="Email:")
    emailLabel.place(x= labelsX, y=emailEntry.winfo_y() - (screenManager.winHeight/20))
    # emailLabel.update()

    sendY = emailEntry.winfo_y() + emailEntry.winfo_height() + int(screenManager.winHeight/25)
    sendButton = Button(screenManager.window, image=screenManager.sendBTNImage, bd=0, highlightthickness=0,
                activebackground=screenManager.backgroundColor, bg=screenManager.backgroundColor, command=lambda: sendForgotPasswordEmail(emailEntry.get()))
    sendButton.place(x= int((screenManager.winWidth - screenManager.sendImage.size[0])/2), y= sendY)
    
    sendButton.update()

    resetCodeY = sendButton.winfo_y() + sendButton.winfo_height() + int(screenManager.winHeight/15)

    resetCodeLabel = Label(screenManager.window, bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"),
                            text="Verification Code:")
    resetCodeLabel.place(x=labelsX, y=resetCodeY)

    resetCodeLabel.update()

    resetCodeEntry = Entry(screenManager.window, bg=screenManager.secondColor, font=("Airal", int(screenManager.appTextFontSize), "bold"))
    resetCodeEntry.place(x=labelsX, y=resetCodeLabel.winfo_y() + resetCodeLabel.winfo_height() + int(screenManager.winHeight/100), width=screenManager.mainEntrysWidth)

    resetCodeEntry.update()

    submitButton = Button(screenManager.window, image=screenManager.verifyBTNImage, bd=0, highlightthickness=0,
                activebackground=screenManager.backgroundColor, bg=screenManager.backgroundColor, command=lambda: verifyEmail(resetCodeEntry.get()))
    submitButton.place(x=sendButton.winfo_x(), y=resetCodeEntry.winfo_y() + resetCodeEntry.winfo_height() + int(screenManager.winHeight/25))

def sendForgotPasswordEmail(email):
    d = handle_sends("send verification", email)
    s = d == "S"
    if s:
        notify("email sent", "verficiation sent successfully")
    else:
        notify("email went wrong", "email went wrong, try again late")

def verifyEmail(verficationCode):

    data = handle_sends("verify email", verficationCode).split('|')
    successfully = data[0] == "S"

    if successfully:
        loadScreen("reset password")
    else:
        notify("wrong code", "your verification code is wrong, please check again")

class server_screen():
    def __init__(self):
        self.isMessages = False
        self.serverScreen()

    def serverScreen(self):
        self.current_server = current_server
        # clearScreen()
        self.frameYPos = max(screenManager.titleLowestY, screenManager.homeImage.size[1])
        # frame.pack(side=LEFT, fill=Y, expand=True)
        self.width = screenManager.winWidth - screenManager.settingsImage.size[0]
        self.height = screenManager.winHeight - self.frameYPos
        self.roomsWidth = self.width * 0.15
        self.roomsX = 0
        self.loadRoomsCanvas()

        self.messagesWidth = self.width * 0.7
        self.messagesX = self.roomsWidth
        self.loadMessagesCanvas()

        self.participantsWidth = self.width - self.roomsWidth - self.messagesWidth
        print(self.participantsWidth/self.width)
        self.participantsX = self.messagesWidth + self.roomsWidth
        self.loadParticipantsCanvas()

    def loadRoomsCanvas(self):
        self.roomsFrame = Frame(screenManager.window)

        self.roomsFrame.place(x=self.roomsX, y=self.frameYPos, width=self.roomsWidth, height=self.height)
        self.roomsFrame.update()
        
        self.roomsCanvas = Canvas(self.roomsFrame, bg=screenManager.thirdColor, bd=0, highlightthickness=0, highlightcolor=screenManager.backgroundColor, width=self.roomsFrame.winfo_width(),height=self.roomsFrame.winfo_height())
        self.roomsCanvas.pack(side=LEFT, expand=True, fill=BOTH)
        
        self.roomsScrollBar = ttk.Scrollbar(self.roomsCanvas, orient=VERTICAL, command=self.roomsCanvas.yview, cursor= "double_arrow")
        self.roomsScrollBar.pack(side=RIGHT, fill=Y)

        self.roomsCanvas.configure(yscrollcommand=self.roomsScrollBar.set)

        self.roomsCanvas.bind("<Configure>", lambda e: self.roomsCanvas.configure(scrollregion=self.roomsCanvas.bbox("all")))
        
        self.secRoomsFrame = Frame(self.roomsCanvas, bg=screenManager.thirdColor)
        self.roomsCanvas.create_window((0, 0), window=self.secRoomsFrame, anchor=NW)

        # current_room = "mainRoom"

        self.rooms = handle_sends("get rooms", self.current_server)
        self.rooms = self.rooms.split("|")
        print(self.rooms)
        isSuccessful = self.rooms[0] == "S"
        if not isSuccessful:
            loadScreen("home")
            return
        self.textRooms = self.rooms[1]
        self.voiceRooms =self.rooms[2]
        self.textRooms = self.textRooms.split("*")
        self.voiceRooms = self.voiceRooms.split("*")
        if self.textRooms == [""]:
            self.textRooms.clear()
        if self.voiceRooms == [""]:
            self.voiceRooms.clear()
        # rooms = [(''.join(random.choices(string.ascii_lowercase, k=12))) for i in range(250)]
        self.lastButtonY = 0
        # longest = 0
        if self.textRooms:
            self.textRoomsLabel = Label(self.roomsCanvas, text = "Text Rooms:", bg=screenManager.thirdColor, highlightthickness=0, font=("Airal", screenManager.roomsNamesTextSize, "bold"), fg=screenManager.secondColor)
            self.textRoomsLabel.place(x=0, y=0)
            self.textRoomsLabel.update()
            
            self.lastButtonY = self.textRoomsLabel.winfo_y() + self.textRoomsLabel.winfo_height()

            for room in self.textRooms:   
                if room != "":
                    a = Button(self.roomsCanvas, text=" "+room, image=screenManager.tBTNImage, compound=LEFT, bg=screenManager.thirdColor, highlightthickness=0, font=("Airal", screenManager.roomsNamesTextSize, "bold"), fg=screenManager.secondColor, command=lambda a = room: self.loadTextRoom(a))
                    a.place(x=0, y = int(screenManager.winHeight/70) + self.lastButtonY)
                    a.update()
                    self.lastButtonY = a.winfo_y() + a.winfo_height()
                    # longest = max(longest, a.winfo_width())
                    # longest = min(longest, roomsWidth)

        if self.voiceRooms:
            self.voiceRoomsLabel = Label(self.roomsCanvas, text = "Voice Rooms:", bg=screenManager.thirdColor, highlightthickness=0, font=("Airal", screenManager.roomsNamesTextSize, "bold"), fg=screenManager.secondColor)
            self.voiceRoomsLabel.place(x=0, y=self.lastButtonY + screenManager.winHeight/70)
            self.voiceRoomsLabel.update()
            self.lastButtonY = self.voiceRoomsLabel.winfo_y() + self.voiceRoomsLabel.winfo_height()
            self.voiceRoomsLabel.update()

            for room in self.voiceRooms:
                if room != "":
                    a = Button(self.roomsCanvas, text=" "+room, image=screenManager.vBTNImage, compound=LEFT, bg=screenManager.thirdColor, highlightthickness=0, font=("Airal", screenManager.roomsNamesTextSize, "bold"), fg=screenManager.secondColor)
                    a.place(x=0, y = int(screenManager.winHeight/70) + self.lastButtonY)
                    a.update()
                    self.lastButtonY = a.winfo_y() + a.winfo_height()
                    # longest = max(longest, a.winfo_width())
                    # longest = min(longest, roomsWidth)

        # roomsFrame.place(x=0, y=frameYPos, width=longest + roomsScrollBar.winfo_width(), height=height)
        # roomsFrame.update()
        # roomsScrollBar.pack(side=RIGHT, fill=Y)

    def loadMessagesCanvas(self):
        self.messagesFrame = Frame(screenManager.window)

        self.messagesFrame.place(x=self.messagesX, y=self.frameYPos, width=self.messagesWidth, height=self.height)
        self.messagesFrame.update()
        
        self.messagesCanvas = Canvas(self.messagesFrame, bg=screenManager.thirdColor, bd=0, highlightthickness=0, highlightcolor=screenManager.backgroundColor, width=self.messagesFrame.winfo_width(),height=self.messagesFrame.winfo_height())
        self.messagesCanvas.pack(side=LEFT, expand=True, fill=BOTH)
        
        self.messagesScrollbar = ttk.Scrollbar(self.messagesCanvas, orient=VERTICAL, command=self.messagesCanvas.yview, cursor= "double_arrow")
        self.messagesScrollbar.pack(side=RIGHT, fill=Y)

        self.messagesCanvas.configure(yscrollcommand=self.messagesScrollbar.set)
        self.messagesCanvas.bind("<Configure>", lambda e: self.roomsCanvas.configure(scrollregion=self.messagesCanvas.bbox("all")))
        
        self.secMessagesFrame = Frame(self.messagesCanvas, bg=screenManager.thirdColor)
        self.messagesCanvas.create_window((0, 0), window=self.secMessagesFrame, anchor=NW)

        screenManager.window.update()

    def load_messages(self):
        if self.isMessages:
            self.secMessagesFrame.update()
            lastButtonY = 0
            labels = []
            buttons = []
            for message in self.messages:
                message = json.loads(message)
                messageData = message["data"]
                author = json.loads(message["author"])
                isMessageIsMy = author["isMy"]
                messageAuthor = author["username"]
                coMessageData = messageData
                maxLength = 100
                lines = [coMessageData]
                while len(lines[0]) > maxLength:
                    if " " in lines[0][:maxLength]:
                        si = lines[0].rfind(" ",0 ,maxLength)
                        lines.append(lines[0][:si])
                        print(f"{lines[0][:si]=}")
                        lines[0] = lines[0][si+1:]
                    else:
                        lines.append(lines[0][:maxLength])
                        lines[0] = lines[0][maxLength+1:]
                    if lines[-1][0] == " ":
                        lines[-1][1:]
                    elif lines[-1][-1] == " ":
                        lines[-1][:-1]
                lines.reverse()
                lines="\n".join(lines)
                l = Label(self.secMessagesFrame, text= messageAuthor+":", bd=0, highlightthickness=0, bg=screenManager.thirdColor, font=("Arial", screenManager.messagesFontSize, "bold"), fg = screenManager.secondColor)
                l.grid(row=lastButtonY, column=0, sticky=W)
                labels.append(l)
                b = Button(self.secMessagesFrame, text= lines, bd=0, justify=LEFT, highlightthickness=0, bg=screenManager.thirdColor, font=("Arial", screenManager.messagesFontSize, "bold"), fg = screenManager.secondColor, compound="c", width= maxLength, anchor=W, command=lambda: print("yay"), disabledforeground=screenManager.secondColor)
                if not isMessageIsMy:
                    b.configure(state=DISABLED)
                b.grid(row=lastButtonY + 1, column=10, sticky=W)
                buttons.append(b)
                space = Label(self.secMessagesFrame, text="", bd=0, bg=screenManager.thirdColor)
                space.grid(row=lastButtonY+2, column=0, sticky=W)
                lastButtonY += 3
                self.secMessagesFrame.update()
                # if b.winfo_width() > self.messagesWidth:
                #     i = 1
                #     lines = [messageData]
                #     s_d = messageData.split(" ")
                #     lines = 
                #     while b.winfo_width() > self.messagesWidth:
        screenManager.window.update()

        
    def loadParticipantsCanvas(self):
        self.participantsFrame = Frame(screenManager.window)

        self.participantsFrame.place(x=self.participantsX, y=self.frameYPos, width=self.participantsWidth, height=self.height)
        self.participantsFrame.update()
        
        self.participantsCanvas = Canvas(self.participantsFrame, bg=screenManager.thirdColor, bd=0, highlightthickness=0, highlightcolor=screenManager.backgroundColor, width=self.participantsFrame.winfo_width(),height=self.participantsFrame.winfo_height())
        self.participantsCanvas.pack(side=LEFT, expand=True, fill=BOTH)
        
        self.participantsScrollBar = ttk.Scrollbar(self.participantsCanvas, orient=VERTICAL, command=self.participantsCanvas.yview, cursor= "double_arrow")
        self.participantsScrollBar.pack(side=RIGHT, fill=Y)

        self.participantsCanvas.configure(yscrollcommand=self.participantsScrollBar.set)
        self.participantsCanvas.bind("<Configure>", lambda e: self.participantsCanvas.configure(scrollregion=self.participantsCanvas.bbox("all")))
        
        self.secParticipantsFrame = Frame(self.participantsCanvas, bg=screenManager.thirdColor)
        self.participantsCanvas.create_window((0, 0), window=self.secParticipantsFrame, anchor=N)
        data = handle_sends("get participants").split("|")
        print(f"{data=}")
        if data[0] == "S":
            self.participants = (data[1].split("*"))
            self.isAdmin = bool(data[2])
            self.isOwner = bool(data[3])
        for i, participant in enumerate(self.participants):
            label = Label(self.secParticipantsFrame, bg=screenManager.thirdColor, fg=screenManager.secondColor, font=("Airal", screenManager.participantsFontSize, "bold"), text=participant)
            label.grid(row=i, column=0, sticky=W)
        
    def loadTextRoom(self, room):
        self.current_room = room
        data = handle_sends("load room", room).split("|")
        success = data[0] == "S"
        if success:
            self.messages = data[1].split("*")
            print(self.messages)
            self.isMessages = True
            self.load_messages()
            self.messageEntry = Entry(screenManager.window, bg=screenManager.secondColor, font=("Airal", int(screenManager.messagesFontSize), "bold"))
            self.messageEntry.pack()
            self.messageEntry.update()
            self.messageEntry.place(x=self.messagesX, y=screenManager.winHeight-self.messageEntry.winfo_height(), width=self.messagesFrame.winfo_width()-1.5*self.messagesScrollbar.winfo_width()-screenManager.sendIconImage.size[0])
            self.messageEntry.update()
            screenManager.window.update()
            sendButton = Button(screenManager.window, image=screenManager.sendIconBTNImage, bg=screenManager.thirdColor, command=lambda: self.send_message(self.messageEntry.get()))
            sendButton.place(x=self.messagesFrame.winfo_x() + self.messageEntry.winfo_width(), y = screenManager.winHeight-screenManager.sendIconImage.size[1])
            self.messagesCanvas.update()

        else:
            notify("load room error", data[1])

    def send_message(self, message):
        success = handle_sends("add message", message) == "S"
        self.loadTextRoom(self.current_room)

def loadBasicScreen(window2, screen):

    xButton = Button(window2, image=screenManager.XBTNImage, bd=0, highlightthickness=0, activebackground=screenManager.backgroundColor, bg=screenManager.backgroundColor, command=close, cursor= "X_cursor")
    xButton.pack(anchor=NE)
    
    titleLabel = Label(window2, bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", screenManager.titlesFontSize, "bold"), text=screen.upper())
    titleLabel.place(x=screenManager.titleX, y=int(screenManager.winHeight/29), width=screenManager.titleWidth)
    titleLabel.update()
    screenManager.setTitleLowestY(titleLabel.winfo_y() + titleLabel.winfo_height())

    homeButton = Button(window2, image=screenManager.homeBTNImage, bd=0, highlightthickness=0, activebackground=screenManager.backgroundColor, bg=screenManager.backgroundColor, command=lambda: loadScreen("Home"))
    if not isUser:
        homeButton.config(command=lambda: loadScreen("login"))        
    homeButton.place(x=0, y=0)
    
    if screen != "settings":
        settings = Button(window2, image=screenManager.settingsBTNImage, bd=0, highlightthickness=0, activebackground=screenManager.backgroundColor, bg=screenManager.backgroundColor, command=lambda: loadScreen("settings"))
        settings.place(x=screenManager.winWidth-screenManager.settingsImage.size[0], y=screenManager.winHeight-screenManager.settingsImage.size[1])
        settings.update()

    

def changeUserDataScreen():
    usernameY = int(1.7 * screenManager.winHeight / 4)
    passwordY = usernameY + int(screenManager.winHeight/7)
    labelX = int(screenManager.winWidth / 4)

    submitX = screenManager.mainEntrysWidth - 100
    submitY = passwordY + int(screenManager.winWidth/12)

    changeUsernameLabelText = "New Username:"
    changePasswordLabelText = "New Password:"
    explainText = "not all required".title()
    explainLabel = Label(screenManager.window, bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("assitant", screenManager.appTextFontSize, "bold"), text=explainText)
    explainLabel.place(x=0, y=usernameY - int(screenManager.winHeight/7), width=screenManager.winWidth)

    changeUsernameLabel = Label(screenManager.window, bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"),
                         text=changeUsernameLabelText)
    changeUsernameLabel.place(x=labelX, y=usernameY - int(screenManager.winHeight/17))
    
    changeUsernameEntry = Entry(screenManager.window, bg=screenManager.secondColor, font=("Airal", int(screenManager.appTextFontSize), "bold"))
    changeUsernameEntry.place(x=labelX, y=usernameY, width=screenManager.mainEntrysWidth)

    ChangePasswordLabel = Label(screenManager.window, bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"), text=changePasswordLabelText)
    ChangePasswordLabel.place(x=labelX, y=passwordY - int(screenManager.winHeight/17))
    
    ChangePasswordEntry = Entry(screenManager.window, bg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"), show="*")
    ChangePasswordEntry.place(x=labelX, y=passwordY, width=screenManager.mainEntrysWidth)

    showPasswordButton = Checkbutton(screenManager.window, text="show password", bg=screenManager.backgroundColor, fg=screenManager.secondColor,
                                     highlightthickness=0, activebackground=screenManager.backgroundColor, bd=0,
                                     font=("Airal", int(0.7 * screenManager.appTextFontSize), "bold"), command=lambda: show_password(ChangePasswordEntry))
    showPasswordButton.place(x=labelX, y=passwordY + int(screenManager.winHeight/13))

    submitButton = Button(screenManager.window, image=screenManager.changeBTNImage, bd=0, highlightthickness=0,
                              activebackground=screenManager.backgroundColor, bg=screenManager.backgroundColor, command=lambda: manage_update(changeUsernameEntry.get(), ChangePasswordEntry.get()))
    submitButton.place(x=submitX, y=submitY)

def manage_update(username, password):
    changed = False
    if isUser:
        if username != "":
            if "|" in password or "&" in password:
                notify("password didnt changed", "password is not valid")
                changed = False
                return
        
            if "|" in username or "&" in username:
                data = handle_sends("change username", username).split('|')
                changed = data[0] == "S"
                if changed:
                    notify("username changed", "username changed successfully")
                else:
                    notify("username didnt changed", "username changed failed")
        if password != "":
            if "|" in password or "&" in password:
                notify("password didnt changed", "password is not valid")
                changed = False
                return

            else:
                data = handle_sends("change password", password).split("|")
                changed = data[0] == "S"
                if changed:
                    notify("password changed", "password changed successfully")
                else:
                    data = " ".join(data)
                    notify("password didnt changed", data)
        if changed:
            loadScreen("Home")

    
def DMScreen():
    friendsY = int(screenManager.winHeight/5)
    lefSideX = int(screenManager.winWidth/50)
        
    addFriend = Button(screenManager.window, image=screenManager.addFriendBTNImage, bd=0, highlightthickness=0, activebackground=screenManager.backgroundColor, bg=screenManager.backgroundColor, command=lambda: loadScreen("Add friend"))
    addFriend.place(x=screenManager.winWidth-screenManager.joinServerImage.size[0], y=screenManager.winHeight-screenManager.settingsImage.size[1] - screenManager.joinServerImage.size[1] - screenManager.winHeight/30)

    friends = handle_sends("getFriends")
    friends = dict(json.loads(friends))
    friendsButtons = []
    keys = list(friends.keys())
    for i, frined in enumerate(keys):
        sb = Button(screenManager.window, text=friends[frined], bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", int(screenManager.appTextFontSize * 0.8), "bold"), command=lambda a=frined: loadDMChat(a))
        sb.pack(anchor=N)
        sb.update()
        sb.place(x=lefSideX, y=(friendsY + (int(screenManager.winHeight/50) + sb.winfo_height()) * i))
        screenManager.window.update()
        friendsButtons.append(sb)

def loadDMChat(id):
    pass

def createServerScreen():

    nameY = int(1.7 * screenManager.winHeight / 4)
    isGhostRoomsY = nameY + int(screenManager.winHeight/7)
    labelX = int(screenManager.winWidth / 4)
    ghostRooms = False

    submitX = screenManager.mainEntrysWidth - 100
    submitY = isGhostRoomsY + int(screenManager.winWidth/20)

    nameLabel = Label(screenManager.window, bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"), text="Server Name:")
    nameLabel.place(x=labelX, y=nameY - (screenManager.winHeight/17))

    nameEntry = Entry(screenManager.window, bg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"))
    nameEntry.place(x=labelX, y=nameY, width=screenManager.mainEntrysWidth)

    ghostRoomButton = Checkbutton(screenManager.window, text="ghost room", bg=screenManager.backgroundColor, fg=screenManager.secondColor,
                                     highlightthickness=0, activebackground=screenManager.backgroundColor, bd=0, font=("Airal", int(0.7 * screenManager.appTextFontSize), "bold"), variable=ghostRooms, offvalue=False, onvalue=True)
    ghostRoomButton.place(x=labelX, y=nameY + int(screenManager.winHeight/13))
    screenManager.window.update()

    submitButton = Button(screenManager.window, image=screenManager.createBTNImage, bd=0, highlightthickness=0,
                              activebackground=screenManager.backgroundColor, bg=screenManager.backgroundColor, command=lambda: createServer(nameEntry.get(), ghostRooms))

    submitButton.place(x=int(screenManager.winWidth/2) - int(screenManager.joinImage.size[0]/2), y=submitY)

def createServer(name, isGhost):
    data = handle_sends("createServer", name, str(isGhost))
    successfully = data != "later"
    if successfully:
        notify("create server", "server created successfully")
        loadScreen("Home")
    


def defualt_screen(screen):    

    labelX = int(screenManager.winWidth / 4)
    idEntryWidth = int(screenManager.winWidth / 4)
    labelY = int(1.2 * screenManager.winHeight / 4)
    submitY = labelY + int(screenManager.winHeight / 7)
    
    match screen:
        case "Add friend":
            labelText = "Friend Email:"
            submitButtonImage = screenManager.addBTNImage
            submitX = int(screenManager.winWidth/2) - int(screenManager.addImage.size[0]/2)
        case "Join Server":
            labelText = "Server ID:"
            submitButtonImage = screenManager.joinBTNImage
            submitX = int(screenManager.winWidth/2) - int(screenManager.joinImage.size[0]/2)
        case "email validation":
            labelText = "Verify Code:"
            submitButtonImage = screenManager.registerBTNImage
            submitX = int(screenManager.winWidth/2) - int(screenManager.addImage.size[0]/2)
        case "reset password":
            labelText = "New Password:"
            submitButtonImage = screenManager.changeBTNImage
            submitX = int(screenManager.winWidth/2) - int(screenManager.changeImage.size[0]/2)
        case _:
            return

    label = Label(screenManager.window, bg=screenManager.backgroundColor, fg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"), text=labelText)
    label.place(x=labelX, y=labelY)

    label.update()
    len = idEntryWidth + int(label.winfo_width())
    labelX = int(screenManager.winWidth/2)-int(len/2)

    label.place(x=labelX, y=labelY)
    label.update()
    entry = Entry(screenManager.window, bg=screenManager.secondColor, font=("Airal", screenManager.appTextFontSize, "bold"))
    entry.place(x=labelX + label.winfo_width(), y=labelY, width=idEntryWidth)
    entry.update()


    submitButton = Button(screenManager.window, image=submitButtonImage, bd=0, highlightthickness=0,
                              activebackground=screenManager.backgroundColor, bg=screenManager.backgroundColor, command=lambda: addFriend(entry.get()))
    match screen:
        case "Join Server":
            newButton =  Button(screenManager.window, image=screenManager.newServerBTNImage, bd=0, highlightthickness=0,
                                    activebackground=screenManager.backgroundColor, bg=screenManager.backgroundColor, command=lambda: loadScreen("Create Server"))
            newButton.place(x=0, y= screenManager.winHeight - screenManager.newServerImage.size[1])
            submitButton.config(command=lambda: joinServer(entry.get()))
        case "email validation":
            submitButton.config(command=lambda: finish_register(entry.get()))
            try:
                newButton =  Button(screenManager.window, text= "Back", bd=0, highlightthickness=0,
                                        activebackground=screenManager.backgroundColor, bg=screenManager.backgroundColor, command=lambda: loadScreen("Create Server"))
                newButton.pack(anchor=CENTER)
            except Exception as e:
                print(e)
            newButton.update()
        case "reset password":
            submitButton.config(command=lambda: resetPassword(entry.get()))
    submitButton.place(x=submitX, y=submitY)
    screenManager.window.update()
def resetPassword(password):
    if password != "":
            if "|" in password or "&" in password:
                print(password)
                notify("password didnt changed", "password is not valid")
                changed = False
                return

            else:
                data = handle_sends("reset password", password)
                changed = data == "S"
                if changed:
                    notify("password changed", "password changed successfully")
                else:
                    notify("password didnt changed", data)

def addFriend(a):
    pass
    
def joinServer(id: Entry):
    data = handle_sends("joinServer", id)
    successfully = data == "S"
    if successfully:
        notify("joined server", "joined successfully to server")
        loadScreen("Home")
    else:
        notify("joined failed", data)


def close():
    # handle_client("close")
    screenManager.window.destroy()

def main():
    global sock, resulations, isUser, screenManager

    isUser = False
    sock = socket.socket()
    sock.connect((ip, port))


    window.update()
    current_res = "fullscreen"
    screenManager = screen_manager(window, current_res)
    
    screenManager.window.resizable(False, False)
    screenManager.window['background'] = screenManager.backgroundColor

    screenManager.window.update()

    change_screen_resulation("login", "fullscreen")

    resulations = getResulations(screenManager.maxResulation)

    # graphic_t = Thread(target=loadScreen, args=("Register",))
    # graphic_t.start()

    window.mainloop()
    # graphic_t.join()

if __name__ == '__main__':
    main()