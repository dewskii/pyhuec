"""
Bridge authentication helper for generating and managing API keys.
"""

import asyncio
import logging
import os
from pathlib import Path
from typing import Optional

import httpx
from dotenv import load_dotenv, set_key

logger = logging.getLogger(__name__)


class BridgeAuthenticator:
    """
    Handles Hue Bridge authentication and API key management.

    Supports:
    - Generating new API keys with button press flow
    - Storing API keys in .env file
    - Loading API keys from environment
    """

    def __init__(
        self,
        bridge_ip: str,
        app_name: str = "pyhuec",
        device_name: str = "python-client",
    ):
        """
        Initialize the authenticator.

        Args:
            bridge_ip: IP address of the Hue Bridge
            app_name: Application name for registration
            device_name: Device name for registration
        """
        self._bridge_ip = bridge_ip
        self._base_url = f"https://{bridge_ip}"
        self._app_name = app_name
        self._device_name = device_name
        self._client = httpx.AsyncClient(verify=False)

    async def get_or_create_api_key(
        self,
        env_file: Optional[Path] = None,
        interactive: bool = True,
    ) -> str:
        """
        Get existing API key from environment or create a new one.

        Args:
            env_file: Path to .env file (defaults to project root)
            interactive: If True, prompts user to press bridge button

        Returns:
            API key string

        Raises:
            RuntimeError: If API key cannot be obtained
        """

        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()

        api_key = os.getenv("HUE_USER")

        if api_key:
            logger.info("Found existing API key in environment")
            if await self._validate_api_key(api_key):
                logger.info("API key is valid")
                return api_key
            else:
                logger.warning("API key in environment is invalid")
        else:
            logger.info("No API key found in environment")

        if not interactive:
            raise RuntimeError(
                "No valid API key found and interactive mode is disabled. "
                "Please set HUE_USER environment variable with a valid API key."
            )

        logger.info("Attempting to create new API key...")
        api_key = await self._request_api_key_interactive()

        if env_file is None:
            env_file = Path.cwd() / ".env"

        self._save_api_key(api_key, env_file)

        return api_key

    async def _validate_api_key(self, api_key: str) -> bool:
        """
        Validate an API key by making a test request.

        Args:
            api_key: API key to validate

        Returns:
            True if valid
        """
        try:
            response = await self._client.get(
                f"{self._base_url}/clip/v2/resource/light",
                headers={"hue-application-key": api_key},
                timeout=5.0,
            )
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"API key validation failed: {e}")
            return False

    async def _request_api_key_interactive(self) -> str:
        """
        Request API key with user interaction (button press prompt).

        Returns:
            Generated API key

        Raises:
            RuntimeError: If key generation fails
        """

        input("Press Enter to continue after pressing the bridge button: ")

        return await self._request_api_key_non_interactive()

    async def _request_api_key_non_interactive(
        self,
        max_attempts: int = 30,
        retry_delay: float = 1.0,
    ) -> str:
        """
        Request API key without user interaction (assumes button was pressed).

        Args:
            max_attempts: Maximum number of attempts
            retry_delay: Delay between attempts in seconds

        Returns:
            Generated API key

        Raises:
            RuntimeError: If key generation fails after all attempts
        """
        device_type = f"{self._app_name}"

        for attempt in range(max_attempts):
            try:
                logger.debug(
                    f"Requesting API key (attempt {attempt + 1}/{max_attempts})"
                )

                response = await self._client.post(
                    f"{self._base_url}/api",
                    json={"devicetype": device_type, "generateclientkey": True},
                    timeout=5.0,
                )

                if response.status_code == 200:
                    data = response.json()

                    if isinstance(data, list) and len(data) > 0:
                        first_item = data[0]

                        if "success" in first_item:
                            api_key = first_item["success"]["username"]
                            logger.info("Successfully obtained API key from bridge")
                            return api_key

                        if "error" in first_item:
                            error_type = first_item["error"].get("type")
                            description = first_item["error"].get(
                                "description", "Unknown error"
                            )

                            if error_type == 101:
                                logger.debug("Waiting for bridge button press...")
                                await asyncio.sleep(retry_delay)
                                continue
                            else:
                                raise RuntimeError(f"Bridge error: {description}")

                logger.debug(f"Unexpected response: {response.text}")
                await asyncio.sleep(retry_delay)

            except httpx.HTTPError as e:
                logger.debug(f"HTTP error during authentication: {e}")
                await asyncio.sleep(retry_delay)
            except Exception as e:
                logger.error(f"Unexpected error during authentication: {e}")
                await asyncio.sleep(retry_delay)

        raise RuntimeError(
            f"Failed to obtain API key after {max_attempts} attempts. "
            "Make sure the bridge button was pressed."
        )

    def _save_api_key(self, api_key: str, env_file: Path) -> None:
        """
        Save API key to .env file.

        Args:
            api_key: API key to save
            env_file: Path to .env file
        """
        try:
            env_file.touch(exist_ok=True)

            set_key(str(env_file), "HUE_USER", api_key)

            logger.info(f"API key saved to {env_file}")

        except Exception as e:
            logger.error(f"Failed to save API key to .env file: {e}")
            logger.warning(f"Your API key is: {api_key}")
            logger.warning("Please save it manually to continue using the client.")

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
