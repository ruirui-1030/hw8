---
name: models
description: Guidelines on what information to gather and prepare when designing a data model or database schema.
---

# 資料模型 (Data Model) 設計必備資料清單

在進行**資料模型設計 (Data Modeling)** 或**資料庫綱要規劃 (Database Schema Design)** 之前，通常需要從產品需求與系統架構中梳理出以下幾大類的資料。這些資訊能夠幫助您設計出擴充性高、效能佳且符合業務邏輯的資料庫架構：

### 1. 業務與需求面 (Business & Requirement Context)
首先要釐清系統中「到底要存哪些東西」，以及這些東西在真實世界中的關係。
* **核心實體 (Data Entities)**：系統中需要記錄哪些主要物件？（例如：使用者 `User`、商品 `Product`、訂單 `Order`）。
* **實體關聯性 (Entity Relationships)**：這些實體之間的互動規則是什麼？
    * 一對一 (1:1)：例如「使用者」與「使用者基本資料」。
    * 一對多 (1:N)：例如「一個使用者」可以有「多筆訂單」。
    * 多對多 (M:N)：例如「一張訂單」可以有「多種商品」，且「一種商品」也可以出現在「多張訂單」中。
* **資料生命週期與狀態 (Data Lifecycle)**：這筆資料何時被建立、更新、歸檔或刪除？例如訂單狀態的變化（待付款 -> 處理中 -> 已出貨），這決定了需要哪些狀態欄位或歷史紀錄表。
* **名詞定義 (Glossary/Ubiquitous Language)**：統一團隊內的稱呼，避免開發與 PM 對「客戶」或「帳號」的定義有落差。

### 2. 屬性與規格面 (Attributes & Specifications)
針對每一個核心實體，需要往下深挖具體的欄位定義。
* **資料欄位 (Fields / Attributes)**：該實體需要儲存哪些具體資訊？（例如 User 需要 `id`, `name`, `email`, `created_at`）。
* **資料型別與限制 (Data Types & Constraints)**：
    * **型別**：文字 (`VARCHAR`, `TEXT`)、數字 (`INT`, `DECIMAL`)、時間 (`DATETIME`, `TIMESTAMP`) 或 JSON 等。
    * **長度與預設值**：字串的長度上限是多少？有沒有預設值 (`Default`)？
    * **是否可為空 (Nullability)**：這個欄位是必填 (`NOT NULL`) 還是選填 (`NULL`)？
* **鍵值 (Keys)**：
    * 什麼欄位是**主鍵 (Primary Key)** 用來唯一識別一筆記錄？
    * 哪裡需要**外鍵 (Foreign Key)** 來連結其他表？
    * 哪些欄位組合必須是唯一的 (**Unique Key**，例如 Email 不能重複)？

### 3. 效能與架構面 (Performance & Architecture Context)
資料庫的設計不僅要符合邏輯，還要考量未來的效能與乘載力。
* **資料讀寫特性 (Read/Write Patterns)**：系統是「讀多寫少」（如文章部落格）還是「寫多讀少」（如系統日誌）？這可能影響是否要為了讀取效能進行**反正規化 (De-normalization)**。
* **查詢需求 (Query Patterns)**：前端或後端通常會怎麼撈資料？（例如「常透過 Email 搜尋用戶」、「總是依建立時間排序」），這決定了要在哪些欄位建立**索引 (Indexes)**。
* **資料量分析與預估 (Data Volume Estimation)**：初期預計有多少資料？一年或三年後會長到多大？這將決定是否需要提早規劃冷熱資料分離、分表分庫 (Sharding / Partitioning)，或是選擇 NoSQL 資料庫。

### 4. 安全與合規面 (Security & Compliance)
確保資料儲存符合法規與資安標準。
* **機敏資料處理 (Sensitive Data)**：是否包含密碼、信用卡號、身分證字號等高度敏感資料？必須釐清這些欄位是否需要**加密儲存 (Encryption)** 或是實作**資料遮罩 (Data Masking)**。
* **審計與刪除機制 (Audit & Deletion)**：
    * **軟刪除 (Soft Delete)**：資料被刪除時，是真的從資料庫移除 (Hard Delete)，還是只標記為已刪除 `is_deleted = true`？
    * **歷史軌跡 (Audit Logs)**：是否需要記錄「誰在什麼時候修改了什麼資料」？若是，可能需要額外的日誌表 (Log Tables)。

---

**💡 總結與關聯：**
資料模型的設計通常銜接在 **架構設計 (Architecture Design)** 及 **PRD** 之後。
架構師或後端工程師會從 PRD 中的「使用者故事」及「功能需求」中提取出**資料實體**，再根據「非功能需求」中的效能及安全指標，定義出完整的資料表結構與索引策略。
