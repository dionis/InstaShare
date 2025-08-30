from typing import List, Optional
from supabase import create_client, Client
from models.log import Log as LogModel
from schemas.log import Log as LogSchema, LogCreate, LogUpdate
import os
from datetime import datetime


class LogService:
    def __init__(self, supabase: Client):
        #supabase_url = os.getenv("SUPABASE_URL")
        #supabase_key = os.getenv("SUPABASE_KEY")
        #self.supabase: Client = create_client(supabase_url, supabase_key)
        self.supabase: Client = supabase

    async def create_log(self, event: str, user_id: Optional[int] = None, event_description: Optional[str] = None) -> LogSchema:
        log_data = {"event": event, "user_id": user_id, "event_description": event_description, "shared_date": datetime.utcnow()}
        data, count = self.supabase.from_('logs').insert(log_data).execute()
        return LogModel(**data[1][0])

    async def list_logs(self, offset: int = 0, limit: int = 100) -> List[LogSchema]:
        data, count = self.supabase.from_('logs').select("*", count='exact').range(offset, offset + limit - 1).execute()
        return [LogModel(**item) for item in data[1]]

    async def get_log(self, log_id: int) -> LogSchema:
        data, count = self.supabase.from_('logs').select("*", count='exact').eq("id", log_id).execute()
        if data[1]:
            return LogModel(**data[1][0])
        return None

    async def get_logs_by_user(self, user_id: int, offset: int = 0, limit: int = 100) -> List[LogSchema]:
        data, count = self.supabase.from_('logs').select("*", count='exact').eq("user_id", user_id).range(offset, offset + limit - 1).execute()
        return [LogModel(**item) for item in data[1]]
