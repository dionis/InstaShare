from typing import List, Optional
from supabase import create_client, Client
from models.role import Role as RoleModel
from models.user import User as UserModel # Import for create_role_event if it logs user actions
from schemas.role import Role as RoleSchema, RoleCreate, RoleUpdate
from schemas.log import Log as LogSchema # Assuming role_service can create logs
import os
from datetime import datetime


class RoleService:
    def __init__(self, supabase: Client):
        #supabase_url = os.getenv("SUPABASE_URL")
        #supabase_key = os.getenv("SUPABASE_KEY")
        #self.supabase: Client = create_client(supabase_url, supabase_key)
        self.supabase: Client = supabase

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
