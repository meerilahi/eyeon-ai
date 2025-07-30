from langchain_core.tools import tool
from app.firebase.firestore import add_event, get_events, update_event_by_id, delete_event_by_id

@tool
def create_event(user_id: str, event_description: str):
    return add_event(user_id, {"description": event_description})

@tool
def read_events(user_id: str):
    return get_events(user_id)

@tool
def update_event(user_id: str, event_id: str, updated_description: str):
    return update_event_by_id(user_id, event_id, {"description": updated_description})

@tool
def delete_event(user_id: str, event_id: str):
    return delete_event_by_id(user_id, event_id)
