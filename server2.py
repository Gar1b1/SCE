import contextvars
import socket, firebase_admin, random, string, pyperclip as cb
import time, hashlib, re, json
from threading import Thread
from datetime import datetime
from pytz import timezone
from cryptography.fernet import Fernet
from firebase_admin import firestore, credentials, storage
from hashlib import md5


# encrypt
fKey = open("key.txt", "rb")
key = fKey.read()
cipher = Fernet(key)
fKey.close()

# global user

# db
cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
app = firebase_admin.initialize_app(cred, {'storageBucket': 'sce-e499f.appspot.com'})
bucket = storage.bucket()
blob = bucket.get_blob('Chats/Tie-Dye.png')
db = firestore.client()

TZ = timezone('Asia/Jerusalem')
server_address = ('127.0.0.1', 3339)
sockets_threads = []


class ClientHandler:
    def __init__(self, sock: socket):
        self.user = None
        self.current_server = None
        self.current_room = None
        self.sock = sock
        print("hello world")

    def run(self):
        while True:
            self._receiver()

    def _receiver(self):
        bd = self.sock.recv(1024)
        bd = cipher.decrypt(bd)
        print("hello world2")
        data = bd.decode("utf-8")
        self._handle_messages(data)
    
    def _handle_messages(self, data: str):
        try:
            if "&" in data:
                s_data = data.split('&')
                print(s_data)
                data = s_data[0]
                print(data)
                s_data = data.split('|')
                print(s_data)
                self._handle_requests(s_data)
            else:
                self._handle_sends("error", "message received unclearly")
        except:
            print("error")
            self.sock.send(cipher.encrypt("error".encode()))
        time.sleep(0.01)

    def _handle_requests(self, data: list):
        print("here??????????????????????????????????")
        if data[0] == "login":
            self._handle_sends(data[0], self._login(email=data[1], password=data[2]), data[1])
        elif data[0] == "register":
            self._handle_sends(data[0], self._register(email=data[2], password=data[3], username=data[1]), data[2])
        if data[0] == "getServers":
            self._handle_sends(data[0], self._get_servers())
        if data[0] == "loadServer":
            self._handle_sends(data[0], self._load_server_rooms(server=data[1]))
        if data[0] == "logout":
            print("yesssssssssssssssssssssssssssssssssssssssssssss")
            self._handle_messages(data[0], self._logout())

    def _login(self, email: str, password: str) -> bool:
        user = db.collection('users').document(email).get()
        print("imhere")
        if user.exists:
            userDict = user.to_dict()
            print(userDict)
            password = hashlib.md5(password.encode()).hexdigest()
            if userDict['password'] == password:
                print(userDict)
                self.user = user
                return True
        print("imhere2")
        return False

    def _logout(self):
        self.user = None
        return True
    
    def _register(self, email: str, username: str, password: str) -> bool:
        user = db.collection('users').document(email).get()
        if user.exists:
            return "email already exists"
        if not self._check_is_password_valid(password):
            return "password is not valid"
        password = hashlib.md5(password.encode()).hexdigest()
        data = {'email': email, 'username': username, 'password': password, 'friends': [], 'servers': []}
        db.collection('users').document(email).set(data)
        self.user = db.collection('users').document(email).get()
        return True
    
    def _load_server_rooms(self, server: str) -> list:
        print("here!!!!!!!!!!!!!!!!!!!!!!!!!!")
        rooms = db.collection("servers").document(server).collection("rooms").get()
        for room in rooms:
            print(room.to_dict)
        print(f"{rooms=}")
        return(rooms)

    def _is_password_valid(self, password: str) -> str:
        if len(password) < 6:
            return "tooShort"
        elif re.search('[0-9]', password) is None:
            return "noDigits"
        elif re.search('[a-z]', password) is None and re.search('[A-Z]', password) is None:
            return "noLetters"
        else:
            return "valid"

    def _check_is_password_valid(self, password: str) -> bool:
        cp = self._is_password_valid(password)
        return True if cp == "valid" else cp

    def _get_servers(self) -> bool:
        if self.user != None:
            serversID = self.user.to_dict()["servers"]
            serversDict = {}
            for serverID in serversID:
                s = db.collection('servers').document(serverID).get()
                if s.exists:
                    serversDict[serverID] = (s.to_dict()["name"])
            return serversDict
        else:
            return "ERR"

    def _handle_sends(self, type: str, *params) -> bool:
        print(f'{type=} | {params=}')
        match type:
            case "login":
                toSend = "loggedin|" + ("successfully" if params[0] else "failed") + f"|{params[1]}"
            case "register":
                toSend = "registered| " + ("successfully" if params[0] == True else (f"failed|" + "password" if params[0] == "password is not valid" else "email")) + f"|{params[1]}"
            case "getServers":
                toSend = f"servers|{json.dumps(params[0])}"
            case "loadServer":
                toSend = f"rooms|{json.dumps[params[0]]}"
            case "error":
                toSend = f"error|{params[0]}"
            case _:
                return False
        self.sock.send(cipher.encrypt(toSend.encode()))
        print(toSend)
        return True

def handle_client(sock, addr):
    c = ClientHandler(sock=sock)
    print(addr)
    c.run()

# def handle_client(sock):
#     while True:
#         bd = sock.recv(1024)
#         bd = cipher.decrypt(bd)

#         data = bd.decode("utf-8")
#         print(data)
#         print(str(len(data)))
#         user.set(data)
#         print(f"p: {i} d: {user.get()}")
#         try:
#             if "&" in data:
#                 s_data = data.split('&')
#                 print(s_data)
#                 data = s_data[0]
#                 print(data)
#                 s_data = data.split('|')
#                 print(s_data)
#                 sock.send(cipher.encrypt("got it".encode()))
#                 print(handle_requests(s_data))
#             else:
#                 sock.send(cipher.encrypt("error".encode()))
#         except:
#             print("error")
#             sock.send(cipher.encrypt("error".encode()))
#         time.sleep(0.01)

# def print_user():
#     global user
#     print(user.get())

# def handle_requests(data):
#     request_type = data[0]
#     print(request_type)
#     if request_type == "login":
#         email = data[1]
#         password = data[2]
#         reply = login(email, password)
#         is_error = reply[0]
#         # return message_build(request_type, is_error)

#     if request_type == "register":
#         username = data[1]
#         email = data[2]
#         password = data[3]
#         isClear = register(username, email, password)
#         print(f"is clear: {isClear}")
#         if isClear:
#             print("everything is ok??????????????")
#             print("everything is ok")
#             return "yay its works"
#     if request_type == "exit":
#         reply = exit()
#     # sock.send("ERR")
#     return

#     sock.send(reply[1])
#     if is_new_user:
#         return user
#     elif is_error:
#         return "ERROR"

# def exit():
#     return

# # def message_build(request_type, problem):
# #     toReturn = f"{request_type}|{ok}"
# #     if problem:
# #         toReturn += problem
# #     return toReturn

# def send_message(sock, type, **values):
#     # match type:
#     #     case "Hello":
#     #         sock.send('Hello, you are in'.encode())
#     #     case _:
#     #         sock.send('OK'.encode())
#     pass

# def handle_message(message, **values):
#     message = message.decode('utf-8')
#     split_message = message.split('|')
#     type = split_message[0]
#     # match type:
#     #     case 'login':
#     #         email = message[1]
#     #         password = message[2]
#     #         login(email, password)
#     #     case 'register':
#     #         email = message[1]
#     #         password = message[2]
#     #         username = message[3]
#     #         register(email, username, password)
#     #     case 'create_server':
#     #         user = message[1]
#     #         server_name = message[2]
#     #         create_server(user, server_name)
#     #     case 'join_server':
#     #         user = message[1]
#     #         serverID = message[2]
#     #         join_server(user, serverID)
#     #     case 'add_admin':
#     #         user = message[1]
#     #         serverID = message[2]
#     #         newAdminID = message[3]
#     #         add_admin(user, serverID, newAdminID)
#     #     case 'add_message':
#     #         user = message[1]
#     #         serverID = message[2]
#     #         chatID = message[3]
#     #         msg = message[4]
#     #         add_message(serverID, chatID, user, msg)
#     #     case _:
#     #         return 'ERROR'

# def login(email, password):
#     global user
#     t_user = db.collection('users').document(email).get()
#     if t_user.exists:
#         userDict = t_user.to_dict()
#         print(userDict)
#         password = md5(password.encode()).hexdigest()
#         if userDict['password'] == password:
#             print(f"the user is {userDict}")
#             return True
#     return False

# def register(username, email, password):
#     global user
#     t_user = db.collection('users').document(email).get()
#     print(f"is exist: {t_user.exists}")
#     if t_user.exists:
#         return False
#     password = md5(password.encode()).hexdigest()
#     data = {'email': email, 'username': username, 'password': password, 'friends': [], 'servers': []}
#     db.collection('users').document(email).set(data)
#     t_user = db.collection('users').document(email).get()
#     user.set(t_user)
#     return True

# def load_servers_names(user):
#     userDict = user.to_dict()
#     serversID = userDict["servers"]
#     servers = db.collection('servers')
#     names = []
#     for serverID in serversID:
#         server = servers.document(serverID).get().to_dict()
#         names.append(server[name])
#     return names


# def create_server(user, name):
#     i = 0
#     userDict = user.to_dict()
#     while True:
#         serverID = (''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=20)))
#         server = db.collection('servers').document(serverID).get()
#         if not server.exists:
#             break
#         if i > 50:
#             return 'error Try again later'
#         i+=1
#     serverName = name
#     data = {'serverID': serverID, 'ownerID': userDict['email'], 'serverName': serverName, 'messages': [], 'members': [userDict['email']], 'admins': []}
#     db.collection('servers').document(serverID).set(data)

# def join_server(user, serverID):
#     server = db.collection('servers').document(serverID).get()
#     userDict = user.to_dict()
#     if server.exists:
#         db.collection('users').document(userDict['email']).update({'servers': firestore.ArrayUnion([serverID])})
#         db.collection('servers').document(serverID).update({'members': firestore.ArrayUnion([userDict['email']])})
#         return 'Success'

# def add_admin(user, serverID, newAdminID):
#     userDict = user.to_dict()
#     server = db.collection('servers').document(serverID).get()
#     if server.exists:
#         if server['ownerID'] == userDict['email']:
#             if not newAdminID['email'] in server['admins']:
#                 db.collection('servers').document(serverID).update({'admins': firestore.ArrayUnion([newAdminID['email']])})
#                 return 'Success'
#             return 'already admin'
#         return 'no permission'

# def add_message(serverID, chatID, user, message):
#     userDict = user.to_dict()
#     server = db.collection('servers').document(serverID).get()
#     if server.exists:
#         username = userDict['username']
#         db.collection('servers').document('881283566').set({'messages': [{'username': username, 'message': message, 'timestamp': datetime.now(TZ), 'chatID': chatID}]})


def main():
    global sockets_threads
    server_sock = socket.socket()
    server_sock.bind(server_address)
    server_sock.listen(50)
    i = 0
    while True:
        client_sock, client_address = server_sock.accept()
        print('connected')
        # send_message(client_sock, "Hello")
        t = Thread(target=handle_client, args=(client_sock, client_address))
        sockets_threads.append(t)
        t.start()
        i += 1
    for t in sockets_threads:
        t.join()

if __name__ == '__main__':
    main()