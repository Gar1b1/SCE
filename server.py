import contextvars
import socket, firebase_admin, random, string
import time, hashlib, re, json
from threading import Thread
from datetime import datetime
from pytz import timezone
from cryptography.fernet import Fernet
from firebase_admin import firestore, credentials, storage
from hashlib import md5
from email.message import EmailMessage
import ssl, smtplib

import numpy as np


class serverData:    
    #email sender
    email_sender = "sceprojectc@gmail.com"
    email_password = "zoulqjmbhogkbcgq"

    # encrypt
    fKey = open("key.txt", "rb")
    key = fKey.read()
    cipher = Fernet(key)
    fKey.close()

    emailT = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    idToSocket = {}

    # db
    cred = credentials.Certificate("serviceAccountKey.json")
    # firebase_admin.initialize_app(cred)
    app = firebase_admin.initialize_app(cred, {'storageBucket': 'sce-e499f.appspot.com'})
    bucket = storage.bucket()
    blob = bucket.get_blob('Chats/Tie-Dye.png')
    db = firestore.client()

    TZ = timezone('Asia/Jerusalem')
    server_ip = '127.0.0.1'
    server_main_port = 3339
    sockets_threads = []

    max_in_vc = 9

    email_to_cam_frame_bytes = {}


class ClientHandler:
    def __init__(self, sock: socket.socket, sd: serverData):
        self.user = None
        self.current_server = None
        self.current_room = None
        self._in_vc_room = None
        self.sock = sock
        self.sd = sd
        self.torun = True

    def run(self):
        while self.torun:
            self._receiver()

    def _receiver(self):
        bd = self.sock.recv(1024)
        bd = self.sd.cipher.decrypt(bd)
        data = bd.decode("utf-8")
        self._handle_messages(data)
    
    def _handle_messages(self, data: str):
        try:
            if "&" in data:
                s_data = data.split('&')
                data = s_data[0]
                s_data = data.split('|')
                self._handle_requests(s_data)
            else:
                self._handle_sends("error", "message received unclearly")
        except Exception as e:
            print(f"error {e}")
            self.sock.send(self.sd.cipher.encrypt("error".encode()))
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
            case "get rooms":
                self._handle_sends(data[0], self._get_rooms(data[1]))
            case "get participants":
                self._handle_sends(data[0], self._get_participants())
            case "load text room":
                self._handle_sends(data[0], self._load_text_room(data[1]))
            case "load voice room":
                self._handle_sends(data[0], self._load_voice_room(data[1]))
            case "add message":
                self._handle_sends(data[0], self._add_message(data[1]))
            case "active camera":
                self._handle_sends(data[0], self._active_camera())
            case "hangup":
                self._handle_sends(data[0], self._hangup())
            case "addFriend":
                self._handle_sends(data[0], self._add_friend(data[1]))
            case "exit":
                self.torun = False

    def _add_friend(self, nf_id):
        if nf_id == self.email:
            return "F"
        user = self.sd.db.collection('users').document(nf_id)
        if not user.get().exists:
            return "F"
        try:
            self.user.update({u'friends': firestore.ArrayUnion([nf_id])})
            user.update({u'friends': firestore.ArrayUnion([self.email])})
        except:
            return "F"
        return "S"
    def _hangup(self):
        self.current_room.update({u'members': firestore.ArrayRemove([self.email])})
        self.current_room = None
        return "S"
        

    def _load_voice_room(self, room):
        try:
            self.current_room = self.current_server.collection("rooms").document(room)
            self.current_room.update({u'members': firestore.ArrayUnion([self.email])})
            self._in_vc_room = True
            ports = self._send_all_cams()
            ports = "*".join(ports)
            return f"S|{ports}"
        except Exception as e:
            print("error 2" + e)
            return "F"
    
    def _send_all_cams(self):
        ports = []
        self._set_vc_members()
        for member in self.inVCMembers:
            if member != self.email:
                cam_socket = socket.socket()
                cam_socket.bind((self.sd.server_ip, 0))
                camera_port = cam_socket.getsockname()[1]
                ports.append(str(camera_port))
                cam_thread = Thread(target=self._send_member_cam, args=(member, cam_socket))
                cam_thread.start()
        return ports
    
    def _send_member_cam(self, email: str, sock: socket.socket):
        sock.listen(1)
        cli_sock, _ = sock.accept()
        while self._in_vc_room:
            try:
                time.sleep(1/30)
                cam_frame = self.sd.email_to_cam_frame_bytes[email]
                cam_len = len(cam_frame)
                cam_len = str(cam_len).zfill(10)
                print("CAM LEN IS: " + cam_len)
                cli_sock.send(cam_len.encode())
                cli_sock.send(cam_frame)
            except Exception as e:
                
                print(e)
                pass

    def _active_camera(self):
        camera_socket = socket.socket()
        camera_socket.bind((self.sd.server_ip, 0))
        my_camera_port = camera_socket.getsockname()[1]
        camera_socket.listen(1)
        self.myCameraThread = Thread(target=self._self_camera_handler, args=(camera_socket,))
        self.myCameraThread.start()
        return f"S|{my_camera_port}"
    
    def _self_camera_handler(self, camera_server_socket: socket.socket):
        cam_sock, client_address = camera_server_socket.accept()
        while True:
            d = cam_sock.recv(10)
            if d == "C".encode():
                camera_server_socket.close()
                self._in_vc_room = False
                return
            try:
                length = int(d)

                print(length)
                cameraInput = b''
                while len(cameraInput) < length:
                    cameraInput = cam_sock.recv(length - len(cameraInput))
                # bytes = np.frombuffer(cameraInput, np.uint8)

                self.sd.email_to_cam_frame_bytes[self.email] = cameraInput
            except:
                camera_server_socket.close()
                return
            
            # pilImage.`s`how()
            # cv2.imshow("a",image)
            # self._send_my_camera_to_vc(cameraInput)
        

    def _set_vc_members(self):
        self.current_room = self.sd.db.collection("servers").document("iZzcJJVbsytpw3F").collection("rooms").document("mainVoiceChat")
        self.inVCMembers = self.current_room.get().to_dict()["members"]

    # def _send_my_camera_to_vc(self, cameraInput: bytes):
    #     self._set_vc_members()
    #     for m in self.inVCMembers:
    #         if not m == self.email:
    #             sock = self.sd.idToSocket(m)
    #             sock.send(cameraInput)


    def _add_message(self, message):
        try:
            messageData = {"author": self.user.get().to_dict()["email"], "data": message, "time": datetime.now(tz=timezone("Asia/Jerusalem"))}
            self.current_room.update({u'messages': firestore.ArrayUnion([messageData])})
            return "S"
        except:
            return "F"

    def _get_rooms(self, serverID):
        server = self.sd.db.collection('servers').document(serverID)
        server2 = server.get()
        if not server2.exists:
            return "F|server not exists"
        else:
            textRooms = []
            voiceRooms = []
            dictRooms = server.collection("rooms").get()
            for room in dictRooms:
                # room = room.to_dict()
                room = room.to_dict()
                if room["type"] == "text":
                    textRooms.append(room["name"])
                else:
                    voiceRooms.append(room["name"])
            self.current_server = server
            return f"S|{'*'.join(textRooms)}|{'*'.join(voiceRooms)}"

    def _verify_email(self, code):
        return "S" if code == self.verifyCode == code else "wrong code"

    def _send_verification_email(self, reciver):
        subject = "reset password confirmation email"
        verifyCode = (''.join(random.choices(string.ascii_lowercase + string.digits, k=10)))
        self.verifyCode = verifyCode
        message = f"your verify code is: {verifyCode}"
        self.email = reciver
        return self._send_email(reciver, subject, message)

    def _change_username(self, new_username):
        if not self.user.get().exists:
            return "user is not exists"
        self.user.update({u'username': new_username})
        return "S"
    
    def _change_password(self, password):
        if not self.user.get().exists:
            return "user is not exists"
        validate = self._check_is_password_valid(password)
        if not validate[0] ==  True:
            return f"password is not valid|{validate[1]}"
        password = hashlib.md5(password.encode()).hexdigest()
        self.user.update({"password": password})
        return "S"
    
    def _reset_password(self, password):
        user = self.sd.db.collection('users').document(self.email)
        user2 = user.get()
        if not user2.exists:
            return "user is not exists"
        password = hashlib.md5(password.encode()).hexdigest()
        user.update({"password": password})
        return "S"
        
    
    def _get_friends(self):
        if self.user != None:
            friendsID = self.user.get().to_dict()["friends"]
            friendsDict = {}
            for friendID in friendsID:
                f = self.sd.db.collection('servers').document(friendID).get()
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
            server = self.sd.db.collection('servers').document(serverID).get()
            if not server.exists:
                break
            if i >= 100:
                return "later"
            i+=1
        email = userDict['email']
        data = {'serverID': serverID, 'ownerID': email, 'serverName': serverName, 'membersID': [email], 'adminsID': [email], 'isGhost': bool(isGhost)}
        self.user.update({u'servers': firestore.ArrayUnion([f'{serverID}'])})
        self.sd.db.collection('servers').document(serverID).set(data)
        mainRoomData = {"name": "mainRoom", "type": "text", "messages": []}
        self.sd.db.collection('servers').document(serverID).collection('rooms').document("mainRoom").set(mainRoomData)
        mainRoomData = {"name": "mainVoiceRoom", "type": "voiceChat", "members": []}
        self.sd.db.collection('servers').document(serverID).collection('rooms').document("mainVoiceRoom").set(mainRoomData)
        return serverID

    def _login(self, email: str, password: str) -> bool:
        user = self.sd.db.collection('users').document(email)
        user2 = user.get()
        if user2.exists:
            userDict = user2.to_dict()
            password = hashlib.md5(password.encode()).hexdigest()
            if userDict['password'] == password:
                self.user = user
                self.email = email
                self.sd.idToSocket[email] = self.sock
                return "S"
        return "F"

    def _logout(self):
        self.user = None
        return "S"
        
    def _register(self, email: str, username: str, password: str) -> bool:
        user = self.sd.db.collection('users').document(email).get()
        if user.exists:
            return "email already exists"
        validate = self._check_is_password_valid(password)
        if not validate[0]:
            return f"password is not valid|{validate[1]}"
        if not self._check_is_email_valid(email):
            return f"email is not valid"
        if self._approve_email(email) == "email went wrong":
            return "email went wrong, please try again"
        self.email = email
        self.password = password
        self.username = username
        self.sd.idToSocket[email] = self.sock
        return "S"
    
    def _finish_register(self, verificationCode):
        if self.email != None and self.password != None and self.username != None and self.verifyCode != None:
            if self.verifyCode == verificationCode:
                password = hashlib.md5(self.password.encode()).hexdigest()
                email = self.email
                username = self.username
                data = {'email': email, 'username': username, 'password': password, 'friends': [], 'servers': []}
                self.sd.db.collection('users').document(email).set(data)
                self.user = self.sd.db.collection('users').document(email)
                self.email = None
                self.password = None
                self.username = None
                self.verifyCode = None
                return "S"
            else:
                return "wrong verification code"
        else:
            return "ERR"
    
    def _approve_email(self, reciver):
        subject = "register confirmation email"
        verifyCode = (''.join(random.choices(string.ascii_lowercase + string.digits, k=10)))
        self.verifyCode = verifyCode
        message = f"your verify code is: {verifyCode}"
        return self._send_email(reciver, subject, message)
    
    def _send_email(self, reciver, subject, message):
        em = EmailMessage()
        em["From"] = self.sd.email_sender
        em["To"] = reciver
        em["Subject"] = subject
        em.set_content(message)
        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(self.sd.email_sender, self.sd.email_password)
                smtp.sendmail(self.sd.email_sender, reciver, em.as_string())
        except Exception as e:
            print(e)
            return "F"
        return "S"


    def _join_server(self, id: str):
        server = self.sd.db.collection('servers').document(id)
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
        return "S"        
    
    def _get_participants(self):
        try:
            ids = self.current_server.get().to_dict()["membersID"]
            membersUsernames = [self._load_username(id) for id in ids ]

            myEmail = self.user.get().to_dict()["email"]
            dictServer = self.current_server.get().to_dict()

            isAdmin = myEmail in dictServer["adminsID"]
            isOwner = myEmail == dictServer["ownerID"]
            return f"S|{'*'.join(membersUsernames)}|{isAdmin}|{isOwner}"
        except Exception as e:
            print("error 4" + e) 
            return f"F"

    def _load_text_room(self, room: str) -> list:
        if not self.current_server:
            return "F|server not set"
        if not self.current_server.get().exists:
            return "F|server not exists"
        c_room = self.current_server.collection("rooms").document(room)
        if not c_room.get().exists:
            return "F|room not exists"
        
        messages = c_room.get().to_dict()["messages"]

        messages.sort(key= lambda x:x["time"])
        
        d_messages = []

        myEmail = self.user.get().to_dict()["email"]

        
        for message in messages:
            del message["time"]
            message["author"] = json.dumps({"isMy": message["author"] == myEmail, "username":self._load_username(message["author"])})

            d_messages.append(json.dumps(message))
            
        self.current_room = c_room

        self._in_vc_room = False

        return f"S|{'*'.join(d_messages)}"
    
    def _load_username(self, email):
        user = self.sd.db.collection('users').document(email).get()
        if user.exists:
            return user.to_dict()["username"]
        else:
            return "deleted user"        
        

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
        return re.fullmatch(self.sd.emailT, email)

    def _get_servers(self):
        if self.user != None:
            serversID = self.user.get().to_dict()["servers"]
            serversDict = {}
            for serverID in serversID:
                s = self.sd.db.collection('servers').document(serverID).get()
                if s.exists:
                    serversDict[serverID] = (s.to_dict()["serverName"])
            return serversDict
        else:
            return "ERR"
        
    def _handle_sends(self, type: str, *params) -> bool:
        if type in ["getServers", "getFriends", "loadServer"]:
            toSend = json.dumps(params[0])
        else:
            toSend = params[0]

        maxChunkLength = 99998
        toSend = '`'.encode() + self.sd.cipher.encrypt(toSend.encode())
        if len(toSend) > maxChunkLength:
            toSendList = self._split_list_to_chuncks(toSend, maxChunkLength)

            for toSendItem in toSendList[:-1]:
                self._send_message(toSendItem + "/".encode())
            toSend = toSendList[-1] 
        self._send_message(toSend + "~".encode())
        return True
    
    def _send_message(self, message):
        self.sock.send(message)
    
    
    def _split_list_to_chuncks(self, string: str, chunkLenght: int) -> list:
        chunks = []
        try:
            chunks = [string[i:i+chunkLenght] for i in range(0, len(string), chunkLenght)]
        except Exception as e:
            print("error 3" + e)
        return chunks

def handle_client(sock, addr, sd):
    c = ClientHandler(sock=sock, sd=sd)
    c.run()

def main():
    sd = serverData()
    server_sock = socket.socket()
    server_sock.bind((sd.server_ip, sd.server_main_port))
    server_sock.listen(50)
    i = 0
    while True:
        client_sock, client_address = server_sock.accept()
        # send_message(client_sock, "Hello")
        t = Thread(target=handle_client, args=(client_sock, client_address, sd))
        sd.sockets_threads.append(t)
        t.start()
        i += 1
    for t in sockets_threads:
        t.join()

if __name__ == '__main__':
    main()