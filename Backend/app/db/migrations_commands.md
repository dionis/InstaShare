# Database Migration Commands (Alembic)

This document outlines the commands for managing database migrations using Alembic in the InstaShare backend.

## Initializing Alembic

If Alembic has not been initialized yet, you can do so by running:

```bash
alembic init -t alembic Backend/app/alembic
```
This command initializes the Alembic environment in the `Backend/app/alembic` directory.

## Generating a New Migration

To generate a new migration script, use the `revision` command. It's recommended to use the `--autogenerate` flag to automatically detect schema changes.

```bash
alembic revision --autogenerate -m "Description of your migration"
```

Replace `"Description of your migration"` with a brief, descriptive message about the changes in this migration (e.g., "Create user and document tables").

Alembic will create a new Python file in the `Backend/app/alembic/versions` directory. Review this file to ensure the generated migration correctly reflects your intended schema changes.

## Applying Migrations

To apply all pending migrations to the database, use the `upgrade` command:

```bash
alembic upgrade head
```

This will apply all migrations up to the latest revision (`head`).

## Downgrading Migrations

To revert the last applied migration, you can use the `downgrade` command:

```bash
alembic downgrade -1
```

To downgrade to a specific revision, use:

```bash
alembic downgrade <revision_id>
```

Replace `<revision_id>` with the unique identifier of the target revision.

## Viewing Current Migration Status

To see the current revision of your database and available migrations, use the `current` command:

```bash
alembic current
```

To view the history of migrations:

```bash
alembic history
```

## Important Considerations

*   **Database URL:** Ensure your `alembic.ini` (or environment variables) is correctly configured with the database connection URL. The `Backend/app/alembic/env.py` file reads the `DATABASE_URL` from environment variables, which is set in `docker-compose.yml` for Dockerized environments.
*   **Model Imports:** Make sure all your SQLAlchemy models are correctly imported in `Backend/app/alembic/env.py` to enable `--autogenerate` to detect changes. With the new structure, they are imported from `Backend.app.models`.
*   **Running within Docker:** When running Alembic commands from your host machine, ensure you have the necessary environment variables set (e.g., `DATABASE_URL`) or are running `alembic` from within the `api` container if database access is required.
*   **Development Workflow:**
    1.  Make changes to your SQLAlchemy models in `Backend/app/models/`.
    2.  Generate a new migration: `alembic revision --autogenerate -m "Your description"`.
    3.  Review the generated migration script.
    4.  Apply the migration: `alembic upgrade head`.
