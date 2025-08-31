from celery import Celery

app = Celery('proy_celery', include=['tasks'])

# Cargar la configuración desde config.py
app.config_from_object('config')

if __name__ == '__main__':
    app.start()