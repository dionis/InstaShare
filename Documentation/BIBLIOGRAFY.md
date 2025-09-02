## [FastAPI + Supabase Template for LLM SaaS Part 2 - Celery and Pg-vector](https://euclideanai.substack.com/p/fastapi-supabase-template-for-llm-941)


## Avoid error in Jest execution test

- [ts-jest-mock-import-meta AST transformer](https://github.com/ThomZz/ts-jest-mock-import-meta)


### SECRECTT KEY AND ACCES_TOKEN


- Es una confusión común y es crucial entender la diferencia para mantener la seguridad.
No, la SECRET_KEY del backend NO debe ser compartida con el frontend.
Aquí te explico los puntos clave:
SECRET_KEY (Backend):

    -   Esta clave es exclusiva del backend. Su propósito es firmar y verificar tokens JWT que tu propio backend pueda generar (por ejemplo, si tu FastAPI generara sus propios tokens de sesión, aunque en tu caso te estás apoyando en Supabase para la autenticación), o para otras operaciones criptográficas internas del servidor (como la gestión de sesiones o la encriptación de datos sensibles).

    - Nunca debe ser expuesta en el frontend porque si un atacante la obtiene, podría falsificar tokens o comprometer la seguridad de tu backend.

    - Tal como mencionaste, no está generada por la configuración de Supabase porque es una clave que tu backend utiliza para su propia seguridad.
    - Tokens de Supabase (Frontend y Backend):
        Cuando el frontend se autentica con Supabase, Supabase le devuelve un access_token (un JWT).
    
    - El frontend envía este access_token al backend en el encabezado Authorization (como ya hemos configurado con el interceptor de Axios).

  El backend (que ya has configurado para validar el token) recibe este access_token y lo verifica utilizando la clave pública de Supabase o el SDK de Supabase, no tu SECRET_KEY interna. Supabase es quien firma esos tokens con su propia clave secreta, y tu backend los valida con la clave pública correspondiente.

En resumen:
    SECRET_KEY: Secreta, solo en el backend, para la seguridad interna de tu API de FastAPI.
    access_token de Supabase: Se genera en el servidor de Supabase, se envía al frontend para que lo guarde y luego el frontend lo envía al backend para autenticar cada petición. El backend valida este token con Supabase (o su clave pública).

Lo importante es que la SECRET_KEY que te pedí añadir al .env del backend se mantenga confidencial y solo en el servidor.

## Comando para generar automaticamente el ACCES_KEY

`python -c "import secrets; print(secrets.token_urlsafe(32))"`


### Periodic Tasks

- [Current stable version of Celery (5.5). For development docs](https://docs.celeryq.dev/en/latest/userguide/periodic-tasks.html)


###"Examples"


Celery can be used to schedule tasks to run at predetermined intervals or specific times using Celery Beat. Celery Beat is a separate component of Celery that acts as a scheduler, adding tasks to the Celery queue for workers to pick up and execute.
Here's how to implement scheduled tasks with Celery: Define your Celery application and task.
Python

    from celery import Celery

    app = Celery('my_app', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

    @app.task
    def my_scheduled_task(arg1, arg2):
        # Your task logic here
        print(f"Executing scheduled task with args: {arg1}, {arg2}")

Configure Celery Beat schedule.
In your Celery configuration (e.g., celeryconfig.py or directly in your app configuration), define the CELERY_BEAT_SCHEDULE:
Python

    from celery.schedules import crontab

    app.conf.beat_schedule = {
        'run-my-scheduled-task-every-minute': {
            'task': 'your_module.my_scheduled_task',  # Path to your task
            'schedule': crontab(minute='*/1'),  # Run every minute
            'args': (10, 20),  # Arguments to pass to the task
        },
        'run-another-task-daily-at-midnight': {
            'task': 'your_module.another_task',
            'schedule': crontab(minute=0, hour=0),  # Run daily at midnight
            'args': ('daily_report',),
        },
    }
    app.conf.timezone = 'UTC'  # Set your desired timezone

    task: Specifies the full import path to your task function.

schedule: Defines the frequency. This can be:

    A timedelta object for simple intervals (e.g., timedelta(seconds=30)).

A crontab expression for more complex schedules (e.g., crontab(minute='0', hour='0') for daily at midnight).

args: and kwargs: Optional arguments to pass to your task function.

Run Celery Worker and Celery Beat.
You need to run both a Celery worker and the Celery Beat scheduler:
Código

    celery -A your_module worker -l info
    celery -A your_module beat -l info

Replace your_module with the actual name of your Python module containing the Celery app and tasks.
Important Considerations:

    Single Celery Beat Instance:
    Only one instance of Celery Beat should be running at a time to prevent duplicate task scheduling.
    Persistent State:
    Celery Beat needs to store its state (e.g., last run times). By default, it uses a local file. For more robust deployments, consider using a database-backed scheduler like django-celery-beat for Django projects or Redbeat with Redis.
    Dynamic Scheduling:
    For schedules that need to be created or modified at runtime, libraries like Redbeat provide mechanisms to manage schedules dynamically in the broker.

## [Using Redis with docker and docker-compose for local development a step-by-step tutorial](https://geshan.com.np/blog/2022/01/redis-docker/)

## [Using Redis](https://docs.celeryq.dev/en/v5.5.3/getting-started/backends-and-brokers/redis.html)


## UV Pytest

uv is a fast Python package and project manager written in Rust, designed as a drop-in replacement for pip and pip-compile. pytest is a popular Python testing framework.
To use pytest with uv, you typically follow these steps: Add pytest as a development dependency.
Código

    uv add --dev pytest

If you also want test coverage reporting, you can add pytest-cov:
Código

    uv add --dev pytest-cov

run your tests.
Use uv run to execute pytest within the project's virtual environment:
Código

    uv run pytest

For more detailed output during test execution, you can add the verbose flag:
Código

    uv run pytest -v

    Run tests with coverage (if pytest-cov is installed):

Código

    uv run pytest --cov=<your_module_name>

To generate a more detailed coverage report, you can add the --cov-report flag:
Código

    uv run pytest --cov=<your_module_name> --cov-report=term-missing


### [How To Use An .env File In Docker Compose](https://www.warp.dev/terminus/docker-compose-env-file)


#### Information about Alembic migrations

# First recreations
- `uv run alembic revision --autogenerate -m "Add file_url and size to Document"` 


## After update the database
- `uv run alembic upgrade head`