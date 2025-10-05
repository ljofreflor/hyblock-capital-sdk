# Hyblock Capital SDK Usage Examples

This directory contains practical examples of how to use the Hyblock Capital SDK for different use cases.

## Example Structure

- `basic_usage.py` - Basic SDK configuration and usage example
- `trading_example.py` - Trading operations examples
- `market_data_example.py` - Market data retrieval and processing
- `websocket_example.py` - Real-time data using WebSockets
- `advanced_features.py` - Advanced SDK features

## Prerequisites

1. **API Credentials**: Get your credentials from [Hyblock Capital](https://hyblock.capital/api)
2. **Environment Variables**: Configure your `.env` file based on `env.example`
3. **SDK Installed**: Make sure the SDK is installed and generated

```bash
# Generate the SDK
python generate_sdk.py

# Install dependencies
poetry install

# Configure environment variables
cp env.example .env
# Edit .env with your real credentials
```

## Running Examples

```bash
# Basic example
poetry run python examples/basic_usage.py

# Trading example
poetry run python examples/trading_example.py

# Market data
poetry run python examples/market_data_example.py
```

## Security Configuration

**IMPORTANT**: 
- Never hardcode credentials in code
- Use environment variables or a secrets manager
- Review your API key permissions
- Use test credentials for development

## Support

If you encounter issues with the examples:
1. Verify that your credentials are valid
2. Confirm that the SDK is properly generated
3. Check logs for specific errors
4. Consult the documentation at [docs.hyblock.capital](https://docs.hyblock.capital)
