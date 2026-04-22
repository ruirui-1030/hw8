from fastapi import APIRouter
from pydantic import BaseModel
import uuid

from backend.app.models.database import get_db
from backend.app.services.llm_service import generate_response

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str

class ChatResponse(BaseModel):
    session_id: str
    reply: str

@router.post("/chat", response_model=ChatResponse)
async def chat_handler(req: ChatRequest):
    conn = get_db()
    cursor = conn.cursor()
    
    # 決定 session_id
    session_id = req.session_id
    if not session_id:
        session_id = str(uuid.uuid4())
        # 新增一份暫時的 ChatSession
        cursor.execute(
            "INSERT INTO ChatSession (id, user_id, status) VALUES (?, ?, ?)",
            (session_id, "anonymous_student", "active")
        )
    
    # 紀錄 User 發送的訊息
    user_msg_id = str(uuid.uuid4())
    cursor.execute(
        "INSERT INTO ChatMessage (id, session_id, sender_type, content) VALUES (?, ?, ?, ?)",
        (user_msg_id, session_id, "user", req.message)
    )
    conn.commit()
    
    # 呼叫 LLM 服務取得回覆 (不限真假)
    reply_text = await generate_response(req.message)
    
    # 紀錄 AI 發送的訊息
    ai_msg_id = str(uuid.uuid4())
    cursor.execute(
        "INSERT INTO ChatMessage (id, session_id, sender_type, content) VALUES (?, ?, ?, ?)",
        (ai_msg_id, session_id, "bot", reply_text)
    )
    conn.commit()
    conn.close()
    
    return ChatResponse(session_id=session_id, reply=reply_text)
