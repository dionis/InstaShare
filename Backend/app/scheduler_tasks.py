from sheduler_app import app as celery_app
from db.base import get_supabase_client, create_client, Client
from services.log_service import LogService
from schemas.log import LogCreate
from dotenv import load_dotenv
from datetime import date, datetime


load_dotenv()



@celery_app.task
def mi_tarea_planificada(mssg):
    print(f"La tarea planificada se ha ejecutado. Mensaje: {mssg}")
   
    supabase: Client = get_supabase_client()
    log_service = LogService(supabase)
    
    # Log the event
    log_entry = LogCreate(
        event="Scheduled Task Execution",
        user_id=1, # Assuming a default user for scheduled tasks, or pass it as an argument
        event_description=f"Compress {mssg} file execution at: {datetime.now()}"
    )
    # The create_log method in LogService expects event, user_id, event_description separately
    log_service.create_log(
        event=log_entry.event, 
        user_id=log_entry.user_id, 
        event_description=log_entry.event_description
    )
    
    return f" Compress {mssg} file execution at: {datetime.now()}"