from fastapi import APIRouter, HTTPException, status, Depends
from app.models.chat import ChatRequest, ChatResponse
from app.chatbot.chatbot import run_chatbot_agent
from app.supabase.auth import get_user

router = APIRouter()

@router.post("/", response_model=ChatResponse)

async def chat(request: ChatRequest, user: str = Depends(get_user)):
    try:
        print(f"User ID: {user.get('id')}")
        print(f"Message: {request.message}")
        reply = await run_chatbot_agent(request.message, user.get("id"))
        return ChatResponse(reply="reply")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat: {str(e)}"
        )
