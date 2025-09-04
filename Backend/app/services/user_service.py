from typing import List, Optional
from supabase import create_client, Client
from models.user import User as UserModel
from models.document import Document as DocumentModel
from schemas.user import User as UserSchema, UserCreate, UserUpdate
from schemas.document import Document as DocumentSchema
from gotrue.errors import AuthApiError
#from sqlalchemy.orm import Session
import os
from datetime import datetime


class UserService:
    def __init__(self, supabase: Client):
        #supabase_url = os.getenv("SUPABASE_URL")
        #supabase_key = os.getenv("SUPABASE_KEY")
        
        #print(f"Session: {db}")
        #print(f"SUPABASE_URL: {supabase_url}")
        #print(f"SUPABASE_KEY: {supabase_key}")
        
        self.supabase: Client = supabase

    async def list_users(self, offset: int = 0, limit: int = 100) -> List[UserSchema]:
        data, count = self.supabase.from_('users').select("*, user_roles(*, roles(*))").is_("deleted_at", None).range(offset, offset + limit - 1).execute()
        users_with_roles = []
        for item in data[1]:
            user_data = {k: v for k, v in item.items() if k not in ["user_roles"]}
            user_model = UserModel(**user_data)
            user_model.role = item['user_roles'][0]['roles']['role_name'] if item['user_roles'] else None # Assign the role name
            users_with_roles.append(user_model)
        return users_with_roles

    async def get_user(self, user_id: int) -> UserSchema:
        data, count = self.supabase.from_('users').select("*, user_roles(*, roles(*))").eq("id", user_id).is_("deleted_at", None).execute()
        if data[1]:
            user_data = {k: v for k, v in data[1][0].items() if k not in ["user_roles"]}
            user_model = UserModel(**user_data)
            user_model.role = data[1][0]['user_roles'][0]['roles']['role_name'] if data[1][0]['user_roles'] else None
            return user_model
        return None

    async def create_user(self, user: UserCreate) -> UserSchema:
        try:
            # Create user in Supabase auth
            auth_response = self.supabase.auth.sign_up({
                "email": user.email,
                "password": user.password # Use the plain password for Supabase auth
            })

            if auth_response.user is None:
                raise AuthApiError("Supabase sign up failed", "", 400)

            # Hash the password for your database (this should be done before passing to service)
            # For now, let's assume user.hashed_password is already set if coming from an endpoint
            # Or, if user.password is provided, you would hash it here.
            # For simplicity, I'm using the passed hashed_password, but in a real app, hash user.password

            # Create user in your database
            user_data = user.model_dump() # Exclude password from database insert
            user_data['hashed_password'] = user.hashed_password # Ensure hashed password is used
                   
            
            data, count = self.supabase.from_('users').insert(user_data).execute()
            return UserModel(**data[1][0])
        except AuthApiError as e:
            # Handle Supabase auth errors
            print(f"Supabase Auth Error: {e}")
            raise e
        except Exception as e:
            # Handle other potential errors
            print(f"Error creating user: {e}")
            raise e

    async def update_user(self, user_id: int, user: UserModel) -> UserSchema:
        data, count = self.supabase.from_('users').update(user.model_dump(exclude_unset=True)).eq("id", user_id).execute()
        return UserModel(**data[1][0])

    async def delete_user(self, user_id: int) -> UserSchema:
        data, count = self.supabase.from_('users').update({"deleted_at":str( datetime.utcnow())}).eq("id", user_id).execute()
        return {"action": "deleted", "message": "User deleted"}

    async def get_documents_uploaded_by_user(self, user_id: int) -> list[DocumentSchema]:
        user_data, count = self.supabase.from_('users').select("*, user_roles(*, roles(*))").eq("id", user_id).is_("deleted_at", None).execute()
        
        if not user_data[1]:
            return None

        user_info = user_data[1][0]
        user_model = UserModel(**{k: v for k, v in user_info.items() if k not in ["user_roles"]})
        user_model.role = user_info['user_roles'][0]['roles']['role_name'] if user_info['user_roles'] else None

        documents_data, count = self.supabase.from_('documents').select("*").eq("uploaded_by_user_id", user_id).is_("deleted_at", None).execute() # Assuming a foreign key 'uploaded_by_user_id' in documents table
        uploaded_documents = [DocumentModel(**item) for item in documents_data[1]]

        return {
            **user_model.model_dump(),
            "upload_documents": uploaded_documents
        }

    async def assign_role_to_user(self, user_id: int, role_id: int) -> dict:
        # Check if the user and role exist
        user_exists = self.supabase.from_('users').select("id").eq("id", user_id).execute()
        role_exists = self.supabase.from_('roles').select("id").eq("id", role_id).execute()

        if not user_exists.data or not role_exists.data:
            return {"message": "User or Role not found"}

        # Create a new entry in the UserRole table
        user_role_data = {"user_id": user_id, "role_id": role_id}
        data, count = self.supabase.from_('user_roles').insert(user_role_data).execute()
        return {"message": "Role assigned successfully"}
