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
    # 測試
    alex_fsm = LifeStageFSM(age=28)
    print(f"Alex 目前狀態: {alex_fsm.state}")
    print(f"現階段核心防禦目標: {alex_fsm.get_core_risk()}")
