# Use Python 3.9 as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies including Poetry
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy all project files
COPY . /app/

# Configure Poetry: Don't create virtual environment (we're already in a container)
RUN poetry config virtualenvs.create false

# Install dependencies using pip directly
RUN pip install pydantic urllib3 python-dateutil typing-extensions

# Install the package in editable mode
RUN pip install -e .

# Debug: Check what's installed
RUN pip list
RUN python -c "import sys; print('Python path:', sys.path)"
RUN python -c "import pydantic; print('Pydantic version:', pydantic.__version__)"

# Test the installation by importing the library
ENV PYTHONPATH=/app
RUN python -c "import hyblock_capital_sdk; print('Library imported successfully!')"

# Test basic functionality
RUN python -c "from hyblock_capital_sdk import ApiClient, Configuration, CatalogApi; print('Core components imported successfully!'); print('Available API classes:', [attr for attr in dir(__import__('hyblock_capital_sdk')) if attr.endswith('Api')]); config = Configuration(); client = ApiClient(config); print('API client created successfully!')"

# Keep container running for interactive testing
CMD ["python", "-c", "print('Hyblock Capital SDK Docker test container is ready!'); import time; time.sleep(3600)"]
