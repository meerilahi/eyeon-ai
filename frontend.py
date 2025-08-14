from http.client import HTTPException
import supabase
import os
import json
import requests
from dotenv import load_dotenv
from supabase_auth import AuthResponse
load_dotenv()

supabase = supabase.create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY"),
)

# response = supabase.auth.sign_up({"email": "meerilahidilawar@gmail.com", "password": "12345678",})
response : AuthResponse = supabase.auth.sign_in_with_password({ "email": "meerilahidilawar@gmail.com", "password": "12345678",})
session = supabase.auth.get_session()
with open("access_token.txt", "w") as f:
    f.write(session.access_token)
