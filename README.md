# InstaShare Platform

**Version:** 0.1.0

**Description:** An online platform for managing and sharing documents securely and efficiently.

## Backend

### Description
A robust API built with FastAPI, providing secure document management, user authentication, and scheduled background tasks for document processing.

### Technology Stack
The backend is built with Python and utilizes the following key technologies:
*   **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.8+ based on standard Python type hints.
*   **Uvicorn:** A lightning-fast ASGI server, used for serving the FastAPI application.
*   **SQLAlchemy:** A powerful and flexible Object Relational Mapper (ORM) for interacting with the database.
*   **psycopg2-binary / psycopg2:** PostgreSQL database adapter for Python, enabling connection to the PostgreSQL database.
*   **Pydantic:** Used for data validation and settings management, ensuring data integrity and clear API schemas.
*   **python-dotenv:** Manages environment variables, allowing for flexible configuration across different environments.
*   **Supabase:** Utilized as a Backend-as-a-Service (BaaS) for its PostgreSQL database capabilities and integrated object storage.
*   **Alembic:** A database migration tool for SQLAlchemy, managing schema changes over time.
*   **python-multipart:** Handles parsing of `multipart/form-data` requests, essential for file uploads.
*   **python-jose:** Implements JSON Web Tokens (JWT) for secure user authentication and authorization.
*   **passlib / bcrypt:** Provides secure password hashing functionalities.
*   **pytest / pytest-asyncio / pytest-cov:** The testing framework for the backend, including support for asynchronous tests and code coverage reporting.
*   **Celery / librabbitmq / redis:** An asynchronous task queue system used for processing background jobs, such as document compression. Redis serves as the message broker.
*   **uv:** A fast Python package installer and resolver.
*   **Docker / Docker Compose:** Used for containerization, enabling consistent development, testing, and deployment environments.
*   **GitHub Actions:** Configured for Continuous Integration (CI) to automate testing on code pushes.

## For Deployment and testing processin the platform was hosting in:

- Frontend: [Vercel](https://insta-share-three.vercel.app/)
- Backend: [Ligthing.ai](https://8000-01k3wgp3gs2dkz20nztgdcgkqn.cloudspaces.litng.ai/docs)
- Storage: [Supabase](https://supabase.com/)
   -  Was create a storage module with name "document"


 ### About  Docker Deploment - Containers for local deployment and development
 Read the [Backend/docker-compose.yml](Backend/docker-compose.yml)

  Threre are four image/container:
    - redis-instashare: For sheduler propouse using with Celery app for execution periodicall task.
    - db: A Postgresql container for local deployment and test, in current only use remote supabase deployment
    - api: All backed and FastApi processing request.
    - sheduler-worker: All backed logic for execute a periodical task (since 2 minutes) for finding all upload document zip document and upload egaint to Supabase store. See file (Backend/app/task.py)[Backend/app/task.py]

### Issues in this version
 - Fix the editing and visualization in frontend.
 - Validate user inpunt in some field.
 - Integrate all authenticate services. 
 - Flutter app in development process.
 - Not add support for Google / Facebook / LikendIn becasue is need payment support at Supabase platform

### Directory Structure (`Backend/app`)
The `app` directory organizes the backend logic into several modules:
*   `alembic/`: Contains Alembic migration scripts and environment configurations for managing database schema changes.
*   `auth/`: Handles all authentication-related logic, including JWT token creation, verification, and FastAPI dependencies for securing API routes.
*   `compressed_files/`: A local directory used for storing compressed document files temporarily or for archival.
*   `core/`: Houses core application components such as the main FastAPI application instance, global configuration settings, and Celery task definitions.
*   `db/`: Contains modules related to database interaction, including SQLAlchemy engine and session setup, as well as utilities for database seeding and cleaning.
*   `models/`: Defines SQLAlchemy ORM models, with each model (e.g., `User`, `Document`, `Role`) separated into its own file for better organization and maintainability.
*   `schemas/`: Holds Pydantic schemas for data validation and serialization, crucial for defining the structure of API request and response bodies.
*   `services/`: Implements the business logic for various entities (e.g., `UserService`, `DocumentService`), abstracting interactions with the database and external services.
*   `sheduler_tasks/`: Contains the Celery application configuration and definitions for scheduled background tasks, such as the document compression process.
*   `test/`: Dedicated to unit and integration tests for the backend services and API endpoints, ensuring the application's reliability.

### Testing
The backend includes a comprehensive suite of tests to ensure reliability and correctness.
*   **Framework:** `pytest` is used as the primary testing framework, with `pytest-asyncio` enabling testing of asynchronous functions.
*   **Configuration:** The `Backend/pytest.ini` file configures the test runner with `pythonpath = app/` for module discovery and `asyncio_mode = auto` for automatic handling of asynchronous tests.
*   **Execution:**
    *   To run all tests locally: navigate to the `Backend` directory and execute `uv run pytest`.
    *   When running within Docker Compose, tests can be executed using: `docker-compose run api uv run pytest`.
*   **Continuous Integration:** A GitHub Actions workflow (`.github/workflows/backend_ci.yml`) is set up to automatically run tests on `push` events to the `main` branch, specifically for changes within the `Backend/**` path.

### Installation
Follow these steps to set up and run the InstaShare Backend locally:
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/instashare_platform.git
    cd instashare_platform
    ```
2.  **Navigate to the Backend directory:**
    ```bash
    cd Backend
    ```
3.  **Install dependencies:**
    ```bash
    uv sync
    ```
4.  **Set up environment variables:**
    Create an `.env` file in the `Backend/app/` directory. This file should contain essential environment variables, including:
    *   `DATABASE_URL`: Your PostgreSQL connection string.
    *   `SUPABASE_URL`: Your Supabase project URL.
    *   `SUPABASE_KEY`: Your Supabase API key.
    *   `SECRET_KEY`: A strong secret key for JWT encryption.
    *   `ALGORITHM`: The JWT signing algorithm (e.g., "HS256").
    *   `ACCESS_TOKEN_EXPIRE_MINUTES`: Expiration time for access tokens.
    *   `REDIS_URL`: URL for your Redis instance (e.g., `redis://redis-instashare:6379/0` for Docker Compose setup).
5.  **Run Database Migrations:**
    ```bash
    uv run alembic upgrade head
    ```
    This command will apply all pending database migrations to set up your database schema.
6.  **Run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker images (if not already built) and start the backend API, PostgreSQL database, and Redis services. The API will be accessible at `http://localhost:8000`.

### Deployment
For production deployment, the Docker images can be deployed to various cloud platforms or container orchestration services. The specific deployment steps will vary depending on the chosen platform (e.g., AWS ECS, Google Cloud Run, Azure Container Instances, Kubernetes).

## Frontend

### Description
A responsive web application built with React and TypeScript, designed to provide a user-friendly interface for interacting with the InstaShare Backend. It allows users to upload, manage, and share documents securely.

### Technology Stack
The frontend is developed using modern web technologies:
*   **React:** A declarative, component-based JavaScript library for building dynamic user interfaces.
*   **TypeScript:** A strongly typed superset of JavaScript that enhances code quality and maintainability.
*   **Vite:** A next-generation frontend tooling that provides an extremely fast development experience with features like hot module replacement (HMR) and optimized builds.
*   **@supabase/supabase-js / @supabase/auth-ui-react / @supabase/auth-ui-shared:** The official Supabase JavaScript client library and UI components for seamless integration with Supabase authentication and services.
*   **axios:** A popular promise-based HTTP client for making API requests to the backend.
*   **react-router-dom:** Provides declarative routing for React applications, enabling navigation between different views.
*   **react-icons:** A library that offers a wide collection of customizable SVG icons for various UI elements.
*   **Jest / @testing-library/react / @testing-library/jest-dom / @testing-library/user-event:** The testing suite for the frontend, providing tools for unit and integration testing of React components, focusing on user behavior.

### Directory Structure (`Frontend/instashare-frontend/src`)
The `src` directory within the frontend project is structured as follows:
*   `components/`: Contains reusable React components, organized by their functionality (e.g., `Navbar`, `Sidebar`, `PrivateRoute`). These components are designed to be modular and promote reusability across the application.
*   `contexts/`: Provides React context for global state management, such as `AuthContext` for handling user authentication state throughout the application.
*   `hooks/`: Custom React hooks designed to encapsulate and reuse stateful logic across different components.
*   `mocks/`: Stores mock implementations of services and external dependencies (e.g., Supabase client) specifically used for testing purposes, allowing for isolated and reliable tests.
*   `pages/`: Defines the main views or pages of the application. Each directory typically corresponds to a specific route or section of the application (e.g., `Dashboard`, `Documents`, `Login`, `Users`).
*   `services/`: Encapsulates the logic for interacting with the backend API and other external services (e.g., `api.ts`, `documentService.ts`, `supabaseClient.ts`), centralizing data fetching and manipulation.
*   `utils/`: Contains general utility functions and helper modules that are used across various parts of the application.

### Testing
The frontend application includes tests to ensure its functionality and user experience.
*   **Framework:** `Jest` is utilized as the testing framework, complemented by `@testing-library/react` for writing user-centric tests.
*   **Execution:**
    *   To run tests in interactive watch mode:
        ```bash
        npm test
        ```
    *   To run all tests once:
        ```bash
        npm run test
        ```

### Installation
To get the InstaShare Frontend running locally, follow these steps:
1.  **Navigate to the Frontend directory:**
    ```bash
    cd Frontend/instashare-frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Set up environment variables:**
    Create a `.env` file in the `Frontend/instashare-frontend/` directory with necessary configurations, such as:
    *   `VITE_SUPABASE_URL`: Your Supabase project URL.
    *   `VITE_SUPABASE_KEY`: Your Supabase API key.
    *   `VITE_API_URL`: The URL of your backend API (e.g., `http://localhost:8000`).
4.  **Run the development server:**
    ```bash
    npm run dev
    ```
    The application will typically be available at `http://localhost:5173`.

### Deployment
To deploy the InstaShare Frontend for production:
1.  **Build for production:**
    ```bash
    npm run build
    ```
    This command will create an optimized production build in the `dist` directory.
2.  **Serve the build (local example):**
    ```bash
    npm install -g serve
    serve -s dist
    ```
    This allows you to serve the production build locally. For actual deployment, you would typically use a static site hosting service (e.g., Vercel, Netlify, GitHub Pages) and configure it to serve the contents of the `dist` directory.
