# Ollive LLM Observability - Architecture Notes

## Project Overview

This project is a lightweight LLM observability system built using:

- FastAPI (Backend)
- React + TailwindCSS (Frontend)
- SQLite Database
- OpenRouter API for LLM responses

The application allows users to:
- Create conversations
- Chat with an AI assistant
- Store chat history
- Log LLM inference metadata
- View analytics summary

---

# How The System Works

## Step 1: User sends a message

The user types a message in the React frontend UI.

Example:
"Tell me about Python"

---

## Step 2: Backend receives the request

Frontend sends the message to FastAPI `/chat` endpoint.

The backend:
- stores the user message
- sends request to OpenRouter model
- gets AI response

---

## Step 3: SDK captures metadata

A lightweight logging wrapper (`llm_logger.py`) automatically captures:

- model name
- provider
- latency
- token usage
- request status
- conversation ID
- input/output preview

---

## Step 4: Logs sent to ingestion API

The SDK sends logs to:

`/ingest/logs`

The ingestion API:
- validates payload
- processes metadata
- stores logs in database

---

## Step 5: Data stored in database

The system stores:

### Conversations
Stores chat sessions

### Messages
Stores user + AI messages

### Inference Logs
Stores observability data like:
- latency
- tokens
- model
- status
- timestamps

---

# Database Design

## conversations table

Stores:
- conversation id
- title
- created time

---

## messages table

Stores:
- message content
- role (user/assistant)
- conversation id

---

## inference_logs table

Stores:
- model
- provider
- latency
- token usage
- status
- previews
- timestamps

---

# Logging Strategy

Every LLM request passes through a custom logging wrapper.

This helps track:
- performance
- failures
- token usage
- response timings

Logs are sent in near real-time.

---

# Analytics Endpoint

`/analytics/summary`

This endpoint provides:
- total requests
- average latency
- total tokens
- success/failure counts

---

# Tradeoffs Made

- SQLite used for simplicity
- Simple UI used for faster implementation
- Synchronous logging used instead of queues

---

# Future Improvements

If given more time, I would add:

- Streaming responses
- Multi-provider support
- Real-time dashboards
- Authentication
- Kafka/RabbitMQ event pipeline
- Kubernetes deployment
- Better analytics charts
- Retry handling for failed ingestion
