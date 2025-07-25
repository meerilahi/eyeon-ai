from firebase_admin import firestore
from backend.firebase.firebase_init import get_firestore_db
from typing import Any

def get_state(doc_id: str) -> dict:
    doc = get_firestore_db().collection("shared_state").document(doc_id).get()
    return doc.to_dict() if doc.exists else {}

def set_state(doc_id: str, data: dict) -> None:
    get_firestore_db().collection("shared_state").document(doc_id).set(data)

def update_state(doc_id: str, updates: dict) -> None:
    print(f"update state : {get_firestore_db()}")
    get_firestore_db().collection("shared_state").document(doc_id).set(updates, merge=True)

def append_to_array(doc_id: str, array_field: str, item: Any) -> None:
    get_firestore_db().collection("shared_state").document(doc_id).update({
        array_field: firestore.ArrayUnion([item])
    })

def delete_state(doc_id: str) -> None:
    get_firestore_db().collection("shared_state").document(doc_id).delete()
