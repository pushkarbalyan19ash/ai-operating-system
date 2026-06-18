from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.monitoring_service import MonitoringService
from app.schemas.monitoring import DashboardMetrics, SystemMetrics, AgentMetrics

router = APIRouter(
    prefix="/api/monitoring",
    tags=["monitoring"]
)


@router.get("/dashboard", response_model=DashboardMetrics)
async def get_dashboard_metrics(db: Session = Depends(get_db)):
    """
    Get comprehensive dashboard metrics including:
    - Agent metrics and status
    - System resource usage
    - Cost analysis
    - Recent alerts
    - Task timeline
    - Active agent loops
    """
    service = MonitoringService(db)
    return await service.get_dashboard_metrics()


@router.get("/agents", response_model=list[AgentMetrics])
async def get_agent_metrics(db: Session = Depends(get_db)):
    """
    Get metrics for all active agents
    """
    service = MonitoringService(db)
    metrics = await service.get_dashboard_metrics()
    return metrics.active_agents


@router.get("/system", response_model=SystemMetrics)
async def get_system_metrics(db: Session = Depends(get_db)):
    """
    Get current system resource metrics
    """
    service = MonitoringService(db)
    metrics = await service.get_dashboard_metrics()
    return metrics.system_metrics


@router.get("/alerts")
async def get_alerts(db: Session = Depends(get_db)):
    """
    Get recent system alerts
    """
    service = MonitoringService(db)
    metrics = await service.get_dashboard_metrics()
    return metrics.recent_alerts


@router.get("/cost")
async def get_cost_analysis(db: Session = Depends(get_db)):
    """
    Get cost analysis and spending trends
    """
    service = MonitoringService(db)
    metrics = await service.get_dashboard_metrics()
    return metrics.cost_analysis


@router.get("/logs")
async def get_prompt_logs(
    agent_id: str = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get prompt and response logs for agents
    """
    service = MonitoringService(db)
    return await service.get_agent_logs(agent_id, limit)
