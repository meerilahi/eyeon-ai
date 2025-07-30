from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode, tools
from langchain_core.runnables import Runnable
from app.agents.tools import create_event, read_events, update_event, delete_event

# Tool definitions for the chatbot
tool_list = tools(
    [
        create_event,
        read_events,
        update_event,
        delete_event
    ]
)

# Simple conversational flow
def simple_chat_node(state):
    messages = state["messages"]
    last_msg = messages[-1].content.lower()

    # Call tools based on keyword
    if "add" in last_msg or "create" in last_msg:
        return {"tool": "create_event"}
    elif "show" in last_msg or "list" in last_msg:
        return {"tool": "read_events"}
    elif "update" in last_msg or "change" in last_msg:
        return {"tool": "update_event"}
    elif "delete" in last_msg or "remove" in last_msg:
        return {"tool": "delete_event"}
    else:
        return {"messages": messages + [AIMessage(content="Sorry, I didn’t understand. Try using keywords like add, update, delete, show.")], "next": END}

# Define state schema
class AgentState(dict):
    messages: list

# Build the LangGraph
builder = StateGraph(AgentState)
builder.add_node("router", simple_chat_node)

# ToolNode calls function based on tool name in state["tool"]
builder.add_node("tool_handler", ToolNode(tool_list))

# Define flow
builder.set_entry_point("router")
builder.add_edge("router", "tool_handler")
builder.add_edge("tool_handler", END)

# Compile graph
chat_graph: Runnable = builder.compile()

# Entry function to run chatbot
async def run_chatbot_agent(message: str, user_id: str) -> str:
    history = [HumanMessage(content=message, name=user_id)]
    result = await chat_graph.ainvoke({"messages": history})
    final_messages = result.get("messages", [])
    return final_messages[-1].content if final_messages else "No response generated."
