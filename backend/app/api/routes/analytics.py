from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.models.inference_log import InferenceLog

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):

    total_requests = db.query(InferenceLog).count()

    success_requests = (
        db.query(InferenceLog)
        .filter(InferenceLog.status == "success")
        .count()
    )

    failed_requests = (
        db.query(InferenceLog)
        .filter(InferenceLog.status == "failed")
        .count()
    )

    avg_latency_ms = (
        db.query(func.avg(InferenceLog.latency_ms))
        .scalar()
    )

    total_tokens = (
        db.query(func.sum(InferenceLog.total_tokens))
        .scalar()
    )

    recent_logs = (
        db.query(InferenceLog)
        .order_by(InferenceLog.created_at.desc())
        .limit(10)
        .all()
    )

    return {
        "total_requests": total_requests,
        "success_requests": success_requests,
        "failed_requests": failed_requests,
        "avg_latency": avg_latency_ms or 0,
        "total_tokens": total_tokens or 0,
        "recent_logs": [
            {
                "id": log.id,
                "model": log.model,
                "provider": log.provider,
                "latency_": log.latency_ms,
                "status": log.status,
                "tokens": log.total_tokens,
                "created_at": log.created_at,
            }
            for log in recent_logs
        ]
    }