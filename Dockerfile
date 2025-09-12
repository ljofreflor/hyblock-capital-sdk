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

# Configure Poetry: Don't create virtual environment (we're already in a container)
RUN poetry config virtualenvs.create false

# Create a new Poetry project to test installation
RUN poetry init --name test-hyblock-sdk --version 0.1.0 --description "Test installation from PyPI" --author "Test User <test@example.com>" --no-interaction

# Show installation attempt
RUN echo "🚀 ATTEMPTING TO INSTALL hyblock-capital-sdk FROM PyPI USING POETRY..."

# Install the library from PyPI using Poetry
RUN poetry add hyblock-capital-sdk && echo "✅ SUCCESS: Package installed from PyPI using Poetry!" || echo "❌ FAILED: Could not install package from PyPI"

# Also install with pip to ensure it's available in the system Python
RUN pip install hyblock-capital-sdk && echo "✅ SUCCESS: Package also installed with pip!" || echo "❌ FAILED: Could not install package with pip"

# Debug: Show what was installed
RUN echo "🔍 DEBUG: Checking installed packages..." && \
    pip list | grep hyblock || echo "Package not found in pip list" && \
    echo "🔍 DEBUG: Python path:" && \
    python -c "import sys; print(sys.path)"

# Verify installation
RUN echo "🔍 VERIFYING INSTALLATION..." && \
    python -c "import hyblock_capital_sdk; print('✅ SUCCESS: Library imported successfully from PyPI!')" && \
    python -c "from hyblock_capital_sdk import ApiClient, Configuration, CatalogApi; print('✅ SUCCESS: Core components imported successfully!')" && \
    python -c "print('✅ SUCCESS: Available API classes:', [attr for attr in dir(__import__('hyblock_capital_sdk')) if attr.endswith('Api')])" && \
    python -c "from hyblock_capital_sdk import ApiClient, Configuration; config = Configuration(); client = ApiClient(config); print('✅ SUCCESS: API client created successfully!')" && \
    echo "🎉 ALL TESTS PASSED: PyPI installation is working correctly!"

# Show final status
RUN echo "📊 INSTALLATION SUMMARY:" && \
    echo "=========================" && \
    pip list | grep hyblock || echo "Package not found in final check" && \
    echo "=========================" && \
    echo "✅ PyPI installation test completed successfully!"

# Copy test script for runtime testing
COPY test_installation.py /app/

# Keep container running for interactive testing
CMD ["python", "test_installation.py"]
