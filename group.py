import pytz
from datetime import datetime
from firebase_admin import firestore, credentials, storage

class Group():
    def __init__(self,db, owner, isGhost, dbID, fb):
        self.owner = owner
        self.isGhost = isGhost
        self.participants = [owner]
        self.TextChatRooms = []
        self.VoiceChatRooms = []
        self.dbID = dbID
        self.db = db
        self.dbLocation = self.db.collection('servers').where("ID", '==', ID)
        self.admins = [owner]
        self.timestamp_loc = pytz.timezone('Asia/Jerusalem')
        self.storage = fb.storage()


    def add_participants(self, adder, participant):
        if participant in self.participants:
            return 'participant already inside'
        if adder in self.admins:
            self.participants.append(participant)
            return 'participant added'
        return "don't have permission"

    def add_admin(self, adder, participant):
        if participant in self.admins:
            return 'participant already admin'
        if adder == self.owner:
            self.admins.append(participant)
            return 'admin set'
        return "don't have permission"

    def remove_participant(self, remover, participant):
        if participant in self.admins:
            if remover == self.owner:
                self.admins.remove(participant)
                self.participants.remove(participant)
                return "removed"
            else:
                return "don't have permission"
        if remover in self.admins:
            if not (participant in self.admins):
                return "removed"
        return "don't have permission"

    def remove_admin(self, remover, participant):
        if remover == self.owner:
            self.admins.remove(participant)
            return "removed"
        return "don't have permission"

    def add_text_message(self, participant, message):
        if participant in self.participants:
            messageObject = {'user' : participant, 'data': message, 'time': datetime.now(self.timestamp_loc), 'type' : 'text'}
            self.dbLocation.update({u'messages': firstore.ArrayUnion([messageObject])})
        else:
            return "not in group"

    def add_image_message(self, participant, image):
        isExists = False
        if participant in self.participants:
            while not isExists:
                self.storage.child("Chats/")
                letters = string.ascii_letters + string.digits
                imgID = ''.join(random.choice(letters) for i in range(length))
                img = self.storage.child(f"Chats/{imgID}")
                isExists = img.exists()[0]
            messageObject = {'user' : participant, 'data': imgID, 'time': datetime.now(self.timestamp_loc), 'type' : 'image'}
            self.dbLocation.update({u'messages': firstore.ArrayUnion([messageObject])})
        else:
            return "not in group"