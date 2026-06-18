from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class AgentStatus(str, Enum):
    ACTIVE = "active"
    IDLE = "idle"
    ERROR = "error"
    STOPPED = "stopped"


class AlertType(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class AgentMetrics(BaseModel):
    """Real-time metrics for an agent"""
    agent_id: str
    agent_name: str
    status: AgentStatus
    tasks_completed: int
    success_rate: float
    avg_execution_time: float
    last_task_timestamp: Optional[datetime] = None
    current_task: Optional[str] = None

    class Config:
        use_enum_values = True


class SystemMetrics(BaseModel):
    """System-wide performance metrics"""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    gpu_usage: float
    active_agents: int
    total_agents: int
    pending_tasks: int
    completed_tasks: int
    failed_tasks: int


class TaskMetrics(BaseModel):
    """Metrics for a specific task execution"""
    task_id: str
    agent_id: str
    start_time: datetime
    end_time: datetime
    duration: float
    status: str
    tokens_used: int
    cost: float
    error_message: Optional[str] = None


class Alert(BaseModel):
    """Alert notification"""
    id: str
    alert_type: AlertType
    message: str
    timestamp: datetime
    severity: str
    metadata: Dict[str, Any] = {}

    class Config:
        use_enum_values = True


class CostAnalysis(BaseModel):
    """Cost tracking and analysis"""
    total_cost: float
    daily_cost: float
    weekly_cost: float
    monthly_cost: float
    cost_per_task: float
    cost_per_token: float
    currency: str = "USD"
    timestamp: datetime


class PromptLog(BaseModel):
    """Log entry for prompts and responses"""
    id: str
    agent_id: str
    prompt: str
    response: str
    tool_used: Optional[str] = None
    result: Optional[str] = None
    status: str
    timestamp: datetime
    execution_time: float
    tokens_used: int


class DashboardMetrics(BaseModel):
    """Complete dashboard metrics snapshot"""
    timestamp: datetime
    overall_success_rate: float
    avg_execution_time: float
    total_tokens_used: int
    error_rate: float
    active_agents: List[AgentMetrics]
    system_metrics: SystemMetrics
    recent_alerts: List[Alert]
    cost_analysis: CostAnalysis
    task_timeline: List[Dict[str, Any]]
    active_loops: Dict[str, int]
