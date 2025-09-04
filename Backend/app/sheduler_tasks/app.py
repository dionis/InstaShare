from celery import Celery

app = Celery('proy_celery', include=['sheduler_tasks'])

# Cargar la configuración desde config.py
app.config_from_object('config_sheduler_tasks')

if __name__ == '__main__':
    app.start()