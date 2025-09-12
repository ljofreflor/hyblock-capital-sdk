# Docker Testing for Hyblock Capital SDK

This directory contains Docker configurations to test the installation and functionality of the Hyblock Capital SDK.

## Overview

We provide two different Docker setups:

1. **Local Testing** (`Dockerfile` + `docker-compose.yml`) - Tests installation from local source
2. **PyPI Testing** (`Dockerfile.pypi` + `docker-compose.pypi.yml`) - Tests installation from PyPI (once published)

## Local Testing (Current)

### Files
- `Dockerfile` - Tests installation from local source code
- `docker-compose.yml` - Easy way to run the local test
- `test_installation.py` - Comprehensive test script

### Usage

```bash
# Build and run the local test
docker-compose up --build

# Or build manually
docker build -t hyblock-sdk-test .
docker run --rm hyblock-sdk-test
```

### What it does
- Creates a Poetry project
- Installs the SDK from local source (simulating PyPI installation)
- Tests all core functionality
- Verifies all API classes are available

## PyPI Testing (Future)

### Files
- `Dockerfile.pypi` - Tests installation from PyPI servers
- `docker-compose.pypi.yml` - Easy way to run the PyPI test

### Usage (Once package is published to PyPI)

```bash
# Build and run the PyPI test
docker-compose -f docker-compose.pypi.yml up --build

# Or build manually
docker build -f Dockerfile.pypi -t hyblock-sdk-pypi-test .
docker run --rm hyblock-sdk-pypi-test
```

### What it does
- Creates a Poetry project
- Installs the SDK directly from PyPI using `poetry add hyblock-capital-sdk`
- Tests all core functionality
- Verifies the package works as published

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
