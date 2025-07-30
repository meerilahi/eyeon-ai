from app.firebase.firebase_init import get_firestore_db

db = get_firestore_db()

def add_event(user_id: str, event_data: dict):
    user_ref = db.collection("users").document(user_id)
    events_ref = user_ref.collection("events")
    events_ref.add(event_data)
    return "Event added successfully."

def get_events(user_id: str):
    user_ref = db.collection("users").document(user_id)
    events_ref = user_ref.collection("events")
    docs = events_ref.stream()
    return [doc.to_dict() | {"id": doc.id} for doc in docs]

def update_event_by_id(user_id: str, event_id: str, updated_data: dict):
    event_ref = db.collection("users").document(user_id).collection("events").document(event_id)
    event_ref.update(updated_data)
    return "Event updated successfully."

def delete_event_by_id(user_id: str, event_id: str):
    event_ref = db.collection("users").document(user_id).collection("events").document(event_id)
    event_ref.delete()
    return "Event deleted successfully."
