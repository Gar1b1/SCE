# import the opencv library
import cv2, os, socket
from PIL import Image
import numpy as np
from cryptography.fernet import Fernet
import pygame

curPath = os.getcwd()
fkey = open(curPath+"/key.txt", "rb")
key = fkey.read()
cipher = Fernet(key)
fkey.close()

ip = "127.0.0.1"
port = 1000
sock = socket.socket()
sock.connect((ip, port))
# define a video capture object
vid = cv2.VideoCapture(0)


# vid.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
# vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)
# vid.set(cv2.CAP_PROP_FPS, 15)

while True:

	# Capture the video frame
	# by frame

	# Display the resulting frame
	# the 'q' button is set as the
	# quitting button you may use any
	# desired button of your choice
	if vid.isOpened():
		ret, frame = vid.read()
		maxWidth =250
		maxHeight = 250
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
		print(f"{width=} {height=}")


		# frame = cv2.GaussianBlur(frame, (3, 3), 0)

		is_success, buf_array = cv2.imencode(".png", frame)

		s = buf_array.tostring()
		print(type(s))
		# print(bytes)
		print("---------------------------------------------\n" + f"{len(s)=}\n {s}")
		sock.send(s)
		



		







# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()