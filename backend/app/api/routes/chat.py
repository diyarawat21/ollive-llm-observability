from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.message import Message
from app.services.openai_service import generate_response

router = APIRouter()


@router.post("/chat")
def chat(data: dict):
    db: Session = SessionLocal()

    try:
        conversation_id = data["conversation_id"]
        user_message = data["message"]

        user_db_message = Message(
            conversation_id=conversation_id,
            role="user",
            content=user_message,
        )

        db.add(user_db_message)
        db.commit()

        previous_messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).all()

        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in previous_messages
        ]

        ai_response = generate_response(
            formatted_messages,
            conversation_id=conversation_id,
        )

        assistant_message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=ai_response,
        )

        db.add(assistant_message)
        db.commit()

        return {"response": ai_response}
    finally:
        db.close()
