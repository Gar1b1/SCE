import pygame, cv2, time, threading, socket
import sounddevice as sd
from  scipy.io.wavfile import write
import PIL.Image as P
import io
import numpy
import firebase_admin

global sock, username, current_chat
current_chat = 'i'
username = 'b'
toUseCamera = True
toUseMicrophone = True
ip = '127.0.0.1'
port = 1234


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
            sock.send(f'{current_chat}|camera|{username}|'.encode()+img_data + '~'.encode())

    webcam.release()

def manage_microphone():
    fs = 44100  # Sample rate
    seconds = 3  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write('output.wav', fs, myrecording)  # Save as WAV file


def main():
    global sock
    sock = socket.socket()
    sock.connect((ip, port))
    manage_camera()

if __name__ == '__main__':
    main()

