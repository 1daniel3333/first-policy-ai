# Day 9 — 串接雲端主流 API：計費陷阱、快取機制與安全連線

> **前情提要**：昨天我們建立好了 AI 的靈魂主控台 `SKILL.md`。
> **本日目標**：在混合工作流的「雲端大腦」階段，我們必須搞懂 API 怎麼計費，以及如何安全地把 API Key 餵給 OpenCode。

---

## 1. 雲端大腦的計費陷阱 (The Meat)

在我們這個專案中，當你跟 AI 聊天時，它不只會看你最後一句話，它會把 `SKILL.md`、`events.json` 以及之前的對話歷史「全部重看一遍」。這會導致 Input Token 呈指數型增長。如果不搞懂計費規則，你的信用卡帳單會爆炸。

1.  **Input Token（輸入）**：發送給 AI 的所有內容（包含隱藏的背景設定與專案檔案）。
2.  **Output Token（輸出）**：AI 回覆的話或程式碼。單價通常是 Input 的 3 到 5 倍。
3.  **Prompt Caching（快取機制）**：**這是窮人救星！** 為了避免重複計費，Claude 和 Gemini 都有快取機制。例如 Claude，當你重複讀取一樣的 `SKILL.md` 時，快取部分會直接打 **1 折（省 90%）**。這對於頻繁存取專案檔案的 OpenCode 來說，是巨幅的成本節省。

因此，我們的策略是：開發架構時用 Claude 3.5 Sonnet (享受快取優惠)，測試執行時切換回我們 Day 7 裝好的本地 Ollama (免費)。

## 2. 實作核心：建立 `.env` 保護你的 API Key (Code Snippet)

**千萬不要把 API Key 直接寫在程式碼中！** 萬一不小心推上 GitHub，三分鐘內你的帳戶就會被駭客刷爆。

請在專案根目錄下建立一個名為 `.env` 的隱藏檔案。這是用來存放機密資訊的保險箱。請複製以下內容，並填入你從 OpenAI / Anthropic / Google 申請到的金鑰：

```env
# .env
# 雲端三巨頭 API Key (請將 xxx 替換為你的真實 Key)
OPENAI_API_KEY="sk-proj-xxxxxx..."
ANTHROPIC_API_KEY="sk-ant-xxxxxx..."
GEMINI_API_KEY="AIzaSyxxxxxx..."

# 本地 Ollama 接口 (免 Key，配 Base URL 即可)
OLLAMA_BASE_URL="http://localhost:11434"
```

接著，我們要確保這個檔案「絕對不會」被傳上 Git 伺服器。請在根目錄建立 `.gitignore` 檔案：

```text
# .gitignore
.env
__pycache__/
*.pyc
```

現在，當你在 OpenCode 的終端機裡需要切換大腦時，只需輸入 `/connect claude` 或 `/connect openai`，系統就會自動去讀取 `.env` 裡的密碼了。

---

## 3. 今日總結與明日預告

今天我們學會了如何在雲端 API 的世界裡省錢（靠快取）與保命（靠 `.env` 與 `.gitignore`）。基礎設施與大腦都已就位！

**思考題**：你去各家 AI 官網查看一下，目前的 Input 和 Output Token 定價差多少倍？

**明日預告**：萬事俱備，只欠東風。明天（Day 10），我們將一口氣把 `first-policy` 的 4 大核心子命令骨架建立起來，準備迎接下半場的實作！

---
* 🔗 專案 GitHub 倉庫：[first-policy-ai](https://github.com/1daniel3333/first-policy-ai)
