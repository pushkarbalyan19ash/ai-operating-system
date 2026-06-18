# WebSocket, ML Alerts, and Testing Documentation

## WebSocket Integration

### Overview

The WebSocket integration provides real-time, bidirectional communication between the frontend and backend, enabling live metric streaming and instant alert notifications without polling.

### Features

- **Real-time Metric Updates** - Live streaming of all metrics every 5 seconds
- **Instant Alert Notifications** - Alerts pushed to clients as they occur
- **Channel-Based Subscriptions** - Subscribe/unsubscribe to specific data channels
- **Automatic Reconnection** - Exponential backoff retry strategy
- **Connection Management** - Track active connections and manage subscriptions
- **Scalable Broadcasting** - Efficient message delivery to multiple clients

### Architecture

#### Backend Components

```
app/websocket/
├── connection_manager.py  # Connection and subscription management
└── routes.py             # WebSocket endpoints

app/api/routes/
└── ml_alerts.py          # ML-powered alerts endpoints
```

#### Frontend Components

```
frontend/src/
├── hooks/
│   └── useMonitoringWebSocket.ts  # WebSocket hook
└── store/
    ├── monitoring.ts  # Metrics store (Zustand)
    └── alerts.ts      # Alerts store (Zustand)
```

### Connection Flow

```
1. Client connects to: ws://localhost:8001/api/ws/monitoring/{client_id}
2. Client subscribes to channels:
   - metrics: Real-time metrics updates
   - alerts: Alert notifications
   - agent_status: Agent status changes
   - cost: Cost updates
   - system: System resource updates
3. Server broadcasts updates to subscribed clients
4. On disconnect, automatic reconnection with exponential backoff
```

### Usage

#### Backend Setup

Add to your `app.main` or startup event:

```python
from app.websocket.routes import start_metric_broadcaster, start_alert_broadcaster
import asyncio

@app.on_event("startup")
async def startup_events():
    # Start background broadcasters
    asyncio.create_task(start_metric_broadcaster(db))
    asyncio.create_task(start_alert_broadcaster(db))
```

#### Frontend Usage

```typescript
import { useMonitoringWebSocket } from '@/hooks/useMonitoringWebSocket';

function MyComponent() {
  const { isConnected, subscribe, unsubscribe, send } = useMonitoringWebSocket('user-123');
  
  useEffect(() => {
    if (isConnected) {
      // Subscribe to metrics
      subscribe('metrics');
      subscribe('alerts');
    }
  }, [isConnected]);
  
  // Use Zustand stores for data
  const metrics = useMonitoringStore(state => state.metrics);
  const alerts = useAlertsStore(state => state.alerts);
  
  return (
    <div>
      <p>Connected: {isConnected ? 'Yes' : 'No'}</p>
      <p>Success Rate: {metrics?.success_rate}%</p>
      {alerts.map(alert => <Alert key={alert.id} alert={alert} />)}
    </div>
  );
}
```

### Message Format

#### Subscribe to Channel

```json
{
  "action": "subscribe",
  "channel": "metrics"
}
```

#### Unsubscribe from Channel

```json
{
  "action": "unsubscribe",
  "channel": "metrics"
}
```

#### Server Response (Metrics Update)

```json
{
  "channel": "metrics",
  "timestamp": "2026-06-18T12:34:56.789Z",
  "data": {
    "success_rate": 92.5,
    "avg_execution_time": 14.3,
    "total_tokens_used": 3800,
    "error_rate": 5.2,
    "active_agents": 3,
    "system_metrics": {
      "cpu_usage": 45.5,
      "memory_usage": 62.3,
      "gpu_usage": 38.1
    },
    "cost_analysis": {
      "daily_cost": 45.50,
      "weekly_cost": 782.00,
      "monthly_cost": 3200.00
    }
  }
}
```

#### Server Response (Alert)

```json
{
  "channel": "alerts",
  "timestamp": "2026-06-18T12:34:56.789Z",
  "data": {
    "alerts": [
      {
        "id": "alert_1",
        "alert_type": "error",
        "message": "High Error Rate Detected",
        "timestamp": "2026-06-18T12:34:56Z",
        "severity": "high",
        "metadata": { ... }
      }
    ],
    "count": 1
  }
}
```

### Reconnection Strategy

The client automatically reconnects with exponential backoff:

```
Attempt 1: 3 seconds
Attempt 2: 6 seconds
Attempt 3: 12 seconds
Attempt 4: 24 seconds
Attempt 5: 48 seconds
```

After 5 failed attempts, reconnection stops and an error is logged.

---

## ML-Powered Alert System

### Overview

The ML alerts system uses machine learning algorithms to detect anomalies, predict performance degradation, and forecast costs without explicit rule configuration.

### Features

#### 1. Anomaly Detection

Uses **Isolation Forest** algorithm to detect unusual patterns:

- Identifies tasks with anomalous execution times
- Detects unusual token usage patterns
- Flags unexpected cost spikes
- Works without labeled training data

```python
from sklearn.ensemble import IsolationForest

model = IsolationForest(
    contamination=0.1,  # 10% anomalies expected
    random_state=42,
    n_estimators=100
)
```

#### 2. Performance Degradation Detection

Identifies patterns indicating service degradation:

- **Execution Time Trends** - Detects consistent increases in task duration
- **Error Rate Spikes** - Identifies sudden increases in failure rates
- **Agent-Level Analysis** - Per-agent degradation tracking

```python
# Detects if execution times are consistently increasing
if np.mean(diffs) > 0 and np.sum(diffs > 0) >= len(diffs) - 1:
    alert = create_degradation_alert(agent)
```

#### 3. Cost Prediction

Forecasts future costs using linear regression:

- Predicts next day's cost
- Extrapolates weekly and monthly costs
- Identifies spending trends
- Provides cost analysis data

```python
import numpy as np

# Linear regression on historical data
x = np.arange(len(costs))
z = np.polyfit(x, costs, 1)  # Linear fit
p = np.poly1d(z)
next_day_cost = p(len(costs))
```

#### 4. Performance Prediction

Forecasts performance metrics using time series analysis:

- Predicts average execution time
- Forecasts success rate
- Estimates token usage
- Provides trend indicators

```python
# Moving average for trend prediction
moving_avg = np.convolve(
    execution_times,
    np.ones(window_size) / window_size,
    mode='valid'
)
```

### API Endpoints

#### GET `/api/ml-alerts/anomalies`

Detect anomalies in agent performance.

**Response:**
```json
[
  {
    "id": "ml_anomaly_task_123",
    "alert_type": "warning",
    "message": "Anomaly detected in task 123: Unusual execution pattern",
    "timestamp": "2026-06-18T12:34:56Z",
    "severity": "medium",
    "metadata": {
      "task_id": "task_123",
      "anomaly_score": -2.45,
      "execution_time": 45.2,
      "tokens_used": 5000
    }
  }
]
```

#### GET `/api/ml-alerts/predictions/performance`

Get performance predictions for the next period.

**Response:**
```json
{
  "predicted_execution_time": 14.8,
  "trend": "increasing",
  "predicted_success_rate": 91.5,
  "predicted_avg_tokens": 1050,
  "token_usage_std": 250
}
```

#### GET `/api/ml-alerts/predictions/cost`

Get cost predictions for the next period.

**Response:**
```json
{
  "predicted_daily_cost": 52.30,
  "cost_trend": "increasing",
  "predicted_weekly_cost": 366.10,
  "predicted_monthly_cost": 1569.00,
  "historical_daily_costs": {
    "2026-06-18": 45.50,
    "2026-06-17": 48.20,
    "2026-06-16": 50.10
  }
}
```

#### GET `/api/ml-alerts/degradation`

Detect performance degradation patterns.

**Response:**
```json
[
  {
    "id": "perf_degrad_agent_1",
    "alert_type": "warning",
    "message": "Performance degradation detected for agent 'Research Agent'",
    "timestamp": "2026-06-18T12:34:56Z",
    "severity": "medium",
    "metadata": {
      "agent_id": "agent_1",
      "execution_times": [5.0, 5.2, 5.1, 5.3, 5.2, 5.4, 5.3, 5.5],
      "trend": "degrading"
    }
  }
]
```

#### GET `/api/ml-alerts/active`

Get all active ML-detected alerts.

**Response:**
```json
[
  { ...anomaly_alerts... },
  { ...degradation_alerts... }
]
```

#### GET `/api/ml-alerts/summary`

Get comprehensive ML metrics and predictions.

**Response:**
```json
{
  "performance_predictions": { ... },
  "cost_predictions": { ... },
  "active_alerts": [ ... ],
  "alert_count": 3,
  "timestamp": "2026-06-18T12:34:56Z"
}
```

### Configuration

#### Anomaly Detection Parameters

```python
contamination=0.1      # Expect 10% of data to be anomalies
n_estimators=100       # Number of trees in the forest
random_state=42        # Reproducible results
```

#### Degradation Detection Thresholds

```python
error_rate_threshold=0.20  # 20% error rate triggers alert
window_size=10             # Analyze last 10 tasks
```

---

## Integration Testing

### Overview

Comprehensive integration tests ensure all components work together correctly.

### Test Structure

```
backend/tests/
├── test_monitoring_integration.py  # Monitoring service and API tests
└── test_websocket.py              # WebSocket connection tests
```

### Test Categories

#### 1. Monitoring Service Tests

**TestMonitoringService**
- `test_get_dashboard_metrics` - Retrieve complete dashboard
- `test_get_agent_metrics` - Get per-agent metrics
- `test_get_system_metrics` - Get system resource data

#### 2. ML Alerts Service Tests

**TestMLAlertsService**
- `test_predict_performance` - Performance prediction accuracy
- `test_predict_cost` - Cost prediction accuracy
- `test_detect_performance_degradation` - Degradation detection
- `test_detect_anomalies` - Anomaly detection accuracy

#### 3. API Endpoint Tests

**TestMonitoringAPI**
- `test_get_dashboard_metrics_endpoint` - Dashboard endpoint
- `test_get_agents_endpoint` - Agent metrics endpoint
- `test_get_system_metrics_endpoint` - System metrics endpoint
- `test_get_alerts_endpoint` - Alerts endpoint
- `test_get_cost_endpoint` - Cost endpoint

**TestMLAlertsAPI**
- `test_get_anomalies_endpoint` - Anomaly detection endpoint
- `test_get_performance_predictions_endpoint` - Performance prediction
- `test_get_cost_predictions_endpoint` - Cost prediction
- `test_get_degradation_endpoint` - Degradation detection
- `test_get_ml_summary_endpoint` - ML summary endpoint

#### 4. WebSocket Tests

**TestConnectionManager**
- `test_connect` - Client connection
- `test_disconnect` - Client disconnection
- `test_subscribe` - Channel subscription
- `test_unsubscribe` - Channel unsubscription
- `test_broadcast` - Message broadcasting
- `test_send_personal` - Personal messaging
- `test_handle_subscription` - Subscription handling
- `test_get_connection_stats` - Connection statistics
- `test_broadcast_to_multiple_channels` - Multi-channel broadcasting
- `test_disconnect_on_send_error` - Error handling

### Running Tests

#### Install dependencies

```bash
pip install pytest pytest-asyncio pytest-cov
```

#### Run all tests

```bash
pytest backend/tests/ -v
```

#### Run specific test class

```bash
pytest backend/tests/test_monitoring_integration.py::TestMonitoringService -v
```

#### Run specific test

```bash
pytest backend/tests/test_monitoring_integration.py::TestMonitoringService::test_get_dashboard_metrics -v
```

#### Run with coverage

```bash
pytest backend/tests/ --cov=app --cov-report=html
```

### Test Database Setup

Tests use SQLite in-memory database:

```python
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### Fixtures

#### db fixture

```python
@pytest.fixture(scope="function")
def db():
    """Create test database and tables"""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)
```

Each test gets a fresh database.

### Example Test

```python
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
```

### Mocking

Use `unittest.mock` for external dependencies:

```python
from unittest.mock import Mock, AsyncMock, patch

@pytest.mark.asyncio
async def test_broadcast(self, connection_manager):
    websocket1 = AsyncMock()
    websocket2 = AsyncMock()
    
    connection_manager.active_connections["client_1"] = [websocket1]
    connection_manager.subscriptions[websocket1] = {"metrics"}
    
    await connection_manager.broadcast({"data": "test"}, channel="metrics")
    
    websocket1.send_json.assert_called_once()
```

### Coverage Goals

- **Line Coverage:** > 85%
- **Branch Coverage:** > 80%
- **Function Coverage:** 100%

### Continuous Integration

Add to `.github/workflows/tests.yml`:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - run: pip install -r backend/requirements.txt
      - run: pip install pytest pytest-asyncio pytest-cov
      - run: pytest backend/tests/ --cov=app --cov-report=xml
      - uses: codecov/codecov-action@v2
```

---

## Integration Workflow

### How They Work Together

```
┌─────────────────────────────────────┐
│   Frontend Dashboard (React)        │
│  - Real-time metric display         │
│  - Alert notifications              │
│  - Cost visualization               │
└────────────┬────────────────────────┘
             │
      WebSocket (bi-directional)
             │
┌────────────▼────────────────────────┐
│   Backend Services (FastAPI)        │
│                                     │
│  ┌─ Monitoring Service ─────────┐  │
│  │  Collects and aggregates     │  │
│  │  real-time metrics           │  │
│  └──────────────┬────────────────┘  │
│                 │                    │
│  ┌──────────────▼──────────────┐   │
│  │   ML Alerts Service        │   │
│  │  - Anomaly detection       │   │
│  │  - Performance prediction  │   │
│  │  - Cost forecasting        │   │
│  │  - Degradation detection   │   │
│  └──────────────┬──────────────┘   │
│                 │                    │
│  ┌──────────────▼──────────────┐   │
│  │  Connection Manager         │   │
│  │  - Manages WebSocket conns  │   │
│  │  - Handles subscriptions    │   │
│  │  - Broadcasts messages     │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
             ▲
             │
      PostgreSQL Database
    (Tasks, Agents, Logs)
```

### Real-Time Update Flow

1. **Task Execution** - Agent completes a task
2. **Metrics Collection** - Monitoring Service calculates metrics
3. **ML Analysis** - ML Alerts Service analyzes data for anomalies/predictions
4. **Broadcasting** - Connection Manager sends updates via WebSocket
5. **Frontend Update** - React components receive and display data
6. **User Notification** - Real-time alerts displayed to user

---

## Performance Optimization

### Backend

- **Async Operations** - Non-blocking WebSocket handlers
- **Database Indexes** - Fast query execution
- **Batch Broadcasts** - Efficient multi-client messaging
- **ML Caching** - Cache model predictions

### Frontend

- **Zustand Stores** - Minimal re-renders
- **Memoization** - Prevent unnecessary component updates
- **Lazy Loading** - Load components on demand
- **Debounced Updates** - Limit update frequency

---

## Troubleshooting

### WebSocket Connection Issues

**Problem:** Client cannot connect to WebSocket

**Solution:**
- Check WebSocket URL is correct
- Verify backend is running
- Check CORS and firewall settings
- Review browser console for errors

### ML Alerts Not Firing

**Problem:** No anomaly alerts detected

**Solution:**
- Ensure sufficient historical data exists (>10 tasks)
- Check contamination parameter
- Verify task data quality
- Review logs for errors

### Test Failures

**Problem:** Tests fail with "Database locked" error

**Solution:**
- Clear test database: `rm test.db`
- Use in-memory SQLite: `DATABASE_URL = "sqlite:///:memory:"`
- Check for concurrent test execution

---

## Next Steps

1. **Deploy to Production** - Set up cloud infrastructure
2. **Add More ML Models** - Random Forest, Neural Networks
3. **Implement Caching** - Redis for performance
4. **Add Auth** - Secure WebSocket connections
5. **Scale Horizontally** - Load balancing for multiple servers
