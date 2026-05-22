from app.db.database import engine, Base

from app.models.conversation import Conversation
from app.models.message import Message
from app.models.inference_log import InferenceLog
Base.metadata.create_all(bind=engine)

print("Database tables created successfully")