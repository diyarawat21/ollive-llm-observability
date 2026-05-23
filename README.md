# Ollive LLM Observability

A lightweight LLM observability and ingestion platform built using React, FastAPI, PostgreSQL, and OpenRouter.

## Features

- Multi-turn chatbot
- Conversation history
- Inference logging SDK
- Analytics endpoint
- PostgreSQL storage
- OpenRouter integration
- Modern UI

## Tech Stack

Frontend:
- React
- TailwindCSS

Backend:
- FastAPI
- SQLAlchemy
- PostgreSQL

LLM:
- OpenRouter

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Architecture

Frontend → FastAPI → OpenRouter  
                     ↓  
               Logging SDK  
                     ↓  
                Ingestion API  
                     ↓  
                PostgreSQL

## Future Improvements

- Streaming responses
- Docker deployment
- Dashboards
- Multi-provider support
