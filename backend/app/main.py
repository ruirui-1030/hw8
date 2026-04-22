from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.app.api.chat_router import router as chat_router
from backend.app.models.database import init_db

app = FastAPI(title="AI Chatbot Assignment MVP")

# 允許跨域請求 (測試開發用)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    # 程式啟動時自動初始化 SQLite 資料表
    init_db()

# 掛載對話端點
app.include_router(chat_router, prefix="/api")

# 定義前端靜態檔路徑 (以 uvicorn 啟動目錄為基準)
frontend_path = os.path.join(os.getcwd(), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def serve_index():
    from fastapi.responses import FileResponse
    return FileResponse(os.path.join(frontend_path, "index.html"))
