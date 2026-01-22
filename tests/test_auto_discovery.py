"""
Tests for auto-discovery and authentication functionality.
"""

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from pyhuec.hue_client_factory import HueClientFactory
from pyhuec.transport.bridge_authenticator import BridgeAuthenticator


class TestBridgeAuthenticator:
    """Tests for BridgeAuthenticator class."""

    @pytest.fixture
    def mock_env(self, tmp_path):
        """Create a temporary .env file for testing."""
        env_file = tmp_path / ".env"
        return env_file

    @pytest.mark.asyncio
    async def test_authenticator_initialization(self):
        """Test authenticator initializes correctly."""
        auth = BridgeAuthenticator(
            bridge_ip="127.0.0.1",
            app_name="test-app",
            device_name="test-device",
        )

        assert auth._bridge_ip == "127.0.0.1"
        assert auth._base_url == "https://127.0.0.1"
        assert auth._app_name == "test-app"
        assert auth._device_name == "test-device"

        await auth.close()

    @pytest.mark.asyncio
    async def test_validate_api_key_valid(self):
        """Test API key validation with valid key."""
        auth = BridgeAuthenticator(bridge_ip="127.0.0.1")

        # Mock successful response
        with patch.object(auth._client, "get") as mock_get:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            result = await auth._validate_api_key("valid-key")

            assert result is True
            mock_get.assert_called_once()

        await auth.close()

    @pytest.mark.asyncio
    async def test_validate_api_key_invalid(self):
        """Test API key validation with invalid key."""
        auth = BridgeAuthenticator(bridge_ip="127.0.0.1")

        # Mock failed response
        with patch.object(auth._client, "get") as mock_get:
            mock_response = AsyncMock()
            mock_response.status_code = 401
            mock_get.return_value = mock_response

            result = await auth._validate_api_key("invalid-key")

            assert result is False

        await auth.close()

    @pytest.mark.asyncio
    async def test_save_api_key(self, mock_env):
        """Test saving API key to .env file."""
        auth = BridgeAuthenticator(bridge_ip="127.0.0.1")

        auth._save_api_key("test-key-123", mock_env)

        # Verify file was created and contains the key
        assert mock_env.exists()
        content = mock_env.read_text()
        assert "HUE_USER" in content
        assert "test-key-123" in content

        await auth.close()


class TestHueClientFactory:
    """Tests for HueClientFactory auto-discovery features."""

    @pytest.mark.asyncio
    async def test_create_client_with_explicit_params(self):
        """Test creating client with explicit bridge IP and API key."""
        with patch("pyhuec.hue_client_factory.HttpClient") as mock_http:
            mock_http_instance = MagicMock()
            mock_http.return_value = mock_http_instance

            client = await HueClientFactory.create_client(
                bridge_ip="127.0.0.1",
                api_key="test-key",
                enable_events=False,  # Simplify test
            )

            # Verify HTTP client was configured correctly
            mock_http_instance.set_base_url.assert_called_with("https://127.0.0.1")
            mock_http_instance.set_auth_token.assert_called_with("test-key")

    @pytest.mark.asyncio
    async def test_create_client_auto_discovery(self):
        """Test client creation with auto-discovery."""
        with patch("pyhuec.hue_client_factory.MdnsClient") as mock_mdns_class:
            # Mock mDNS discovery
            mock_mdns = AsyncMock()
            mock_mdns.discover_bridges.return_value = [{"ip": "127.0.0.1"}]
            mock_mdns_class.return_value = mock_mdns

            with patch("pyhuec.hue_client_factory.HttpClient"):
                client = await HueClientFactory.create_client(
                    bridge_ip=None,  # Trigger discovery
                    api_key="test-key",
                    enable_events=False,
                )

                # Verify discovery was called
                mock_mdns.discover_bridges.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_client_no_bridge_found(self):
        """Test client creation fails when no bridge found."""
        with patch("pyhuec.hue_client_factory.MdnsClient") as mock_mdns_class:
            # Mock no bridges found
            mock_mdns = AsyncMock()
            mock_mdns.discover_bridges.return_value = []
            mock_mdns_class.return_value = mock_mdns

            with pytest.raises(RuntimeError, match="No Hue Bridge found"):
                await HueClientFactory.create_client(
                    bridge_ip=None,
                    api_key="test-key",
                )

    @pytest.mark.asyncio
    async def test_create_client_auto_authenticate(self):
        """Test client creation with auto-authentication."""
        with patch("pyhuec.hue_client_factory.BridgeAuthenticator") as mock_auth_class:
            # Mock authentication
            mock_auth = AsyncMock()
            mock_auth.get_or_create_api_key.return_value = "generated-key"
            mock_auth_class.return_value = mock_auth

            with patch("pyhuec.hue_client_factory.HttpClient"):
                client = await HueClientFactory.create_client(
                    bridge_ip="127.0.0.1",
                    api_key=None,  # Trigger authentication
                    auto_authenticate=True,
                    enable_events=False,
                )

                # Verify authentication was attempted
                mock_auth.get_or_create_api_key.assert_called_once()
                mock_auth.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_from_discovery(self):
        """Test create_from_discovery convenience method."""
        with patch.object(HueClientFactory, "create_client") as mock_create:
            mock_create.return_value = MagicMock()

            await HueClientFactory.create_from_discovery(
                api_key="test-key",
                mdns_timeout=10.0,
            )

            # Verify create_client was called with bridge_ip=None
            mock_create.assert_called_once()
            call_kwargs = mock_create.call_args.kwargs
            assert call_kwargs["bridge_ip"] is None
            assert call_kwargs["api_key"] == "test-key"
            assert call_kwargs["mdns_timeout"] == 10.0


class TestIntegrationFlow:
    """Integration tests for the complete discovery and auth flow."""

    @pytest.mark.asyncio
    async def test_full_auto_flow(self):
        """Test the complete automatic discovery and authentication flow."""
        # Mock all dependencies
        with (
            patch("pyhuec.hue_client_factory.MdnsClient") as mock_mdns_class,
            patch("pyhuec.hue_client_factory.BridgeAuthenticator") as mock_auth_class,
            patch("pyhuec.hue_client_factory.HttpClient"),
        ):
            # Setup mDNS mock
            mock_mdns = AsyncMock()
            mock_mdns.discover_bridges.return_value = [{"ip": "127.0.0.1"}]
            mock_mdns_class.return_value = mock_mdns

            # Setup auth mock
            mock_auth = AsyncMock()
            mock_auth.get_or_create_api_key.return_value = "auto-generated-key"
            mock_auth_class.return_value = mock_auth

            # Create client with no parameters (full auto mode)
            client = await HueClientFactory.create_client(
                auto_authenticate=True,
                enable_events=False,
            )

            # Verify the complete flow
            mock_mdns.discover_bridges.assert_called_once()
            mock_auth.get_or_create_api_key.assert_called_once()
            mock_auth.close.assert_called_once()

            # Verify authenticator was created with discovered IP
            auth_call_args = mock_auth_class.call_args
            assert auth_call_args.kwargs["bridge_ip"] == "127.0.0.1"
