# 測試驗證計畫書 (Test Plan)：AI Chatbot 功能

本文件依據 AI Chatbot 的 PRD、系統架構與資料模型，針對本次繳交的 MVP 版本（FastAPI + 原生 JavaScript + SQLite）訂定具體的測試驗證藍圖。

## 1. 產品與需求基準 (Product & Requirements Baseline)
* **測試範圍**：以首頁右下角的 Chat Widget 互動體驗為主，涵蓋開啟關閉視窗、訊息收發、前端動畫渲染，以及後端 API (`/api/chat`) 處理與資料庫讀寫功能。
* **核心驗收標準 (AC)**：
  - 聊天圖示與視窗開關需具備平滑流暢的微動畫特效。
  - 使用者發出訊息後，前端能即時渲染氣泡，並在等候伺服器回應期間顯示「跳動的三個點」打字指示器。
  - 聊天室擁有自動捲動機制，新訊息出現時捲軸必須自動定位至最底部。
  - 輸入訊息不得破壞畫面排版。

## 2. 技術與系統架構資訊 (Technical & Architectural Info)
* **API 端點驗證**：請求 `POST /api/chat`。
  - **Request** 需能接受 JSON 包含 `session_id` (初次對話為空) 與 `message`。
  - **Response** 必定回傳 UUID 格式的 `session_id` 以及字串格式的 `reply`。
* **資料庫驗證 (Database Validation)**：
  - 對話完成後，檢視根目錄產生的 `chat.db` 檔案，確保 `ChatSession` 被建立。
  - 確保該對話階段新增了兩筆 `ChatMessage` (一筆 `sender_type = 'user'`、一筆 `sender_type = 'bot'`)，並且 `session_id` 與剛剛拿到的回傳值一致。

## 3. 測試環境與前置條件 (Test Environment & Prerequisites)
* **環境設定**：
  - 本地開發者環境 (Localhost)。
  - 依賴指令 `uvicorn backend.app.main:app` 啟動服務。測試瀏覽器推薦使用最新版本 Chrome。
* **測試資料與前置條件**：
  - 無需事先載入 Seed Data，若系統偵測不到表結構，後端的 `@app.on_event("startup")` 機制必須保證能從無到有動態建表。

## 4. 測試情境與邊界條件 (Test Scenarios & Edge Cases)
* **正常路徑 (Happy Path)**：
  1. 訪客開啟 `http://localhost:8000`，點擊漂浮按鈕展開對話框。
  2. 輸入「你好」，按下 Enter 或發送。
  3. 畫面顯示自己的對話氣泡與 AI 思考中的跳動動畫。
  4. 約 1.5 秒後，跳動動畫消失，顯示 AI 預設招呼語。
* **異常路徑 (Negative Path)**：
  - **前端空白防呆**：純粹輸入空白鍵或什麼都不打按下發送，JS 必須擋下請求，不觸發 `fetch` 也不顯示氣泡。
  - **後端斷線處理**：在畫面輸入完文字後，從背景強制關閉 Uvicorn 服務，接著按下發送。此時前端在 fetch 失敗時，應捕捉錯誤並顯示「系統錯誤，無法回覆。請稍後再試。」於畫面上。
* **邊界條件 (Edge Cases)**：
  - **排版破版測試**：輸入連續且「不包含任何空格的英文字母」(如：`aaaaabbbbb...` 超過 100 字) 以及長篇中文文章。測試 CSS 的 `word-wrap: break-word` 是否正常觸發，避免視窗出現異常水平捲動。
  - **高頻重壓測試 (Debounce)**：使用滑鼠快速狂點「發送」按鈕。測試這是否會導致同一個訊息被重複送出多次。

## 5. 非功能性需求指標 (Non-Functional Requirements)
* **效能 (Performance)**：目前為本地單純 Mock 驗證，重點在「前端 UI 回饋延遲」需趨近即時（0.1s內），而 AI 回覆為固定延遲展示（1.5s）。
* **安全性 (Security)**：此為作業與展示用的 MVP 版本，先以能接受標準 JSON 為主，尚未導入跨站請求防護 (CSRF) 嚴格檢查或個資遮蔽字典 (Data Masking)。未來升級真實 LLM 需列入稽核。
