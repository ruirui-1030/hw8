---
name: implement
description: Guidelines on what information to gather and prepare before performing code generation or implementation.
---

# 程式碼生成（實作）必備資料清單

在進行**程式碼生成 (Code Generation)** 或開始**實作開發 (Implementation)** 之前，為了確保生成的程式碼符合預期功能、架構且能無縫整合至既有專案中，通常需要準備以下幾大類的資料：

### 1. 產品需求與驗收標準 (Product Requirements & Acceptance Criteria)
這是決定「要寫出什麼功能」的基準。
* **產品需求文件 (PRD)**：清楚描述該功能要解決什麼問題、主要流程為何。
* **使用者故事 (User Stories)**：從使用者的角度定義操作的情境。
* **驗收標準 (Acceptance Criteria, AC)**：需要滿足哪些條件才算開發完成？這也是後續撰寫自動化測試或單元測試的基礎。

### 2. 架構與系統設計文件 (Architecture & System Design)
決定程式碼要「怎麼寫」才不會破壞現有系統。
* **系統架構圖 (System Architecture)**：了解該模組在整個系統切分上的定位與交互關係。
* **API 規格書 (API Specifications)**：包含 Request / Response 的格式、狀態碼 (Status Codes)，通常以 Swagger 或 OpenAPI 格式呈現。如果前後端分離，這是雙方溝通的橋樑。
* **既有程式碼與專案結構 (Project Structure / Legacy Code)**：目前專案的目錄劃分原則（例如 MVC 還是 Clean Architecture 等）。

### 3. UI/UX 設計與前端規範 (UI/UX Design & Frontend Specs)
若涉及前端頁面實作，需要明確的視覺參考。
* **設計稿 (Wireframes / Mockups)**：如 Figma 等工具上的設計圖，包含尺寸、排版與狀態（如 Hover、Disabled 等）。
* **UI 元件與設計系統 (Design Systems / Tokens)**：是否已有現成的按鈕 (Buttons)、顏色變數 (CSS variables)、字體等規範要遵循。

### 4. 資料模型與狀態管理 (Data Model & State Management)
影響後端與前端如何儲存與傳遞資料。
* **資料庫綱要 (Database Schema / ER Diagram)**：定義了哪些資料表、欄位名稱與資料型別。
* **前端狀態管理 (State Management)**：如 Redux、Vuex 或 React Context，釐清哪些是全域狀態、哪些是局部狀態。

### 5. 開發環境、技術棧與規範 (Tech Stack, Environment & Standards)
規範具體實作細節，避免各自為政。
* **使用的技術棧 (Tech Stack)**：程式語言與其版本 (如 Python 3.10、Node 18)、前端框架 (如 React, Vue)。
  > [!IMPORTANT]
  > **⭐ 本專案指定技術棧 (Project Required Stack)**
  > - **前端 (Frontend)**：原生 HTML / CSS / JavaScript (Vanilla)
  > - **後端 (Backend)**：Python + FastAPI
  > - **資料庫 (Database)**：SQLite
* **第三方相依套件 (Dependencies)**：需要安裝哪些現有套件來輔助開發。
* **程式碼規範 (Coding Standards / Linters)**：例如 ESLint 配置、Prettier、或者團隊定義的變數命名風格 (CamelCase / snake_case)。
* **環境變數 (Environment Variables)**：需不需要特別配置的 `.env` 變數來存取測試機器的第三方金鑰。

---

**💡 總結與關聯：**
要讓 AI 或是工程師寫出高品質的程式碼，**「上下文（Context）的完整度」**是最關鍵的。
將 `PRD`、`Architecture` 及 `Data Model` 等前面的產出提供給程式碼生成階段，能最大幅度減少因「未定義的邊界條件」所產生的 Bug 與重構成本。
