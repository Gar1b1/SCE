import socket, firebase_admin, random, string, pyperclip as cb
import time
from threading import Thread
from datetime import datetime
from pytz import timezone

from firebase_admin import firestore
from firebase_admin import credentials
from hashlib import md5
import os

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

TZ = timezone('Asia/Jerusalem')
server_address = ('127.0.0.1', 1234)
sockets_threads = []

def handle_client(socket):
    bd = socket.recv(10000000000)
    data = bd.decode("utf-8")
    print(data)
    print(str(len(data)))
    time.sleep(0.01)

    s = data.split('|')
    if s[0] == 'login':
        print(True)

def send_message(sock, type, **values):
    match type:
        case "Hello":
            sock.send('Hello, you are in'.encode())
        case _:
            sock.send('OK'.encode())

def handle_message(message, **values):
    message = message.decode('utf-8')
    split_message = message.split('|')
    type = split_message[0]
    match type:
        case 'login':
            email = message[1]
            password = message[2]
            login(email, password)
        case 'register':
            email = message[1]
            password = message[2]
            username = message[3]
            register(email, username, password)
        case 'create_server':
            user = message[1]
            server_name = message[2]
            create_server(user, server_name)
        case 'join_server':
            user = message[1]
            serverID = message[2]
            join_server(user, serverID)
        case 'add_admin':
            user = message[1]
            serverID = message[2]
            newAdminID = message[3]
            add_admin(user, serverID, newAdminID)
        case 'add_message':
            user = message[1]
            serverID = message[2]
            chatID = message[3]
            msg = message[4]
            add_message(serverID, chatID, user, msg)
        case _:
            return 'ERROR'

def login(email, password):
    user = db.collection('users').document(email).get()
    if user.exists:
        user = user.to_dict()
        print(user)
        if user['password'] == password:
            print(user)
            return user
    return 'email or password is incorrect'

def register(email, username, password):
    user = db.collection('users').document(email).get()
    if user.exists:
        return 'email already registered'
    data = {'email': email, 'username': username, 'password': password, 'friends': [], 'servers': []}
    db.collection('users').document(email).set(data)

def create_server(user, name):
    i = 0
    while True:
        serverID = (''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=20)))
        server = db.collection('servers').document(serverID).get()
        if not server.exists:
            break
        if i > 50:
            return 'error Try again later'
        i+=1
    serverName = name
    data = {'serverID': serverID, 'ownerID': user['email'], 'serverName': serverName, 'messages': [], 'members': [user['email']], 'admins': []}
    db.collection('servers').document(serverID).set(data)

def join_server(user, serverID):
    server = db.collection('servers').document(serverID).get()
    if server.exists:
        db.collection('users').document(user['email']).update({'servers': firestore.ArrayUnion([serverID])})
        db.collection('servers').document(serverID).update({'members': firestore.ArrayUnion([user['email']])})
        return 'Success'

def add_admin(user, serverID, newAdminID):
    server = db.collection('servers').document(serverID).get()
    if server.exists:
        if server['ownerID'] == user['email']:
            if not newAdminID['email'] in server['admins']:
                db.collection('servers').document(serverID).update({'admins': firestore.ArrayUnion([newAdminID['email']])})
                return 'Success'
            return 'already admin'
        return 'no permission'

def add_message(serverID, chatID, user, message):
    server = db.collection('servers').document(serverID).get()
    if server.exists:
        username = user['username']
        db.collection('servers').document('881283566').set({'messages': [{'username': username, 'message': message, 'timestamp': datetime.now(TZ), 'chatID': chatID}]})


def main():
    global sockets_threads
    server_sock = socket.socket()
    server_sock.bind(server_address)
    server_sock.listen(50)
    while True:
        client_sock, client_address = server_sock.accept()
        print('connected')
        # send_message(client_sock, "Hello")
        t = Thread(target=handle_client, args=(client_sock,))
        sockets_threads.append(t)
        t.start()
    for t in sockets_threads:
        t.join()

if __name__ == '__main__':
    main()