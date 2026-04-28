import os
import google.generativeai as genai
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 設定 Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # 選擇使用的模型，這裡使用最新的 gemini-1.5-flash
    model = genai.GenerativeModel('gemini-1.5-flash') 
else:
    model = None

async def generate_response(prompt: str) -> str:
    """
    呼叫真實的 Gemini API 取得回覆。
    """
    if not model:
        return "系統錯誤：找不到 GEMINI_API_KEY。請確保已在 .env 檔案中設定您的 API Key。"
    
    try:
        # 使用 generate_content_async 進行非同步呼叫
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API 錯誤: {e}")
        return f"抱歉，連線到 Gemini API 時發生錯誤：{str(e)}"
