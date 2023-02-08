from datetime import datetime, timezone
import numpy as np
import pyrebase
import random, string, pyperclip as cb, pytz, sys
from firebase_admin import firestore, credentials, storage
import firebase_admin
import cv2, pygame
# from hashlib import md5
# import urllib.request as
from  urllib.request import urlopen as uo
import urlopen
import io

# #
cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
app = firebase_admin.initialize_app(cred, {'storageBucket': 'sce-e499f.appspot.com'})
bucket = storage.bucket()
blob = bucket.get_blob('Chats/Tie-Dye.png')
# print(d)
# img = uo(d).read()
# img_file = io.BytesIO(img)

# a = pygame.image.fromstring(d, (500, 500), 'RGBA')
# print(a)
# arr = np.frombuffer(blob.download_as_string(), np.uint8)
#
# pygame.init()
# screen = pygame.display.set_mode((400, 400))
# pygame.display.set_caption("SCE")
# screen_tb = pygame.image.load(img_file)
# screen.blit(screen_tb, (0, 0))
# pygame.display.flip()
# # cv2.waitKey(0)



# #
# # # username = 'alon2'
# # # password = md5('garibi554'.encode()).hexdigest()
# # # messages = ['a', 'b', 'd', 'j']
# # #

# a = db.collection('servers').document('881283566').collection('chat_rooms').document('')
# b = a.get()
# b = b.to_dict()
# print(b)
# messages = b['messages']
# messageID = '113'
# # print(messages)
# for m in messages:
#     if m["msgID"] == messageID:
#         # print(m)
#         # if (messages[m]["user"] in participant) or (participant == self.owner) or (participant in self.admins and not (messages[m]["user"] in self.admins)):
#         # print([messages[m]])
#         print ("deleted successfully")

global db

def update_array():
    email = 'alongaribi24@gmail.com'
    a = db.collection('servers').document('881283566')
    b = a.get().to_dict()
    print(b)
    a.update({u'participants': firestore.ArrayUnion([f'{email}'])})
    print(a.get().to_dict())
    # locRoom.update({u'messages': firestore.ArrayUnion([messageObject])})

if __name__ == '__main__':
    db = firestore.client()
    update_array()

# print(ms)
# for m in range(len(ms)):
#     # if ms[m]['ID'] == msgID:
#     #     del ms[m]
#     #     b['messages'] = ms
#     #     a.set(b)
#     msgID = '11111'
#     msg = 'pls work'
#     messageObject = {'user': 'alongaribi123@gmail.com', 'data': msg, 'time': datetime.now(pytz.timezone('Asia/Jerusalem')), 'type': 'text'}
#     a.update({u'messages': messageObject})
#
#     break
# print(ms)

# characters = string.ascii_letters + string.digits
# isExist = True
# # msgID = ''.join(random.choice(characters) for i in range(random.randrange(255)))
# ID = 110
# msgID = ''
# while isExist:
#     a = db.collection('servers').document('881283566').get()
#     ID += 1
#     msgID = str(ID)
#     if a.exists:
#         a = a.to_dict()
#         messages = a['messages']
#         print(messages)
#         for message in messages:
#             if message['ID'] == msgID:
#                 isExist = True
#                 break
#             else:
#                 isExist = False
#
# print(msgID)

# messages = self.db.get().to_dict()['messages']
# if participant in self.participants:


# print("HI:" + msgID)
# self.db.where("")
# # # # data = {'username':username, 'password':password, 'messages':messages}
# # # # email = 'alongaribi123@gmail.com'
# # # # db.collection('users').document(email).set(data)
# # #
# # # docs = db.collection('users').where("username", '==', '123').where('password', '==', password).get()
# # # for doc in docs:
# # #     print(doc.to_dict())
# # # email = 'alongaribi123@gmail.com'
# # # password = md5('garibi554'.encode()).hexdigest()
# # # user = db.collection('users').document(email).get()
# # # if user.exists:
# # #     user = user.to_dict()
# # #     print(user)
# # #     if user['password'] == password:
# # #         print(user)
# # email = 'alonaribi554@gmail.com'
# # password = md5('garibi554'.encode()).hexdigest()
# # username = '123'
# # # while True:
# # #     serverID = str(random.randint(0, 999999999))
# # #     server = db.collection('servers').document(id).get()
# # #     if not server.exists:
# # #         break
# # serverID = '881283566'
# # user = db.collection('users').document(email).get().to_dict()
# # # if user.exists:
# # #     print('email already registered')
# # # else:
# # #     data = {'email': email, 'username': username, 'password': password, 'friends': [], 'servers': []}
# # #     db.collection('users').document(email).set(data)
# # # serverName = "Garibi's server"
# # # data = {'serverID': serverID, 'ownerID': user['email'], 'serverName': serverName, 'messages': [], 'members': [user['email']], 'admins': []}
# # # db.collection('servers').document(serverID).set(data)
# #
# # # data = {'email': email, 'username': username, 'password': password, 'friends': [], 'servers': []}
# # # db.collection('users').document(email).set(data)
# #
# # server = db.collection('servers').document(serverID).get()
# # if server.exists:
# #     db.collection('users').document(user['email']).update({'servers': firestore.ArrayUnion([serverID])})
# #     db.collection('servers').document(serverID).update({'members': firestore.ArrayUnion([user['email']])})
#
# id = (''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=18)))
# print(id)
# cb.copy(id)
# print(pytz.all_timezones)

# JSTZ = pytz.timezone('Asia/Jerusalem')
# print(datetime.now(JSTZ))
# email = 'alonaribi123@gmail.com'
# user = db.collection('users').document(email).get()
# if user.exists:
#     user = user.to_dict()
#     username = user['username']
#     db.collection('servers').document('881283566').set({'messages':[{'username': username, 'message': 'hello world', 'timestamp': datetime.now(JSTZ)}]})

# firebaseConfig = {
#     "apiKey": "AIzaSyAHJ_wISRy-klYCoBmJecTJfc8ay4raHgA",
#     "authDomain": "sce-e499f.firebaseapp.com",\
#     "projectId": "sce-e499f",
#     "storageBucket": "sce-e499f.appspot.com",
#     "messagingSenderId": "408835808919",
#     "appId": "1:408835808919:web:c89beca98a2a9a11f6d3d2",
#     "measurementId": "G-2C0FFM8V7R"
# }
# firebase = pyrebase.initilize_app(firebaseConfig)
# storage = firebase.storage()
# storage.child('images/add_friend_screen.png').put('screens/add_friends.png')
