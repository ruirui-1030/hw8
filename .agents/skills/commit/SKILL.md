---
name: Commit
description: Guidelines on what information to gather and prepare before performing a git commit and push.
---

# 提交與推送 (Commit & Push) 必備資料清單

在進行版本控制的 **提交 (Commit)** 及 **推送 (Push)** 之前，為了確保專案程式碼庫的整潔與歷史紀錄的易讀性，通常需要確認並準備以下幾項關鍵資訊：

### 1. 欲提交的檔案變更清單 (Staged Files / Changes)
明確知道這次提交包含了哪些檔案，以及排除了哪些不應提交的檔案目錄。
* **異動概覽**：哪些檔案被新增 (Added)、修改 (Modified) 或刪除 (Deleted)；僅暫存 (Stage) 相關的變更。
* **排除不必要檔案**：確保沒有將臨時檔案 (如日誌、作業系統預設隱藏檔或中介檔案) 誤加進去，應善用 `.gitignore` 控管。

### 2. 提交訊息規範 (Commit Message Format)
好的 Commit Message 能讓團隊快速了解此次變更目的，建議遵循「約定式提交」(Conventional Commits) 標籤：
* **變更類型 (Type)**：例如 `feat` (新功能), `fix` (修復 Bug), `docs` (文件維護), `style` (格式化), `refactor` (重構), `test` (測試), `chore` (日常建置或雜務) 等。
* **簡明描述 (Subject)**：簡短且清楚地說明做了什麼修改。
* **詳細描述 (Body)**：(選填) 若變更邏輯較大或有特殊原因，補充說明修改動機與具體細節。

### 3. 目標分支 (Target Branch)
確定程式碼的作用域，是否提交到了正確的地方：
* **目前分支確認**：確認是否處於預期的分支，例如：是正在開發的 `feature/xxx` 分支，還是 `main`/`develop` 分支。

### 4. 提交者資訊 (Author Information)
記錄這次 Commit 是由誰完成的，關係到歷史紀錄的作者標籤。

> [!IMPORTANT]
> **⭐ 本專案預設提交者資訊 (Default Git Author)**
> 若開發環境中尚未配置或需要動態指定 Git 提交的 使用者名稱 (user.name) 與 電子郵件 (user.email)，請一律使用以下預設資訊：
> - **使用者名稱 (User Name)**：`Antigravity`
> - **電子郵件 (User Email)**：`antigravity@local` (或專案預設信箱)

### 5. 推送目標與認證 (Push Target & Authentication)
在推送到遠端伺服器 (Remote) 時的必要確認。
* **遠端與分支名稱**：例如推送到 `origin` 的特定分支。
* **權限認證**：確保環境具備相應的推送權限 (Token, SSH Key 或帳密認證) 且可正確連線至遠端儲存庫。

---

**💡 總結與關聯：**
嚴謹的 Commit & Push 流程不僅是將程式碼備份，更是專案團隊用來追蹤、回溯與協作的重要資產。依照上述規範並統一使用 `Antigravity` 作為識別，可以幫助確保所有由自動化系統或 Agent 完成的任務在版控歷史裡留下清晰的查核點。
