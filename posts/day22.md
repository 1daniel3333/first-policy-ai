# Day 22 — 遊戲的終點：寫出三種 FIRE (財務自由) 的判定引擎

> **前情提要**：昨天我們為人生模擬器建立《致富心態》的哲學觀。
> **本日目標**：今天我們要寫 Python 程式碼，為遊戲定義「過關條件」。當玩家資產達到什麼程度時，AI 會恭喜你破關？

---

## 1. 遊戲過關條件：FIRE 數學模型 (The Meat)

在 `/life-simulate` 遊戲中，只要你達成以下三種 FIRE 的任何一種，都會觸發過關動畫。這不僅是遊戲，這也是你真實人生的財務目標：

### (1) 傳統 FIRE (Traditional FIRE) - 完全財務自由
* **定義**：你不工作，靠 4% 法則的被動收入就能活到老。
* **過關條件**：`可投資資產 >= 年支出 x 25`。

### (2) 海灘躺平 FIRE (Coast FIRE) - 解除存錢壓力
* **定義**：你現在的資產，只要放在 7% 的大盤 ETF 裡，即使**從今天起不再存任何一毛錢**，靠複利滾到 60 歲時，就能達成 Traditional FIRE。
* **過關條件**：`現有資產 x (1 + 0.07)^(60 - 現在年齡) >= 年支出 x 25`。
* **作者點評**：這是我最喜歡的 FIRE！一旦達成，你每個月賺的錢都可以全部花掉（不用再存錢），去衝浪、去旅行，享受人生。

### (3) 咖啡師 FIRE (Barista FIRE) - 退而不休
* **定義**：你的資產還不夠完全退休，但只要你去做個輕鬆的兼職（例如星巴克店員，賺取微薄收入與勞健保），剩下的缺口靠資產的 4% 補足即可。
* **過關條件**：`可投資資產 >= (年支出 - 兼職年收入) x 25`。
* **作者點評**：當你在遊戲中遇到「黑天鵝爆倉」破產時，系統會引導你透過重構「人力資本」來達成 Barista FIRE 重生。

## 2. 實作核心：FIRE 判定引擎 (Code Snippet)

請在專案中建立 `fire_calculator.py`，這是 AI 用來判定你是否過關的核心程式：

```python
# fire_calculator.py
import json

def calculate_fire_status(player_state):
    age = player_state.get("age", 28)
    annual_expense = player_state.get("annual_expense", 480000)
    liquid_assets = player_state.get("liquid_assets", 0)
    human_capital_yield = player_state.get("human_capital_yield", 0)
    real_return_rate = player_state.get("real_return_rate", 0.07)
    target_retirement_age = player_state.get("target_retirement_age", 60)
    
    # 1. Traditional FIRE (25x Annual Expense)
    trad_target = annual_expense * 25
    trad_progress = round((liquid_assets / trad_target) * 100, 1) if trad_target > 0 else 0
    trad_achieved = liquid_assets >= trad_target
    
    # 2. Coast FIRE (Compounded at 7% to retirement age without new contributions)
    years_to_retire = max(0, target_retirement_age - age)
    projected_assets_at_retire = round(liquid_assets * ((1 + real_return_rate) ** years_to_retire))
    coast_achieved = projected_assets_at_retire >= trad_target
    coast_gap = max(0, trad_target - projected_assets_at_retire)
    
    # 3. Barista FIRE (Human capital covers part of expense)
    net_annual_expense_gap = max(0, annual_expense - human_capital_yield)
    barista_target = net_annual_expense_gap * 25
    barista_progress = round((liquid_assets / barista_target) * 100, 1) if barista_target > 0 else 100.0
    barista_achieved = liquid_assets >= barista_target
    
    return {
        "traditional_fire": {
            "target": trad_target,
            "progress": f"{trad_progress}%",
            "achieved": trad_achieved
        },
        "coast_fire": {
            "target_at_60": trad_target,
            "projected_assets": projected_assets_at_retire,
            "years_remaining": years_to_retire,
            "achieved": coast_achieved,
            "gap": coast_gap
        },
        "barista_fire": {
            "human_capital_annual_yield": human_capital_yield,
            "net_expense_gap": net_annual_expense_gap,
            "target": barista_target,
            "progress": f"{barista_progress}%",
            "achieved": barista_achieved
        },
        "is_bankrupt": player_state.get("is_bankrupt", False)
    }

def apply_market_shock(player_state, drop_rate):
    """
    Apply market shock and leverage liquidation.
    drop_rate: float (e.g. 0.35 for 35% market drop)
    """
    leverage = player_state.get("leverage_ratio", 1.0)
    effective_drop = drop_rate * leverage
    
    if effective_drop >= 1.0:
        player_state["liquid_assets"] = 0
        player_state["is_bankrupt"] = True
        result = "BANKRUPT_WIPEOUT"
    else:
        player_state["liquid_assets"] = round(player_state["liquid_assets"] * (1.0 - effective_drop))
        result = "NORMAL_VOLATILITY"
        
    return result, player_state

if __name__ == "__main__":
    # Test script with dummy state
    state = {
        "age": 28,
        "annual_expense": 480000,       # 40k/month
        "liquid_assets": 1200000,       # 1.2M investments
        "emergency_fund": 240000,
        "leverage_ratio": 1.0,
        "human_capital_yield": 240000,  # 20k/month side income
        "is_bankrupt": False,
        "real_return_rate": 0.07,
        "target_retirement_age": 60
    }
    
    status = calculate_fire_status(state)
    print("FIRE Status Calculation Test:")
    print(json.dumps(status, indent=2, ensure_ascii=False))
```

這段簡單的 Python 程式碼，將會在每個回合（每過一年）被呼叫。一旦其中一個布林值變成 `True`，AI 就會噴出慶祝的文字！

---

## 3. 今日總結與明日預告

今天我們寫好了 FIRE 的數學判定引擎。你會發現，只要不貪心開槓桿，趁年輕把錢丟進 7% 的 ETF 裡，Coast FIRE 其實非常容易達成。

**思考題**：算算看，如果你的年支出是 50 萬，你現在需要多少資產才能解鎖 Coast FIRE？

**明日預告**：你說 7% 是哪裡來的？明天（Day 23），我們將把「真實的歷史股市數據」匯入遊戲中，讓玩家體驗無上帝視角的 30 年市場絞肉機！

---
* 🔗 專案 GitHub 倉庫：[first-policy-ai](https://github.com/1daniel3333/first-policy-ai)
