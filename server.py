import contextvars
import socket, firebase_admin, random, string, pyperclip as cb
import time, hashlib, re, json
from threading import Thread
from datetime import datetime
from pytz import timezone
from cryptography.fernet import Fernet
from firebase_admin import firestore, credentials, storage
from hashlib import md5
from email.message import EmailMessage
import ssl, smtplib

#email
global reciver

#email sender
email_sender = "sceprojectc@gmail.com"
email_password = "fpiskvcmlmhyifxj"

# encrypt
fKey = open("key.txt", "rb")
key = fKey.read()
cipher = Fernet(key)
fKey.close()

emailT = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

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

    def run(self):
        while True:
            self._receiver()

    def _receiver(self):
        bd = self.sock.recv(1024)
        bd = cipher.decrypt(bd)
        data = bd.decode("utf-8")
        self._handle_messages(data)
    
    def _handle_messages(self, data: str):
        try:
            if "&" in data:
                s_data = data.split('&')
                data = s_data[0]
                s_data = data.split('|')
                print(f"{s_data=}")
                self._handle_requests(s_data)
            else:
                self._handle_sends("error", "message received unclearly")
        except:
            print("error")
            self.sock.send(cipher.encrypt("error".encode()))
        time.sleep(0.01)

    def _handle_requests(self, data: list):
        match data[0]:
            case "login":
                self._handle_sends(data[0], self._login(email=data[1], password=data[2]), data[1])
            case "register":
                self._handle_sends(data[0], self._register(email=data[2], password=data[3], username=data[1]), data[2])
            case "finish register":
                self._handle_sends(data[0], self._finish_register(verificationCode=data[1]))
            case "getServers":
                self._handle_sends(data[0], self._get_servers())
            case "getFriends":
                self._handle_sends(data[0], self._get_friends())
            case "loadServer":
                self._handle_sends(data[0], self._load_server_rooms(server=data[1]))
            case "logout":
                self._handle_sends(data[0], self._logout())
            case "joinServer":
                self._handle_sends(data[0], self._join_server(data[1]))
            case "createServer":
                self._handle_sends(data[0], self._create_server(data[1], data[2]))
            case "change username":
                self._handle_sends(data[0], self._change_username(data[1]))
            case "change password":
                self._handle_sends(data[0], self._change_password(data[1]))
            case "send verification":
                self._handle_sends(data[0], self._send_verification_email(data[1]))
            case "verify email":
                self._handle_sends(data[0], self._verify_email(data[1]))
            case "reset password":
                self._handle_sends(data[0], self._reset_password(data[1]))



    def _verify_email(self, code):
        print(code, self.verifyCode)
        return "successfully" if code == self.verifyCode == code else "wrong code"

    def _send_verification_email(self, reciver):
        subject = "reset password confirmation email"
        verifyCode = (''.join(random.choices(string.ascii_lowercase + string.digits, k=10)))
        self.verifyCode = verifyCode
        message = f"your verify code is: {verifyCode}"
        self.email = reciver
        return self._send_email(reciver, subject, message)

    def _change_username(self, new_username):
        print(new_username)
        if not self.user.get().exists:
            return "user is not exists"
        self.user.update({u'username': new_username})
        return "successfully"
    
    def _change_password(self, password):
        print(password)
        if not self.user.get().exists:
            return "user is not exists"
        print(password)
        validate = self._check_is_password_valid(password)
        if not validate[0] ==  True:
            print(f"{validate=}")
            return f"password is not valid|{validate[1]}"
        print("r u ok?")
        password = hashlib.md5(password.encode()).hexdigest()
        self.user.update({"password": password})
        return "successfully"
    
    def _reset_password(self, password):
        user = db.collection('users').document(self.email)
        user2 = user.get()
        if not user2.exists:
            return "user is not exists"
        password = hashlib.md5(password.encode()).hexdigest()
        user.update({"password": password})
        return "successfully"
        
    
    def _get_friends(self):
        print("here??????????????????????????????????")
        if self.user != None:
            # print(self.user.get().to_dict()["friends"])
            friendsID = self.user.get().to_dict()["friends"]
            friendsDict = {}
            for friendID in friendsID:
                f = db.collection('servers').document(friendID).get()
                if f.exists:
                    friendsDict[friendID] = (f.to_dict()["username"])
            return friendsDict
            
        else:
            return "ERR"

    def _create_server(self, serverName, isGhost):
        userDict = self.user.get().to_dict()
        i = 0
        while True:
            serverID = (''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=15)))
            server = db.collection('servers').document(serverID).get()
            if not server.exists:
                break
            if i >= 100:
                return "later"
            i+=1
        email = userDict['email']
        data = {'serverID': serverID, 'ownerID': email, 'serverName': serverName, 'membersID': [email], 'adminsID': [email], 'isGhost': bool(isGhost)}
        self.user.update({u'servers': firestore.ArrayUnion([f'{serverID}'])})
        db.collection('servers').document(serverID).set(data)
        mainRoomData = {"name": "mainRoom", "type": "text", "messages": []}
        db.collection('servers').document(serverID).collection('rooms').document("mainRoom").set(mainRoomData)
        return serverID

    def _login(self, email: str, password: str) -> bool:
        user = db.collection('users').document(email)
        user2 = user.get()
        if user2.exists:
            userDict = user2.to_dict()
            print(userDict)
            password = hashlib.md5(password.encode()).hexdigest()
            if userDict['password'] == password:
                print(userDict)
                self.user = user
                return True
        return False

    def _logout(self):
        self.user = None
        return True
        
    def _register(self, email: str, username: str, password: str) -> bool:
        user = db.collection('users').document(email).get()
        if user.exists:
            return "email already exists"
        validate = self._check_is_password_valid(password)
        if not validate[0]:
            print(f"{validate=}")
            return f"password is not valid|{validate[1]}"
        if not self._check_is_email_valid(email):
            return f"email is not valid"
        if self._approve_email(email) == "email went wrong":
            return "email went wrong, please try again"
        print("here please please please work")
        self.email = email
        self.password = password
        self.username = username
        return "successfully"
    
    def _finish_register(self, verificationCode):
        if self.email != None and self.password != None and self.username != None and self.verifyCode != None:
            print(f"{self.email}, {self.password},  {self.username}, {self.verifyCode}")
            if self.verifyCode == verificationCode:
                print("here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                password = hashlib.md5(self.password.encode()).hexdigest()
                email = self.email
                username = self.username
                data = {'email': email, 'username': username, 'password': password, 'friends': [], 'servers': []}
                db.collection('users').document(email).set(data)
                self.user = db.collection('users').document(email)
                print("here1")
                self.email = None
                self.password = None
                self.username = None
                self.verifyCode = None
                print("here2")
                return "successfully"
            else:
                return "wrong verification code"
        else:
            return "ERR"
    
    def _approve_email(self, reciver):
        subject = "register confirmation email"
        verifyCode = (''.join(random.choices(string.ascii_lowercase + string.digits, k=10)))
        self.verifyCode = verifyCode
        print('here1')
        message = f"your verify code is: {verifyCode}"
        return self._send_email(reciver, subject, message)
    
    def _send_email(self, reciver, subject, message):
        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = reciver
        em["Subject"] = subject
        em.set_content(message)
        print('here2')
        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, reciver, em.as_string())
                print(f"email sent to: {reciver}")
        except Exception as e:
            print(e)
            return "email went wrong"
        return "email sent"


    def _join_server(self, id: str):
        server = db.collection('servers').document(id)
        server2 = server.get()
        if self.user == None:
            return "user not found"
        if not server2.exists:
            return "server not found"
        userDict = self.user.get().to_dict()
        email = userDict['email']
        if email in server2.to_dict()["membersID"]:
            return "user already in server"
        self.user.update({u'servers': firestore.ArrayUnion([f'{id}'])})
        server.update({u'membersID': firestore.ArrayUnion([f'{email}'])})
        return "successfully"        
    
    def _load_server_rooms(self, server: str) -> list:
        rooms = db.collection("servers").document(server).collection("rooms").get()
        for room in rooms:
            print(room.to_dict())
        return(rooms)

    def _is_password_valid(self, password: str) -> str:
        if len(password) < 6:
            return "Too Short"
        elif re.search('[0-9]', password) is None:
            return "No Digits"
        elif re.search('[a-z]', password) is None and re.search('[A-Z]', password) is None:
            return "No Letters"
        else:
            return "valid"

    def _check_is_password_valid(self, password: str):
        cp = self._is_password_valid(password)
        return True if cp == "valid" else False, cp
    
    def _check_is_email_valid(self, email: str):
        return re.fullmatch(emailT, email)

    def _get_servers(self):
        if self.user != None:
            serversID = self.user.get().to_dict()["servers"]
            serversDict = {}
            for serverID in serversID:
                s = db.collection('servers').document(serverID).get()
                if s.exists:
                    serversDict[serverID] = (s.to_dict()["serverName"])
            return serversDict
        else:
            return "ERR"

    def _handle_sends(self, type: str, *params) -> bool:
        print("pls work")
        print(f'{type=} | {params=}')
        match type:
            case "login":
                toSend = "{type}|" + ("successfully" if params[0] else "failed") + f"|{params[1]}"
            case "logout":
                toSend = "{type}|" + ("successfully" if params[0] else "failed")
            case "getServers":
                toSend = f"{type}|{json.dumps(params[0])}"
            case "getFriends":
                toSend = f"{type}|{json.dumps(params[0])}"
            case "loadServer":
                toSend = f"{type}|{json.dumps[params[0]]}"
            case _:
                toSend = f"{type}|{params[0]}"

        self.sock.send(cipher.encrypt(toSend.encode()))
        print(f"{toSend=}")
        return True

def handle_client(sock, addr):
    c = ClientHandler(sock=sock)
    c.run()

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