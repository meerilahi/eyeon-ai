from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.models.chat import ChatRequest, ChatResponse
from app.agent.chatbot_agent import run_chatbot_agent

router = APIRouter()

@router.post("/", response_model=ChatResponse)

async def chat_with_agent(request: ChatRequest, user_id):
    try:
        reply = await run_chatbot_agent(request.message, user_id)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat: {str(e)}"
        )
