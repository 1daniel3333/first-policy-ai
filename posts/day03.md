# Day 3 — 如何用 AI 設計可程式化的世界觀：台灣 25–35 歲典型角色畫像

> **前情提要**：昨天我們建立了一個精準的 Python 複利計算器，確立了「AI 語意 + Python 運算」的雙引擎架構。
> **本日目標**：為我們的 `/life-simulate` (人生模擬器) 建立「主角」，學習如何用 JSON Schema 定義一個帶有財務狀態與故事背景的典型台灣年輕人。

---

## 1. 為什麼要用 JSON 定義角色？ (The Architecture)

在開發 AI 應用的過程中，最怕 AI 把數據跟故事混在一起。如果我們只給 AI 一段文字描述：「Alex 是個 28 歲的新竹工程師，月薪七萬五...」，當下一次我們需要把薪水扣除保費時，AI 很容易算錯。

**正確的做法是：敘事與邏輯解耦 (Decoupling)**。

我們用標準的 JSON Schema 來儲存角色的「硬數據」（資產、負債、年紀），這樣 Python 狀態機隨時可以精準讀取與修改；同時，我們在 JSON 裡保留一個 `narrative_background` 欄位，讓 LLM 能夠根據這個背景，用帶有溫度的語氣跟使用者對話。

這就是所謂的「可程式化的世界觀」。

## 2. 實作核心：建立台灣典型理財畫像 JSON (Code Snippet)

為了讓模擬器夠真實，我歸納了幾個台灣 25-35 歲年輕人的典型痛點：高房價焦慮、高工時健康疑慮、不知如何投資。

請在專案資料夾中建立 `schemas/` 目錄，並新增 `persona_alex.json` 檔案。你可以直接 Copy-Paste 下面的代碼，這就是我們遊戲的第一個預設主角。

```json
// schemas/persona_alex.json
{
  "persona_id": "tw_tech_engineer_28",
  "name": "陳明宇 (Alex)",
  "age": 28,
  "location": "新竹市",
  "occupation": "知名科技大廠軟體工程師",
  "monthly_income": 75000,
  "monthly_expenses": 42000,
  "financial_anxiety_tags": ["房價太高買不起", "長期加班擔心健康", "不知如何選 ETF"],
  "initial_assets": {
    "cash": 250000,
    "investments": 100000,
    "debts": 0
  },
  "insurance_coverage": {
    "has_labor_insurance": true,
    "has_commercial_health": true,
    "policy_type": "終身醫療險 (年繳4.5萬，保額偏低)"
  },
  "narrative_background": "明宇出社會 4 年，薪水優渥但生活節奏極快。出社會第一年聽親戚介紹買了高額終身險，每月扣完保費與房租後，發現手邊能用的流動資金所剩無幾，對未來的投資規劃充滿茫然..."
}
```

這個 JSON 檔案，未來將會在使用者觸發 `/life-simulate` 時，作為狀態機的初始狀態 (Initial State) 載入。

---

## 3. 今日總結與明日預告

今天我們透過 JSON Schema，把一個活生生、充滿焦慮的新竹工程師「數位化」了。有了角色，接下來我們需要給他一個舞台。

**思考題**：如果把上面的 JSON 改寫成你自己的狀態，你的 `financial_anxiety_tags`（理財焦慮標籤）會填什麼？

**明日預告**：明天（Day 4），我們將畫出這個角色從 22 歲到 60 歲退休的「人生主線狀態機 (FSM)」，並標出每個階段最重要的「保險決策點」！

---
* 🔗 專案 GitHub 倉庫：[first-policy-ai](https://github.com/1daniel3333/first-policy-ai)
