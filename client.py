from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import socket, json
from PIL import Image, ImageTk
from threading import Thread
from cryptography.fernet import Fernet
import ctypes, os
# from windows_toasts import WindowsToaster, ToastDisplayImage, ToastImageAndText1
import random, string, math, pyperclip, cv2
import numpy as np

curPath = os.getcwd()

print(curPath)
# encrypt
fkey = open(curPath+"/key.txt", "rb")
key = fkey.read()
cipher = Fernet(key)
fkey.close()

# notification
# winToaster = WindowsToaster("SCE")
msgbox = messagebox

# graphic
global resulations, screen_manager
window = Tk()

global isUser, current_server, toRemember

#connection
ip = "127.0.0.1"
port = 3339
global sock

# cam_port = 1000
# cam_sock.connect((ip, port))
# define a video capture object


class ScreenManager():
    def __init__(self, window: Tk, current_res: str):
        """
        This function initializes various variables and loads images for a GUI window.
        
        :param window: The Tkinter window object that the code is running in
        :type window: Tk
        :param current_res: The current screen resolution of the user's device
        :type current_res: str
        """
        
        self.max_camera_width = 250
        self.max_camera_height = 250

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
        self.shareOriginImage = Image.open(f"{self.imgPath}shareButton.png")
        self.cameraOriginImage = Image.open(f"{self.imgPath}camera.png")
        self.microphoneOriginImage = Image.open(f"{self.imgPath}microphone.png")

        user32 = ctypes.windll.user32
        self.maxResulation = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

        self.current_res = current_res

        self.resize_screen()
    
    # def should_resize(self):
    #     return not (self.window.winfo_width() == self.winWidth and self.window.winfo_height() == self.winHeight)
    
    def resize_screen(self):
        """
        This function resizes various images and adjusts font sizes based on the size of the window in a
        GUI application.
        """
        self.window.update()
        self.winWidth = self.window.winfo_width()
        self.winHeight = self.window.winfo_height()
        print(f"{self.winWidth=} {self.winHeight=}")
        # texts data
        self.titlesFontSize  = int(self.winWidth/25)
        self.appTextFontSize = int(self.winWidth/65)
        self.roomsNamesTextSize = int(self.winWidth/125)
        self.messagesFontSize = int(self.winWidth/175)
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

        #share button
        originalSize = self.shareOriginImage.size
        self.shareImage = self.shareOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.shareBTNImage = ImageTk.PhotoImage(self.shareImage)

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

        #voices icons
        proportion = 17
        newWidth = int(self.winWidth/proportion)
    
        originalSize = self.cameraOriginImage.size
        self.cameraImage = self.cameraOriginImage.resize(self._get_new_size(originalSize, newWidth))
        self.cameraBTNImage = ImageTk.PhotoImage(self.cameraImage)

        originalSize = self.microphoneOriginImage.size
        self.microphoneImage = self.microphoneOriginImage.resize((self._get_new_size(originalSize, newWidth)))
        self.microphoneBTNImage = ImageTk.PhotoImage(self.microphoneImage)

        
    def _get_new_size(self, originalSize: tuple, newWidth: int):
        """
        This function calculates the new height of an image based on its original size and a new width.
        
        :param originalSize: A tuple containing the original size of an image in the format (width,
        height)
        :type originalSize: tuple
        :param newWidth: The desired new width of the image
        :type newWidth: int
        :return: A tuple containing the new width and height of an image after resizing. The new width
        is specified by the `newWidth` parameter, while the new height is calculated based on the
        original size of the image (`originalSize`) and the ratio of the new width to the original
        width.
        """
        return (newWidth, int(originalSize[1] * newWidth/originalSize[0]))


    def setTitleLowestY(self, titleLowestY: int):
        """
        This function sets the value of the "titleLowestY" attribute in an object to the input integer
        value.
        
        :param titleLowestY: titleLowestY is a parameter of type integer that represents the lowest
        Y-coordinate of the title in a graphical user interface. This method sets the value of the
        instance variable "titleLowestY" to the value passed as the parameter
        :type titleLowestY: int
        """
        self.titleLowestY = titleLowestY

    def setCurrentRes(self, res: str):
        """
        This function sets the current resolution to a given value.
        
        :param res: The parameter "res" is a string that represents the current resolution. It is being
        passed as an argument to the method "setCurrentRes" which sets the value of the instance
        variable "currentRes" to the value of "res"
        :type res: str
        """
        self.currentRes = res


def getResulations(maxResulation: str):
    """
    The function takes a maximum resolution as input and returns a list of possible resolutions based on
    a predefined dictionary.
    
    :param maxResulation: The parameter maxResulation is a string representing the maximum resolution
    supported by the system. It is expected to be in the format "widthxheight", where width and height
    are integers representing the maximum width and height of the screen
    :type maxResulation: str
    :return: a list of possible resolutions based on the maximum resolution provided as an argument. The
    list includes "fullscreen" as the first option, followed by any resolutions that have a width less
    than or equal to the maximum width provided.
    """

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
    """
    The function registers a user by checking the validity of their email, password, and username, and
    sends a verification code to their email if successful.
    
    :param email: A string representing the email address of the user who wants to register
    :type email: str
    :param password: a string representing the password entered by the user during registration
    :type password: str
    :param username: a string representing the desired username for the user's account
    :type username: str
    :return: nothing (i.e., None). It either calls the `notify` function with a message and returns, or
    it proceeds to send a registration request and load a new screen.
    """
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
        load_screen("email validation")

    else:
        notify("register failed", data)

def finish_register(verificationCode: str):
    """
    This function finishes the registration process by sending a verification code and loading the home
    screen if successful.
    
    :param verificationCode: The verification code is a string parameter that is used to confirm the
    user's identity during the registration process. It is typically sent to the user's email or phone
    number and is required to complete the registration process
    :type verificationCode: str
    """
    global isUser
    data = handle_sends("finish register", verificationCode).split("|")
    successfully = data == "S"
    if successfully:
        isUser = True
        notify("registered successfully", "welcome to SCE")
        load_screen("Home")


def login(email: str, password: str):
    """
    The function "login" handles user login attempts, checks for invalid characters in the email and
    password, sends login information to a server, loads the home screen if successful, and saves the
    user's email and password if the "toRemember" flag is set.
    
    :param email: A string representing the user's email address
    :type email: str
    :param password: The password parameter is a string that represents the user's password input for
    the login function
    :type password: str
    :return: The function does not return anything explicitly, but it may return None implicitly if the
    conditions in the if statement are not met.
    """
    global toRemember
    global isUser
    if "|" in password or "&" in password or "|" in email or "&" in email:
        notify("login failed","user params are inncorect")
        return

    successfully = handle_sends("login", email, password) == "S"

    if successfully:
        isUser=True
        load_screen("Home")
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

def notify(title1: str, message1: str):
    """
    This function creates a notification with a title and message, and displays it using a Windows
    toaster and a message box.
    
    :param title1: The title of the notification or message box
    :param message1: The message that will be displayed in the notification or message box
    """
    try:
        # win11toast.ToastNotificationManager.create_toast_notifier("Python")
        # winToaster2 = InteractableWindowsToaster("SCE")
        # newToast = ToastImageAndText1()
        # newToast.SetBody(title1 + " | " + message1)
        # newToast.SetHeadline(title1)
        # newToast.AddImage(ToastDisplayImage.fromPath(f"{os.getcwd()}/{screen_manager.imgPath}sce_logo.png"))
        # winToaster.show_toast(newToast)
        # newToast.AddInput(ToastInputTextBox("name", "your name", "Alon Garibi"))
        # newToast.AddAction(ToastButton("Submit", "submit"))
        # winToaster2.show_toast(newToast)
        pass
    except Exception as e:
        print(e)

    try:
       print("here!!!")
       msgbox.showinfo(title=title1, message=message1)
    except Exception as e:
        print(e)

    

def handle_sends(*arguments):
    """
    This function takes in multiple arguments, joins them with a "|" separator, encrypts the resulting
    string using a cipher, sends the encrypted message over a socket, and returns a decrypted message.
    :return: The code is incomplete and does not provide enough information to determine what is being
    returned by the `handle_sends` function. The last line of the function is calling a
    `decrypt_message` function, but it is not shown in the provided code.
    """
    toSend ="|".join(arguments) + "&"
    print(f"{toSend=}")
    encrypted_message = cipher.encrypt(toSend.encode())
    sock.send(encrypted_message)

    return decrypt_message()

def decrypt_message():
    """
    This function decrypts a message using a cipher and returns the decoded message.
    :return: The function `decrypt_message()` is returning the decrypted message obtained by decrypting
    the result of the `waitToConfirm()` function using the `decrypt()` method of the `cipher` object.
    The decrypted message is then decoded using the `decode()` method and returned.
    """
    return cipher.decrypt(waitToConfim()).decode()

def waitToConfim():
    """
    This function receives a message through a socket connection and recursively concatenates it until
    the end of the message is confirmed.
    :return: The function is recursively calling itself until it receives a message that ends with a
    tilde (~) character. Once it receives such a message, it extracts the message content, removes any
    backticks (`) or forward slashes (/) that may be present at the beginning or end of the message, and
    returns the cleaned message content. If the message does not end with a tilde character or if there
    is
    """
    message = sock.recv(100000)
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
        return "error"#
# def handle_sends(*arguments):
#     toSend ="|".join(arguments) + "&"
#     print(f"{toSend=}")
#     encrypted_message = cipher.encrypt(toSend.encode())
#     sock.send(encrypted_message)

#     data = waitToConfim()
#     print(f"{data=}")
#     isError = data == "ERROR"
#     if not isError:
#         return data
    
# def waitToConfim():
#     data = b""
#     while True:
#         try:
#             chunk = sock.recv(9000)
#         except Exception as exeption:
#             print(f"{exeption=}")
#             notify("ERROR", "Please restart your\napp and try again")
#             return "ERROR"
        
#         # print(chunk)
#         data += chunk
#         endSign = cipher.encrypt("~".encode())
#         if chunk.endswith(endSign):
#             break
#     return cipher.decrypt(data()).decode()


def clearScreen():
    """
    The function clears all widgets from a tkinter window.
    """
    for widget in screen_manager.window.winfo_children():
        widget.destroy()

def show_password(passwordEntry):
    """
    This function toggles the visibility of a password entry field in a GUI between showing the actual
    password and showing asterisks.
    
    :param passwordEntry: The parameter `passwordEntry` is a reference to a tkinter Entry widget that is
    used to input a password. The function `show_password` toggles the visibility of the password
    characters in the widget by changing the `show` attribute of the widget. If the `show` attribute is
    set to `
    """
    if passwordEntry.cget('show') == '*':
        passwordEntry.config(show='')
    else:
        passwordEntry.config(show='*')

def loadServer(server: str):
    """
    This function loads a server and displays a loading screen.
    
    :param server: The parameter "server" is a string that represents the name or address of the server
    that needs to be loaded
    :type server: str
    """
    global current_server
    current_server = server
    load_screen("server")
    # dataOfMessages = handle_sends("loadServer", server)

def home_sceen():
    """
    This function creates the home screen of an application with buttons for direct messages, joining
    servers, and displaying a list of available servers.
    """
    global toRemember
    dmY = int(screen_manager.winHeight/6.5)
    serversY = int(screen_manager.winHeight/3.5)
    lefSideX = int(screen_manager.winWidth/50)
    dm = Button(screen_manager.window, image=screen_manager.dmBTNImage, bd=0, highlightthickness=0, activebackground=screen_manager.backgroundColor, bg=screen_manager.backgroundColor, command=lambda: load_screen("dm"))
    dm.place(x=lefSideX, y=dmY)
    
    joinServer = Button(screen_manager.window, image=screen_manager.joinServerBTNImage, bd=0, highlightthickness=0, activebackground=screen_manager.backgroundColor, bg=screen_manager.backgroundColor, command=lambda: load_screen("Join Server"))
    joinServer.place(x=screen_manager.winWidth-screen_manager.joinServerImage.size[0], y=screen_manager.winHeight-screen_manager.settingsImage.size[1] - screen_manager.joinServerImage.size[1] - screen_manager.winHeight/30)

    joinServer.update()

    servers = handle_sends("getServers").split("|")[0]
    servers = dict(json.loads(servers))
    serversButtons = []
    keys = list(servers.keys())
    first = True
    for server in keys:
        sb = Button(screen_manager.window, text=servers[server], bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Airal", int(screen_manager.appTextFontSize * 0.8), "bold"), command=lambda a=server: loadServer(a))
        y = serversY
        if not first:
            y = serversButtons[-1].winfo_y() + serversButtons[-1].winfo_height() + int(screen_manager.winHeight/100)
        first = False
        
        sb.place(x=lefSideX, y= y)
        sb.update()
        serversButtons.append(sb)
    screen_manager.window.update()

def login_register_screens(screen: str):
    """
    This function creates the login and registration screens for a GUI application and includes
    functionality for remembering user login information.
    
    :param screen: The parameter "screen" is a string that specifies which screen to display - either
    the login screen or the register screen
    :type screen: str
    """
    global toRemember
    screen_manager.window.update()

    emailY = int(screen_manager.winHeight/3.5)
    labelX = int(screen_manager.winWidth / 4)
    getOtherLabel = 0
    
    if screen == "Register":
        usernameY = emailY + int(screen_manager.winHeight/7)
        passwordY = emailY + int(screen_manager.winHeight/3.5)
        usernameEntry = Entry(screen_manager.window, bg=screen_manager.secondColor, font=("Airal", int(screen_manager.appTextFontSize), "bold"))
        usernameEntry.place(x=labelX, y=usernameY, width=screen_manager.mainEntrysWidth)
        usernameLabel = Label(screen_manager.window, bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Airal", screen_manager.appTextFontSize, "bold"),
                              text="Username:")
        usernameLabel.place(x=labelX, y=usernameY - int(screen_manager.winHeight/17))
        
        getOtherLabel = Label(screen_manager.window, bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Airal", int(screen_manager.appTextFontSize * 0.8), "bold"),
                              text="Already have account?")
        getOtherButton = Button(screen_manager.window, image=screen_manager.smallLoginBTNImage, bd=0, highlightthickness=0,
                                activebackground=screen_manager.backgroundColor, bg=screen_manager.backgroundColor, command=lambda: load_screen("login"))
        submitWidth = screen_manager.registerImage.size[0]
        submitX = int(screen_manager.mainEntrysWidth/2) + labelX - (submitWidth)/2
        

    else:
        passwordY = emailY + int(screen_manager.winHeight/7)

        getOtherLabel = Label(screen_manager.window, bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Airal", int(screen_manager.appTextFontSize * 0.8), "bold"),
                              text="Still don't have account?")
        getOtherButton = Button(screen_manager.window, image=screen_manager.smallRegisterBTNImage, bd=0, highlightthickness=0,
                                activebackground=screen_manager.backgroundColor, bg=screen_manager.backgroundColor, command=lambda: load_screen("Register"))
        
        submitWidth = screen_manager.loginImage.size[0]
        submitX = int(screen_manager.mainEntrysWidth/2) + labelX - (submitWidth)/2

    emailLabel = Label(screen_manager.window, bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Airal", screen_manager.appTextFontSize, "bold"), text="Email:")
    emailLabel.place(x=labelX, y=emailY - (screen_manager.winHeight/17))

    emailEntry = Entry(screen_manager.window, bg=screen_manager.secondColor, font=("Airal", screen_manager.appTextFontSize, "bold"))
    emailEntry.place(x=labelX, y=emailY, width=screen_manager.mainEntrysWidth)

    passwordLabel = Label(screen_manager.window, bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Airal", screen_manager.appTextFontSize, "bold"), text="Password:")
    passwordLabel.place(x=labelX, y=passwordY - int(screen_manager.winHeight/17))

    passwordEntry = Entry(screen_manager.window, bg=screen_manager.secondColor, font=("Airal", screen_manager.appTextFontSize, "bold"), show="*")
    passwordEntry.place(x=labelX, y=passwordY, width=screen_manager.mainEntrysWidth)

    showPasswordButton = Checkbutton(screen_manager.window, text="show password", bg=screen_manager.backgroundColor, fg=screen_manager.secondColor,
                                     highlightthickness=0, activebackground=screen_manager.backgroundColor, bd=0,
                                     font=("Airal", int(0.7 * screen_manager.appTextFontSize), "bold"), command= lambda: show_password(passwordEntry))
    showPasswordButton.place(x=labelX, y=passwordY + int(screen_manager.winHeight/13))
    screen_manager.window.update()

    if screen == "Register":
        submitY = showPasswordButton.winfo_y() + showPasswordButton.winfo_height() + int(screen_manager.winHeight/40)

        submitButton = Button(screen_manager.window, image=screen_manager.registerBTNImage, bd=0, highlightthickness=0,
                activebackground=screen_manager.backgroundColor, bg=screen_manager.backgroundColor, command= lambda: register(emailEntry.get(), passwordEntry.get(), usernameEntry.get()))
        submitButton.place(x=submitX, y=submitY)
    else:
        toRemember = False
        remmeberMeButton = Checkbutton(screen_manager.window, text="remmeber me", bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, highlightthickness=0, activebackground=screen_manager.backgroundColor, bd=0,
                                       font=("Airal", int(0.7 * screen_manager.appTextFontSize), "bold"), command=toggleToRemember)

        remmeberMeButton.place(x=labelX, y=showPasswordButton.winfo_y() + showPasswordButton.winfo_height() + int(screen_manager.winHeight/40))
    
        screen_manager.window.update()
        
        submitY = remmeberMeButton.winfo_y() + remmeberMeButton.winfo_height() + int(screen_manager.winHeight/40)

        submitButton = Button(screen_manager.window, image=screen_manager.loginBTNImage, bd=0, highlightthickness=0, activebackground=screen_manager.backgroundColor,
                              bg=screen_manager.backgroundColor, command= lambda: login(emailEntry.get(), passwordEntry.get()))
        submitButton.place(x=submitX, y=submitY)
        screen_manager.window.update()

        width = int(screen_manager.winWidth/5)
        forgotPassword = Button(screen_manager.window, text="Forgot Password", bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Airal", screen_manager.appTextFontSize, "bold"), command= lambda: load_screen("forgot password"))
        forgotPassword.place(x = submitButton.winfo_x() + int(submitButton.winfo_width()/2) - int(width/2), y= submitButton.winfo_y() + submitButton.winfo_height() + int(screen_manager.winHeight/20), width=width)

    gobx = submitX + int(screen_manager.winWidth / 2.5)
    getOtherLabel.place(x= gobx, y=(submitY - (screen_manager.winHeight/24)))
    getOtherButton.place(x=gobx - int(screen_manager.winWidth/60), y=submitY)
    screen_manager.window.update()

    if screen == "login":
        location = os.getcwd()+"/user.txt"
        if os.path.getsize(location) > 0:
            with open(location, 'rb') as encrypted_user_file:
                lines = encrypted_user_file.readlines()
                encryptedEmail = lines[0][:-1]
                encryptedPassword = lines[1]
                login(cipher.decrypt(encryptedEmail).decode(), cipher.decrypt(encryptedPassword).decode())

def toggleToRemember():
    """
    The function toggles the value of a global variable called "toRemember".
    """
    global toRemember
    toRemember = not toRemember

def settings_screen():
    """
    This function creates a settings screen with options for changing the screen resolution and logging
    out or changing user data if the user is logged in.
    """
    global resulations, isUser

    LabelX = int(screen_manager.winWidth/10)
    resulationLabelY = int(screen_manager.winHeight/5.5)
    resulationLabel = Label(screen_manager.window, bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Airal", screen_manager.appTextFontSize, "bold"), text="Resulation:")
    resulationLabel.place(x=LabelX, y=resulationLabelY)
    resulationButtons = []

    for i, resulation in enumerate(resulations):
        rb = Button(screen_manager.window, text=resulations[i], bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Airal", int(screen_manager.appTextFontSize * 0.9), "bold"), command=lambda a=resulation: change_screen_resulation("settings", a))
        rb.pack(anchor=N)
        rb.update()
        bh = rb.winfo_height()
        max = ((resulationLabelY + resulationLabel.winfo_height() + int(screen_manager.winHeight/50)) + (int(screen_manager.winHeight/50) + rb.winfo_height()) * i)
        rb.place(x=LabelX + int (screen_manager.winWidth/ 50), y = max)
        rb.update()
        resulationButtons.append(rb)
    if isUser:
        logout = Button(screen_manager.window, text="Logout", bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Airal", screen_manager.appTextFontSize, "bold"), command=logout_user)
        logout.place(x=LabelX, y= max + rb.winfo_height() + int(screen_manager.winHeight/25))

        screen_manager.window.update()
        chnageUser = Button(screen_manager.window, text="change user data", bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Airal", screen_manager.appTextFontSize, "bold"), command = lambda: load_screen("change user"))
        chnageUser.place(x=LabelX, y = logout.winfo_y() + logout.winfo_height() + int(screen_manager.winHeight/25))

    # resulation.place(x=0, y=0)
    
def logout_user():
    """
    The function logs out the user by setting a global variable to False, sending a logout request to a
    server, deleting a user file, and loading the login screen.
    """
    global isUser, homeButton
    isUser = False
    successfully = handle_sends("logout").split("|")[0] == "S"
    if successfully:
        location = os.getcwd()+"/user.txt"
        with open(location,'r+') as file:
            file.truncate(0)
        load_screen("login")
    else:
        print("error")

def change_screen_resulation(screen: str, res: str):
    """
    This function changes the screen resolution and loads a specified screen.
    
    :param screen: The name or identifier of the screen or window that needs to have its resolution
    changed
    :type screen: str
    :param res: The resolution to set the screen to. It can be a string representing a specific
    resolution (e.g. "1920x1080") or the string "fullscreen" to set the screen to full screen mode
    :type res: str
    """
    screen_manager.setCurrentRes(res)

    if res == "fullscreen":
        screen_manager.window.attributes('-fullscreen', True)       
    else:
        screen_manager.window.attributes('-fullscreen', False)       
        screen_manager.window.geometry(res)

    screen_manager.resize_screen()
    load_screen(screen)

def load_screen(screen: str):
    """
    The function loads a screen and calls other functions based on the screen type.
    
    :param screen: The parameter "screen" is a string that represents the name of the screen to be
    loaded. The function "load_screen" takes this parameter and uses it to load the corresponding screen
    on the user interface. If the screen is "Register" or "login", it calls the function
    "login_register_s
    :type screen: str
    """
    clearScreen()

    screen_manager.window.update()

    loadBasicScreen(screen_manager.window, screen)

    screen_manager.window.update()

    print(screen)
    
    match screen:
        case "Register":
            login_register_screens(screen)
        case "login":
            login_register_screens(screen)
        case "Home":
            home_sceen()
        case "settings":
            settings_screen()
        case "Create Server":
            create_server_screen()
        case "change user":
            change_user_data_screen()
        case "dm":
            DMScreen()
        case "server":
            server_screen()
        case "forgot password":
            forgot_password_screen()
        case _:
            defualt_screen(screen)

def forgot_password_screen():
    email_y = int(screen_manager.winHeight / 3.75)
    labels_x = int(screen_manager.winWidth / 4)

    email_entry = Entry(screen_manager.window, bg=screen_manager.secondColor, font=("Arial", screen_manager.appTextFontSize, "bold"))
    email_entry.place(x=labels_x, y=email_y, width=screen_manager.mainEntrysWidth)
    email_entry.update()

    email_label = Label(screen_manager.window, bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Arial", screen_manager.appTextFontSize, "bold"), text="Email:")
    email_label.place(x=labels_x, y=email_entry.winfo_y() - (screen_manager.winWidth / 20))
    email_label.update()

    send_y = email_entry.winfo_y() + email_entry.winfo_height() + int(screen_manager.winHeight / 25)
    send_button = Button(screen_manager.window, image=screen_manager.sendBTNImage, bd=0, highlightthickness=0,
                activebackground=screen_manager.backgroundColor, bg=screen_manager.backgroundColor, command=lambda: sendForgotPasswordEmail(email_entry.get()))
    send_button.place(x=int((screen_manager.winWidth - screen_manager.sendImage.size[0]) / 2), y=send_y)
    send_button.update()

    reset_code_y = send_button.winfo_y() + send_button.winfo_height() + int(screen_manager.winHeight / 15)

    reset_code_label = Label(screen_manager.window, bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Arial", screen_manager.appTextFontSize, "bold"),
                            text="Verification Code:")
    reset_code_label.place(x=labels_x, y=reset_code_y)
    reset_code_label.update()

    reset_code_entry = Entry(screen_manager.window, bg=screen_manager.secondColor, font=("Arial", int(screen_manager.appTextFontSize), "bold"))
    reset_code_entry.place(x=labels_x, y=reset_code_label.winfo_y() + reset_code_label.winfo_height() + int(screen_manager.winHeight / 100), width=screen_manager.mainEntrysWidth)
    reset_code_entry.update()

    submit_button = Button(screen_manager.window, image=screen_manager.verifyBTNImage, bd=0, highlightthickness=0,
                activebackground=screen_manager.backgroundColor, bg=screen_manager.backgroundColor, comman=lambda: verifyEmail(reset_code_entry.get()))
    submit_button.place(x=send_button.winfo_x(), y=reset_code_entry.winfo_y() + reset_code_entry.winfo_height() + int(screen_manager.winHeight / 25))


def sendForgotPasswordEmail(email: str):
    """
    The function takes an email address as input and is likely used to send a forgot password email to
    the user associated with that email.
    
    :param email: The email parameter is a string that represents the email address of the user who has
    forgotten their password. This email will be used to send a password reset link or instructions on
    how to reset their password
    :type email: str
    """
    d = handle_sends("send verification", email)
    s = d == "S"
    if s:
        notify("email sent", "verficiation sent successfully")
    else:
        notify("email went wrong", "email went wrong, try again late")

def verifyEmail(verficationCode):
    """
    The function "verifyEmail" takes in a verification code as a parameter.
    
    :param verficationCode: The verification code is a string of characters or numbers that is used to
    confirm the validity of an email address. It is usually sent to the email address being verified and
    the user must enter it into a form or click on a link to confirm that they own the email address.
    The purpose of this function
    """

    data = handle_sends("verify email", verficationCode).split('|')
    successfully = data[0] == "S"

    if successfully:
        load_screen("reset password")
    else:
        notify("wrong code", "your verification code is wrong, please check again")

class server_screen():
    def __init__(self):
        self.isMessages = False
        self.maxMembersInLine = 3
        self.ot_widgets = []
        self.start_pos = (350, 100)
        self.max_in_vc = 9
        self.margin = 100
        self.serverScreen()

    def serverScreen(self):
        self.current_server = current_server
        shareButton = Button(screen_manager.window, image=screen_manager.shareBTNImage, bd=0, highlightthickness=0, activebackground=screen_manager.backgroundColor,
                             bg=screen_manager.backgroundColor, command=lambda: self.copy_server_id(self.current_server))
        shareButton.place(x=screen_manager.winWidth - screen_manager.shareImage.size[0], y = screen_manager.winHeight -
                          screen_manager.settingsImage.size[1] - screen_manager.shareImage.size[1])
        # clearScreen()
        self.frameYPos = max(screen_manager.titleLowestY, screen_manager.homeImage.size[1])
        # frame.pack(side=LEFT, fill=Y, expand=True)
        self.width = screen_manager.winWidth - screen_manager.settingsImage.size[0]
        self.height = screen_manager.winHeight - self.frameYPos
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

    def copy_server_id(self, server_id: str):
        print(f"server id is: {server_id}")
        pyperclip.copy(server_id)
        notify("code copied", "the code of this server copied\nshare the code with who you want to join the server")

    def loadRoomsCanvas(self):
        self.roomsFrame = Frame(screen_manager.window)

        self.roomsFrame.place(x=self.roomsX, y=self.frameYPos, width=self.roomsWidth, height=self.height)
        self.roomsFrame.update()
        
        self.roomsCanvas = Canvas(self.roomsFrame, bg=screen_manager.thirdColor, bd=0, highlightthickness=0, highlightcolor=screen_manager.backgroundColor, width=self.roomsFrame.winfo_width(),height=self.roomsFrame.winfo_height())
        self.roomsCanvas.pack(side=LEFT, expand=True, fill=BOTH)
        
        self.roomsScrollBar = ttk.Scrollbar(self.roomsCanvas, orient=VERTICAL, command=self.roomsCanvas.yview, cursor= "double_arrow")
        self.roomsScrollBar.pack(side=RIGHT, fill=Y)

        self.roomsCanvas.configure(yscrollcommand=self.roomsScrollBar.set)

        self.roomsCanvas.bind("<Configure>", lambda e: self.roomsCanvas.configure(scrollregion=self.roomsCanvas.bbox("all")))
        
        self.secRoomsFrame = Frame(self.roomsCanvas, bg=screen_manager.thirdColor)
        self.roomsCanvas.create_window((0, 0), window=self.secRoomsFrame, anchor=NW)

        # current_room = "mainRoom"

        self.rooms = handle_sends("get rooms", self.current_server)
        self.rooms = self.rooms.split("|")
        print(self.rooms)
        isSuccessful = self.rooms[0] == "S"
        if not isSuccessful:
            load_screen("home")
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
            self.textRoomsLabel = Label(self.roomsCanvas, text = "Text Rooms:", bg=screen_manager.thirdColor, highlightthickness=0, font=("Airal", screen_manager.roomsNamesTextSize, "bold"), fg=screen_manager.secondColor)
            self.textRoomsLabel.place(x=0, y=0)
            self.textRoomsLabel.update()
            
            self.lastButtonY = self.textRoomsLabel.winfo_y() + self.textRoomsLabel.winfo_height()

            for room in self.textRooms:   
                if room != "":
                    a = Button(self.roomsCanvas, text=" "+room, image=screen_manager.tBTNImage, compound=LEFT, bg=screen_manager.thirdColor, highlightthickness=0, font=("Airal", screen_manager.roomsNamesTextSize, "bold"), fg=screen_manager.secondColor, command=lambda a = room: self.loadTextRoom(a))
                    a.place(x=0, y = int(screen_manager.winHeight/70) + self.lastButtonY)
                    a.update()
                    self.lastButtonY = a.winfo_y() + a.winfo_height()
                    # longest = max(longest, a.winfo_width())
                    # longest = min(longest, roomsWidth)

        if self.voiceRooms:
            self.voiceRoomsLabel = Label(self.roomsCanvas, text = "Voice Rooms:", bg=screen_manager.thirdColor, highlightthickness=0, font=("Airal", screen_manager.roomsNamesTextSize, "bold"), fg=screen_manager.secondColor)
            self.voiceRoomsLabel.place(x=0, y=self.lastButtonY + screen_manager.winHeight/70)
            self.voiceRoomsLabel.update()
            self.lastButtonY = self.voiceRoomsLabel.winfo_y() + self.voiceRoomsLabel.winfo_height()
            self.voiceRoomsLabel.update()

            for room in self.voiceRooms:
                if room != "":
                    a = Button(self.roomsCanvas, text=" "+room, image=screen_manager.vBTNImage, compound=LEFT, bg=screen_manager.thirdColor, highlightthickness=0, font=("Airal", screen_manager.roomsNamesTextSize, "bold"), fg=screen_manager.secondColor, command=lambda a = room: self.loadVoiceRoom(a))
                    a.place(x=0, y = int(screen_manager.winHeight/70) + self.lastButtonY)
                    a.update()
                    self.lastButtonY = a.winfo_y() + a.winfo_height()
                    # longest = max(longest, a.winfo_width())
                    # longest = min(longest, roomsWidth)

        # roomsFrame.place(x=0, y=frameYPos, width=longest + roomsScrollBar.winfo_width(), height=height)
        # roomsFrame.update()
        # roomsScrollBar.pack(side=RIGHT, fill=Y)

    def loadMessagesCanvas(self):
        self.messagesFrame = Frame(screen_manager.window)

        self.messagesFrame.place(x=self.messagesX, y=self.frameYPos, width=self.messagesWidth, height=self.height)
        self.messagesFrame.update()
        
        self.messagesCanvas = Canvas(self.messagesFrame, bg=screen_manager.thirdColor, bd=0, highlightthickness=0, highlightcolor=screen_manager.backgroundColor, width=self.messagesFrame.winfo_width(),height=self.messagesFrame.winfo_height())
        self.messagesCanvas.pack(side=LEFT, expand=True, fill=BOTH)
        
        self.messagesScrollbar = ttk.Scrollbar(self.messagesCanvas, orient=VERTICAL, command=self.messagesCanvas.yview, cursor= "double_arrow")
        self.messagesScrollbar.pack(side=RIGHT, fill=Y)

        self.messagesCanvas.configure(yscrollcommand=self.messagesScrollbar.set)
        self.messagesCanvas.bind("<Configure>", lambda e: self.roomsCanvas.configure(scrollregion=self.messagesCanvas.bbox("all")))
        
        self.secMessagesFrame = Frame(self.messagesCanvas, bg=screen_manager.thirdColor)
        self.messagesCanvas.create_window((0, 0), window=self.secMessagesFrame, anchor=NW)

        screen_manager.window.update()

    def load_messages(self):
        for widget in self.secMessagesFrame.winfo_children():
            widget.destroy()
        for widget in self.messagesCanvas.winfo_children():
            if not isinstance(widget, Frame) and not isinstance(widget, Scrollbar):
                widget.destroy()
        self.to_limit_y_view = True
        self.messagesCanvas.yview_moveto(0)
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
                maxLength = 120
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
                lines.append(lines[0])
                lines = lines[1:]
                # lines.reverse()
                lines="\n".join(lines)
                print(f"\n\n\n\n{lines=}")
                l = Label(self.secMessagesFrame, text= messageAuthor+":", bd=0, highlightthickness=0, bg=screen_manager.thirdColor, font=("Arial", screen_manager.messagesFontSize, "bold"), fg = screen_manager.secondColor)
                l.grid(row=lastButtonY, column=0, sticky=W)
                labels.append(l)
                b = Button(self.secMessagesFrame, text= lines, bd=0, justify=LEFT, highlightthickness=0, bg=screen_manager.thirdColor, font=("Arial", screen_manager.messagesFontSize, "bold"), fg = screen_manager.secondColor, compound="c", width= maxLength, anchor=W, command=lambda: print("yay"), disabledforeground=screen_manager.secondColor)
                if not isMessageIsMy:
                    b.configure(state=DISABLED)
                b.grid(row=lastButtonY + 1, column=10, sticky=W)
                buttons.append(b)
                space = Label(self.secMessagesFrame, text="", bd=0, bg=screen_manager.thirdColor)
                space.grid(row=lastButtonY+2, column=0, sticky=W)
                lastButtonY += 3
                self.secMessagesFrame.update()
                # if b.winfo_width() > self.messagesWidth:
                #     i = 1
                #     lines = [messageData]
                #     s_d = messageData.split(" ")
                #     lines = 
                #     while b.winfo_width() > self.messagesWidth:
        screen_manager.window.update()

        
    def loadParticipantsCanvas(self):
        self.participantsFrame = Frame(screen_manager.window)

        self.participantsFrame.place(x=self.participantsX, y=self.frameYPos, width=self.participantsWidth, height=self.height)
        self.participantsFrame.update()
        
        self.participantsCanvas = Canvas(self.participantsFrame, bg=screen_manager.thirdColor, bd=0, highlightthickness=0, highlightcolor=screen_manager.backgroundColor, width=self.participantsFrame.winfo_width(),height=self.participantsFrame.winfo_height())
        self.participantsCanvas.pack(side=LEFT, expand=True, fill=BOTH)
        
        self.participantsScrollBar = ttk.Scrollbar(self.participantsCanvas, orient=VERTICAL, command=self.participantsCanvas.yview, cursor= "double_arrow")
        self.participantsScrollBar.pack(side=RIGHT, fill=Y)

        self.participantsCanvas.configure(yscrollcommand=self.participantsScrollBar.set)
        self.participantsCanvas.bind("<Configure>", lambda e: self.participantsCanvas.configure(scrollregion=self.participantsCanvas.bbox("all")))
        
        self.secParticipantsFrame = Frame(self.participantsCanvas, bg=screen_manager.thirdColor)
        self.participantsCanvas.create_window((0, 0), window=self.secParticipantsFrame, anchor=N)
        data = handle_sends("get participants").split("|")
        print(f"{data=}")
        if data[0] == "S":
            self.participants = (data[1].split("*"))
            self.isAdmin = bool(data[2])
            self.isOwner = bool(data[3])
        for i, participant in enumerate(self.participants):
            label = Label(self.secParticipantsFrame, bg=screen_manager.thirdColor, fg=screen_manager.secondColor, font=("Airal", screen_manager.participantsFontSize, "bold"), text=participant)
            label.grid(row=i, column=0, sticky=W)
        
    def loadTextRoom(self, room: str):
        """
        This function loads a text room and displays messages and a message entry field.
        
        :param room: The parameter "room" is the identifier of the room that needs to be loaded. It is used
        to retrieve the messages and other information related to that room
        """
        self.current_room = room
        data = handle_sends("load text room", room).split("|")
        success = data[0] == "S"
        if success:
            self.messages = data[1].split("*")
            print(self.messages)
            self.isMessages = True
            self.load_messages()
            self.messageEntry = Entry(screen_manager.window, bg=screen_manager.secondColor, font=("Airal", int(screen_manager.messagesFontSize), "bold"))
            self.messageEntry.pack()
            self.messageEntry.update()
            self.messageEntry.place(x=self.messagesX, y=screen_manager.winHeight-self.messageEntry.winfo_height(), width=self.messagesFrame.winfo_width()-1.5*self.messagesScrollbar.winfo_width()-screen_manager.sendIconImage.size[0])
            self.messageEntry.update()
            screen_manager.window.update()
            self.sendButton = Button(screen_manager.window, image=screen_manager.sendIconBTNImage, bg=screen_manager.thirdColor, command=lambda: self.send_message(self.messageEntry.get()))
            self.sendButton.place(x=self.messagesFrame.winfo_x() + self.messageEntry.winfo_width(), y = screen_manager.winHeight-screen_manager.sendIconImage.size[1])
            self.messagesCanvas.update()

        else:
            notify("load room error", data[1])
    
    def clear_canvas(self):
        try:
            for ot_widget in self.ot_widgets:
                ot_widget.destroy()
        except:
            pass

    def toggle_camera_mode(self):
        self.to_use_camera = not self.to_use_camera
        print(f"{self.to_use_camera=}")
        if self.to_use_camera:
            d = handle_sends("active camera").split("|")
            if d[0] == "S":
                self.vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                self.vid.set(cv2.CAP_PROP_BUFFERSIZE, 2)
                self.cam_sock = socket.socket()
                cam_port = int(d[1])
                print(f"{cam_port=}")
                self.cam_sock.connect((ip, cam_port))
                send_camera_thread = Thread(target=self.sendMyCamera ,args=())
                send_camera_thread.start()

    def recv_camera_data(self, port, n):
        r = math.floor(n % 3)
        c = math.floor(n / 3)
        l = Label(self.messagesCanvas)
        x_pos = self.start_pos[0] + c * (self.margin + screen_manager.max_camera_width)
        y_pos = self.start_pos[1] + r * (self.margin + screen_manager.max_camera_height)
        print(f"{n=} {c=} {r=} {x_pos=} {y_pos=}")
        l.place(x=x_pos, y=y_pos)

        sock = socket.socket()

        port = int(port)
        sock.connect(("127.0.0.1", port))
        while True:
            try:
                frame = sock.recv(999999999)
                # print(frame)
                bytes = np.frombuffer(frame, np.uint8)
                
                image = cv2.imdecode(bytes, cv2.IMREAD_COLOR)
                rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                pilImage = Image.fromarray(rgb_frame)
                img = ImageTk.PhotoImage(pilImage)
                l.config(image=img)
                l.update()
                # l = Label(screen_manager.window, image=img, bg=screen_manager.backgroundColor, fg=screen_manager.secondColor)
                # l.place(x=150, y=150)
            except:
                pass

    def loadVoiceRoom(self, room: str):
        for widget in self.secMessagesFrame.winfo_children():
            widget.destroy()
        for widget in self.messagesCanvas.winfo_children():
            if not isinstance(widget, Frame) and not isinstance(widget, Scrollbar):
                widget.destroy()
            try:
                self.sendButton.destroy()
                self.messageEntry.destroy()
            except:
                pass
        camera_sockets = []
        # for i in range(1, self.max_in_vc):
        #     sock = socket.socket()
        #     camera_sockets.append(sock)
        #     camera_thread = Thread(target=self.recv_camera_data, args=(sock, i))
        #     camera_thread.start()

        self.current_room = room
        data = handle_sends("load voice room", room).split("|")
        success = data[0] == "S"
        print(f"{success=}")
        if success:
            ports = data[1].split("*")
            self.to_use_camera = False
            camera_button = Button(self.messagesCanvas, image=screen_manager.cameraBTNImage, bg=screen_manager.thirdColor, command=self.toggle_camera_mode)
            camera_button.place(x=self.messagesCanvas.winfo_width()/2 - screen_manager.cameraImage.size[0]/2, y=self.messagesCanvas.winfo_height() - screen_manager.cameraImage.size[1])
            self.ot_widgets.append(camera_button)

            for i, port in enumerate(ports):
                i += 1
                t = Thread(target=self.recv_camera_data, args=(port, i))
                t.start()
            # t = Thread(target=self.loadCamera)
            # t = Thread(target=self.sendMyCamera)
            
            # m_threads = {}
            # inVC = data[1].split("*")
    
            # for i, m_id in enumerate(inVC):
            #     line = math.floor(i/self.maxMembersInLine)
            #     row = i % self.maxMembersInLine
            #     mt = Thread(target=self.load_member_camera, args=(line, row, m_id))
            #     mt.start()
            #     m_threads[m_id] = mt 
            # for t in m_threads:
            #     pass

    # def load_cam(self, port):



    def sendMyCamera(self):
        cl = Label(self.messagesCanvas)
        cl.place(x=self.start_pos[0], y=self.start_pos[1])
        while self.to_use_camera:
            if self.vid.isOpened():
                ret, frame = self.vid.read()
                maxWidth =200
                maxHeight = 200
                height, width = frame.shape[:2]
                print(f"{width=} {height=}")
                if width > maxWidth:
                    p = maxWidth/width
                    print(p)
                    frame = cv2.resize(frame, (0, 0),  fx=p, fy=p)
                height, width = frame.shape[:2]
                if height > maxHeight:
                    p = maxHeight/height
                    frame = cv2.resize(frame, (0, 0),  fx=p, fy=p)
                height, width = frame.shape[:2]
                # frame = cv2.GaussianBlur(frame, (3, 3), 0)


                # time.sleep(1/24)

                is_success, buf_array = cv2.imencode(".png", frame)

                s = buf_array.tostring()

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pilImage = Image.fromarray(rgb_frame)

                my_camera_image = ImageTk.PhotoImage(pilImage)
                cl.config(image=my_camera_image)
                cl.update()
                # print(type(s))
                # # print(bytes)
                # print("---------------------------------------------\n" + f"{s}\n{len(s)}")
                # print(f"{width=} {height=}")
                self.cam_sock.send(s)
        self.vid.release()
        self.cam_sock.close()
        

    def load_member_camera(self,line: int, row: int):
        pass

    def send_message(self, message: str):
        success = handle_sends("add message", message) == "S"
        self.loadTextRoom(self.current_room)

def loadBasicScreen(window2: Tk, screen: str):

    xButton = Button(window2, image=screen_manager.XBTNImage, bd=0, highlightthickness=0, activebackground=screen_manager.backgroundColor, bg=screen_manager.backgroundColor, command=close, cursor= "X_cursor")
    xButton.pack(anchor=NE)
    
    titleLabel = Label(window2, bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Airal", screen_manager.titlesFontSize, "bold"), text=screen.upper())
    titleLabel.place(x=screen_manager.titleX, y=int(screen_manager.winHeight/29), width=screen_manager.titleWidth)
    titleLabel.update()
    screen_manager.setTitleLowestY(titleLabel.winfo_y() + titleLabel.winfo_height())

    homeButton = Button(window2, image=screen_manager.homeBTNImage, bd=0, highlightthickness=0, activebackground=screen_manager.backgroundColor, bg=screen_manager.backgroundColor, command=lambda: load_screen("Home"))
    if not isUser:
        homeButton.config(command=lambda: load_screen("login"))        
    homeButton.place(x=0, y=0)
    
    if screen != "settings":
        settings = Button(window2, image=screen_manager.settingsBTNImage, bd=0, highlightthickness=0, activebackground=screen_manager.backgroundColor, bg=screen_manager.backgroundColor, command=lambda: load_screen("settings"))
        settings.place(x=screen_manager.winWidth-screen_manager.settingsImage.size[0], y=screen_manager.winHeight-screen_manager.settingsImage.size[1])
        settings.update()

    

def change_user_data_screen():
    usernameY = int(1.7 * screen_manager.winHeight / 4)
    passwordY = usernameY + int(screen_manager.winHeight/7)
    labelX = int(screen_manager.winWidth / 4)

    submitX = screen_manager.mainEntrysWidth - 100
    submitY = passwordY + int(screen_manager.winWidth/12)

    changeUsernameLabelText = "New Username:"
    changePasswordLabelText = "New Password:"
    explainText = "not all required".title()
    explainLabel = Label(screen_manager.window, bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("assitant", screen_manager.appTextFontSize, "bold"), text=explainText)
    explainLabel.place(x=0, y=usernameY - int(screen_manager.winHeight/7), width=screen_manager.winWidth)

    changeUsernameLabel = Label(screen_manager.window, bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Airal", screen_manager.appTextFontSize, "bold"),
                         text=changeUsernameLabelText)
    changeUsernameLabel.place(x=labelX, y=usernameY - int(screen_manager.winHeight/17))
    
    changeUsernameEntry = Entry(screen_manager.window, bg=screen_manager.secondColor, font=("Airal", int(screen_manager.appTextFontSize), "bold"))
    changeUsernameEntry.place(x=labelX, y=usernameY, width=screen_manager.mainEntrysWidth)

    ChangePasswordLabel = Label(screen_manager.window, bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Airal", screen_manager.appTextFontSize, "bold"), text=changePasswordLabelText)
    ChangePasswordLabel.place(x=labelX, y=passwordY - int(screen_manager.winHeight/17))
    
    ChangePasswordEntry = Entry(screen_manager.window, bg=screen_manager.secondColor, font=("Airal", screen_manager.appTextFontSize, "bold"), show="*")
    ChangePasswordEntry.place(x=labelX, y=passwordY, width=screen_manager.mainEntrysWidth)

    showPasswordButton = Checkbutton(screen_manager.window, text="show password", bg=screen_manager.backgroundColor, fg=screen_manager.secondColor,
                                     highlightthickness=0, activebackground=screen_manager.backgroundColor, bd=0,
                                     font=("Airal", int(0.7 * screen_manager.appTextFontSize), "bold"), command=lambda: show_password(ChangePasswordEntry))
    showPasswordButton.place(x=labelX, y=passwordY + int(screen_manager.winHeight/13))

    submitButton = Button(screen_manager.window, image=screen_manager.changeBTNImage, bd=0, highlightthickness=0,
                              activebackground=screen_manager.backgroundColor, bg=screen_manager.backgroundColor, command=lambda: manage_update(changeUsernameEntry.get(), ChangePasswordEntry.get()))
    submitButton.place(x=submitX, y=submitY)

def manage_update(username: str, password: str):
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
            load_screen("Home")

    
def DMScreen():
    friendsY = int(screen_manager.winHeight/5)
    lefSideX = int(screen_manager.winWidth/50)
        
    addFriend = Button(screen_manager.window, image=screen_manager.addFriendBTNImage, bd=0, highlightthickness=0, activebackground=screen_manager.backgroundColor, bg=screen_manager.backgroundColor, command=lambda: load_screen("Add friend"))
    addFriend.place(x=screen_manager.winWidth-screen_manager.joinServerImage.size[0], y=screen_manager.winHeight-screen_manager.settingsImage.size[1] - screen_manager.joinServerImage.size[1] - screen_manager.winHeight/30)

    friends = handle_sends("getFriends")
    friends = dict(json.loads(friends))
    friendsButtons = []
    keys = list(friends.keys())
    for i, frined in enumerate(keys):
        sb = Button(screen_manager.window, text=friends[frined], bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Airal", int(screen_manager.appTextFontSize * 0.8), "bold"), command=lambda a=frined: loadDMChat(a))
        sb.pack(anchor=N)
        sb.update()
        sb.place(x=lefSideX, y=(friendsY + (int(screen_manager.winHeight/50) + sb.winfo_height()) * i))
        screen_manager.window.update()
        friendsButtons.append(sb)

def loadDMChat(id):
    pass

def create_server_screen():
    nameY = int(1.7 * screen_manager.winHeight / 4)
    isGhostRoomsY = nameY + int(screen_manager.winHeight/7)
    labelX = int(screen_manager.winWidth / 4)
    ghostRooms = False

    submitX = screen_manager.mainEntrysWidth - 100
    submitY = isGhostRoomsY + int(screen_manager.winWidth/20)

    nameLabel = Label(screen_manager.window, bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Airal", screen_manager.appTextFontSize, "bold"), text="Server Name:")
    nameLabel.place(x=labelX, y=nameY - (screen_manager.winHeight/17))

    nameEntry = Entry(screen_manager.window, bg=screen_manager.secondColor, font=("Airal", screen_manager.appTextFontSize, "bold"))
    nameEntry.place(x=labelX, y=nameY, width=screen_manager.mainEntrysWidth)

    ghostRoomButton = Checkbutton(screen_manager.window, text="ghost room", bg=screen_manager.backgroundColor, fg=screen_manager.secondColor,
                                     highlightthickness=0, activebackground=screen_manager.backgroundColor, bd=0, font=("Airal", int(0.7 * screen_manager.appTextFontSize), "bold"), variable=ghostRooms, offvalue=False, onvalue=True)
    ghostRoomButton.place(x=labelX, y=nameY + int(screen_manager.winHeight/13))
    screen_manager.window.update()

    submitButton = Button(screen_manager.window, image=screen_manager.createBTNImage, bd=0, highlightthickness=0,
                              activebackground=screen_manager.backgroundColor, bg=screen_manager.backgroundColor, command=lambda: createServer(nameEntry.get(), ghostRooms))

    submitButton.place(x=int(screen_manager.winWidth/2) - int(screen_manager.joinImage.size[0]/2), y=submitY)

def createServer(name: str, isGhost: bool):
    data = handle_sends("createServer", name, str(isGhost))
    successfully = data != "later"
    if successfully:
        notify("create server", "server created successfully")
        load_screen("Home")
    


def defualt_screen(screen: str):    
    labelX = int(screen_manager.winWidth / 4)
    idEntryWidth = int(screen_manager.winWidth / 4)
    labelY = int(1.2 * screen_manager.winHeight / 4)
    submitY = labelY + int(screen_manager.winHeight / 7)
    
    match screen:
        case "Add friend":
            labelText = "Friend Email:"
            submitButtonImage = screen_manager.addBTNImage
            submitX = int(screen_manager.winWidth/2) - int(screen_manager.addImage.size[0]/2)
        case "Join Server":
            labelText = "Server ID:"
            submitButtonImage = screen_manager.joinBTNImage
            submitX = int(screen_manager.winWidth/2) - int(screen_manager.joinImage.size[0]/2)
        case "email validation":
            labelText = "Verify Code:"
            submitButtonImage = screen_manager.registerBTNImage
            submitX = int(screen_manager.winWidth/2) - int(screen_manager.addImage.size[0]/2)
        case "reset password":
            labelText = "New Password:"
            submitButtonImage = screen_manager.changeBTNImage
            submitX = int(screen_manager.winWidth/2) - int(screen_manager.changeImage.size[0]/2)
        case _:
            return

    label = Label(screen_manager.window, bg=screen_manager.backgroundColor, fg=screen_manager.secondColor, font=("Airal", screen_manager.appTextFontSize, "bold"), text=labelText)
    label.place(x=labelX, y=labelY)

    label.update()
    len = idEntryWidth + int(label.winfo_width())
    labelX = int(screen_manager.winWidth/2)-int(len/2)

    label.place(x=labelX, y=labelY)
    label.update()
    entry = Entry(screen_manager.window, bg=screen_manager.secondColor, font=("Airal", screen_manager.appTextFontSize, "bold"))
    entry.place(x=labelX + label.winfo_width(), y=labelY, width=idEntryWidth)
    entry.update()


    submitButton = Button(screen_manager.window, image=submitButtonImage, bd=0, highlightthickness=0,
                              activebackground=screen_manager.backgroundColor, bg=screen_manager.backgroundColor, command=lambda: addFriend(entry.get()))
    match screen:
        case "Join Server":
            newButton =  Button(screen_manager.window, image=screen_manager.newServerBTNImage, bd=0, highlightthickness=0,
                                    activebackground=screen_manager.backgroundColor, bg=screen_manager.backgroundColor, command=lambda: load_screen("Create Server"))
            newButton.place(x=0, y= screen_manager.winHeight - screen_manager.newServerImage.size[1])
            submitButton.config(command=lambda: joinServer(entry.get()))
        case "email validation":
            submitButton.config(command=lambda: finish_register(entry.get()))
            try:
                newButton =  Button(screen_manager.window, text= "Back", bd=0, highlightthickness=0,
                                        activebackground=screen_manager.backgroundColor, bg=screen_manager.backgroundColor, command=lambda: load_screen("Create Server"))
                newButton.pack(anchor=CENTER)
            except Exception as e:
                print(e)
            newButton.update()
        case "reset password":
            submitButton.config(command=lambda: resetPassword(entry.get()))
    submitButton.place(x=submitX, y=submitY)
    screen_manager.window.update()

def resetPassword(password: str):
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
    
def joinServer(id: str):
    data = handle_sends("joinServer", id)
    successfully = data == "S"
    if successfully:
        notify("joined server", "joined successfully to server")
        load_screen("Home")
    else:
        notify("joined failed", data)


def close():
    # handle_client("close")
    screen_manager.window.destroy()

def main():
    global sock, resulations, isUser, screen_manager

    isUser = False
    sock = socket.socket()
    sock.connect((ip, port))
    # sock.settimeout(10)

    window.update()
    current_res = "fullscreen"
    screen_manager = ScreenManager(window, current_res)

    screen_manager.window.resizable(False, False)
    screen_manager.window['background'] = screen_manager.backgroundColor

    screen_manager.window.update()

    change_screen_resulation("login", "fullscreen")

    resulations = getResulations(screen_manager.maxResulation)

    # graphic_t = Thread(target=loadScreen, args=("Register",))
    # graphic_t.start()

    window.mainloop()
    # graphic_t.join()

if __name__ == '__main__':
    main()