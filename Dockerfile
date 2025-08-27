FROM python:3.11-slim

WORKDIR /app

# Install uv for dependency management
RUN pip install uv

# Copy pyproject.toml and poetry.lock (if you were using poetry)
COPY Backend/pyproject.toml ./

# Install dependencies
RUN uv sync

# Copy application code
COPY Backend/. .

# Expose port
EXPOSE 8000

# Command to keep container running for debugging
CMD ["tail", "-f", "/dev/null"]






