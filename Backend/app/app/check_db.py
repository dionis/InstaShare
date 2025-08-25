import os
from sqlmodel import create_engine
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

DATABASE_URL = os.getenv("SUPABASE_URL")

if DATABASE_URL:
    DATABASE_URL = DATABASE_URL.strip() # Strip any whitespace or newline characters

if not DATABASE_URL:
    print("Error: SUPABASE_URL environment variable not set or is empty.")
else:
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            print("Successfully connected to the database!")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
