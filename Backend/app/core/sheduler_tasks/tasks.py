from app import app as celery_app

@celery_app.task
def mi_tarea_planificada(mensaje):
    print(f"La tarea planificada se ha ejecutado. Mensaje: {mensaje}")
    return f"Tarea completada con el mensaje: {mensaje}"