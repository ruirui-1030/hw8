---
name: test
description: Guidelines on what information to gather and prepare before performing test verification and Q/A.
---

# Test Verification Required Information

在進行系統、功能的測試驗證（Test & Verification）之前，請確保收集並釐清以下資訊，這將幫助確保測試涵蓋了所有的業務邏輯、技術限制以及潛在的極端情況。

## 1. 產品與需求基準 (Product & Requirements Baseline)
此部分確認「系統是不是做對了事情」。
- **產品需求文件 (PRD)**：功能的具體描述、使用者流程（User Flow）及商業羅輯。
- **驗收標準 (Acceptance Criteria, AC)**：針對每個功能或 User Story 具體定義「怎樣才算完成」的條件。
- **UI/UX 資源**：設計圖、多媒體資源，供畫面檢視、響應式（RWD）測試及互動行為驗證對照。

## 2. 技術與系統架構資訊 (Technical & Architectural Info)
了解系統是如何實作的，有助於規劃整合測試及效能測試。
- **系統架構圖與 API 文件**：API 的 Request/Response 規格、使用的通訊協定（如 HTTP/WebSocket）。
- **資料模型 (Data Models / Schema)**：資料儲存的結構，用以驗證資料庫行為。
- **外部依賴與第三方服務**：系統是否介接外部 API（如金流、簡訊服務），以及這些服務是否提供沙盒（Sandbox）測試環境。

## 3. 測試環境與前置條件 (Test Environment & Prerequisites)
確保測試順利執行的先決條件。
- **環境設定**：測試執行的目標環境（如 Local、Staging、UAT）以及軟硬體限制（支援的 OS、瀏覽器版本、螢幕解析度等）。
- **測試權限**：不同角色的測試帳號資料與權限配置（如 Admin、一般使用者、訪客等）。
- **測試資料 (Test Data)**：必需準備的假資料（Mock Data）、資料庫初始狀態（Seed Data）。

## 4. 測試情境與邊界條件 (Test Scenarios & Edge Cases)
給予測試腳本具體的執行藍圖。
- **正常路徑 (Happy Path)**：使用者最常走的正確操作流程。
- **異常路徑 (Negative Path)**：輸入錯誤資料、格式不符或必填欄位為空時，系統應有的報錯或防呆機制。
- **邊界條件 (Edge Cases)**：極端情況，如數值的最大/最小值測試、斷線處理、高併發操作。

## 5. 非功能性需求指標 (Non-Functional Requirements)
針對效能與安全性的最低要求標準（視專案情況選填）。
- **效能壓力標準 (Performance)**：如「頁面加載必須在 2 秒內完成」、「API 需能承受 1000 QPS」。
- **安全性要求 (Security)**：如密碼加密傳輸、敏感資料脫敏檢查、防止 XSS / SQL Injection 等。
