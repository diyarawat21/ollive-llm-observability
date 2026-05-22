from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.conversation import (
    ConversationCreate,
    ConversationResponse
)

router = APIRouter()

@router.post("/conversations", response_model=ConversationResponse)
def create_conversation(data: ConversationCreate):
    db: Session = SessionLocal()

    try:
        conversation = Conversation(title=data.title)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation
    finally:
        db.close()


@router.get("/conversations")
def get_conversations():
    db: Session = SessionLocal()

    try:
        return db.query(Conversation).all()
    finally:
        db.close()

@router.get("/conversations/{conversation_id}/messages")
def get_messages(conversation_id: int):
    db: Session = SessionLocal()

    try:
        return (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .all()
        )
    finally:
        db.close()