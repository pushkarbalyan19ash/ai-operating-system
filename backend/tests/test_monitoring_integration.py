import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import asyncio

from app.main import app
from app.db.database import Base, get_db
from app.models.task import Task
from app.models.agent import Agent
from app.services.monitoring_service import MonitoringService
from app.services.ml_alerts_service import MLAlertsService

# Test database setup
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function")
def db():
    """Create test database and tables"""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


class TestMonitoringService:
    """Test cases for MonitoringService"""

    def test_get_dashboard_metrics(self, db):
        """Test retrieving dashboard metrics"""
        service = MonitoringService(db)
        
        # Create test data
        agent = Agent(
            id="test_agent_1",
            name="Test Agent",
            is_active=True
        )
        db.add(agent)
        
        task = Task(
            id="test_task_1",
            agent_id="test_agent_1",
            status="completed",
            execution_time=5.0,
            tokens_used=1000,
            cost=0.05
        )
        db.add(task)
        db.commit()
        
        # Get metrics
        metrics = asyncio.run(service.get_dashboard_metrics())
        
        assert metrics is not None
        assert metrics.overall_success_rate >= 0
        assert metrics.avg_execution_time >= 0
        assert metrics.total_tokens_used >= 0

    def test_get_agent_metrics(self, db):
        """Test retrieving metrics for a specific agent"""
        service = MonitoringService(db)
        
        agent = Agent(
            id="test_agent_2",
            name="Test Agent 2",
            is_active=True
        )
        db.add(agent)
        
        # Create multiple tasks
        for i in range(5):
            task = Task(
                id=f"test_task_{i}",
                agent_id="test_agent_2",
                status="completed" if i < 4 else "failed",
                execution_time=float(i + 1),
                tokens_used=1000 * (i + 1),
                cost=0.05 * (i + 1)
            )
            db.add(task)
        
        db.commit()
        
        agent_metrics = service._get_agent_metrics(agent)
        
        assert agent_metrics.agent_id == "test_agent_2"
        assert agent_metrics.tasks_completed == 4
        assert agent_metrics.success_rate == 80.0
        assert agent_metrics.avg_execution_time > 0

    def test_get_system_metrics(self, db):
        """Test retrieving system metrics"""
        service = MonitoringService(db)
        
        agent1 = Agent(id="agent_1", name="Agent 1", is_active=True)
        agent2 = Agent(id="agent_2", name="Agent 2", is_active=False)
        db.add_all([agent1, agent2])
        
        task1 = Task(
            id="task_1", agent_id="agent_1", status="completed",
            execution_time=5.0, tokens_used=1000, cost=0.05
        )
        task2 = Task(
            id="task_2", agent_id="agent_1", status="pending",
            execution_time=None, tokens_used=0, cost=0
        )
        db.add_all([task1, task2])
        db.commit()
        
        system_metrics = asyncio.run(service._get_system_metrics())
        
        assert system_metrics.active_agents == 1
        assert system_metrics.total_agents == 2
        assert system_metrics.pending_tasks == 1
        assert system_metrics.completed_tasks == 1


class TestMLAlertsService:
    """Test cases for MLAlertsService"""

    def test_predict_performance(self, db):
        """Test performance prediction"""
        service = MLAlertsService(db)
        
        agent = Agent(id="ml_agent_1", name="ML Agent 1", is_active=True)
        db.add(agent)
        
        # Create tasks with execution times
        execution_times = [1.0, 1.2, 1.1, 1.3, 1.2, 1.4, 1.3, 1.5]
        for i, exec_time in enumerate(execution_times):
            task = Task(
                id=f"ml_task_{i}",
                agent_id="ml_agent_1",
                status="completed",
                execution_time=exec_time,
                tokens_used=1000,
                cost=0.05
            )
            db.add(task)
        
        db.commit()
        
        predictions = asyncio.run(service.predict_performance())
        
        assert "predicted_execution_time" in predictions
        assert predictions["predicted_execution_time"] > 0
        assert "predicted_success_rate" in predictions

    def test_predict_cost(self, db):
        """Test cost prediction"""
        service = MLAlertsService(db)
        
        agent = Agent(id="cost_agent_1", name="Cost Agent 1", is_active=True)
        db.add(agent)
        
        # Create tasks with costs over 7 days
        now = datetime.utcnow()
        costs = [10.0, 15.0, 12.0, 18.0, 14.0, 20.0, 16.0]
        
        for i, cost in enumerate(costs):
            task = Task(
                id=f"cost_task_{i}",
                agent_id="cost_agent_1",
                status="completed",
                execution_time=5.0,
                tokens_used=1000,
                cost=cost,
                created_at=now - timedelta(days=6 - i)
            )
            db.add(task)
        
        db.commit()
        
        predictions = asyncio.run(service.predict_cost())
        
        assert "predicted_daily_cost" in predictions
        assert "predicted_weekly_cost" in predictions
        assert "predicted_monthly_cost" in predictions
        assert predictions["predicted_daily_cost"] >= 0

    def test_detect_performance_degradation(self, db):
        """Test performance degradation detection"""
        service = MLAlertsService(db)
        
        agent = Agent(id="degrad_agent_1", name="Degradation Agent", is_active=True)
        db.add(agent)
        
        # Create tasks with increasing execution times (degradation)
        for i in range(10):
            task = Task(
                id=f"degrad_task_{i}",
                agent_id="degrad_agent_1",
                status="completed" if i < 8 else "failed",
                execution_time=1.0 + (i * 0.5),  # Increasing times
                tokens_used=1000,
                cost=0.05
            )
            db.add(task)
        
        db.commit()
        
        alerts = asyncio.run(service.detect_performance_degradation())
        
        # Should detect degradation
        assert len(alerts) > 0
        degradation_alerts = [a for a in alerts if "degradation" in a.message.lower()]
        assert len(degradation_alerts) > 0

    def test_detect_anomalies(self, db):
        """Test anomaly detection"""
        service = MLAlertsService(db)
        
        agent = Agent(id="anomaly_agent_1", name="Anomaly Agent", is_active=True)
        db.add(agent)
        
        # Create normal tasks
        for i in range(15):
            is_anomaly = i == 7  # One anomalous task
            task = Task(
                id=f"anomaly_task_{i}",
                agent_id="anomaly_agent_1",
                status="failed" if is_anomaly else "completed",
                execution_time=10.0 if is_anomaly else 5.0,
                tokens_used=5000 if is_anomaly else 1000,
                cost=0.5 if is_anomaly else 0.05
            )
            db.add(task)
        
        db.commit()
        
        alerts = asyncio.run(service.detect_anomalies())
        
        assert isinstance(alerts, list)


class TestMonitoringAPI:
    """Test cases for Monitoring API endpoints"""

    def test_get_dashboard_metrics_endpoint(self, db):
        """Test GET /api/monitoring/dashboard endpoint"""
        # Create test data
        agent = Agent(id="api_agent_1", name="API Agent", is_active=True)
        db.add(agent)
        
        task = Task(
            id="api_task_1",
            agent_id="api_agent_1",
            status="completed",
            execution_time=5.0,
            tokens_used=1000,
            cost=0.05
        )
        db.add(task)
        db.commit()
        
        response = client.get("/api/monitoring/dashboard")
        
        assert response.status_code == 200
        data = response.json()
        assert "overall_success_rate" in data
        assert "avg_execution_time" in data
        assert "active_agents" in data

    def test_get_agents_endpoint(self, db):
        """Test GET /api/monitoring/agents endpoint"""
        agent = Agent(id="api_agent_2", name="API Agent 2", is_active=True)
        db.add(agent)
        db.commit()
        
        response = client.get("/api/monitoring/agents")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_system_metrics_endpoint(self, db):
        """Test GET /api/monitoring/system endpoint"""
        response = client.get("/api/monitoring/system")
        
        assert response.status_code == 200
        data = response.json()
        assert "cpu_usage" in data
        assert "memory_usage" in data
        assert "gpu_usage" in data

    def test_get_alerts_endpoint(self, db):
        """Test GET /api/monitoring/alerts endpoint"""
        response = client.get("/api/monitoring/alerts")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_cost_endpoint(self, db):
        """Test GET /api/monitoring/cost endpoint"""
        response = client.get("/api/monitoring/cost")
        
        assert response.status_code == 200
        data = response.json()
        assert "daily_cost" in data
        assert "weekly_cost" in data
        assert "monthly_cost" in data


class TestMLAlertsAPI:
    """Test cases for ML Alerts API endpoints"""

    def test_get_anomalies_endpoint(self, db):
        """Test GET /api/ml-alerts/anomalies endpoint"""
        agent = Agent(id="ml_api_agent_1", name="ML API Agent", is_active=True)
        db.add(agent)
        
        for i in range(15):
            task = Task(
                id=f"ml_api_task_{i}",
                agent_id="ml_api_agent_1",
                status="completed",
                execution_time=5.0,
                tokens_used=1000,
                cost=0.05
            )
            db.add(task)
        
        db.commit()
        
        response = client.get("/api/ml-alerts/anomalies")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_performance_predictions_endpoint(self, db):
        """Test GET /api/ml-alerts/predictions/performance endpoint"""
        agent = Agent(id="perf_pred_agent", name="Perf Prediction Agent", is_active=True)
        db.add(agent)
        
        for i in range(10):
            task = Task(
                id=f"perf_pred_task_{i}",
                agent_id="perf_pred_agent",
                status="completed",
                execution_time=float(i + 1),
                tokens_used=1000,
                cost=0.05
            )
            db.add(task)
        
        db.commit()
        
        response = client.get("/api/ml-alerts/predictions/performance")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_get_cost_predictions_endpoint(self, db):
        """Test GET /api/ml-alerts/predictions/cost endpoint"""
        agent = Agent(id="cost_pred_agent", name="Cost Prediction Agent", is_active=True)
        db.add(agent)
        
        now = datetime.utcnow()
        for i in range(10):
            task = Task(
                id=f"cost_pred_task_{i}",
                agent_id="cost_pred_agent",
                status="completed",
                execution_time=5.0,
                tokens_used=1000,
                cost=0.05,
                created_at=now - timedelta(days=9 - i)
            )
            db.add(task)
        
        db.commit()
        
        response = client.get("/api/ml-alerts/predictions/cost")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_get_degradation_endpoint(self, db):
        """Test GET /api/ml-alerts/degradation endpoint"""
        response = client.get("/api/ml-alerts/degradation")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_ml_summary_endpoint(self, db):
        """Test GET /api/ml-alerts/summary endpoint"""
        response = client.get("/api/ml-alerts/summary")
        
        assert response.status_code == 200
        data = response.json()
        assert "performance_predictions" in data or "cost_predictions" in data
