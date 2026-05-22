import requests

API_URL = "http://127.0.0.1:8001/ingest/logs"


def log_inference(
    conversation_id,
    provider,
    model,
    latency_ms,
    prompt_tokens,
    completion_tokens,
    total_tokens,
    status,
    input_preview,
    output_preview,
):
    payload = {
        "conversation_id": conversation_id,
        "provider": provider,
        "model": model,
        "latency_ms": latency_ms,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "status": status,
        "input_preview": input_preview,
        "output_preview": output_preview,
    }

    try:
        response = requests.post(API_URL, json=payload)
        print("Log sent:", response.status_code)

    except Exception as e:
        print("Logging failed:", str(e))