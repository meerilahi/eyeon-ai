from backend.firebase.firebase_init import get_firestore_db  # wrapper for firebase-admin Firestore
import uuid
from datetime import datetime

def save_event_to_firebase(event: dict):
    event_id = str(uuid.uuid4())
    event['created_at'] = datetime.utcnow().isoformat()
    get_firestore_db().collection("events").document(event_id).set(event)
    return event_id
