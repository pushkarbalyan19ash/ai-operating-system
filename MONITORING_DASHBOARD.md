# Advanced Monitoring Dashboard

## Overview

The Monitoring Dashboard is a real-time analytics and performance tracking system for the NEXUS AI OS. It provides comprehensive insights into agent activities, system metrics, costs, and alerts.

## Features

### 1. **Real-Time Agent Metrics**
- Success rate tracking
- Average execution time
- Token usage monitoring
- Error rate tracking
- Agent status indicators (Active, Idle, Error)

### 2. **System Metrics Dashboard**
- CPU usage tracking
- Memory utilization
- GPU usage monitoring
- Real-time performance graphs
- Historical data visualization

### 3. **Task Execution Timeline**
- Visual timeline of task phases
- Duration breakdown per phase
- Start, API Call, Processing, LLM Response, Completion phases
- Color-coded status indicators

### 4. **Cost Analysis**
- Daily, weekly, monthly cost tracking
- Cost per task metrics
- Cost per token analysis
- Spending trend charts
- Budget threshold alerts

### 5. **Alert Management**
- High error rate detection
- Excessive logging warnings
- Cost threshold alerts
- Real-time alert notifications
- Alert history tracking

### 6. **Agent Activity Panel**
- List of active agents
- Current task assignment
- Task completion counts
- Agent status indicators
- Live update indicators

### 7. **Active Agent Loops**
- Visualization of concurrent agent operations
- Loop type breakdown (Active, Samples, Retries)
- Loop statistics and distribution
- Active loop count tracking

### 8. **Prompt & Response Logs**
- Detailed prompt and response history
- Tool usage tracking
- Execution result logging
- Status indicators
- Expandable log entries for details

## Architecture

### Frontend Components

```
MonitoringDashboard/
├── AgentActivityPanel.tsx      # Real-time agent status
├── TaskTimelineVisualization.tsx # Task execution timeline
├── CostAnalysisPanel.tsx        # Cost tracking and trends
├── SystemMetricsPanel.tsx       # System resource monitoring
├── AlertsPanel.tsx              # Alert management
├── ActiveAgentLoops.tsx         # Loop visualization
└── PromptResponseLogs.tsx       # Prompt/response history
```

### Backend Services

```
MonitoringService/
├── get_dashboard_metrics()      # Aggregate all metrics
├── get_agent_metrics()          # Per-agent metrics
├── get_system_metrics()         # System resource data
├── get_recent_alerts()          # Active alerts
├── get_cost_analysis()          # Cost tracking
├── get_task_timeline()          # Task execution data
└── get_active_loops()           # Loop statistics
```

### Database Models

- `SystemAlert` - Alert records
- `TaskMetrics` - Task execution metrics
- `PromptLog` - Prompt/response history
- `CostRecord` - Cost tracking records

## API Endpoints

### `/api/monitoring/dashboard`
**GET** - Get comprehensive dashboard metrics

Response includes:
- Overall success rate
- Average execution time
- Total tokens used
- Error rate
- Active agent metrics
- System metrics
- Recent alerts
- Cost analysis
- Task timeline
- Active loops

### `/api/monitoring/agents`
**GET** - Get metrics for all agents

### `/api/monitoring/system`
**GET** - Get system resource metrics

### `/api/monitoring/alerts`
**GET** - Get recent alerts

### `/api/monitoring/cost`
**GET** - Get cost analysis data

### `/api/monitoring/logs`
**GET** - Get prompt/response logs
Query Parameters:
- `agent_id` (optional) - Filter by agent
- `limit` (default: 50) - Number of logs to return

## Real-Time Updates

### WebSocket Integration (Future)

```typescript
const socket = new WebSocket('ws://localhost:8001/ws/monitoring');

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // Update dashboard with real-time metrics
};
```

## Usage

### Access the Dashboard

```
http://localhost:3000/dashboard/monitoring
```

### Fetch Dashboard Metrics

```typescript
const response = await fetch('/api/monitoring/dashboard');
const metrics = await response.json();

console.log(metrics.overall_success_rate);
console.log(metrics.active_agents);
console.log(metrics.cost_analysis);
```

## Metrics Definitions

### Success Rate
Percentage of tasks that completed successfully.
```
Success Rate = (Completed Tasks / Total Tasks) × 100
```

### Average Execution Time
Mean time taken to execute a task.
```
Avg Time = Sum(Execution Times) / Number of Tasks
```

### Token Usage
Total tokens consumed by LLM operations.
```
Total Tokens = Sum of tokens from all LLM calls
```

### Error Rate
Percentage of tasks that failed.
```
Error Rate = (Failed Tasks / Total Tasks) × 100
```

### Cost Analysis
```
Daily Cost = Sum of costs for tasks completed today
Cost per Task = Total Weekly Cost / Number of Tasks
Cost per Token = Total Weekly Cost / Total Tokens Used
```

## Alerts Configuration

### Alert Types

1. **High Error Rate**
   - Trigger: Error rate > 5%
   - Severity: High
   - Action: Investigate agent failures

2. **Excessive Logging**
   - Trigger: Log volume > threshold
   - Severity: Medium
   - Action: Review logging configuration

3. **Cost Threshold**
   - Trigger: Daily cost > $100
   - Severity: High
   - Action: Review spending trends

### Custom Alerts

To add custom alerts, extend the `_get_recent_alerts()` method in `MonitoringService`:

```python
if await self._check_custom_condition():
    alerts.append(Alert(
        id="custom_alert_id",
        alert_type=AlertType.WARNING,
        message="Custom alert message",
        timestamp=now,
        severity="medium"
    ))
```

## Performance Optimization

### Frontend
- Lazy loading of components
- Memoized calculations
- Efficient chart rendering with Recharts
- Debounced real-time updates

### Backend
- Query optimization with indexes
- Caching of computed metrics
- Asynchronous data fetching
- Database connection pooling

## Future Enhancements

1. **Real-Time WebSocket Updates**
   - Live metric streaming
   - Push notifications for alerts
   - Reduced polling overhead

2. **Advanced Analytics**
   - Predictive performance metrics
   - Anomaly detection
   - Pattern recognition
   - Trend forecasting

3. **Custom Dashboards**
   - User-defined widgets
   - Configurable layouts
   - Saved dashboard views
   - Export capabilities

4. **Alerting Automation**
   - Automated remediation
   - Escalation policies
   - Integration with monitoring tools
   - Webhook support

5. **Machine Learning Integration**
   - Performance predictions
   - Cost optimization suggestions
   - Anomaly detection
   - Root cause analysis

## Troubleshooting

### Missing Metrics
- Ensure agents are properly registered
- Check database connectivity
- Verify task records are being created

### High CPU Usage
- Reduce update frequency
- Optimize chart rendering
- Enable data virtualization

### Cost Tracking Issues
- Verify cost calculation logic
- Check LLM API cost configuration
- Validate token counting

## Support

For issues or questions about the monitoring dashboard, please refer to:
- Project documentation
- GitHub issues
- Contributing guidelines
