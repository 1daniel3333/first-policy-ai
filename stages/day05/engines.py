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
