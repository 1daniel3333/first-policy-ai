# Day 11 — 釐清你的財務防禦力：/financial-check 的 Schema 設計

> **前情提要**：我們已經架設好了 OpenCode Skill 的骨架與大腦。
> **本日目標**：正式進入第三階段！我們要開始打造第一個核心功能 `/financial-check`，首先定義 AI 該如何收集並結構化我們的財務數據。

---

## 1. 財富水庫與防波堤 (The Meat)

在請 AI 幫我們做財務健檢之前，我們必須先給它正確的「財務觀」。在我們的設計中，理財就像是管理一座水庫：
*   **進水管 (月收入)**：你每個月賺的錢。
*   **出水管 (月支出)**：生活開銷與債務。
*   **水庫裡的存水 (月結餘與存款)**：這才是你真正擁有的財富，也是用來滾動複利雪球的本金。
*   **防波堤 (保險)**：為了避免突如其來的地震（重病、意外）震垮水庫，我們需要花一點點水（保費）去蓋防波堤。

為了讓 AI 能夠精準評估你的防波堤到底該蓋多高，我們不能只讓 AI 隨便問問題，我們必須定義一個嚴格的 JSON Schema 讓 AI 依循。

## 2. 實作核心：定義財務畫像 JSON Schema (Code Snippet)

請在專案中建立 `schemas/financial_profile.json`，並貼上以下定義：

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "FinancialProfile",
  "type": "object",
  "properties": {
    "basic_info": {
      "type": "object",
      "description": "基本財務與人口統計資訊（必填）",
      "properties": {
        "age": { "type": "integer", "description": "年齡" },
        "monthly_income": { "type": "integer", "description": "平均月收入" },
        "monthly_surplus": { "type": "integer", "description": "每月結餘 (收入減去生活費與債務)" },
        "total_savings": { "type": "integer", "description": "目前可動用的緊急預備金/活存總額" }
      },
      "required": ["age", "monthly_income", "monthly_surplus", "total_savings"]
    },
    "extension_info": {
      "type": "object",
      "description": "家庭狀況與風險細節（選填）",
      "properties": {
        "family_status": {
          "type": "string",
          "enum": ["Single", "Married_No_Kids", "Married_With_Kids"],
          "description": "家庭狀況，決定家庭責任與壽險需求"
        },
        "mortgage_balance": { "type": "integer", "description": "剩餘房貸/大筆債務總額" }
      }
    }
  },
  "required": ["basic_info"]
}
```

未來當使用者輸入 `/financial-check` 時，AI 就會扮演一個溫柔的教練，用聊天的方式引導使用者說出這些數字，並在背景默默將對話轉化為符合這個 Schema 的 JSON 檔案，存放在 `memory/user_profile.json` 中。這就是 AI Agent 強大的「狀態抽取」能力！

---

## 3. 今日總結與明日預告

今天我們定義了 AI 蒐集財務資料的標準格式，區分了「必填的個人水庫數據」與「選填的家庭責任數據」。

**思考題**：算算看，你每個月的 `monthly_surplus` (結餘) 佔了 `monthly_income` 的百分之幾？

**明日預告**：有了這些數字，AI 該怎麼評分？明天（Day 12），我們將撰寫 Python 腳本，把這些冰冷的 JSON 數字轉換成遊戲中的 HP (生命值) 與 MP (防禦力) 指標！

---
* 🔗 專案 GitHub 倉庫：[first-policy-ai](https://github.com/1daniel3333/first-policy-ai)
