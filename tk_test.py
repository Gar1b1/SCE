from tkinter import *

# create a new tkinter window
window = Tk()
i = 0

def addButton():
    global i
    name = f'botton{i}'
    x = 'botton0 = Button(window, text=f"Click me!{i}")'
    exec(x)
    print('added')
    button_width = int(25 + i)
    button_height = int(25 + i)
    i = i + 25
    # configure the size and position of the button
    botton0.config(width=button_width, height=button_height)
    botton0.place(relx=0.25, rely=0.25)

imgPath = "images/"
backgroundColor = "#040030"

# bgimg = PhotoImage(file="images/background.png")
# limg = Label(window, i=bgimg)

window['background'] = backgroundColor
# create a button widget
window.geometry("800x600")
homeBTNImage = PhotoImage(file=f"{imgPath}homeBTN.png")
img_label= Label(image=homeBTNImage)
homeButton = Button(window, image=homeBTNImage, bd=0, highlightthickness=0, activebackground=backgroundColor, command=addButton).pack(anchor=SW)

# limg.pack()

# calculate the desired size of the button as half of the window size


# run the main event loop
window.mainloop()
