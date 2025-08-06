import sqlite3
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage, RemoveMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from app.agent.tools import tools
from langgraph.prebuilt import ToolNode, tools_condition
from typing import List, Optional
from dotenv import load_dotenv
load_dotenv()

# --- SQLite-backed memory checkpoint ---
db_path = "chatbot_memory.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)

# --- Language Model ---
llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# --- LangGraph State class ---
class ChatbotState(MessagesState):
    summary: Optional[str] = None

# --- Assistant Node ---
system_message = SystemMessage(
    content="You are a home surveillance assistant. Help users manage security events. Use tools to perform actions like create, update, delete, or read events."
)

def assistant_node(state: ChatbotState):
    messages = state["messages"]
    summary = state.get("summary")
    if summary:
        context = SystemMessage(content=f"Summary of earlier conversation: {summary}")
        messages = [context] + messages
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# --- Summarize Node ---
def summarize_conversation(state: ChatbotState):
    summary = state.get("summary", "")
    summary_prompt = (
        f"This is the current summary: {summary}\n\n"
        "Update the summary based on the new conversation above."
        if summary else
        "Summarize the conversation above:"
    )
    messages = state["messages"] + [HumanMessage(content=summary_prompt)]
    response = llm.invoke(messages)
    recent = state["messages"][-2:]
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]

    return {
        "summary": response.content,
        "messages": recent + delete_messages,
    }

# --- Condition: Decide whether to end or summarize ---
def should_continue(state: ChatbotState):
    if len(state["messages"]) > 6:
        return "summarize_conversation"
    return END

# --- LangGraph Construction ---
builder = StateGraph(ChatbotState)
builder.add_node("assistant", assistant_node)
builder.add_node("tools", ToolNode(tools))
builder.add_node("summarize_conversation", summarize_conversation)

builder.set_entry_point("assistant")

# Assistant node -> tool or END
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")
builder.add_conditional_edges("assistant", should_continue)
builder.add_edge("summarize_conversation", END)

# Compile with memory
chat_graph = builder.compile(checkpointer=memory)

# --- Public async function to use chatbot ---
async def run_chatbot_agent(message: str, user_id: str) -> str:
    input_msg = HumanMessage(content=message)
    config = {"configurable": {"thread_id": user_id}}

    result = await chat_graph.ainvoke({"messages": [input_msg]}, config)
    messages: List = result["messages"]

    return messages[-1].content if messages else "No response generated."
