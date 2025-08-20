import os
from supabase import create_client, Client

class SupabaseClient:

    def __init__(self, supabase_client):
        self.supabase : Client = supabase_client

    def upsert_active_events(self, user_id: str, active_events: list[str]):
        try:
            self.supabase.table("active_events").upsert({"user_id": user_id, "events": active_events}).execute()
        except Exception as e:
            return f"Error parsing JSON: {e}"
        
    def get_active_events(self, user_id: str):
        try:
            response = self.supabase.table("active_events").select("events").eq("user_id", user_id).execute()
            return response.data
        except Exception as e:
            return f"Error retrieving active events: {e}"
        
    def upsert_camera(self, user_id: str, title: str, description: str, active: bool, link: str):
        try:
            self.supabase.table("connected_cameras").upsert({
                "user_id": user_id,
                "title": title,
                "description": description,
                "active": active,
                "link": link
            }).execute()
        except Exception as e:
            return f"Error upserting cameras: {e}"
        
    def get_active_cameras(self, user_id: str):
        try:
            response = self.supabase.table("connected_cameras").select("cam_id, title, description, link").eq("user_id", user_id).eq("active",True).execute()
            return response.data
        except Exception as e:
            return f"Error retrieving cameras: {e}"
            
    def upsert_scene(self, user_id: str, cam_id : str, description: str, processed: bool = False):  
        try:
            self.supabase.table("scene_analysis").upsert({
                "user_id": user_id,
                "cam_id": cam_id,
                "description": description,
                "processed": processed
            }).execute()
        except Exception as e:
            return f"Error upserting scene description: {e}"
        
    def get_unprocced_scene(self, user_id: str):
        try:
            response = self.supabase.table("scene_analysis") \
            .select("scene_id, created_at, cam_id, description, cameras(title, description)") \
            .eq("user_id", user_id) \
            .eq("processed", False) \
            .execute()
            return response.data
        except Exception as e:
            return f"Error retrieving unprocessed scene descriptions: {e}"
    
    def upsert_event_analysis(self, user_id: str, scene_id: str,  description: str, alert: bool = False, alert_issue: bool = False):
        try:
            self.supabase.table("event_analysis").upsert({
                "user_id": user_id,
                "scene_id": scene_id,
                "description": description,
                "alert": alert,
                "alert_issue": alert_issue
            }).execute()
        except Exception as e:
            return f"Error upserting event analysis: {e}"

def get_supabase_client() -> SupabaseClient:
    """Create and return a Supabase client."""
    return SupabaseClient(
        create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
    ) 