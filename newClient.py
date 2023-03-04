from tkinter import *
import re
# create a new tkinter window


imgPath = "images/"
backgroundColor = "#040030"
secondColor = "#76E6CB"
screenSize = (800, 600)

window = Tk()

XBTNImage = PhotoImage(file=f"{imgPath}xButton.png")
homeBTNImage = PhotoImage(file=f"{imgPath}homeButton.png")
registerBTNImage = PhotoImage(file=f"{imgPath}registerButton.png")
loginBTNImage = PhotoImage(file=f"{imgPath}loginButton.png")
smallLoginImage = PhotoImage(file=f"{imgPath}smallLogin.png")
smallRegisterImage = PhotoImage(file=f"{imgPath}smallRegister.png")

global emailEntry, passwordEntry, usernameEntry

# def createHomewindow():

def register():
    global emailEntry, passwordEntry, usernameEntry
    username = usernameEntry.get()
    email = emailEntry.get()
    password = passwordEntry.get()
    passwordValidate = checkPassword(password)
    print('register')
    if passwordValidate == "valid":
        loadScreen("login")
        print("username: " + username + " email: " + email + " password: " + password)
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
    global emailEntry, passwordEntry
    email = emailEntry.get()
    password = passwordEntry.get()
    print('login')

def clearScreen():
    for widget in window.winfo_children():
        widget.destroy()

def loadRegisterScreen():
    loadScreen("register")

def loadLogingScreen():
    loadScreen("login")

def loadScreen(screen):
    global window, emailEntry, passwordEntry, usernameEntry

    clearScreen()

    winWidth = window.winfo_width()
    winHeight = window.winfo_height()
    titleWidth = 1000

    titleX = winWidth / 2 - titleWidth / 2
    emailY = 1.7 * winHeight / 4
    passwordY = emailY + 200
    labelX = winWidth / 4

    submitX = winWidth / 3 - 100
    submitY = passwordY + 150
    homeButton = Button(window, image=homeBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=loadHomeScreen)
    homeButton.place(x=0, y=0)
    xButton = Button(window, image=XBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=close)
    xButton.pack(anchor=NE)

    if screen == "register" or screen == "login":

        emailLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", 45, "bold"), text="Email:")
        emailLabel.place(x=labelX, y=emailY - 75)

        emailEntry = Entry(window, bg=secondColor, font=("Assistant", 45, "bold"))
        emailEntry.place(x=labelX, y=emailY, width=int(winWidth / 3))
        passwordLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", 45, "bold"), text="Password:")
        passwordLabel.place(x=labelX, y=passwordY - 75)
        passwordEntry = Entry(window, bg=secondColor, font=("Assistant", 45, "bold"), show="*")
        passwordEntry.place(x=labelX, y=passwordY, width=int(winWidth / 3))

        if screen == "register":
            print('registerrrrrrrrrrrrrrrrrrr')

            usernameEntry = Entry(window, bg=secondColor, font=("Assistant", 45, "bold"))
            usernameEntry.place(x=labelX, y=emailY - 200, width=int(winWidth / 3))
            usernameLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", 45, "bold"), text="Username:")
            usernameLabel.place(x=labelX, y=emailY - 200 - 75)
            titleLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", 125, "bold"), text="register")
            submitButton = Button(window, image=registerBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=register)
            getOtherLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", 35, "bold"), text="Already have account?")
            getOtherButton = Button(window, image=smallLoginImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=loadLogingScreen)

        else:
            print('login')
            titleLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", 125, "bold"), text="login")
            submitButton = Button(window, image=loginBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=register)
            getOtherLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", 35, "bold"), text="Still don't have account?")
            getOtherButton = Button(window, image=smallRegisterImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=loadRegisterScreen)
        print(submitX)
        print()
        submitButton.place(x=submitX, y=submitY)
        titleLabel.place(x=titleX, y=50, width=titleWidth)
        getOtherLabel.place(x=submitX + int(winWidth/2.5), y=submitY - 60)
        getOtherButton.place(x=submitX + int(winWidth/2.5), y=submitY)

    window.update()







def updateSize():
    global screenSize
    close()
    screenSize = (screenSize[0] + 100, screenSize[1] + 100)
    mainG()

def close():
    global window
    window.destroy()

def loadHomeScreen():
    global window, imgPath
    print('loading')

def mainG():
    global screenSize
    global window

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

