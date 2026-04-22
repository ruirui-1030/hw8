from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api.chat_router import router as chat_router
from app.models.database import init_db

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

# 定義前端靜態檔路徑，這裡抓取專案目錄中的 frontend 資料夾
frontend_path = os.path.join(os.path.dirname(__file__), "../../../frontend")
if os.path.exists(frontend_path):
    # 掛載靜態檔案目錄 (這樣 FastAPI 就可以 serve js/css)
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def serve_index():
    # 直接轉向掛載的靜態首頁
    return RedirectResponse("/static/index.html")
