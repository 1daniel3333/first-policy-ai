# Day 2 — 在娛樂與壓力之間：尋找 AI 人生財務模擬的「第三種選擇」

> **前情提要**：昨天我們確立了要打造一個能計算防線缺口、看懂保單並模擬人生的 AI Financial Planner (`first-policy`)。
> **本日目標**：釐清產品定位，探討為何市面上的工具不夠用，以及我們為何需要「AI + Python」雙引擎。

---

## 1. 為什麼我們需要「第三種選擇」？ (The Meat)

市面上有許多探討財務或人生的工具，但往往走向兩個極端：

1.  **娛樂型人生遊戲（如 BitLife、大富翁）**：好玩且有華麗 UI，但數值往往是隨機與簡化的，無法真實反映通膨、複利或台灣真實的健保與稅務環境。
2.  **傳統真人顧問 / 門戶諮詢**：精準，但可能帶有推銷保單的社交壓力，且需要交出極度隱私的個人財務數據。

我們的 `first-policy` 定位在兩者之間的**第三種選擇**：一個**零壓力、隱私優先、具備嚴謹數值運算**的文字對話沙盒。我們雖然沒有華麗的遊戲介面，但我們擁有最懂你的 AI 大腦與隨時根據你財務狀況生成的即時動態劇本。

| 評估維度 | 娛樂型人生遊戲 | 傳統真人顧問 | 本專案：AI Financial Planner |
| :--- | :--- | :--- | :--- |
| **互動體驗與客製化** | 點擊按鈕、看寫死的隨機結局 | 人際對話（帶有社交壓力） | **AI 溫暖對話 + 為你量身打造的動態劇本** |
| **隱私保護** | 高（純遊戲資料） | 需提供真實數據給第三方 | 🟢 **極高（資料僅存於本機）** |
| **數據核心** | 隨機簡化數值 | 靜態試算表 | **Python 歷史數據 + 精準狀態機** |

### 為什麼不能只用 LLM？(The Engineering Rigor)

LLM（大語言模型）很會聊天，但它們有嚴重的「數字幻覺」。如果你問 LLM：「每年存 10 萬，投報率 7%，30 年後有多少錢？」它可能會自信地給出一個算錯的答案。在財務規劃中，這是致命傷。

因此，我們的架構將採取 **AI 語意理解 + Python 數值引擎** 的雙軌制。LLM 負責解析你的話語與保單條款，而任何牽涉到「加減乘除、複利、保費計算」的工作，全部交給 Python 處理。

## 2. 實作核心：建立精準的 Python 複利計算器 (Code Snippet)

為了證明 Python 引擎的必要性，我們今天先實作一個簡單但絕對精準的複利計算函數。請在昨天建立的資料夾中，新增一個 `engines.py` 並貼上以下程式碼：

```python
# engines.py
def calculate_compound_interest(principal: float, annual_contribution: float, annual_rate: float, years: int) -> float:
    """
    精準計算複利，拒絕 LLM 數字幻覺
    :param principal: 初始本金
    :param annual_contribution: 每年持續投入金額
    :param annual_rate: 年化報酬率 (例如 0.07 代表 7%)
    :param years: 投資年限
    """
    total = principal
    for _ in range(years):
        # 假設每年年底投入
        total = total * (1 + annual_rate) + annual_contribution
    return round(total, 2)

if __name__ == "__main__":
    # 測試：本金 0，每年投 10 萬，年化 7%，持續 30 年
    result = calculate_compound_interest(0, 100000, 0.07, 30)
    print(f"30 年後的精準資產為: {result:,.0f} 元") 
    # 答案應該要是 9,446,079 元，你可以拿去問問 ChatGPT 看它會不會算錯。
```

---

## 3. 今日總結與明日預告

今天我們確立了「拒絕 LLM 通靈算數學」的工程底線，並完成了第一個 Python 數值引擎的雛形。這將是我們後續開發 `/financial-check` 與 `/life-simulate` 的重要基石。

**思考題**：你試著把 `engines.py` 裡的年化報酬率改成 `0.05` 和 `0.07`，看看 30 年後的差距有多大？這就是我們堅持被動投資大盤的原因。

**明日預告**：既然要打造人生模擬器，明天（Day 3）我們將定義「角色狀態 JSON Schema」，教 AI 如何建立一個 25 歲、月薪 7 萬、在竹科工作但充滿理財焦慮的典型台灣工程師！

---
* 🔗 專案 GitHub 倉庫：[first-policy-ai](https://github.com/1daniel3333/first-policy-ai)
