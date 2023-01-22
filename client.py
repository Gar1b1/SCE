import pygame, cv2, time, socket, ctypes
import sounddevice as sd
from scipy.io.wavfile import write
from threading import Thread
import PIL.Image as P
import io
import numpy
import firebase_admin
import hashlib

global server, username, current_chat, graphic_thread, screen, current_screen
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
    global screen, font, current_screen
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("SCE")
    load_screen_first('login')


def load_screen_first(screen_img):
    global current_screen, first
    screen_tb = pygame.image.load(f'images/{screen_img}_screen.png')
    first = True
    current_screen = screen_img
    screen.blit(screen_tb, (0, 0))
    pygame.display.flip()

def load_screen(screen_img):
    global current_screen, first
    screen_tb = pygame.image.load(f'images/{screen_img}_screen.png')
    current_screen = screen_img
    screen.blit(screen_tb, (0, 0))
    pygame.display.flip()

def login(email, password):
    password = hashlib.md5(password.encode()).hexdigest()
    server.send(f'login|{email}|{password}'.encode())

def handle_graphic():
    global first
    init_screen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        match current_screen:
            case 'login':
                if first:
                    print(True)
                    pressed = False
                    typed_email = ''
                    typed_password = ''
                    ts_password = ''
                    first = False
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()

                    if 520 <= pos[0] <= 1515:
                        if 230 <= pos[1] <= 350:
                            pressed = True
                            to_type = 'email'
                        elif 495 <= pos[1] <= 615:
                            pressed = True
                            to_type = 'password'
                    elif 800 <= pos[0] <= 1240 and 705 <= pos[1] <= 865:
                        # TODO: login
                        print('login')
                    elif 140 <= pos[0] <= 425 and 845 <= 910:
                        load_screen_first('register')
                    else:
                        to_type = False
                # print(pressed)
                if pressed:
                    # print(pressed)
                    # print(to_type)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_BACKSPACE:
                                if to_type == 'email':
                                    typed_email = typed_email[:-1]
                                elif to_type == 'password':
                                    typed_password = typed_password[:-1]
                                    ts_password = ts_password[:-1]
                            else:
                                if to_type == 'email':
                                    typed_email += event.unicode
                                else:
                                    typed_password += event.unicode
                                    ts_password += '*'
                            print(f'email: {typed_email} \n password: {typed_password}')
                            font = pygame.font.Font(pygame.font.get_default_font(), 80)
                            load_screen(current_screen)
                            typed_email = typed_email.lower()
                            os_email = font.render(typed_email, False, colors['black'])
                            os_password = font.render(ts_password, False, colors['black'])
                            screen.blit(os_email, (550, 250))
                            screen.blit(os_password, (550, 530))
                            pygame.display.flip()

            case 'register':
                font = pygame.font.Font(pygame.font.get_default_font(), 50)
                if first:
                    typed_email = ''
                    typed_password = ''
                    typed_username = ''
                    typed_verification_code = ''
                    ts_password = ''
                    to_type = False
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if 1385 <= pos[0] <= 1735 and 820 <= pos[1] <= 900:
                        load_screen_first('login')
                    elif 270 <= pos[0] <= 785 and 755 <= pos[1] <= 900:
                        # TODO: register
                        print('register')
                    elif 120 <= pos[0] <= 935:
                        if 180 <= pos[1] <= 280:
                            to_type = 'username'
                        elif 375 <= pos[1] <= 475:
                            to_type = 'email'
                        elif 565 <= pos[1] <= 665:
                            to_type = 'password'
                    elif 1320 <= pos[0] <= 1810:
                        if 320 <= pos[1] <= 420:
                            to_type = 'verification code'
                        elif 475 <= pos[1] <= 615:
                            # TODO: verify
                            print('verify')

                if to_type:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_BACKSPACE:
                                load_screen(current_screen)
                                if to_type == 'email':
                                    typed_email = typed_email[:-1]
                                elif to_type == 'password':
                                    typed_password = typed_password[:-1]
                                    ts_password = ts_password[:-1]
                                elif to_type == 'username':
                                    typed_username = typed_username[:-1]
                                elif to_type == 'verification code':
                                    typed_verification_code = typed_verification_code[:-1]

                            else:
                                if to_type == 'email':
                                    typed_email += event.unicode
                                elif to_type == 'password':
                                    typed_password += event.unicode
                                    ts_password += '*'
                                elif to_type == 'username':
                                    typed_username += event.unicode
                                else:
                                    typed_verification_code += event.unicode
                            print(f'email: {typed_email} \n password: {typed_password} \n username: {typed_username} \n verification_code: {typed_verification_code}')
                            font = pygame.font.Font(pygame.font.get_default_font(), 80)
                            typed_email = typed_email.lower()
                            load_screen(current_screen)
                            os_email = font.render(typed_email, False, colors['black'])
                            os_password = font.render(ts_password, False, colors['black'])
                            os_username = font.render(typed_username, False, colors['black'])
                            os_typed_verification_code = font.render(typed_verification_code, False, colors['black'])
                            # screen.blit(os_username, ())
                            # screen.blit(os_typed_verification_code, ())
                            screen.blit(os_email, (150, 405))
                            screen.blit(os_password, (550, 530))
                            pygame.display.flip()




def main():
    global server, graphic_thread
    server = socket.socket()
    server.connect((ip, port))

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

    server.send(string.encode())
    print('sent')
    # graphic_thread = Thread(target=handle_graphic())
    # graphic_thread.start()
    # # manage_camera()

    graphic_thread.join()


if __name__ == '__main__':
    main()
