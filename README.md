# PhantomBuster Python SDK

## Overview

A production-ready, asynchronous Python SDK for the PhantomBuster API. This library provides a convenient and robust way to interact with both v1 and v2 of the PhantomBuster API, with built-in support for retries, rate limiting, and data validation using Pydantic.

## Features

- **Asynchronous:** Built with `asyncio` and `httpx` for high-performance, non-blocking I/O.
- **Comprehensive Endpoint Coverage:** Implements a wide range of v1 and v2 API endpoints.
- **Pydantic Models:** Includes Pydantic models for request and response validation.
- **Singleton Client:** Uses a singleton pattern for efficient client management.
- **Robust Error Handling:** Provides clear, specific exceptions for different API errors.

## Installation

```bash
pip install -e .  # Assuming you are in the root of the project
```

## Configuration

Create a `PhantombusterConfig` object and initialize the client with it:

```python
from phantombuster.client import PhantombusterClient
from phantombuster.config import PhantombusterConfig

config = PhantombusterConfig(api_key="YOUR_API_KEY")
client = PhantombusterClient.get_instance(config)
```

## Usage Examples

### Fetching All Agents (v2)

```python
import asyncio

async def main():
    agents = await client.agents.fetch_all()
    print(agents)

asyncio.run(main())
```

### Launching an Agent (v2)

```python
from phantombuster.__global_models__ import LaunchAgentRequest

async def main():
    request = LaunchAgentRequest(id=12345)
    response = await client.agents.launch(request)
    print(response)

asyncio.run(main())
```

### Getting User Info (v1)

```python
async def main():
    user_info = await client.v1.get_user()
    print(user_info)

asyncio.run(main())
```

## Running Tests

To run the full test suite:

```bash
pytest backend/app/core/third_party_integrations/phantombuster/_tests/
```
