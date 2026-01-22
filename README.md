# pyhuec
**Python Hue Client**

Python client for interfacing with Philips Hue API v2, supports REST and Event streaming

> [!NOTE]
> This is very much a work in progress. API features have not been fully implemented. If you stumble upon this looking for a working hue client, it's not that yet. Feel free to contribute!

## What's it do?

- **Auto-Discovery** - Automatically finds your Hue Bridge on the network  
- **Auto-Authentication** - Generates and saves API keys with guided setup  
- **Event Streaming** - Real-time updates via Server-Sent Events (SSE)  
- **State Caching** - Cache synchronized with REST API and events  
- **Asynchronous** - It's async

## Quick Start

```python
import asyncio
from pyhuec.hue_client_factory import HueClientFactory

async def main():
    # use HueClientFactory.create_client(auto_authenticate=False)
    # to disable auto fetching api key
    client = await HueClientFactory.create_client()
    
    await client.start_event_stream()
    # Enable in memory caching, optional
    await client.initialize_cache()
    

    lights = await client.get_lights()
    await client.turn_on_light(lights[0].id, brightness=100)
    
    # Get events from bridge and update state
    await client.subscribe_to_light_events(
        lambda event: print(f"Light changed: {event}")
    )
    
    await client.stop_event_stream()

asyncio.run(main())
```

> [!NOTE]
> More example code can be found in [example.py](example.py)

On first run, you'll be prompted to press the button on your bridge. The API key is saved automatically for future use.

## Installation
> [!NOTE]
> Will add here when published to pypi

## Developing
This project using uv for handling dependencies and build scripts. See [Instructions on Installing](https://docs.astral.sh/uv/getting-started/installation/)

#### Sync the project
```
❯ uv sync
```
#### Run tests
```
❯ uv run tests
```

#### Run Sample
```
❯ uv run example.py
```

## Connecting to your bridge

>[!Note]
> This client *only* uses mDNS for automatic bridge discovery. If you are having trouble finding your bridge with mDNS, feel free to follow [Hue's guide](https://developers.meethue.com/develop/get-started-2/#follow-3-easy-steps) on finding your bridge ip.

### Automatic Setup (Recommended)

The easiest way is to let pyhuec handle everything:

```python
client = await HueClientFactory.create_client(auto_authenticate=True)
```

This will:
1. Discover your bridge via mDNS
2. Check for existing API key in `.env` file
3. Prompt you to press the bridge button if needed
4. Generate and save a new API key
5. Connect to your bridge automatically

## Manual Setup

If you prefer manual configuration:

```python
client = await HueClientFactory.create_client(
    bridge_ip="<bridge-ip-address>",
    api_key="<your-api-key-here>"
)
```

### Environment Variables

Set these in your `.env` file:

```bash
HUE_USER=your-api-key-here
TARGET_MDNS=_hue._tcp.local.  # Optional, has default
```

The `HUE_USER` variable is automatically created when you use auto-authentication.

## Contributing
Feel free to fork or open a PR. Will not be looking at issues until feature complete. 

This project uses pre-commit for managing git-hooks, and is included as part of the dev dependences.
To use it you'll still need to run a single command to install the hooks in your local branch
```
❯ pre-commit install
```
Current hooks run tests and ruff linting as pre-commits.


Any additional dev/testing dependencies should be add to the dev group.
```
❯ uv add <some-dev-package> --dev
```



