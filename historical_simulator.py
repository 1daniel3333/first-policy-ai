# historical_simulator.py
import json
import random

ETF_CONFIGS = {
    "VT": {
        "name": "全球極致分散派 (VT)",
        "currency": "USD",
        "avg_return": 0.07,
        "volatility": 0.15
    },
    "VOO": {
        "name": "美國強權龍頭派 (VOO)",
        "currency": "USD",
        "avg_return": 0.08,
        "volatility": 0.18
    },
    "0050": {
        "name": "在地護國神山派 (0050/006208)",
        "currency": "TWD",
        "avg_return": 0.085,
        "volatility": 0.20
    },
    "CASH": {
        "name": "純現金避難防守派 (CASH)",
        "currency": "TWD",
        "avg_return": -0.02,  # Inflation decay
        "volatility": 0.0
    }
}

SCENARIOS = {
    "SCENARIO_ALPHA": {"name": "平穩順風成長期", "market_drawdown": -0.10, "usdtwd_fx_change": -0.02},
    "SCENARIO_BETA": {"name": "歷史大修正黑天鵝期", "market_drawdown": -0.40, "usdtwd_fx_change": -0.08},
    "SCENARIO_GAMMA": {"name": "溫和震盪輪動期", "market_drawdown": -0.15, "usdtwd_fx_change": 0.03}
}

def simulate_year(etf_style, leverage_ratio=1.0, scenario_key=None):
    if etf_style not in ETF_CONFIGS:
        etf_style = "VT"
        
    config = ETF_CONFIGS[etf_style]
    
    if not scenario_key or scenario_key not in SCENARIOS:
        scenario_key = random.choice(list(SCENARIOS.keys()))
        
    scenario = SCENARIOS[scenario_key]
    drawdown = scenario["market_drawdown"]
    fx_change = scenario["usdtwd_fx_change"] if config["currency"] == "USD" else 0.0
    
    # Calculate effective return considering leverage
    base_return = config["avg_return"] + drawdown
    effective_return = base_return * leverage_ratio + fx_change
    
    is_wipeout = effective_return <= -1.0 or (drawdown * leverage_ratio) <= -0.8
    
    return {
        "etf_style": etf_style,
        "etf_name": config["name"],
        "currency": config["currency"],
        "scenario_name": scenario["name"],
        "effective_return_pct": f"{round(effective_return * 100, 1)}%",
        "fx_impact": f"{round(fx_change * 100, 1)}%" if config["currency"] == "USD" else "無匯率影響 (TWD)",
        "is_wipeout": is_wipeout
    }

if __name__ == "__main__":
    print("Testing ETF Historical Simulator:")
    print("1. VT (No leverage, Black Swan Scenario):")
    res1 = simulate_year("VT", leverage_ratio=1.0, scenario_key="SCENARIO_BETA")
    print(json.dumps(res1, indent=2, ensure_ascii=False))
    
    print("\n2. 0050 (2.5x Leverage, Black Swan Scenario):")
    res2 = simulate_year("0050", leverage_ratio=2.5, scenario_key="SCENARIO_BETA")
    print(json.dumps(res2, indent=2, ensure_ascii=False))
