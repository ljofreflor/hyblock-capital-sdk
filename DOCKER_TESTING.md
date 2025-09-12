# Docker Testing for Hyblock Capital SDK

This directory contains Docker configuration to test the installation and functionality of the Hyblock Capital SDK from PyPI.

## Overview

We provide a single Docker setup that tests the real installation from PyPI using Poetry:

- **PyPI Testing** (`Dockerfile` + `docker-compose.yml`) - Tests installation from PyPI servers

## PyPI Testing

### Files
- `Dockerfile` - Tests installation from PyPI servers using Poetry
- `docker-compose.yml` - Easy way to run the PyPI test
- `test_installation.py` - Comprehensive test script

### Usage

```bash
# Build and run the PyPI test
docker-compose up --build

# Or build manually
docker build -t hyblock-sdk-test .
docker run --rm hyblock-sdk-test
```

### What it does
- Creates a Poetry project
- Installs the SDK directly from PyPI using `poetry add hyblock-capital-sdk`
- Tests all core functionality
- Verifies the package works as published
- Shows clear success/failure feedback

## Test Results

Both tests verify:

✅ Library imports correctly  
✅ Core components (ApiClient, Configuration, CatalogApi) are available  
✅ All 11 API classes are available:
- ApiUsageApi
- CatalogApi
- FundingRateApi
- LiquidityApi
- LongsAndShortsApi
- OpenInterestApi
- OptionsApi
- OrderbookApi
- OrderflowApi
- ProfileToolApi
- SentimentApi

✅ API client can be created successfully  
✅ API instances can be created successfully  

## Manual Testing

You can also run the test script manually:

```bash
# With Poetry (local development)
poetry run python test_installation.py

# With pip (if installed)
python test_installation.py
```

## Notes

- The current `Dockerfile` simulates PyPI installation by building from local source
- The `Dockerfile.pypi` will work once the package is published to PyPI
- Both use Poetry for dependency management as requested
- The tests run in isolated Docker containers to ensure clean environments
