from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from agents.chat_agent.planner import parse_event_from_instruction
from agents.chat_agent.firebase_writer import save_event_to_firebase

def chat_node(state):
    user_input = state['messages'][-1]['content']
    event = parse_event_from_instruction(user_input)
    return {"event": event, "messages": add_messages(state, [{"role": "assistant", "content": str(event)}])}

def write_to_firebase_node(state):
    event = state['event']
    event_id = save_event_to_firebase(event)
    return {"messages": add_messages(state, [{"role": "assistant", "content": f"✅ Event saved with ID: {event_id}"}])}

def build_chat_agent_graph():
    builder = StateGraph()
    builder.add_node("Chat", chat_node)
    builder.add_node("SaveEvent", write_to_firebase_node)

    builder.set_entry_point("Chat")
    builder.add_edge("Chat", "SaveEvent")
    builder.add_edge("SaveEvent", END)

    return builder.compile()
