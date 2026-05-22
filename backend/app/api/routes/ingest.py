from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.inference_log import InferenceLog
from app.schemas.inference_log import InferenceLogCreate

router = APIRouter(tags=["Ingestion"])


@router.post("/ingest/logs")
def ingest_logs(
    payload: InferenceLogCreate,
    db: Session = Depends(get_db)
):
    log = InferenceLog(
        model=payload.model,
        provider=payload.provider,
        latency_ms=payload.latency_ms,
        prompt_tokens=payload.prompt_tokens,
        completion_tokens=payload.completion_tokens,
        status=payload.status,
        conversation_id=payload.conversation_id,
        input_preview=payload.input_preview,
        output_preview=payload.output_preview,
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return {
        "message": "Log ingested successfully",
        "id": log.id,
    }