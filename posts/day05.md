# Day 5 — 打造真實生活的黑天鵝：如何用 Prompt 批次產生隨機事件庫

> **前情提要**：昨天我們建立人生狀態機 (FSM)，明確了各個年齡階段的核心風險。
> **本日目標**：為了讓 `/life-simulate` 更逼真，我們要透過 Prompt Engineering，請 AI 一次生成 100 個符合台灣實情的隨機事件資料庫。

---

## 1. 拒絕罐頭事件，擁抱「財務衝擊」 (The Meat)

如果玩過《大富翁》，你會發現裡面的事件通常是「中樂透得 2000 元」或「出車禍賠 500 元」，數值跟現實脫節。

真正的黑天鵝事件，對財務的衝擊是多維度的。例如「車禍韌帶撕裂」，你不只要付手術費（單筆現金流出），還可能會有 3 個月無法工作（收入中斷），甚至留下後遺症（每月醫療常態支出增加）。

為了讓 AI 替我們產生符合邏輯的事件，我們必須先定義出嚴謹的 JSON Schema。每個事件必須包含：
1.  `one_time_cash` (單筆收支)
2.  `monthly_income_delta` (每月收支變化)
3.  `income_freeze_months` (收入中斷月數)

## 2. 實作核心：產生 100 個事件的 Prompt (Code Snippet)

請複製以下的 Prompt，貼到 ChatGPT 或 Claude 裡面，讓 LLM 幫你產生一個專屬的 `events.json`。這也是我們第一階段最硬核的資料準備工作。

```text
請扮演一位台灣資深理財規劃師與遊戲企劃。
我正在開發一款名為 first-policy 的財務人生模擬器。
請幫我生成 10 個隨機人生事件（涵蓋 Health, Career, Family, Finance 類別），並嚴格輸出為以下 JSON 陣列格式。

事件必須符合台灣 25-60 歲的真實物價與情境。
請確保有 20% 是超級好運（如升職加薪），30% 是日常小破財，50% 是需要保險理賠的中重大風險（如罹癌、車禍）。

JSON 格式要求如下：
[
  {
    "id": "EVT_HEALTH_001",
    "title": "韌帶撕裂微創手術",
    "category": "Health",
    "severity": "minor_neg", 
    "description": "週末打籃球不慎膝蓋韌帶撕裂，醫生建議採用自費微創手術與自費醫材，復健期約 1 個月。",
    "financial_impact": {
      "one_time_cash": -85000,
      "monthly_income_delta": 0,
      "income_freeze_months": 1
    },
    "insurance_claimable": true,
    "claim_category": "medical_real_expense"
  }
]

請直接輸出 JSON，不要包含任何解釋文字。
```
*(備註：為了示範，上面的 Prompt 只要求 10 個。在實際開發時，你可以分批請 AI 產生 100 個，並存入 `references/events.json` 供後續 Python 程式讀取。)*

---

## 3. 今日總結與明日預告 (階段一完結！)

恭喜！到今天為止，我們完成了**第一階段 (破題與佈局)**。我們有了專案藍圖、數學引擎、角色畫像、人生狀態機，以及事件庫。有了這些材料，我們就具備了打造 AI 顧問的基石。

**思考題**：你遇過對你財務衝擊最大的一個「隨機事件」是什麼？

**明日預告**：明天（Day 6），我們將正式進入**第二階段 (OpenCode Skill 基礎)**。我將教大家如何擺脫傳統 IDE，用極簡的終端機環境 (TUI) 來與 AI 協同撰寫 `first-policy` 的核心程式碼！

---
* 🔗 專案 GitHub 倉庫：[first-policy-ai](https://github.com/1daniel3333/first-policy-ai)
