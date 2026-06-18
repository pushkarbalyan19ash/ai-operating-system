from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.ml_alerts_service import MLAlertsService

router = APIRouter(
    prefix="/api/ml-alerts",
    tags=["ml-alerts"]
)


@router.get("/anomalies")
async def detect_anomalies(db: Session = Depends(get_db)):
    """
    Detect anomalies in agent performance using ML
    """
    service = MLAlertsService(db)
    return await service.detect_anomalies()


@router.get("/predictions/performance")
async def predict_performance(db: Session = Depends(get_db)):
    """
    Get performance predictions using time series analysis
    """
    service = MLAlertsService(db)
    return await service.predict_performance()


@router.get("/predictions/cost")
async def predict_cost(db: Session = Depends(get_db)):
    """
    Get cost predictions for upcoming days/weeks/months
    """
    service = MLAlertsService(db)
    return await service.predict_cost()


@router.get("/degradation")
async def detect_degradation(db: Session = Depends(get_db)):
    """
    Detect performance degradation patterns
    """
    service = MLAlertsService(db)
    return await service.detect_performance_degradation()


@router.get("/active")
async def get_active_alerts(db: Session = Depends(get_db)):
    """
    Get all active ML-detected alerts
    """
    service = MLAlertsService(db)
    return await service.get_active_alerts()


@router.get("/summary")
async def get_ml_summary(db: Session = Depends(get_db)):
    """
    Get comprehensive ML metrics and predictions
    """
    service = MLAlertsService(db)
    return await service.get_metrics_summary()
