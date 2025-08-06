from firebase_admin import auth
from fastapi import HTTPException, status, Header


async def verify_firebase_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Firebase ID token")