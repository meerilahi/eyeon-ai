from langchain_core.tools import tool
from app.firebase.firestore import (
    add_event,
    get_events,
    update_event_by_id,
    delete_event_by_id
)

@tool
def create_event(user_id: str, event_description: str):
    """Create a new surveillance event to monitor."""
    return add_event(user_id, {"description": event_description})

@tool
def read_events(user_id: str):
    """Read all active surveillance events for this user."""
    return get_events(user_id)

@tool
def update_event(user_id: str, event_id: str, updated_description: str):
    """Update a specific surveillance event with a new description."""
    return update_event_by_id(user_id, event_id, {"description": updated_description})

@tool
def delete_event(user_id: str, event_id: str):
    """Delete an active surveillance event."""
    return delete_event_by_id(user_id, event_id)

# Export list of tools
tools = [create_event, read_events, update_event, delete_event]
