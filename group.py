import sys, pytz, string, random, os
from datetime import datetime
from firebase_admin import firestore, storage

class Group:
    def __init__(self, owner, isGhost, dbID, fb):
        self.owner = owner
        self.isGhost = isGhost
        self.participants = [owner]
        self.TextChatRooms = []
        self.VoiceChatRooms = []
        self.dbID = dbID
        self.db = fb.collection('servers').document(dbID)
        self.admins = [owner]
        self.timestamp_loc = pytz.timezone('Asia/Jerusalem')
        self.storage = storage.bucket()

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

    def add_text_message(self, participant, message, chat):
        locRoom = self.db.collection("chats").document(chat).get()
        if not locRoom.exists():
            return "room not found"
        locRoom = locRoom.to_dict()["messages"]

        if participant in self.participants:
            msgID = self.__get_id_for_message()
            messageObject = {'user': participant, 'data': message, 'time': datetime.now(self.timestamp_loc), 'type': 'text', 'msgID': msgID}
            locRoom.update({u'messages': firestore.ArrayUnion([messageObject])})
            return "added"
        else:
            return "not in group"

    def add_image_message(self, participant, image, chat):
        locRoom = self.db.collection("chats").document(chat).get()
        if not locRoom.exists():
            return "room not found"
        locRoom = locRoom.to_dict()["messages"]

        if participant in self.participants:
            msgID = self.__get_id_for_message()
            messageObject = {'user': participant, 'data': msgID, 'time': datetime.now(self.timestamp_loc), 'type': 'image', 'msgID': msgID}
            locRoom.update({u'messages': firestore.ArrayUnion([messageObject])})
            imageLoc = f'imagesToUpload/{chat}/{imgID}'
            with open(imageLoc, 'x+') as file:
                file.write(image)
            file.close()
            blob = self.storage.blob(f'chats/{chat}/{imgID}')
            blob.upload_from_filename(imageLoc)
            os.remove(imageLoc)
            return "added"
        else:
            return "not in group"

    def delete_message(self, participant, messageID):  # TODO: find how to delete file in firebase storage.
        messages = self.get_messages()
        if participant in self.participants:
            for m in messages:
                if m["msgID"] == messageID:
                    if (messages[m]["user"] in participant) or (participant == self.owner) or (participant in self.admins and not (messages[m]["user"] in self.admins)):
                        self.db.update({u'messages': firestore.ArrayRemove([m])})
                        return "deleted successfully"
                    else:
                        return "don't have permission"
        return "error"

    def get_messages(self):
        return self.db.get().to_dict()['messages']

    def __get_id_for_message(self):
        characters = string.ascii_letters + string.digits
        isExist = True
        msgID = ''
        while isExist:
            a = self.db.get()
            msgID = ''.join(random.choice(characters) for i in range(random.randrange(255)))
            if a.exists:
                a = a.to_dict()
                messages = a['messages']
                for message in messages:
                    if message['ID'] == msgID:
                        isExist = True
                        break
                    else:
                        isExist = False
        if msgID == '':
            return 'ERROR'
        return msgID
