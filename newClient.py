import cv2, time, socket, ctypes
import sounddevice as sd
from scipy.io.wavfile import write
from threading import Thread
import PIL.Image as P
import io
import numpy
import firebase_admin
from tkinter import *
import hashlib

global server, username, current_chat, graphic_thread, screen, current_screen, window
first = True
current_chat = 'i'
username = 'b'
toUseCamera = True
toUseMicrophone = True
ip = '127.0.0.1'
port = 1234
# user32 = ctypes.windll.user32
# screen_size = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
screen_size = (1920, 1080)
colors = {'yellow': (246, 255, 0), 'blue': (0, 0, 255), 'red': (255, 0, 0),
          'green': (0, 255, 0), 'black': (0, 0, 0), 'white': (255, 255, 255),
          'orange': (255, 125, 0), 'pink': (200, 50, 144), 'purple': (112, 9, 222)}
imgPath = "images/"
backgroundColor = "#040030"


def manage_camera():
    global toUseCamera
    webcam = cv2.VideoCapture(0)
    webcam.set(3, 640)
    webcam.set(4, 480)
    print(webcam.get(3), webcam.get(4))
    while toUseCamera:
        print(True)
        ret, frame = webcam.read()
        cv2.imwrite('my_webcam.png', frame)
        with open('my_webcam.png', 'rb') as img:
            img_data = img.read()
            print(len(img_data))
            server.send(f'{current_chat}|camera|{username}|'.encode() + img_data + '~'.encode())

    webcam.release()


def manage_microphone():
    pass


def init_screen():
    global screen, font, current_screen, window
    window = Tk()
    load_screen_first('login')


def load_screen_first(screen_img):
    global current_screen, first, window
    for widget in window.winfo_children():
        widget.destroy()
    first = True
    current_screen = screen_img
    window.geometry("1280x720")
    window['background'] = backgroundColor
    homeBTNImage = PhotoImage(file=f"{imgPath}homeBTN.png")
    img_label = Label(image=homeBTNImage)
    homeButton = Button(window, image=homeBTNImage, bd=0, highlightthickness=0, c).pack(anchor=SW)
    window.mainloop()
    # for widget in window.winfo_children():
    #     widget.destroy()
    # window.mainloop()
    Tk.destroy()


def load_screen(screen_img):
    global current_screen, first
    current_screen = screen_img
    window.mainloop()


def login(email, password):
    password = hashlib.md5(password.encode()).hexdigest()
    server.send(f'login|{email}|{password}'.encode())


def handle_graphic():
    global first
    init_screen()
    while True:
        if current_screen == 'login':
            if first:
                print(True)
                typed_email = ''
                typed_password = ''
                ts_password = ''
                first = False

def main():
    global server, graphic_thread
    server = socket.socket()
    # server.connect((ip, port))

    string = ''
    i = 0
    while i < 1000000:
        i += 1
        print
        # print(i)
        string += 'a'
    print(len(string))

    string += string
    string += string
    string += string

    # server.send(string.encode())
    print('sent')
    graphic_thread = Thread(target=handle_graphic())
    graphic_thread.start()
    # # manage_camera()

    graphic_thread.join()


if __name__ == '__main__':
    main()

# create a button widget
button = Button(window, text="Click me!")
window.geometry("800x600")
homeBTNImage = PhotoImage(file=f"{imgPath}homeBTN.png")
img_label = Label(image=homeBTNImage)

homeButton = Button(window, image=homeBTNImage, bd=0, highlightthickness=0).pack(anchor=SW)

# limg.pack()

# calculate the desired size of the button as half of the window size
button_width = int(window.winfo_width() * 0.5)
button_height = int(window.winfo_height() * 0.5)

# configure the size and position of the button
button.config(width=button_width, height=button_height)
button.place(relx=0.25, rely=0.25)

# run the main event loop
