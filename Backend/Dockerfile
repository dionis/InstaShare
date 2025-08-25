FROM python:3.11-slim

WORKDIR /app

# Install uv and create a virtual environment
RUN pip install uv
RUN uv pip install -e ".[dev]"
#RUN uv venv
#ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies into the virtual environment
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
RUN uv sync --frozen 

# Copy application code
COPY ./app ./app
COPY ./specs ./specs

# Expose port
EXPOSE 8000

# Command to run uvicorn with hot reload
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
