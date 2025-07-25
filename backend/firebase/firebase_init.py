import firebase_admin
from firebase_admin import credentials, firestore, storage
from backend.core.config import settings

firebase_app = None
_firestore_db = None
_firebase_bucket = None

def init_firebase():
    global firebase_app, _firestore_db, _firebase_bucket
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.firebase_creds_path)
        firebase_app = firebase_admin.initialize_app(cred, {
            "storageBucket": f"{settings.firebase_project_id}.appspot.com"
        })

        _firestore_db = firestore.client()
        _firebase_bucket = storage.bucket()
        print("✅ Firebase initialized")

def get_firestore_db():
    return _firestore_db

def get_firebase_bucket():
    return _firebase_bucket
