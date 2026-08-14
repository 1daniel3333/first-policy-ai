# financial_status.py
import json
import os

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
