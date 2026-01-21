# pyhuec
**Python HueV2 Client**

> [!NOTE]
> This is very much a work in progress. API features have not been fully implemented. If you stumble upon this looking for a working hue client, it's not that yet. Feel free to contribute!

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
❯ uv run main.py
```

## Connecting to your bridge
> [!Note]
> The client exclusively using mDNS for bridge discovery. It does not use the hue discovery service, and probably never will. More information on interfacing with the [Developer Hue Getting Started](https://developers.meethue.com/develop/get-started-2/) and the [HUE V2 API Reference](https://developers.meethue.com/develop/hue-api-v2/api-reference/#)

The [main.py](main.py) in the root directory is acting as a scratch pad for quick testing. It currently finds a bridge, authenticates and fetches an API key, and finds any lights associated with the bridge. 

On first run the client will attempt to fetch an API key for authentication.

The client will write the key to a .env file at the root of the project under the name `HUE_USER`, and will leverage this key for future use.

> [!IMPORTANT]
> On first run when first fetching a key, you will be required to press the top button on you Hue Bridge. The program will halt waiting for input to proceed. If you are having trouble discoverying over mDNS, you can increase the timeout in ServiceFinder, or follow the instructions in the Hue documentation.

```
❯ uv run main.py
INFO:...:Bridges to warm 1
INFO:...:Warming controller
INFO:...:Requesting new key
Please press the connect button on hue bridge, press anykey to continue
INFO:...:Authenticated with bridge; got key
INFO:...:Obtained new key and wrote to dotenv
INFO:...:Warming lights
INFO:...:Found 5
INFO:__main__:Lights found
("dict_keys(['051ba29d-b073-44b1-ab23-a794a766feb2', "
 "'7aea3cdb-4833-4343-bbf0-9fad39564d53', "
 "'a84a1c2c-1968-4c81-bc9c-24e98a0d1b2b', "
 "'c3256160-81f7-48bc-8bd5-47ed5aa5fcbc', "
 "'cb4138af-af04-485b-8ce3-68070790d3a2'])")

```

## Contributing
> [!NOTE]
> Ignore the makefile for now, haven't landed on what I want in it yet.
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



