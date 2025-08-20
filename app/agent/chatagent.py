import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg import AsyncConnection
from psycopg.rows import dict_row
from app.db.crud import get_supabase_client

load_dotenv()

# Constants
MODEL_SYSTEM_MESSAGE = """You are an AI assistant that helps users manage their home security system.
You can update the user's active monitoring events based on their requests.
Camera descriptions (read-only, do not change):
{cameras}
Current active events (editable):
{active_events}
INSTRUCTIONS:
1. Identify any updates to the active events list:
    - Add new events explicitly mentioned by the user.
    - Remove events that the user explicitly requests to stop monitoring.
    - Modify existing events if the user provides new details."""

# Initialize clients
supabase = get_supabase_client()
llm = ChatOpenAI(model="gpt-4o", temperature=0)

@tool
def update_active_events_tool(active_events: list[str], user_id: str) -> str:
    """Updates the active events list and saves it to Supabase."""
    supabase.upsert_active_events(user_id=user_id, active_events=active_events)
    return f"Active events updated for user {user_id}."

llm_with_tools = llm.bind_tools([update_active_events_tool])

class AgentState(MessagesState):
    user_id: str
    thread_id: str

def chat_node(state: AgentState):
    cameras = supabase.get_active_cameras(user_id=state["user_id"])
    active_events = supabase.get_active_events(user_id=state["user_id"])[0]['events']
    
    system_message = SystemMessage(
        content=MODEL_SYSTEM_MESSAGE.format(cameras=cameras, active_events=active_events)
    )
    
    messages = [system_message] + state["messages"]
    ai_reply = llm_with_tools.invoke(messages, config={"configurable": {"thread_id": state["thread_id"]}})
    
    return {"messages": state["messages"] + [ai_reply]}

# Build and compile graph
graph_builder = StateGraph(AgentState)
graph_builder.add_node("chat", chat_node)
graph_builder.add_node("tools", ToolNode(tools=[update_active_events_tool]))
graph_builder.add_edge(START, "chat")
graph_builder.add_conditional_edges("chat", tools_condition)
graph_builder.add_edge("tools", "chat")

async def initialize_agent():
    """Initialize the agent with database connection."""
    conn = await AsyncConnection.connect(
        os.getenv("SUPABASE_CONNECTION_STRING"), 
        autocommit=True, 
        prepare_threshold=0, 
        row_factory=dict_row
    )
    memory = AsyncPostgresSaver(conn=conn)
    await memory.setup()
    return graph_builder.compile(checkpointer=memory)

async def run_chat_agent(message: str, user_id: str, thread_id  :str) -> str:
    """Run the chat agent and return the response."""
    agent = await initialize_agent()
    
    result = await agent.ainvoke(
        {"messages": [HumanMessage(content=message)], "user_id": user_id, "thread_id": thread_id},
        config={"configurable": {"thread_id": thread_id}}
    )
    
    # Log conversation
    for msg in result["messages"]:
        if isinstance(msg, HumanMessage):
            print(f"User: {msg.content}")
        elif isinstance(msg, AIMessage):
            print(f"AI: {msg.content}")
    
    return result["messages"][-1].content if result["messages"] else "No response generated."