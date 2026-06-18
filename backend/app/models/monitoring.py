from sqlalchemy import Column, String, Float, DateTime, JSON, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
import uuid


class SystemAlert(Base):
    __tablename__ = "system_alerts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    alert_type = Column(String, index=True)  # error, warning, info
    message = Column(String)
    severity = Column(String)  # low, medium, high, critical
    metadata = Column(JSON, default={})
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    resolved_at = Column(DateTime, nullable=True)


class TaskMetrics(Base):
    __tablename__ = "task_metrics"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String, ForeignKey("tasks.id"), index=True)
    agent_id = Column(String, ForeignKey("agents.id"), index=True)
    execution_time = Column(Float)
    tokens_used = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    status = Column(String)  # success, error, timeout
    error_message = Column(String, nullable=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class PromptLog(Base):
    __tablename__ = "prompt_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String, ForeignKey("agents.id"), index=True)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=True)
    prompt = Column(String)
    response = Column(String)
    tool_used = Column(String, nullable=True)
    result = Column(String, nullable=True)
    status = Column(String)  # success, error
    execution_time = Column(Float)
    tokens_used = Column(Integer, default=0)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class CostRecord(Base):
    __tablename__ = "cost_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String, ForeignKey("tasks.id"), index=True)
    agent_id = Column(String, ForeignKey("agents.id"), index=True)
    cost = Column(Float)
    tokens_used = Column(Integer)
    model = Column(String)
    currency = Column(String, default="USD")
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
