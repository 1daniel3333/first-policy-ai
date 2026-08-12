# Day 12 — 建立角色財務狀態系統：AI 如何解讀你的防禦力？

> **前情提要**：昨天我們定義了 AI 蒐集財務數據的 JSON Schema。
> **本日目標**：今天我們要寫一段 Python 程式，讓 AI 把這些冰冷的 JSON 數字轉換成遊戲中的「防禦等級」與「健康指標」。

---

## 1. 理財的 HP 與 MP 設計 (The Meat)

在我們的 `first-policy` 系統中，你的財務狀況將被量化成三個核心指標：

1.  **緊急預備金月數 (防禦力)**：存款 / 每月支出。這決定了你萬一失業或生病，可以活幾個月。低於 3 個月，你的防禦力就是 🔴 C 級（危險）。
2.  **蓄水率 (攻擊力/滾雪球速度)**：每月結餘 / 月收入。低於 10% 代表你是月光族，水庫漏水，無法累積複利。
3.  **責任負擔 (Debuffs)**：是否有房貸？是否有小孩？這會大幅提高你遇到意外時的「爆擊傷害」。

為什麼要特別算這些？因為**保險是為了補足防禦力的缺口**。如果你有 500 萬存款（防禦力 S 級），你根本不需要買醫療險，因為你可以自己賠給自己；但如果你只有 5 萬存款且背負房貸，你就必須買高槓桿的定期險來保命。

## 2. 實作核心：Python 財務指標計算引擎 (Code Snippet)

請在專案中新增一個檔案 `financial_status.py`，這是 AI 代理的數學引擎。你可以直接複製以下程式碼：

```python
# financial_status.py
import json

def analyze_financial_status(user_profile):
    basic = user_profile.get("basic_info", {})
    ext = user_profile.get("extension_info", {})
    
    income = basic.get("monthly_income", 0)
    surplus = basic.get("monthly_surplus", 0)
    savings = basic.get("total_savings", 0)
    
    # 1. 計算每月支出 (支出 = 收入 - 結餘)
    monthly_expenses = max(income - surplus, 1)  # 避免除以零
    
    # 2. 計算緊急預備金月數
    reserve_months = round(savings / monthly_expenses, 1)
    
    # 3. 計算儲蓄率
    savings_rate = round((surplus / income) * 100, 1) if income > 0 else 0
    
    # 4. 評估防禦力等級
    if reserve_months >= 6:
        defense_rating = "A (安全穩健)"
    elif reserve_months >= 3:
        defense_rating = "B (基本防禦)"
    else:
        defense_rating = "C (防禦薄弱，需優先補充預備金)"
        
    # 5. 評估潛在負擔風險
    has_mortgage = ext.get("mortgage_balance", 0) > 0
    is_pillar = ext.get("family_status") in ["Married_With_Kids", "Single_Parent"]
    
    risk_level = "低"
    if has_mortgage or is_pillar:
        risk_level = "高 (身上有貸款或需要扶養家庭，經不起收入中斷)"
    elif ext.get("dependents_count", 0) > 0:
        risk_level = "中"

    return {
        "reserve_months": reserve_months,
        "savings_rate": f"{savings_rate}%",
        "defense_rating": defense_rating,
        "liability_risk": risk_level,
        "raw_data": {
            "health": 100,      # 初始健康度
            "happiness": 100    # 初始幸福度
        }
    }

if __name__ == "__main__":
    # Test script with dummy profile
    dummy_profile = {
        "basic_info": {
            "age": 28,
            "gender": "F",
            "monthly_income": 50000,
            "monthly_surplus": 15000,
            "total_savings": 300000,
            "target_retirement_age": 60
        },
        "extension_info": {
            "family_status": "Married_With_Kids",
            "dependents_count": 1,
            "mortgage_balance": 0,
            "existing_policies": [],
            "risk_appetite": "Moderate"
        }
    }
    result = analyze_financial_status(dummy_profile)
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

這段程式碼將會被我們的 OpenCode Skill 呼叫。當你輸入 `/financial-check` 時，AI 會先蒐集你的資料，然後把 JSON 餵給這支 Python 程式，最後再把計算結果講給你聽。

---

## 3. 今日總結與明日預告

今天我們實作了財務健檢的「大腦運算區」。透過 Python 嚴謹的除法與四捨五入，我們確保了 AI 在評估你的生存月數時，絕對不會產生數字幻覺。

**思考題**：試著用上面的公式算算看，你的 `reserve_months` (防禦力) 落在 A、B 還是 C 級？

**明日預告**：明天（Day 13），我們將為 AI 注入靈魂！我們將撰寫 `financial-basics.md`，把「6-3-1 預算分配」與「保大不保小」的核心理財知識教給 AI。

---
* 🔗 專案 GitHub 倉庫：[first-policy-ai](https://github.com/1daniel3333/first-policy-ai)
