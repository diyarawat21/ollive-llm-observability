from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.db.database import Base


class InferenceLog(Base):

    __tablename__ = "inference_logs"

    id = Column(Integer, primary_key=True, index=True)

    conversation_id = Column(Integer)

    provider = Column(String)

    model = Column(String)

    latency_ms = Column(Float)

    prompt_tokens = Column(Integer)

    completion_tokens = Column(Integer)

    total_tokens = Column(Integer)

    status = Column(String)

    input_preview = Column(String)

    output_preview = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
        
    )