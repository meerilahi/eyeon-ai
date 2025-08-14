from langchain_core.messages import HumanMessage, SystemMessage, RemoveMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres import AsyncPostgresStore
from typing import List, Optional
from dotenv import load_dotenv
import os
load_dotenv()






class ChatbotState(MessagesState):
    summary: Optional[str] = None

system_message = SystemMessage(
    content="You are a home surveillance assistant. Help users manage security events. Use tools to perform actions like create, update, delete, or read events."
)

def update_event(state: ChatbotState):
    messages = state["messages"]
    summary = state.get("summary")
    if summary:
        context = SystemMessage(content=f"Summary of earlier conversation: {summary}")
        messages = [context] + messages
    response = llm.invoke(messages)
    return {"messages": [response]}

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

def should_continue(state: ChatbotState):
    if len(state["messages"]) > 6:
        return "summarize_conversation"
    return END

builder = StateGraph(ChatbotState)
builder.add_node("update_event", update_event)
builder.add_node("summarize_conversation", summarize_conversation)

builder.set_entry_point("update_event")

builder.add_edge("tools", "update_event")
builder.add_conditional_edges("update_event", should_continue)
builder.add_edge("summarize_conversation", END)

chat_graph = builder.compile(checkpointer=memory)

async def run_chatbot_agent(message: str, user_id: str) -> str:
    input_msg = HumanMessage(content=message)
    config = {"configurable": {"thread_id": user_id}}

    result = await chat_graph.ainvoke({"messages": [input_msg],"user_id" : user_id}, config )
    messages: List = result["messages"]

    response =  messages[-1].content if messages else "No response generated."
    print(response)

    return response
