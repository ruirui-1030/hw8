import asyncio

async def generate_response(prompt: str) -> str:
    """
    此為模擬回覆 (Mock) 功能。
    為了作業實作用，暫不串接真實 OpenAI。
    """
    # 模擬 1.5 秒的思考延遲
    await asyncio.sleep(1.5)
    
    prompt_lower = prompt.lower()
    
    if "你好" in prompt_lower or "hi" in prompt_lower or "hello" in prompt_lower:
        return "你好！我是你的專屬 AI 助理。很高興為你服務！請問今天有什麼我可以幫忙的？"
    
    if "功能" in prompt_lower or "能做什麼" in prompt_lower:
        return "我目前是一個初階演練模型，我示範了如何透過 FastAPI 與原生前端建立順暢的 Chat Widget，包含對話紀錄與模擬思考效果！"
    
    return f"收到您的訊息了！您剛剛提到：「{prompt}」。\n(*這是一則由系統產生的預設測試回覆*)"
