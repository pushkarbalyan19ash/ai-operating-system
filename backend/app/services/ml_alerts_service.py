from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import logging

from app.models.task import Task
from app.models.agent import Agent
from app.models.monitoring import SystemAlert, TaskMetrics
from app.schemas.monitoring import Alert, AlertType

logger = logging.getLogger(__name__)


class MLAlertsService:
    """Machine Learning-powered anomaly detection and alerts"""

    def __init__(self, db: Session):
        self.db = db
        self.scaler = StandardScaler()
        self.isolation_forest = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )

    async def detect_anomalies(self) -> List[Alert]:
        """
        Detect anomalies in agent performance using Isolation Forest ML algorithm
        """
        alerts = []
        
        try:
            # Get task metrics from last 24 hours
            now = datetime.utcnow()
            time_window = now - timedelta(hours=24)
            
            tasks = self.db.query(Task).filter(
                Task.created_at >= time_window
            ).all()
            
            if len(tasks) < 10:
                logger.warning("Not enough data for anomaly detection")
                return alerts
            
            # Extract features
            features = []
            task_map = []
            
            for task in tasks:
                try:
                    execution_time = task.execution_time or 0
                    tokens = task.tokens_used or 0
                    cost = task.cost or 0
                    
                    features.append([
                        execution_time,
                        tokens,
                        cost,
                        1 if task.status == "completed" else 0
                    ])
                    task_map.append(task)
                except Exception as e:
                    logger.error(f"Error processing task {task.id}: {e}")
                    continue
            
            if len(features) < 5:
                return alerts
            
            # Normalize features
            features_array = np.array(features)
            features_scaled = self.scaler.fit_transform(features_array)
            
            # Detect anomalies
            predictions = self.isolation_forest.fit_predict(features_scaled)
            anomaly_scores = self.isolation_forest.score_samples(features_scaled)
            
            # Get anomalies
            anomalies = np.where(predictions == -1)[0]
            
            for idx in anomalies:
                task = task_map[idx]
                score = anomaly_scores[idx]
                
                alert = Alert(
                    id=f"ml_anomaly_{task.id}",
                    alert_type=AlertType.WARNING,
                    message=f"Anomaly detected in task {task.id}: Unusual execution pattern",
                    timestamp=now,
                    severity="medium",
                    metadata={
                        "task_id": task.id,
                        "agent_id": task.agent_id,
                        "anomaly_score": float(score),
                        "execution_time": task.execution_time,
                        "tokens_used": task.tokens_used
                    }
                )
                alerts.append(alert)
                logger.warning(f"Anomaly detected: {alert.message}")
            
        except Exception as e:
            logger.error(f"Error in anomaly detection: {e}")
        
        return alerts

    async def predict_performance(self) -> Dict[str, Any]:
        """
        Predict future performance metrics using time series analysis
        """
        predictions = {}
        
        try:
            now = datetime.utcnow()
            time_window = now - timedelta(hours=24)
            
            tasks = self.db.query(Task).filter(
                Task.created_at >= time_window
            ).order_by(Task.created_at).all()
            
            if len(tasks) < 5:
                return predictions
            
            # Extract execution times
            execution_times = [
                task.execution_time for task in tasks
                if task.execution_time is not None
            ]
            
            if len(execution_times) < 3:
                return predictions
            
            # Simple moving average prediction
            window_size = min(5, len(execution_times) // 2)
            if window_size > 0:
                moving_avg = np.convolve(
                    execution_times,
                    np.ones(window_size) / window_size,
                    mode='valid'
                )
                
                if len(moving_avg) > 0:
                    predicted_execution_time = float(moving_avg[-1])
                    predictions['predicted_execution_time'] = predicted_execution_time
                    predictions['trend'] = 'increasing' if moving_avg[-1] > moving_avg[0] else 'decreasing'
            
            # Calculate success rate trend
            completed = len([t for t in tasks if t.status == "completed"])
            success_rate = (completed / len(tasks)) * 100 if tasks else 0
            predictions['predicted_success_rate'] = success_rate
            
            # Predict resource usage
            tokens_list = [t.tokens_used for t in tasks if t.tokens_used]
            if tokens_list:
                avg_tokens = np.mean(tokens_list)
                std_tokens = np.std(tokens_list)
                predictions['predicted_avg_tokens'] = float(avg_tokens)
                predictions['token_usage_std'] = float(std_tokens)
            
        except Exception as e:
            logger.error(f"Error in performance prediction: {e}")
        
        return predictions

    async def predict_cost(self) -> Dict[str, float]:
        """
        Predict future costs using ML models
        """
        cost_prediction = {}
        
        try:
            now = datetime.utcnow()
            
            # Historical data (last 7 days)
            daily_costs = {}
            for i in range(7):
                day = now - timedelta(days=i)
                day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
                day_end = day_start + timedelta(days=1)
                
                tasks = self.db.query(Task).filter(
                    Task.created_at >= day_start,
                    Task.created_at < day_end
                ).all()
                
                daily_cost = sum(t.cost for t in tasks if t.cost)
                daily_costs[day.strftime('%Y-%m-%d')] = daily_cost
            
            costs = list(daily_costs.values())
            
            if len(costs) >= 3:
                # Linear regression trend
                x = np.arange(len(costs))
                z = np.polyfit(x, costs, 1)
                p = np.poly1d(z)
                
                # Predict next day
                next_day_cost = float(p(len(costs)))
                cost_prediction['predicted_daily_cost'] = max(0, next_day_cost)
                cost_prediction['cost_trend'] = 'increasing' if z[0] > 0 else 'decreasing'
                
                # Weekly and monthly extrapolation
                cost_prediction['predicted_weekly_cost'] = max(0, next_day_cost * 7)
                cost_prediction['predicted_monthly_cost'] = max(0, next_day_cost * 30)
                cost_prediction['historical_daily_costs'] = daily_costs
            
        except Exception as e:
            logger.error(f"Error in cost prediction: {e}")
        
        return cost_prediction

    async def detect_performance_degradation(self) -> List[Alert]:
        """
        Detect performance degradation patterns
        """
        alerts = []
        
        try:
            now = datetime.utcnow()
            window_size = 10  # Last 10 tasks
            
            agents = self.db.query(Agent).all()
            
            for agent in agents:
                recent_tasks = self.db.query(Task).filter(
                    Task.agent_id == agent.id
                ).order_by(Task.created_at.desc()).limit(window_size).all()
                
                if len(recent_tasks) < 3:
                    continue
                
                recent_tasks.reverse()  # Chronological order
                
                # Check execution time trend
                execution_times = [
                    t.execution_time for t in recent_tasks
                    if t.execution_time is not None
                ]
                
                if len(execution_times) >= 3:
                    # Check if execution time is consistently increasing
                    diffs = np.diff(execution_times)
                    if np.mean(diffs) > 0 and np.sum(diffs > 0) >= len(diffs) - 1:
                        alert = Alert(
                            id=f"perf_degrad_{agent.id}",
                            alert_type=AlertType.WARNING,
                            message=f"Performance degradation detected for agent '{agent.name}'",
                            timestamp=now,
                            severity="medium",
                            metadata={
                                "agent_id": agent.id,
                                "execution_times": [float(t) for t in execution_times],
                                "trend": "degrading"
                            }
                        )
                        alerts.append(alert)
                        logger.warning(f"Performance degradation: {alert.message}")
                
                # Check error rate spike
                errors = len([t for t in recent_tasks if t.status == "failed"])
                error_rate = (errors / len(recent_tasks)) * 100
                
                if error_rate > 20:
                    alert = Alert(
                        id=f"error_spike_{agent.id}",
                        alert_type=AlertType.ERROR,
                        message=f"High error rate detected for agent '{agent.name}': {error_rate:.1f}%",
                        timestamp=now,
                        severity="high",
                        metadata={
                            "agent_id": agent.id,
                            "error_rate": error_rate,
                            "errors": errors,
                            "total_tasks": len(recent_tasks)
                        }
                    )
                    alerts.append(alert)
                    logger.error(f"Error spike detected: {alert.message}")
        
        except Exception as e:
            logger.error(f"Error in performance degradation detection: {e}")
        
        return alerts

    async def get_active_alerts(self) -> List[Alert]:
        """
        Get all active alerts from multiple detection methods
        """
        all_alerts = []
        
        try:
            # Anomaly detection
            anomaly_alerts = await self.detect_anomalies()
            all_alerts.extend(anomaly_alerts)
            
            # Performance degradation
            perf_alerts = await self.detect_performance_degradation()
            all_alerts.extend(perf_alerts)
            
            # Remove duplicates
            seen_ids = set()
            unique_alerts = []
            for alert in all_alerts:
                if alert.id not in seen_ids:
                    seen_ids.add(alert.id)
                    unique_alerts.append(alert)
            
            return unique_alerts
        
        except Exception as e:
            logger.error(f"Error getting active alerts: {e}")
            return []

    async def get_metrics_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive ML metrics and predictions
        """
        try:
            performance = await self.predict_performance()
            cost = await self.predict_cost()
            alerts = await self.get_active_alerts()
            
            return {
                "performance_predictions": performance,
                "cost_predictions": cost,
                "active_alerts": [a.dict() for a in alerts],
                "alert_count": len(alerts),
                "timestamp": datetime.utcnow().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error getting ML metrics summary: {e}")
            return {}
