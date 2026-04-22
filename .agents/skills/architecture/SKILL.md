---
name: architecture
description: Guidelines on what information to gather and prepare before performing a product and technical architecture design.
---

# 產品架構設計必備資料清單

進行一項完整的**產品架構設計 (Product Architecture Design)** 之前，架構師或技術主管通常需要先蒐集並釐清一系列的輸入資料。

產品架構通常可以分為「**資訊架構** (Information Architecture, 偏產品與 UX 體驗)」與「**系統/技術架構** (System/Technical Architecture, 偏後端與工程)」，為了能畫出合理且可擴充的架構，您會需要準備以下幾大類的資料：

### 1. 商業與產品需求面 (Business & Product Needs)
這是決定架構方向的最核心基礎。
* **產品需求文件 (PRD)**：包含產品目標、核心功能清單、使用者故事 (User Stories) 以及驗收標準等。
* **非功能性需求 (Non-functional Requirements, NFR)**：
    * **效能與規模**：預估的每日活躍用戶數 (DAU)、最高同時上線人數 (Concurrency)、系統回應時間的要求。
    * **可用性**：系統允許的停機時間 (Uptime 要求，如 99.9%)。
* **流程與介面規劃**：
    * **使用者流程圖 (User Flow)**：釐清網頁或 App 中的頁面跳轉邏輯與操作動線。
    * **狀態機 (State Machine)**：例如訂單的狀態變化（待付款 -> 處理中 -> 已出貨 -> 已完成），這對後端架構非常重要。

### 2. 系統環境與邊界 (System Context & Boundaries)
釐清您的產品在真實世界中需要跟誰溝通。
* **現有系統架構與限制**：如果這不是一個全新的專案，必須了解目前的「技術棧 (Tech Stack)」、伺服器配置與既有的歷史包袱 (Legacy Code)。
* **第三方服務與 API 依賴**：產品是否需要串接外部金流、簡訊發送系統 (SMS)、社群登入 (如 Google/Apple Login)、地圖服務、或 ERP 系統？
* **資源限制**：包含開發團隊的技術能力（會什麼語言、框架）、開發上線的「時程」與「專案預算」（決定要自己花時間開發，還是花錢買現成的雲端服務 (SaaS)）。

### 3. 資料與合規性 (Data & Compliance)
這決定了資料庫與儲存架構的選型。
* **資料模型初步規劃 (Data Model / ER Diagram)**：系統中會擁有那些核心資料實體（如：用戶、商品、訂單、文章）以及它們的關聯性。
* **安全性與隱私規範**：處理的資料是否包含敏感個資、信用卡號等？有沒有符合特定法規的需求（如歐盟的 GDPR、資安標準 ISO 27001 等）。
* **資料增長速度**：資料量是大還是小？是讀取比較多 (Read-heavy) 還是寫入比較多 (Write-heavy)？這會影響要用關聯式資料庫 (如 MySQL) 還是非關聯式 (如 MongoDB)，甚至是加入快取層 (如 Redis)。

### 4. 營運與未來規劃 (Operations & Roadmap)
* **產品發展藍圖 (Roadmap)**：未來半年到一年，預計會長出什麼新功能？好的架構要能「預留彈性」，避免未來加功能時需要整個打掉重練。
* **部署與維運需求**：資料要放在 AWS、GCP 還是地端機房？團隊是否需要自動化部署 (CI/CD) 、日誌分析 (Logging) 與系統監控 (Monitoring) 機制？

---

**💡 總結與關聯：**
就如同 `PRD Writing Guide` 所述，**PRD 其實就是架構設計最重要的「前置輸入」**。
在標準的工作流程中，**PM (產品經理)** 產出 PRD 以及 Wireframe 之後，**Tech Lead 或架構師**就會拿著這份 PRD，再去盤點上述的「技術限制、預估流量、API 串接需求」，最終才能產出具體可行的**產品架構圖**交給工程團隊進行開發。
