# Day 14 — 組裝大腦：實作 /financial-check 指令邏輯

> **前情提要**：前幾天我們準備了 JSON Schema、Python 引擎與理財知識庫。
> **本日目標**：把所有的零件組裝起來！正式完成 `commands/financial-check.md`，讓 AI 學會幫你做財務健檢。

---

## 1. 指令執行流設計 (The Meat)

當我們輸入 `/financial-check` 時，AI 在背後會經歷一個嚴謹的工作流，以避免它陷入純粹的瞎聊：

1.  **資料蒐集**：依照 `schemas/financial_profile.json`，用溫柔的教練語氣向你提問，補齊必要的數字。
2.  **呼叫 Python 引擎**：把蒐集到的資料轉成 JSON，並呼叫我們在 Day 12 寫的 `financial_status.py`，精準算出防禦力 (A/B/C) 與結餘率。
3.  **檢索知識庫**：讀取 `references/financial-basics.md`，獲取 6-3-1 比例與保費 10% 天花板的鐵律。
4.  **生成報告**：結合你的「真實數字」與「理財鐵律」，產出一份客製化的健檢報告。

## 2. 實作核心：撰寫指令 Prompt (Code Snippet)

請打開我們在 Day 10 建立的 `commands/financial-check.md`，把裡面的內容替換為以下完整的 Prompt：

```markdown
---
name: financial-check
description: 執行個人財務與防線檢測，計算緊急預備金與保費預算。
---

# 系統指令 (System Prompt)

你是一位專業且溫暖的財務教練。當使用者呼叫此命令時，請嚴格遵循以下步驟：

## Step 1: 資料蒐集
請以友善的語氣，引導使用者提供 `schemas/financial_profile.json` 裡的必填資訊（年齡、月收入、月結餘、總存款）。一次不要問超過兩個問題，避免給人壓力。

## Step 2: 狀態計算
當資料蒐集齊全後，請執行 `python financial_status.py` 進行數學運算，嚴禁自己心算。

## Step 3: 生成健檢報告
請閱讀 `@references/financial-basics.md`，並根據 Python 計算出的「防禦等級」與「蓄水率」，給出一份健檢報告。報告必須包含：
1. **防禦力評比**：你的預備金能撐幾個月？是 A、B 還是 C 級？
2. **水庫狀態**：你的儲蓄率是否達標 30%？
3. **保費預算天花板**：算出使用者年收入的 10%，嚴格警告買保險不得超過此數字。
4. **下一步建議**：若預備金 < 3個月，請勸退他買任何保險，先存錢再說。
```

> 💡 **技巧**：在 OpenCode 中，我們可以直接在 Prompt 裡使用 `@` 來引用專案內的檔案。這能確保 AI 確實去讀取了我們設定好的知識庫。

---

## 4. 今日總結與明日預告

今天我們寫出了第一個真正具有「系統性思維」的 AI 指令。它不再只是跟你聊天，而是會走訪檔案、跑腳本、查手冊，然後給你最中肯的建議。

**思考題**：如果你是 AI 顧問，面對一個月薪 3 萬、存款 0 元、卻想買每年 4 萬保費終身險的年輕人，你會怎麼勸退他？

**明日預告**：是騾子是馬，拉出來遛遛！明天（Day 15）是我們的**中期檢查點**，我將直接用兩個真實案例（月光新鮮人 vs 已婚媽媽）來 Demo `/financial-check` 的實際執行效果！

---
* 🔗 專案 GitHub 倉庫：[first-policy-ai](https://github.com/1daniel3333/first-policy-ai)
