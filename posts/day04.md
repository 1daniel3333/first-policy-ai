# Day 4 — 設計人生主線狀態機：從 22 歲畢業到 60 歲退休的動態保險決策點

> **前情提要**：昨天我們建立了一個 28 歲新竹工程師的 JSON 數位畫像。
> **本日目標**：為這個角色設計一個「人生舞台」，我們將使用有限狀態機 (Finite State Machine, FSM) 來定義人生各階段的保險與理財決策點。

---

## 1. 為什麼保險不能「買完放著」？ (The Meat)

很多業務員喜歡推銷「終身險」，標榜繳費 20 年保障終身，讓你有一種「買完就可以高枕無憂」的錯覺。但這在財務工程上是極不合理的。

人生的風險是動態的。25 歲的你，最大風險是騎車摔斷腿無法工作（需要意外與實支實付）；35 歲剛生小孩的你，最大風險是你突然倒下，房貸與教育費壓垮另一半（需要高保額定期壽險）；到了 60 歲，你的房貸繳清了，小孩獨立了，你的家庭責任趨近於零，這時候你根本不需要壽險。

這就是為什麼，我們的 `first-policy` 模擬器採用了**狀態機 (FSM)** 架構。

### 人生主線狀態機 (Life Cycle FSM)

*   **狀態 1 (22-25 歲 職場新人)**：低資產。核心風險是意外。防禦點：定期意外險。
*   **狀態 2 (28-35 歲 成家立業)**：高負債 (房貸) 與高責任 (育兒)。核心風險是家庭支柱倒塌。防禦點：高保額定期壽險。
*   **狀態 3 (40-45 歲 職涯高峰)**：收入頂峰。核心風險是罹癌中斷高薪。防禦點：一次性給付癌症險。
*   **狀態 4 (50+ 歲 資產自保)**：負債歸零，投資水庫滿載。這時定期險保費變貴，我們應該**逐步解約保險**，靠自己的資產達成「自保 (Self-Insurance)」。

## 2. 實作核心：Python 狀態機骨架 (Code Snippet)

為了讓 AI 模擬器能在這幾個階段中切換，我們需要一個狀態管理的 Python 類別。請在專案中建立 `fsm.py`：

```python
# fsm.py
class LifeStageFSM:
    def __init__(self, age: int):
        self.age = age
        self.state = self._determine_state(age)

    def _determine_state(self, age: int) -> str:
        if age < 25:
            return "STAGE_1_ROOKIE"
        elif age < 35:
            return "STAGE_2_FAMILY"
        elif age < 45:
            return "STAGE_3_PEAK"
        elif age < 60:
            return "STAGE_4_COASTING"
        else:
            return "STAGE_5_RETIRED"

    def get_core_risk(self) -> str:
        risks = {
            "STAGE_1_ROOKIE": "意外致殘、突發急診",
            "STAGE_2_FAMILY": "家庭經濟支柱倒塌（房貸/育兒費）",
            "STAGE_3_PEAK": "重病導致中斷高薪收入",
            "STAGE_4_COASTING": "保費隨年齡暴漲的現金流消耗",
            "STAGE_5_RETIRED": "長照需求與資產通膨"
        }
        return risks.get(self.state, "未知風險")

if __name__ == "__main__":
    # 測試：我們昨天建立的 28 歲工程師 Alex
    alex_fsm = LifeStageFSM(age=28)
    print(f"Alex 目前狀態: {alex_fsm.state}")
    print(f"現階段核心防禦目標: {alex_fsm.get_core_risk()}")
```

這段程式碼確保了，當遊戲推進、角色年齡增加時，AI 拋出的考驗與建議也會隨之進化。

---

## 3. 今日總結與明日預告

今天我們用 Python 寫出了人生狀態機，徹底打破了「終身保固」的保險迷思。保險只是一個階段性的工具，當你夠有錢的時候，你就是自己的保險公司。

**思考題**：對照上面的 FSM，你目前處於哪一個階段？你覺得自己最大的財務風險是什麼？

**明日預告**：既然人生狀態機已經架好了，明天（Day 5）我們要請 AI 幫我們批次生成「100 個台灣在地化的黑天鵝隨機事件」，做成事件資料庫！

---
* 🔗 專案 GitHub 倉庫：[first-policy-ai](https://github.com/1daniel3333/first-policy-ai)
