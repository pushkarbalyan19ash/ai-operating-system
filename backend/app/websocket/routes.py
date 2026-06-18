from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
import logging
import asyncio
from typing import Dict

from app.db.database import get_db
from app.websocket.connection_manager import ConnectionManager
from app.services.monitoring_service import MonitoringService
from app.services.ml_alerts_service import MLAlertsService

logger = logging.getLogger(__name__)

# Global connection manager instance
manager = ConnectionManager()

router = APIRouter(
    prefix="/api/ws",
    tags=["websocket"]
)


@router.websocket("/monitoring/{client_id}")
async def websocket_monitoring(websocket: WebSocket, client_id: str):
    """
    WebSocket endpoint for real-time monitoring updates.
    
    Clients can subscribe to channels:
    - metrics: Real-time metrics updates
    - alerts: Alert notifications
    - agent_status: Agent status changes
    - cost: Cost updates
    - system: System resource updates
    """
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # Receive subscription requests from client
            data = await websocket.receive_json()
            await manager.handle_subscription(websocket, data)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
        logger.info(f"Client {client_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}")
        manager.disconnect(websocket, client_id)


@router.get("/monitoring/stats")
async def get_connection_stats():
    """
    Get statistics about active WebSocket connections
    """
    return manager.get_connection_stats()


async def start_metric_broadcaster(db: Session):
    """
    Background task to broadcast metrics updates to all connected clients.
    Run this in a separate asyncio task.
    """
    monitoring_service = MonitoringService(db)
    
    while True:
        try:
            # Get updated metrics every 5 seconds
            metrics = await monitoring_service.get_dashboard_metrics()
            
            await manager.broadcast(
                {
                    "success_rate": metrics.overall_success_rate,
                    "avg_execution_time": metrics.avg_execution_time,
                    "total_tokens_used": metrics.total_tokens_used,
                    "error_rate": metrics.error_rate,
                    "active_agents": len([a for a in metrics.active_agents if a.status == "active"]),
                    "system_metrics": metrics.system_metrics.dict(),
                    "cost_analysis": metrics.cost_analysis.dict(),
                },
                channel="metrics"
            )
            
            await asyncio.sleep(5)
            
        except Exception as e:
            logger.error(f"Error in metric broadcaster: {e}")
            await asyncio.sleep(10)


async def start_alert_broadcaster(db: Session):
    """
    Background task to broadcast alerts to all connected clients.
    Run this in a separate asyncio task.
    """
    ml_alerts_service = MLAlertsService(db)
    
    while True:
        try:
            # Get alerts every 10 seconds
            alerts = await ml_alerts_service.get_active_alerts()
            
            if alerts:
                await manager.broadcast(
                    {
                        "alerts": [alert.dict() for alert in alerts],
                        "count": len(alerts)
                    },
                    channel="alerts"
                )
            
            await asyncio.sleep(10)
            
        except Exception as e:
            logger.error(f"Error in alert broadcaster: {e}")
            await asyncio.sleep(15)
