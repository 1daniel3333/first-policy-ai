# Day 7 — Ollama 地端 vs 雲端 API：打造不卡關的 2026 最強混合工作流

> **前情提要**：昨天我們搞定了開發介面與開放工具選型（OpenCode / Claude Code / Cursor 等）。
> **本日目標**：為我們的 AI 顧問挑選「大腦」。我們將優先教你如何架設免費、絕對保護隱私的**地端 Ollama 引擎**；如果你電腦配備不夠也別擔心，我們同時提供**零成本的免費雲端 API 降級方案**！

---

## 1. 隱私優先：為什麼我們首選地端 Ollama？

在開發像 `first-policy` 這種會處理使用者「真實財務金額與保單數據」的工具時，最核心的考量就是**資料隱私（Privacy First）**。

透過地端模型（如 Ollama）：

* 🔒 **資料 100% 不離機**：你的薪水、存款、保單 PDF 等敏感資訊全在個人電腦運算，絕不上傳第三方伺服器。
* 💰 **完全免費且無 Token 限制**：想怎麼測試就怎麼測試，不用看 API 帳單心驚膽跳。

**解答是：用雲端的智慧做設計，用地端的隱私做落地。**

在專案剛起步、架構尚未定型（例如現在）時，我們切換到雲端 API 來幫我們寫 Prompt 與規劃架構；等到專案寫好，進入頻繁測試與真實資料投入的階段時，我們一鍵切換回地端的 **Ollama + Qwen 2.5 Coder**，享受無成本且絕對隱私的推論環境。

---

## 2. 實作一：主線方案 — 建立地端 Ollama 引擎

如果你有一台具備獨立顯卡，或是 Apple Silicon (M1/M2/M3/M4, 16GB RAM 以上) 的電腦，請直接跟著以下步驟安裝：

```bash
# Windows (PowerShell) 一鍵安裝
winget install Ollama.Ollama

# macOS (Terminal) 一鍵安裝
brew install ollama

# 啟動專為程式碼優化的輕量模型 (Qwen 2.5 Coder 7B 僅需約 8GB 記憶體)
ollama run qwen2.5-coder:7b

```

> 💡 **小撇步**：若顯存較小，可以改載入 `ollama run qwen2.5-coder:3b` 或 `ollama run qwen2.5-coder:1.5b`，反應會更輕量流暢！

---

## 3. 實作二：降級備案 — 電腦跑不動？免費雲端 API 來救場！

如果你的電腦是舊型筆電或記憶體較小（8GB 以下），執行 Ollama 感到吃力，**完全不需要勉強升級硬體**！我們推薦以下兩個目前開發者圈最熱門、且提供免費額度（Free Tier）的雲端 API 備案：

### 備案 A：Groq API（極速推論，免費 Llama 3.3 / Qwen）

* **特點**：使用專用 LPU 晶片，推論速度每秒高達 300+ Token，幾乎不需要等待。
* **免費額度**：每日提供相當大方的免費請求次數。
* **申請方式**：前往 [Groq Console](https://console.groq.com/) 註冊並建立免費 `API Key`。

### 備案 B：Google Gemini API（超大 context，免費 Gemini Flash）

* **特點**：理解力極強、支援超長文本，非常適合未來讓 AI 讀取整份保單條款 PDF。
* **免費額度**：Gemini 1.5/2.0 Flash 模型提供 15 RPM (每分鐘請求數)，個人開發與測試完全夠用。
* **申請方式**：前往 [Google AI Studio](https://aistudio.google.com/) 一鍵領取免費 API Key。

---

## 4. 開發工具串接設定（OpenCode / CLI 設定檔）

不論你選擇地端 Ollama 還是免費雲端 API，都可以透過 OpenCode 設定檔（在對話框輸入 `/config` 或修改 `.opencode.json`）進行一鍵切換：

### 🎯 情境 A：串接地端 Ollama

```json
{
  "provider": {
    "ollama": {
      "api": "openai",
      "options": {
        "baseURL": "http://localhost:11434/v1",
        "apiKey": "ollama"
      }
    }
  },
  "model": "ollama/qwen2.5-coder:7b"
}

```

### 🎯 情境 B：串接 Groq 免費 API

```json
{
  "provider": {
    "groq": {
      "api": "openai",
      "options": {
        "baseURL": "https://api.groq.com/openai/v1",
        "apiKey": "YOUR_GROQ_API_KEY"
      }
    }
  },
  "model": "groq/qwen-2.5-coder-32b"
}

```

---

## 💡 今日總結與明日預告

今天我們確保了不論你的硬體設備如何，都能順利架設好免費且順暢的 AI 大腦！地端 Ollama 給你 100% 的隱私防護，免費雲端 API 則提供無負擔的流暢推論。

**思考題**：你最後選擇了「地端 Ollama」還是「免費雲端 API」？運行的速度還滿意嗎？

**明日預告**：大腦準備好了！明天（Day 8），我們將正式進入 **階段 2（6-3-1 財務核心引擎開發）**，撰寫 `first-policy` Skill 的「主控台」與「子命令」架構！

---
* 🔗 專案 GitHub 倉庫：[first-policy-ai](https://github.com/1daniel3333/first-policy-ai)
