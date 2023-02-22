from tkinter import *

# create a new tkinter window


imgPath = "images/"
backgroundColor = "#040030"
secondColor = "#76E6CB"
screenSize = (800, 600)

global window


# def createHomewindow():

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
    window = Tk()
    XBTNImage = PhotoImage(file=f"{imgPath}XBTN.png")
    homeBTNImage = PhotoImage(file=f"{imgPath}homeBTN.png")
    window.resizable(False, False)
    window.attributes('-fullscreen', True)
    window.geometry("1280x720")
    window.update()

    window['background'] = backgroundColor

    titleX = window.winfo_width()/2
    titleWidth = 1000
    emailY = 2 * int(window.winfo_height()/4)
    passwordY = emailY + 250
    labelX = int(window.winfo_width()/4)

    homeButton = Button(window, image=homeBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, command=loadHomeScreen).place(x=0, y=0)
    xButton = Button(window, image=XBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, bg=backgroundColor, command=close).pack(anchor=NE)

    loginLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", 125, "bold"), text="login").place(x=titleX-(titleWidth/2), y=50, width=titleWidth)

    emailLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", 40, "bold"), text="Email:").place(x=labelX, y=emailY - 75)
    EmailEntry = Entry(window, bg=secondColor, font=("Assistant", 40, "bold")).place(x=labelX, y=emailY, width=int(window.winfo_width()/2))
    emailLabel = Label(window, bg=backgroundColor, fg=secondColor, font=("Assistant", 40, "bold"), text="Password:").place(x=labelX, y=passwordY - 75)
    Password = Entry(window, bg=secondColor, font=("Assistant", 40, "bold"), show="*").place(x=labelX, y=passwordY, width=int(window.winfo_width()/2))

    window.mainloop()


if __name__ == '__main__':
    mainG()

