# import the opencv library
import cv2, os, socket, pygame
from PIL import Image, ImageTk
import numpy as np
from cryptography.fernet import Fernet
from pygame.locals import *

window = pygame.display.set_mode((1000, 1000))

server_address = ('127.0.0.1', 1000)

server_sock = socket.socket()
server_sock.bind(server_address)
server_sock.listen(50)
i = 0
client_sock, client_address = server_sock.accept()

while True:
    s = client_sock.recv(100000)
    print(s)
    bytes = np.frombuffer(s, np.uint8)
    
    image = cv2.imdecode(bytes, cv2.IMREAD_COLOR)
    rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pilImage = Image.fromarray(rgb_frame)

    raw_str = pilImage.tobytes("raw", "RGB")
    surface  = pygame.image.fromstring(raw_str, pilImage.size, "RGB")
    window.blit(surface, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            break
    pygame.display.update()
    print("HERE!")

    # pilImage.show()
    # cv2.imshow("a",image)
pygame.quit()