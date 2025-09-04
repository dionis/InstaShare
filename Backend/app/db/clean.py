from sqlalchemy.orm import Session
from sqlalchemy import text
from db.base import Base, engine

def clean_db_tables(db: Session):
    print("Cleaning database tables...")
    
    # Disable foreign key checks for PostgreSQL
    # Note: For SQLite, you would use PRAGMA foreign_keys = OFF;
    # For PostgreSQL, we might need to handle dependencies manually or use specific commands.
    # SQLAlchemy's Base.metadata.sorted_tables gives us tables in dependency order for creation.
    # We will delete in reverse order to respect foreign key constraints.
    
    # For a robust solution in PostgreSQL, consider: 
    # ALTER TABLE <table_name> DISABLE TRIGGER ALL; 
    # TRUNCATE TABLE <table_name> RESTART IDENTITY CASCADE; 
    # ALTER TABLE <table_name> ENABLE TRIGGER ALL; 
    # However, for simply clearing data in reverse dependency order, this approach is simpler.

    # Get all tables defined in Base.metadata in reverse order of dependency for deletion
    for table in reversed(Base.metadata.sorted_tables):
        table_name = table.name
        try:
            print(f"Deleting data from table: {table_name}")
            db.execute(table.delete())
            db.commit()
            print(f"Successfully deleted data from table: {table_name}")
        except Exception as e:
            db.rollback()
            print(f"Error deleting data from table {table_name}: {e}")

    print("Database tables cleaned.")
