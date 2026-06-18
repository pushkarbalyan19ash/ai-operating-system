from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
import asyncio
import json

from app.models.task import Task
from app.models.agent import Agent
from app.schemas.monitoring import (
    DashboardMetrics,
    SystemMetrics,
    AgentMetrics,
    Alert,
    CostAnalysis,
    PromptLog,
    AgentStatus,
    AlertType
)


class MonitoringService:
    """Service for monitoring and tracking agent metrics"""

    def __init__(self, db: Session):
        self.db = db

    async def get_dashboard_metrics(self) -> DashboardMetrics:
        """Get comprehensive dashboard metrics"""
        now = datetime.utcnow()

        # Get agent metrics
        agents = self.db.query(Agent).all()
        agent_metrics = [self._get_agent_metrics(agent) for agent in agents]

        # Get system metrics
        system_metrics = await self._get_system_metrics()

        # Get overall statistics
        all_tasks = self.db.query(Task).filter(
            Task.created_at >= now - timedelta(hours=24)
        ).all()

        completed_tasks = [t for t in all_tasks if t.status == "completed"]
        failed_tasks = [t for t in all_tasks if t.status == "failed"]

        success_rate = (
            len(completed_tasks) / len(all_tasks) * 100
            if all_tasks
            else 0
        )

        avg_execution_time = (
            sum(t.execution_time for t in completed_tasks) / len(completed_tasks)
            if completed_tasks
            else 0
        )

        total_tokens = sum(
            t.tokens_used for t in completed_tasks if t.tokens_used
        )

        error_rate = (
            len(failed_tasks) / len(all_tasks) * 100
            if all_tasks
            else 0
        )

        # Get alerts
        alerts = await self._get_recent_alerts()

        # Get cost analysis
        cost_analysis = await self._get_cost_analysis()

        # Get task timeline
        task_timeline = self._get_task_timeline(all_tasks)

        # Get active loops
        active_loops = self._get_active_loops()

        return DashboardMetrics(
            timestamp=now,
            overall_success_rate=success_rate,
            avg_execution_time=avg_execution_time,
            total_tokens_used=total_tokens,
            error_rate=error_rate,
            active_agents=agent_metrics,
            system_metrics=system_metrics,
            recent_alerts=alerts,
            cost_analysis=cost_analysis,
            task_timeline=task_timeline,
            active_loops=active_loops
        )

    def _get_agent_metrics(self, agent: Agent) -> AgentMetrics:
        """Calculate metrics for a specific agent"""
        now = datetime.utcnow()
        agent_tasks = self.db.query(Task).filter(
            and_(
                Task.agent_id == agent.id,
                Task.created_at >= now - timedelta(hours=24)
            )
        ).all()

        completed = [t for t in agent_tasks if t.status == "completed"]
        success_rate = (
            len(completed) / len(agent_tasks) * 100
            if agent_tasks
            else 0
        )

        avg_time = (
            sum(t.execution_time for t in completed) / len(completed)
            if completed
            else 0
        )

        status = AgentStatus.IDLE
        if agent.is_active:
            status = AgentStatus.ACTIVE
        elif agent.last_error:
            status = AgentStatus.ERROR

        return AgentMetrics(
            agent_id=agent.id,
            agent_name=agent.name,
            status=status,
            tasks_completed=len(completed),
            success_rate=success_rate,
            avg_execution_time=avg_time,
            last_task_timestamp=agent.last_task_timestamp,
            current_task=agent.current_task
        )

    async def _get_system_metrics(self) -> SystemMetrics:
        """Get current system metrics"""
        # Note: In production, integrate with actual system monitoring
        # This is a placeholder implementation
        now = datetime.utcnow()
        agents = self.db.query(Agent).all()
        active_agents = len([a for a in agents if a.is_active])
        total_agents = len(agents)

        all_tasks = self.db.query(Task).all()
        pending = len([t for t in all_tasks if t.status == "pending"])
        completed = len([t for t in all_tasks if t.status == "completed"])
        failed = len([t for t in all_tasks if t.status == "failed"])

        return SystemMetrics(
            timestamp=now,
            cpu_usage=45.5,  # Placeholder
            memory_usage=62.3,  # Placeholder
            gpu_usage=38.1,  # Placeholder
            active_agents=active_agents,
            total_agents=total_agents,
            pending_tasks=pending,
            completed_tasks=completed,
            failed_tasks=failed
        )

    async def _get_recent_alerts(self, limit: int = 10) -> List[Alert]:
        """Get recent alerts"""
        # Placeholder implementation
        # In production, fetch from Alert model
        alerts = []
        now = datetime.utcnow()

        if await self._check_high_error_rate():
            alerts.append(Alert(
                id="alert_1",
                alert_type=AlertType.ERROR,
                message="High Error Rate Detected",
                timestamp=now,
                severity="high"
            ))

        if await self._check_excessive_logging():
            alerts.append(Alert(
                id="alert_2",
                alert_type=AlertType.WARNING,
                message="Excessive Logging Warning",
                timestamp=now - timedelta(minutes=5),
                severity="medium"
            ))

        if await self._check_cost_threshold():
            alerts.append(Alert(
                id="alert_3",
                alert_type=AlertType.ERROR,
                message="Cost Threshold Exceeded",
                timestamp=now - timedelta(minutes=12),
                severity="high"
            ))

        return alerts[:limit]

    async def _get_cost_analysis(self) -> CostAnalysis:
        """Get cost analysis data"""
        now = datetime.utcnow()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        daily_tasks = self.db.query(Task).filter(
            Task.created_at >= today
        ).all()
        weekly_tasks = self.db.query(Task).filter(
            Task.created_at >= week_ago
        ).all()
        monthly_tasks = self.db.query(Task).filter(
            Task.created_at >= month_ago
        ).all()

        daily_cost = sum(t.cost for t in daily_tasks if t.cost)
        weekly_cost = sum(t.cost for t in weekly_tasks if t.cost)
        monthly_cost = sum(t.cost for t in monthly_tasks if t.cost)

        total_tokens = sum(t.tokens_used for t in weekly_tasks if t.tokens_used)
        cost_per_token = weekly_cost / total_tokens if total_tokens > 0 else 0
        cost_per_task = weekly_cost / len(weekly_tasks) if weekly_tasks else 0

        return CostAnalysis(
            total_cost=monthly_cost,
            daily_cost=daily_cost,
            weekly_cost=weekly_cost,
            monthly_cost=monthly_cost,
            cost_per_task=cost_per_task,
            cost_per_token=cost_per_token,
            timestamp=now
        )

    def _get_task_timeline(self, tasks: List[Task]) -> List[Dict[str, Any]]:
        """Get task execution timeline phases"""
        phases = []
        for task in tasks[:1]:  # Example with first task
            if task.execution_details:
                phases = task.execution_details.get("phases", [])
        return phases

    def _get_active_loops(self) -> Dict[str, int]:
        """Get count of active agent loops by type"""
        # Placeholder implementation
        return {
            "active": 14,
            "samples": 9,
            "retries": 3
        }

    async def _check_high_error_rate(self, threshold: float = 5.0) -> bool:
        """Check if error rate exceeds threshold"""
        now = datetime.utcnow()
        recent_tasks = self.db.query(Task).filter(
            Task.created_at >= now - timedelta(hours=1)
        ).all()

        if not recent_tasks:
            return False

        error_rate = (
            len([t for t in recent_tasks if t.status == "failed"]) /
            len(recent_tasks) * 100
        )
        return error_rate > threshold

    async def _check_excessive_logging(self) -> bool:
        """Check for excessive logging"""
        # Placeholder
        return False

    async def _check_cost_threshold(self, threshold: float = 100.0) -> bool:
        """Check if daily cost exceeds threshold"""
        cost_analysis = await self._get_cost_analysis()
        return cost_analysis.daily_cost > threshold

    async def get_agent_logs(
        self,
        agent_id: Optional[str] = None,
        limit: int = 50
    ) -> List[PromptLog]:
        """Get prompt and response logs"""
        # Placeholder implementation
        # In production, fetch from logs database
        return []
