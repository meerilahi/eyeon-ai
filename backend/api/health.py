# backend/api/health.py

from fastapi import APIRouter
from backend.firebase.shared_state import get_state, update_state

router = APIRouter()

@router.get("/health")
def health_check():
    update_state("camera_001", {"status": "active"})
    data = get_state("camera_001")
    return {"message": "healthy", "state": data}
