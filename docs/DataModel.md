# 資料模型設計文件：AI Chatbot 功能

本文件基於 AI Chatbot 的系統架構與產品需求文件 (PRD)，詳細規劃後端關聯式資料庫及向量資料庫的資料模型 (Data Model) 與結構設計準則，以作為後續資料庫 Schema 開發的依據。

## 1. 業務與需求面 (Business & Requirement Context)
首先定義資料庫中用於支撐 Chatbot 運作的核心實體與關係。
* **核心實體 (Data Entities)**：
  1. `User` (使用者)：發起對話的人，可能為匿名訪客或已登入會員。
  2. `ChatSession` (對話工作階段)：一次具連貫性的對話視窗週期。
  3. `ChatMessage` (對話訊息)：在工作階段中產生的單筆對話內容。
  4. `KnowledgeChunk` (知識庫切片)：存放於 Vector DB 內，作為 RAG 檢索用的文檔片段。
* **實體關聯性 (Entity Relationships)**：
  * `User` (1) 對多 (N) `ChatSession`：一個使用者可在不同時間發起多次對話。
  * `ChatSession` (1) 對多 (N) `ChatMessage`：一次對話內包含多筆雙方的訊息來回。
* **資料生命週期與狀態 (Data Lifecycle)**：
  * `ChatSession` 的狀態機演講：
    * `active` (進行中)
    * `idle` (閒置，超過 N 分鐘未回應)
    * `handed_over` (已成功轉接人工客服)
    * `closed` (已結束，使用者主動關閉或系統強制超時關機)
* **名詞定義 (Glossary)**：
  * `User/Visitor`：系統中的提問端。
  * `Bot`：AI 模型生成的回覆端。
  * `Agent`：接手的真人客服端。

## 2. 屬性與規格面 (Attributes & Specifications)
針對核心實體拆解出具體的資料庫欄位設計，考慮通用關聯式資料庫 (如 PostgreSQL/MySQL) 的語法。

### 2.1 User
*(註：若現有系統已有 User 表，此處僅作為關聯參考)*
* `id` (UUID, PK): 用戶唯一識別碼。
* `is_guest` (BOOLEAN, Default: TRUE): 是否為未登入訪客。
* `created_at` (TIMESTAMP, NOT NULL): 建立時間。

### 2.2 ChatSession
* `id` (UUID, PK): 工作階段唯一碼。
* `user_id` (UUID, FK -> User.id): 關聯發起的用戶。
* `status` (VARCHAR(30), NOT NULL, Default: 'active'): 當前狀態。
* `csat_score` (TINYINT, NULL): 滿意度評分 (例如 1-5 顆星，預設為 NULL 代表未評)。
* `metadata` (JSON, NULL): 存放前端傳入的擴充變數，如瀏覽器資訊、來源頁面。
* `created_at` (TIMESTAMP, NOT NULL): 開始時間。
* `closed_at` (TIMESTAMP, NULL): 結束時間。

### 2.3 ChatMessage
* `id` (UUID, PK): 訊息唯一識別碼。
* `session_id` (UUID, FK -> ChatSession.id): 所屬的會話 ID。
* `sender_type` (VARCHAR(10), NOT NULL): 發送方 (`user`, `bot`, `agent`)。
* `content` (TEXT, NOT NULL): 訊息本身 (支援長文字)。
* `prompt_tokens` (INT, Default: 0): LLM 消耗輸入的 Token 數 (由 Bot 發出時有值)。
* `completion_tokens` (INT, Default: 0): LLM 消耗輸出的 Token 數 (由 Bot 發出時有值)。
* `created_at` (TIMESTAMP, NOT NULL): 訊息建立時間。

### 2.4 KnowledgeChunk (Vector DB 表 - 如 Pinecone/Qdrant)
* `id` (String, PK): 特徵片段 ID。
* `doc_title` (String): 文件或 FAQ 的標題。
* `content` (TEXT): 文檔內容片段。
* `embedding` (VECTOR/Array[Float]): 用於相似度對比的浮點數陣列。

## 3. 效能與架構面 (Performance & Architecture Context)
資料庫的存取策略及效能優化方向。
* **資料讀寫特性 (Read/Write Patterns)**：
  * `ChatMessage` 為高度 **寫多讀少 (Write-heavy)**，使用者與機器人的每一次互動都需要即時 Insert 紀錄。
  * 但在串接 LLM 時，需要撈出 `Session` 中最新的 5~10 筆歷史作為上下文 (Read)。
  * `KnowledgeChunk` 為極端 **讀多寫少 (Read-heavy)**，僅在由後台匯入 FAQ 或手冊變更時寫入。
* **查詢需求與索引 (Query Patterns & Indexes)**：
  * 頻繁查詢：「取得某個 Session 中由新到舊排序的 Message」。
  * **建議索引**： `ChatMessage` 必須在 `session_id` + `created_at` 建立複合索引 (Composite Index)。
  * 若要能從後台查詢特定使用者的聊天紀錄，`ChatSession` 的 `user_id` 需建立索引。
* **資料量分析與預估 (Data Volume Estimation)**：
  * 假設每日有 2,000 個 Session，平均每個 Session 包含 12 條對話（6次來回），每日將新增 2.4 萬筆 Message 紀錄。
  * 一年期預估量達約 870 萬筆。未來針對 `ChatMessage` 資料表，可能需引入以月或季為單位的分表 (Partitioning) 機制。

## 4. 安全與合規面 (Security & Compliance)
確保資料儲存不會踩到資安與法規紅線。
* **機敏資料處理 (Sensitive Data / PII)**：
  * `ChatMessage.content` 是使用者自由輸入的純文字，極有可能包含敏感個資（帳號密碼、信用卡號）。
  * 儲存時建議對文字進行去識別化 (Data Masking) 處理，如過濾並取代為 `[ID_MASKED]`。
  * 整個資料庫實體需開啟 TDE (Transparent Data Encryption) 靜態資料加密。
* **審計與刪除機制 (Audit & Deletion)**：
  * **禁止硬刪除 (No Hard Delete)**：對話紀錄牽涉到客訴追溯與日後的模型微調訓練 (Fine-Tuning)，應禁止直接從 DB 中 `DELETE`。
  * 若因隱私權要求需清除關聯，考量使用「軟刪除」或「匿名化」，即把 `ChatSession.user_id` 清空或洗掉，但保留無識別對象的單純對話字串。
