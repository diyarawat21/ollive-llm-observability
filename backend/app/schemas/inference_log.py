from pydantic import BaseModel
from typing import Optional


class InferenceLogCreate(BaseModel):
    model: str
    provider: str
    latency_ms: int

    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None

    status: str

    conversation_id: Optional[int] = None

    input_preview: Optional[str] = None
    output_preview: Optional[str] = None