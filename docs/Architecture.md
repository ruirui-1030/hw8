# 產品架構設計文件：AI Chatbot 功能

本文件基於 AI Chatbot 的產品需求文件 (PRD) ，盤點與規劃系統前期的技術架構重點與評估面向，作為技術團隊實作前的設計依據。

## 1. 商業與產品需求面 (Business & Product Needs)
這部分承接 `docs/PRD.md` 中定義的商業目標與預期功能。
* **核心依賴**：請對齊 AI Chatbot 功能 PRD 的第一至三章節。
* **非功能性需求 (NFR) 的架構轉換**：
  * **效能與延遲**：PRD 要求 3 秒內反應。這表示除了 LLM 本身的推理時間 (Inference latency) 之外，RAG (檢索增強生成) 去抓取 Vector DB 資料的速度必須控制在數百毫秒以內。
  * **併發能力 (Concurrency)**：支援 1,000 人同時在線，意味著後端需要考量使用非同步架構 (如 Node.js, Python FastAPI/Asyncio) 或是 Serverless 架構以利彈性橫向擴展 (Auto-scaling)。
  * **高可用性 (High Availability)**：AI API 可能遭遇不穩定或 Rate Limits，必須具備 Fallback 機制 (例如：切換到備用 LLM 模型，或平滑轉換為「系統忙碌中，幫您轉接人工客服」狀態)。
* **關鍵狀態機 (State Machine)**：
  * 對話階段 (Session) 的生命週期管理：`未啟動` -> `閒置 (等候輸入)` -> `處理中 (AI 思考/檢索)` -> `已回答 (等待回饋)` -> `已轉交真人 (Handover)` -> `對話結束`。

## 2. 系統環境與邊界 (System Context & Boundaries)
釐清 AI Chatbot 模組與內外部系統的依賴與邊界。
* **現有系統架構與限制**：
  * 前端整合：以 JavaScript Widget (如 Web Component 或 React) 形式嵌入現有前端網頁，需避免與現有 CSS 互相干擾。
  * 通訊協定：考慮即時性，建議前端與後端之間採用 WebSocket 建立持續連線 (Persistent Connection)，或者使用 Server-Sent Events (SSE) 實現打字機般的串流 (Streaming) 效果。
* **第三方服務與 API 依賴**：
  * **LLM 供應商**：如 OpenAI API, Anthropic API (需獨立 API Key 管理、並監控 Token 花費)。
  * **真人客服系統**：需串接內部現有客服系統 (如 Zendesk 或客製人工後台) 的即時訊息 API，進行上下文與連線移轉。
* **資源限制與技術選型**：
  * 開發初期可善用現成的開源框架 (如 LangChain, LlamaIndex)，加速 RAG 機制與對話流的開發，而無需從零打造底層輪子。

## 3. 資料與合規性 (Data & Compliance)
定義系統涉及之資料儲存機制與安全性。
* **資料模型初步規劃 (Data Model)**：
  1. `User`：匿名用戶 (使用 Browser Cookie/Local Storage ID) 或 登入會員 ID。
  2. `Session`：每一次對話的容器，記錄開始/結束時間、最終滿意度分數。
  3. `Message`：雙方對話紀錄，欄位應包含發送方 (User/Bot/Agent)、原文內容、時間戳記、關聯的 Session ID。
  4. `Knowledge_Chunk`：用於 FAQ 檢索的知識庫切片與其對應的 Embedding 向量。
* **儲存選型**：
  * **對話紀錄 (OLTP)**：採用關聯式資料庫 (如 PostgreSQL) 或文件資料庫 (如 MongoDB)，因 Write-heavy (每句對話皆需儲存)。
  * **上下文快取 (Cache)**：使用 Redis 儲存短期對話上文 (近期 N 句話)，以利快速塞入 LLM 的 prompt 中。
  * **向量資料庫 (Vector DB)**：採用 Pinecone, ChromaDB 或 Qdrant 用於儲存與比對 FAQ/文章的 embeddings。
* **安全性與隱私規範 (Data Processing / PII)**：
  * 傳輸全程 TLS / HTTPS 加密。
  * 必須實作「去識別化 (Data Masking) Middleware」，在將對話文檔發送至外部 LLM 之前，自動遮蔽信用卡號、身分證等敏感性個資，防止資料外洩風險。

## 4. 營運與未來規劃 (Operations & Roadmap)
為產品的持續發展與維護預留架構彈性。
* **擴充彈性 (Scalability for Roadmap)**：
  * Phase 3 會整合「內部訂單 API」。因此，架構需導入 Tool-Use (Function Calling) 的設計模式。系統路由需能辨識意圖並觸發特定 Tool API (如 `check_order_status`)，而非只是單純的一問一答。
* **部署與維運監控需求**：
  * 應採用 Docker 進行映像檔打包，並佈署於 Kubernetes (K8s) 或受管服務 (如 AWS ECS / GCP Cloud Run)。
  * 建立全面的監測儀表板 (Dashboard)：
    * **系統面**：監看 API Latency、HTTP 5xx 錯誤率、記憶體消耗。
    * **營運面**：監看 Token 使用花費 (Cost Tracking)、LLM 拒答率、轉接真人率。
  * 定期保留非敏感歷史對話作為後續微調 (Fine-tuning) 與測試集優化的語料庫。
