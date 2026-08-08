# Day 8 — 定義 AI 的靈魂：OpenCode Skill 架構解析

> **前情提要**：昨天我們打通了地端 Ollama 與免費雲端 API 的混合大腦架構。
> **本日目標**：正式開始撰寫 `first-policy`，了解 OpenCode Skill 的架構（SKILL.md、Commands、References）是如何運作的。

---

## 1. 什麼是 OpenCode Skill？ (The Meat)

在以前，我們要在 ChatGPT 貼上落落長的一大段 Prompt，AI 才能變成「保險顧問」。但只要換個對話視窗，它又失憶了。

OpenCode Skill 的概念是：**把 Prompt、背景知識、工作流程，全部「程式碼化」並用資料夾管理起來**。只要你切換到這個專案，AI 就自動裝備了這個 Skill 的知識，變成該領域的專家。

我們的 `first-policy` 將採用經典的 **Subcommand Pattern (子命令模式)** 架構：

```text
first-policy-ai/
├── SKILL.md                    ← AI 的大腦主入口 (定義人設與免責聲明)
├── commands/
│   ├── financial-check.md      ← 子技能 1：財務健檢
│   └── insurance-review.md     ← 子技能 2：保單健檢
└── references/
    └── events.json             ← 靜態知識庫：昨天產生的隨機事件
```

為什麼要這樣分？為了**避免 Context 膨脹**。如果把所有邏輯塞在一個大檔案，AI 會抓不到重點。透過 `commands/`，我們只有在輸入 `/financial-check` 時，AI 才會去讀取相關的步驟；透過 `references/`，AI 只有在需要時才去檢索背景知識。

## 2. 實作核心：建立主入口 `SKILL.md` (Code Snippet)

請在專案根目錄下，編輯我們 Day 1 建立的 `SKILL.md`，貼上以下內容：

```markdown
---
name: first-policy
description: A financial and insurance planner specialized in Taiwan's environment.
metadata:
  workflow: insurance-advisor
  domain: personal-finance
---

## ⚠️ 免責聲明 / Disclaimer

本 skill 為【教育性工具】，非保險諮詢服務、非投資顧問服務。
本工具「不」主動推薦特定保單，亦「不」取代合格從業人員之專業判斷。

## Overview
你是專屬 AI 財務顧問。你堅信「大腦的人力資本是終極底牌」，推崇指數化被動投資，並強調「保大不保小」的風險轉嫁哲學。

## Available Commands
- `/financial-check`：執行財務與防線檢測
- `/insurance-review`：上傳保單條款並進行缺口分析
- `/life-simulate`：啟動 30 年人生財務沙盒模擬
- `/future-self`：讓 60 歲的自己回覆一封信
```

> 💡 **注意**：檔案開頭的 `---` 包夾區塊是 **YAML Frontmatter**。這非常重要！OpenCode 依賴這裡的 `name` 和 `description` 來決定要不要自動載入這個技能。名稱只能是小寫和連字號。

---

## 3. 今日總結與明日預告

今天我們寫下了 AI 的靈魂主控台 `SKILL.md`，並把「免責聲明」放在最顯眼的位置（這對這類工具來說是絕對的紅線）。

**思考題**：如果你要寫一個幫你「自動 Code Review」的 Skill，你會在 `SKILL.md` 裡面賦予它什麼樣的人設？是嚴厲的資深架構師，還是溫柔的鼓勵者？

**明日預告**：既然主控台有了，明天（Day 9）我們將搞定最棘手的「API 金鑰管理」與「快取計費陷阱」，教你如何在雲端開發時省下 90% 的 Token 費用！

---
* 🔗 專案 GitHub 倉庫：[first-policy-ai](https://github.com/1daniel3333/first-policy-ai)
