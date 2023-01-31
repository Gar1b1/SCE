from group import Group
from firebase_admin import firestore, credentials, storage
import firebase_admin

cred = credentials.Certificate("serviceAccountKey.json")
app = firebase_admin.initialize_app(cred, {'storageBucket': 'sce-e499f.appspot.com'})
db = firestore.client()
db_servers = db.collection('servers')
myGroup = Group('alongaribi123@gmail.com', True, 881283566, db_servers)
isOk = myGroup.add_text_message()