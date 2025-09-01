import os
from celery import Celery
from celery.schedules import crontab
from datetime import date, datetime

from dotenv import load_dotenv
from supabase import create_client, Client
from ..db.base import get_supabase_client
from ..services.log_service import LogService
from ..schemas.log import LogCreate

load_dotenv()


appSchedulerManagement = Celery('my_tasks', 
             broker='redis://default:eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81@localhost:6379/0',
             backend='redis://default:eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81@localhost:6379/0')

@appSchedulerManagement.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    # Calls test('hello') every 10 seconds.
    #sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('hello') every 30 seconds.
    # It uses the same signature of previous task, an explicit name is
    # defined to avoid this task replacing the previous one defined.
    # sender.add_periodic_task(30.0, test.s('hello'), name='add every 30')

    # Calls test('world') every 30 seconds
    # sender.add_periodic_task(60.0*5, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     run_scheduled_compress_file_task.s('Happy Mondays!'),
    # )
    
        # Calls test('world') every 30 seconds
    sender.add_periodic_task(60.0*2, run_scheduled_compress_file_task.s('world'), expires=10)
    


@appSchedulerManagement.task
def test(arg):
    print(arg)

@appSchedulerManagement.task
def add(x, y):
    z = x + y
    print(z)
   
@appSchedulerManagement.task 
def run_scheduled_compress_file_task(arg):
    supabase: Client = get_supabase_client()
    log_service = LogService(supabase)
    
    # Log the event
    log_entry = LogCreate(
        event="Scheduled Task Execution",
        user_id=1, # Assuming a default user for scheduled tasks, or pass it as an argument
        event_description=f"Compress {arg} file execution at: {datetime.utcnow()}"
    )
    # The create_log method in LogService expects event, user_id, event_description separately
    log_service.create_log(
        event=log_entry.event, 
        user_id=log_entry.user_id, 
        event_description=log_entry.event_description
    )
    
    return f" Compress {arg} file execution at: {date.today().now}"

