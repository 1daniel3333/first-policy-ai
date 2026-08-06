# Day 6 — 兵馬未動，糧草先行：OpenCode 與極簡開發環境設定

> **前情提要**：第一階段我們準備好了人生狀態機與 100 個隨機黑天鵝事件 JSON。
> **本日目標**：正式進入開發階段！我們將捨棄肥大的傳統 IDE 設定，改用極簡的 OpenCode 終端機流 (TUI) 作為我們未來 25 天的 AI 結對程式夥伴。

---

## 1. 為什麼選擇純終端機的 OpenCode？ (The Meat)

開發 AI Agent 或 Skill 時，我們往往需要在編輯器、終端機與瀏覽器之間來回切換，複製貼上報錯訊息。這不僅打斷心流，也浪費時間。

OpenCode 是一款專為 AI 輔助開發設計的工具。雖然它有 VSCode 外掛，但對於像我們這種常常需要直接跑 Python 腳本、看 Terminal 輸出的情境，**純終端機流 (Terminal UI)** 反而是最直覺、最沒有干擾的選擇。你可以左邊開著 Vim/Nano 寫邏輯，右邊開著 OpenCode 讓 AI 幫你寫單元測試。

### 終端機流四大必殺技：
1.  **`@ 檔案`**：直接在對話中打 `@events.json`，AI 瞬間讀完 100 個事件，不用手動複製貼上。
2.  **`Tab 鍵切換`**：一鍵切換 `Plan` (架構討論) 與 `Build` (實際改 Code) 模式。
3.  **`/run`**：直接輸入 `/run python engines.py`，遇到報錯 AI 會自動接手修 Bug。
4.  **`/undo`**：AI 寫壞了？一句 `/undo` 瞬間時光倒流，安全感爆棚。

---

## 2. 實作核心：一鍵安裝與啟動指令 (Code Snippet)

請打開你的 Terminal (Windows 建議使用 PowerShell 或 Windows Terminal)，跟著以下指令安裝並啟動我們的 AI 開發基地：

```bash
# 1. 安裝 OpenCode (擇一執行)
# macOS / Linux
brew install opencode

# Windows (如果你有裝 npm)
npm install -g opencode-ai

# 2. 進入我們 Day 1 建立的專案目錄
cd first-policy-ai

# 3. 召喚 AI 夥伴！
opencode
```

當你看到終端機畫面一閃，變成一個完整的聊天與開發介面時，恭喜你，你的專屬 AI 結對工程師已經正式上線了！

---

## 3. 今日總結與明日預告

今天我們搞定了神兵利器，建立了一個能與 AI 無縫溝通的開發環境。但現在的 AI 還是個「空殼」，它需要連接大腦才能運作。

**思考題**：你平常寫扣是用 VSCode、Cursor 還是純 Vim 派？你覺得 AI 工具最讓你崩潰的缺點是什麼？

**明日預告**：AI 的大腦要選誰？明天（Day 7），我們將上演「Ollama 地端 vs 雲端 API」的對決，教你如何打造不卡關的 2026 最強混合工作流！

---
* 🔗 專案 GitHub 倉庫：[first-policy-ai](https://github.com/1daniel3333/first-policy-ai)
