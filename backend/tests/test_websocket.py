import pytest
from unittest.mock import Mock, patch, AsyncMock
import asyncio
from datetime import datetime

from app.websocket.connection_manager import ConnectionManager


@pytest.fixture
def connection_manager():
    """Create a ConnectionManager instance"""
    return ConnectionManager()


class TestConnectionManager:
    """Test cases for WebSocket ConnectionManager"""

    @pytest.mark.asyncio
    async def test_connect(self, connection_manager):
        """Test connecting a client"""
        websocket = AsyncMock()
        client_id = "test_client_1"
        
        await connection_manager.connect(websocket, client_id)
        
        assert client_id in connection_manager.active_connections
        assert websocket in connection_manager.active_connections[client_id]
        assert websocket in connection_manager.subscriptions
        websocket.accept.assert_called_once()

    def test_disconnect(self, connection_manager):
        """Test disconnecting a client"""
        websocket = Mock()
        client_id = "test_client_2"
        
        # First connect
        connection_manager.active_connections[client_id] = [websocket]
        connection_manager.subscriptions[websocket] = {"metrics"}
        
        # Then disconnect
        connection_manager.disconnect(websocket, client_id)
        
        assert client_id not in connection_manager.active_connections
        assert websocket not in connection_manager.subscriptions

    @pytest.mark.asyncio
    async def test_subscribe(self, connection_manager):
        """Test subscribing to a channel"""
        websocket = Mock()
        channel = "metrics"
        
        connection_manager.subscriptions[websocket] = set()
        await connection_manager.subscribe(websocket, channel)
        
        assert channel in connection_manager.subscriptions[websocket]

    @pytest.mark.asyncio
    async def test_unsubscribe(self, connection_manager):
        """Test unsubscribing from a channel"""
        websocket = Mock()
        channel = "metrics"
        
        connection_manager.subscriptions[websocket] = {channel}
        await connection_manager.unsubscribe(websocket, channel)
        
        assert channel not in connection_manager.subscriptions[websocket]

    @pytest.mark.asyncio
    async def test_broadcast(self, connection_manager):
        """Test broadcasting a message"""
        websocket1 = AsyncMock()
        websocket2 = AsyncMock()
        
        connection_manager.active_connections["client_1"] = [websocket1]
        connection_manager.active_connections["client_2"] = [websocket2]
        connection_manager.subscriptions[websocket1] = {"metrics"}
        connection_manager.subscriptions[websocket2] = {"alerts"}
        
        message = {"success_rate": 92}
        await connection_manager.broadcast(message, channel="metrics")
        
        # Only websocket1 should receive the message
        websocket1.send_json.assert_called_once()
        websocket2.send_json.assert_not_called()

    @pytest.mark.asyncio
    async def test_send_personal(self, connection_manager):
        """Test sending a personal message"""
        websocket = AsyncMock()
        message = {"status": "subscribed", "channel": "metrics"}
        
        await connection_manager.send_personal(websocket, message)
        
        websocket.send_json.assert_called_once()
        call_args = websocket.send_json.call_args[0][0]
        assert call_args["data"] == message
        assert "timestamp" in call_args

    @pytest.mark.asyncio
    async def test_handle_subscription_subscribe(self, connection_manager):
        """Test handling subscribe action"""
        websocket = AsyncMock()
        channel = "metrics"
        
        connection_manager.subscriptions[websocket] = set()
        
        data = {"action": "subscribe", "channel": channel}
        await connection_manager.handle_subscription(websocket, data)
        
        assert channel in connection_manager.subscriptions[websocket]
        websocket.send_json.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_subscription_unsubscribe(self, connection_manager):
        """Test handling unsubscribe action"""
        websocket = AsyncMock()
        channel = "metrics"
        
        connection_manager.subscriptions[websocket] = {channel}
        
        data = {"action": "unsubscribe", "channel": channel}
        await connection_manager.handle_subscription(websocket, data)
        
        assert channel not in connection_manager.subscriptions[websocket]
        websocket.send_json.assert_called_once()

    def test_get_connection_stats(self, connection_manager):
        """Test getting connection statistics"""
        websocket1 = Mock()
        websocket2 = Mock()
        
        connection_manager.active_connections["client_1"] = [websocket1]
        connection_manager.active_connections["client_2"] = [websocket2, websocket1]
        connection_manager.subscriptions[websocket1] = set()
        connection_manager.subscriptions[websocket2] = set()
        
        stats = connection_manager.get_connection_stats()
        
        assert stats["total_clients"] == 2
        assert stats["total_connections"] == 3
        assert "timestamp" in stats

    @pytest.mark.asyncio
    async def test_broadcast_to_multiple_channels(self, connection_manager):
        """Test broadcasting to specific channels"""
        websocket_metrics = AsyncMock()
        websocket_alerts = AsyncMock()
        websocket_all = AsyncMock()
        
        connection_manager.active_connections["client_1"] = [websocket_metrics]
        connection_manager.active_connections["client_2"] = [websocket_alerts]
        connection_manager.active_connections["client_3"] = [websocket_all]
        
        connection_manager.subscriptions[websocket_metrics] = {"metrics"}
        connection_manager.subscriptions[websocket_alerts] = {"alerts"}
        connection_manager.subscriptions[websocket_all] = {"metrics", "alerts"}
        
        message = {"data": "test"}
        await connection_manager.broadcast(message, channel="metrics")
        
        # websocket_metrics and websocket_all should receive
        assert websocket_metrics.send_json.called
        assert websocket_all.send_json.called
        assert not websocket_alerts.send_json.called

    @pytest.mark.asyncio
    async def test_disconnect_on_send_error(self, connection_manager):
        """Test that clients are disconnected on send errors"""
        websocket = AsyncMock()
        websocket.send_json.side_effect = Exception("Send failed")
        
        connection_manager.active_connections["client_1"] = [websocket]
        connection_manager.subscriptions[websocket] = {"metrics"}
        
        await connection_manager.broadcast({"data": "test"}, channel="metrics")
        
        # Client should be disconnected
        assert "client_1" not in connection_manager.active_connections
        assert websocket not in connection_manager.subscriptions
