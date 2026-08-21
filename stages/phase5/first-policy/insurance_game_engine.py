# insurance_game_engine.py
import json

def calculate_future_value_annuity(annual_payment, rate, years):
    """
    Calculate Future Value of Annuity (FV = P * (((1+r)^n - 1)/r))
    """
    if rate == 0:
        return annual_payment * years
    return round(annual_payment * (((1 + rate) ** years - 1) / rate))

def apply_insurance_choice(player_state, node_choice):
    age = player_state.get("age", 22)
    rate = player_state.get("real_return_rate", 0.07)
    
    if age == 22:
        if node_choice == "WHOLE_LIFE_FULL":
            player_state["annual_insurance_premium"] = 42000
            player_state["protection_score"] = 60
            player_state["annual_saved_premium"] = 0
        elif node_choice == "TERM_LIGHT_SET":
            player_state["annual_insurance_premium"] = 10000
            player_state["protection_score"] = 90
            saved_annual = 32000
            player_state["annual_saved_premium"] = saved_annual
            # Add to liquid assets
            player_state["liquid_assets"] += saved_annual

    elif age == 30:
        if node_choice == "KEEP_OLD":
            player_state["liability_coverage_gap"] = 8000000
            player_state["protection_score"] -= 30
        elif node_choice == "UPGRADE_TERM":
            player_state["annual_insurance_premium"] += 5000
            player_state["liability_coverage_gap"] = 0
            player_state["protection_score"] = 95
            
    # Calculate opportunity costs for 8 years (to age 30) and 30 years (to age 52)
    saved_annual = player_state.get("annual_saved_premium", 0)
    fv_8_years = calculate_future_value_annuity(saved_annual, rate, 8)
    fv_30_years = calculate_future_value_annuity(saved_annual, rate, 30)
    
    return {
        "current_age": age,
        "choice_made": node_choice,
        "annual_insurance_premium": player_state.get("annual_insurance_premium", 0),
        "protection_score": player_state.get("protection_score", 0),
        "liability_coverage_gap": player_state.get("liability_coverage_gap", 0),
        "opportunity_cost_growth": {
            "annual_saved_premium": saved_annual,
            "accumulated_at_age_30": fv_8_years,
            "accumulated_at_age_52": fv_30_years
        }
    }

if __name__ == "__main__":
    state = {
        "age": 22,
        "annual_income": 420000,
        "annual_expense": 252000,
        "liquid_assets": 0,
        "real_return_rate": 0.07
    }
    
    print("Testing Insurance Game Engine:")
    print("--- Option B: Term Light Set at Age 22 ---")
    res_b = apply_insurance_choice(state, "TERM_LIGHT_SET")
    print(json.dumps(res_b, indent=2, ensure_ascii=False))
    
    print("\n--- Option A: Whole Life Full at Age 22 ---")
    state_a = dict(state, age=22, liquid_assets=0)
    res_a = apply_insurance_choice(state_a, "WHOLE_LIFE_FULL")
    print(json.dumps(res_a, indent=2, ensure_ascii=False))
