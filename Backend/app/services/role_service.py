from typing import List, Optional
from supabase import create_client, Client
from models import Role as RoleModel, Log as LogModel
from schemas import Role as RoleSchema
import os
from datetime import datetime


class RoleService:
    def __init__(self, supabase_url: str = os.getenv("SUPABASE_URL"), supabase_key: str = os.getenv("SUPABASE_KEY")):
        self.supabase: Client = create_client(supabase_url, supabase_key)

    async def create_role(self, role: RoleModel) -> RoleSchema:
        data, count = self.supabase.from_('roles').insert(role.model_dump()).execute()
        return RoleModel(**data[1][0])

    async def update_role(self, role_id: int, role: RoleModel) -> RoleSchema:
        data, count = self.supabase.from_('roles').update(role.model_dump(exclude_unset=True)).eq("id", role_id).execute()
        return RoleModel(**data[1][0])

    async def delete_role(self, role_id: int) -> RoleSchema:
        data, count = self.supabase.from_('roles').update({"deleted_at": datetime.utcnow()}).eq("id", role_id).execute()
        return {"action": "deleted", "message": "Role deleted"}

    async def create_role_event(self, event: str, user_id: int, event_description: Optional[str] = None) -> RoleSchema:
        log_data = {"event": event, "user_id": user_id, "event_description": event_description}
        data, count = self.supabase.from_('logs').insert(log_data).execute()
        return LogModel(**data[1][0])
