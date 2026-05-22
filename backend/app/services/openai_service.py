import os
import time
from pathlib import Path

from dotenv import load_dotenv
from fastapi import HTTPException
from openai import OpenAI

from app.sdk.llm_logger import log_inference

load_dotenv(Path(__file__).resolve().parents[2] / ".env", override=True)

_api_key = os.getenv("OPENROUTER_API_KEY")

if not _api_key:
    raise RuntimeError(
        "OPENROUTER_API_KEY is not set. Check backend/.env"
    )

MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openrouter/free"
)

client = OpenAI(
    api_key=_api_key,
    base_url="https://openrouter.ai/api/v1",
)


def generate_response(
    messages: list[dict],
    conversation_id: int,
) -> str:

    start_time = time.time()

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful AI assistant. "
                        "Always reply only in English."
                    ),
                },
                *messages,
            ],
        )

        latency_ms = int(
            (time.time() - start_time) * 1000
        )

        ai_text = (
            response.choices[0].message.content or ""
        )

        usage = response.usage

        prompt_tokens = (
            usage.prompt_tokens
            if usage and usage.prompt_tokens
            else 0
        )

        completion_tokens = (
            usage.completion_tokens
            if usage and usage.completion_tokens
            else 0
        )

        total_tokens = (
            usage.total_tokens
            if usage and usage.total_tokens
            else 0
        )

        # SEND LOG TO INGEST API
        log_inference(
            conversation_id=conversation_id,
            provider="OpenRouter",
            model=MODEL,

            latency_ms=latency_ms,

            prompt_tokens=prompt_tokens,

            completion_tokens=completion_tokens,

            total_tokens=total_tokens,

            status="success",

            input_preview=str(messages)[:200],

            output_preview=ai_text[:200],
        )

        return ai_text

    except Exception as exc:

        latency_ms = int(
            (time.time() - start_time) * 1000
        )

        error_message = str(exc)

        # LOG FAILED REQUEST
        log_inference(
            conversation_id=conversation_id,
            provider="OpenRouter",
            model=MODEL,

            latency_ms=latency_ms,

            prompt_tokens=0,

            completion_tokens=0,

            total_tokens=0,

            status="failed",

            input_preview=str(messages)[:200],

            output_preview=error_message[:200],
        )

        raise HTTPException(
            status_code=502,
            detail=(
                "LLM request failed. "
                "Try another OPENROUTER_MODEL in .env. "
                f"Error: {error_message}"
            ),
        ) from exc