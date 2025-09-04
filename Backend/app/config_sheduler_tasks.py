from celery.schedules import crontab

# Broker de Celery (Redis)
broker_url = 'redis://redis-instashare:6379/0'
# Backend para almacenar los resultados (opcional)
result_backend = 'redis://redis-instashare:6379/0'

# Configuración de las tareas periódicas
# Se pueden añadir más tareas al diccionario
beat_schedule = {
    'ejecutar-tarea-cada-2-minutos': {
        # 'tasks.mi_tarea_planificada' se refiere a la tarea en el archivo tasks.py
        'task': 'tasks.mi_tarea_planificada',
        # crontab(minute='*/2') significa "cada 2 minutos"
        'schedule': crontab(minute='*/2'),
        'args': ('Hola, mundo!',) # Argumentos que se pasarán a la tarea (opcional)
    },
}