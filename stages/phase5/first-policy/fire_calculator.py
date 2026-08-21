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
    
    # Test market shock with 3x leverage
    leveraged_state = dict(state, leverage_ratio=3.5, liquid_assets=500000)
    res_type, updated_state = apply_market_shock(leveraged_state, 0.35)
    print(f"\nMarket Shock Test (35% drop with 3.5x leverage): Result={res_type}")
    print("Updated State:", json.dumps(updated_state, indent=2, ensure_ascii=False))
