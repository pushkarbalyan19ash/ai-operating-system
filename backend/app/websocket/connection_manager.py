import asyncio
from typing import Dict, List, Set
from fastapi import WebSocket, WebSocketDisconnect
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for real-time monitoring updates"""

    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.subscriptions: Dict[WebSocket, Set[str]] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = []
        self.active_connections[client_id].append(websocket)
        self.subscriptions[websocket] = set()
        logger.info(f"Client {client_id} connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket, client_id: str):
        """Remove a disconnected WebSocket"""
        if client_id in self.active_connections:
            self.active_connections[client_id].remove(websocket)
            if not self.active_connections[client_id]:
                del self.active_connections[client_id]
        if websocket in self.subscriptions:
            del self.subscriptions[websocket]
        logger.info(f"Client {client_id} disconnected")

    async def subscribe(self, websocket: WebSocket, channel: str):
        """Subscribe to a specific channel"""
        self.subscriptions[websocket].add(channel)
        logger.info(f"Client subscribed to channel: {channel}")

    async def unsubscribe(self, websocket: WebSocket, channel: str):
        """Unsubscribe from a specific channel"""
        self.subscriptions[websocket].discard(channel)
        logger.info(f"Client unsubscribed from channel: {channel}")

    async def broadcast(self, message: Dict, channel: str = "all"):
        """Broadcast a message to all subscribed clients"""
        disconnected = []
        for client_id, connections in self.active_connections.items():
            for connection in connections:
                if channel in self.subscriptions.get(connection, set()) or channel == "all":
                    try:
                        await connection.send_json({
                            "channel": channel,
                            "timestamp": datetime.utcnow().isoformat(),
                            "data": message
                        })
                    except Exception as e:
                        logger.error(f"Error sending message: {e}")
                        disconnected.append((client_id, connection))

        # Clean up disconnected clients
        for client_id, connection in disconnected:
            self.disconnect(connection, client_id)

    async def send_personal(self, websocket: WebSocket, message: Dict, channel: str = "personal"):
        """Send a message to a specific client"""
        try:
            await websocket.send_json({
                "channel": channel,
                "timestamp": datetime.utcnow().isoformat(),
                "data": message
            })
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")

    async def handle_subscription(self, websocket: WebSocket, data: Dict):
        """Handle subscription requests from client"""
        action = data.get("action")
        channel = data.get("channel")

        if action == "subscribe":
            await self.subscribe(websocket, channel)
            await self.send_personal(
                websocket,
                {"status": "subscribed", "channel": channel},
                channel="subscription"
            )
        elif action == "unsubscribe":
            await self.unsubscribe(websocket, channel)
            await self.send_personal(
                websocket,
                {"status": "unsubscribed", "channel": channel},
                channel="subscription"
            )

    def get_connection_stats(self) -> Dict:
        """Get statistics about active connections"""
        total_connections = sum(len(conns) for conns in self.active_connections.values())
        total_clients = len(self.active_connections)
        return {
            "total_clients": total_clients,
            "total_connections": total_connections,
            "timestamp": datetime.utcnow().isoformat()
        }
