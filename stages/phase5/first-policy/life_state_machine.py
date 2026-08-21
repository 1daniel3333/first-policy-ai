# life_state_machine.py
import json
import random
from fire_calculator import calculate_fire_status, apply_market_shock
from insurance_game_engine import apply_insurance_choice
from historical_simulator import simulate_year

def run_life_simulation_scenario(player_name="Dan", start_age=23, dynamic_mode=True):
    # 初始狀態
    state = {
        "player_name": player_name,
        "age": start_age,
        "annual_income": 312000,          # 26k * 12
        "annual_expense": 300000,         # 25k * 12
        "annual_insurance_premium": 0,
        "annual_saved_premium": 0,
        "liquid_assets": 0,
        "emergency_fund": 10000,          # 初始存款 1萬
        "leverage_ratio": 1.0,
        "human_capital_yield": 0,
        "is_bankrupt": False,
        "real_return_rate": 0.07,         # 股票實質報酬率
        "target_retirement_age": 40,      # 目標 40歲退休
        "protection_score": 0,
        "has_insurance": False,
        "inflation_rate": 0.02
    }
    
    logs = []
    
    # 階段 1：23 歲出社會防具選配
    # 假設玩家選擇 Option B（高槓桿定期險，省下保費做投資）
    apply_insurance_choice(state, "TERM_LIGHT_SET")
    state["has_insurance"] = True
    state["emergency_fund"] = 10000  # 重設為初始存款
    
    logs.append({
        "age": 23,
        "event": "初出社會防具配置",
        "choice": "精準定期險方案（保費 10,000 元/年）",
        "summary": "以小博大，獲得基本實支實付與定期壽險保障，每年省下 32,000 元投入投資水庫。",
        "current_state": {
            "emergency_fund": state["emergency_fund"],
            "liquid_assets": state["liquid_assets"],
            "annual_expense": state["annual_expense"]
        }
    })

    # 階段 2：25 歲轉捩點與職涯起飛（家庭收入增加）
    # 假設找到更好的工作且雙薪，家庭收入到 55k/月，開銷變 30k/月
    state["age"] = 25
    state["annual_income"] = 660000       # 55k * 12
    state["annual_expense"] = 360000      # 30k * 12
    state["emergency_fund"] = 50000       # 緊急預備金累積到 5 萬
    state["liquid_assets"] = 50000        # 開始有投資
    
    logs.append({
        "age": 25,
        "event": "職涯與家庭黃金交叉點",
        "choice": "雙薪家庭月收達 55,000 元，積極配置資產",
        "summary": "年薪升至 66 萬，年開銷 36 萬。緊急預備金補充至 5 萬元，並開始定期定額投入全球 ETF。",
        "current_state": {
            "emergency_fund": state["emergency_fund"],
            "liquid_assets": state["liquid_assets"],
            "annual_expense": state["annual_expense"]
        }
    })

    # 階段 3：26-30 歲期間隨機事件 (Random Life Events)
    # 在 28 歲時發生隨機人生事件或股市波動
    state["age"] = 28
    
    if dynamic_mode:
        try:
            import os
            import json
            import random
            file_path = os.path.join(os.path.dirname(__file__), 'events.json')
            with open(file_path, 'r', encoding='utf-8') as f:
                events_db = json.load(f)
            # 篩選適合年齡的事件
            valid_events = [e for e in events_db if e['min_age'] <= state['age'] <= e['max_age']]
            if not valid_events:
                valid_events = events_db
            selected_event = random.choice(valid_events)
        except Exception as e:
            # Fallback
            selected_event = {
                'id': 'EVT_MEDICAL_SHOCK',
                'title': '醫療黑天鵝',
                'description': '無預警遭遇重大意外需手術治療，醫療費高達 40 萬元！',
                'category': 'Health',
                'financial_impact': {
                    'one_time_cash': -400000,
                    'insured_one_time_cash': -20000,
                    'monthly_income_delta': 0,
                    'income_freeze_months': 0,
                    'annual_expense_increase': 0,
                    'annual_expense_multiplier': 1.0
                },
                'insurance_claimable': True
            }
    else:
        # 預設非股市事件
        selected_event = {
            'id': 'EVT_MEDICAL_SHOCK',
            'title': '醫療黑天鵝',
            'description': '無預警遭遇重大意外需手術治療，醫療費高達 40 萬元！',
            'category': 'Health',
            'financial_impact': {
                'one_time_cash': -400000,
                'insured_one_time_cash': -20000,
                'monthly_income_delta': 0,
                'income_freeze_months': 0,
                'annual_expense_increase': 0,
                'annual_expense_multiplier': 1.0
            },
            'insurance_claimable': True
        }
        
    # 通用事件處理邏輯
    event_title = selected_event['title']
    event_summary = selected_event['description']
    impact = selected_event['financial_impact']
    
    # 處理單次大額支出 (如醫療費、大額花費)
    one_time_cash = impact.get('one_time_cash', 0)
    insured_cash = impact.get('insured_one_time_cash', 0)
    claimable = selected_event.get('insurance_claimable', False)
    
    if one_time_cash < 0:
        bill = -one_time_cash
        if claimable and state.get('has_insurance'):
            out_of_pocket = -insured_cash
            event_summary += f" 幸好有保險理賠，實質僅需自付 {out_of_pocket} 元。"
            state['emergency_fund'] = max(0, state['emergency_fund'] - out_of_pocket)
        else:
            out_of_pocket = bill
            if claimable:
                event_summary += " 因無保險，必須全額自掏腰包！"
            
            if state['emergency_fund'] >= out_of_pocket:
                state['emergency_fund'] -= out_of_pocket
                event_summary += " 幸好有預備金吸收了衝擊。"
            else:
                remaining = out_of_pocket - state['emergency_fund']
                state['emergency_fund'] = 0
                state['liquid_assets'] -= remaining
                if state['liquid_assets'] >= 0:
                    event_summary += f" 預備金不足，被迫變賣投資水庫 {remaining} 元。"
                else:
                    state['is_bankrupt'] = True
                    event_summary += f" 存款與投資不足支付，被迫背負 {-state['liquid_assets']} 元債務，宣告財務破產！"
    elif one_time_cash > 0:
        state['liquid_assets'] += one_time_cash
        event_summary += f" 獲得現金 {one_time_cash} 元，直接投入投資水庫。"

    # 處理失業或減薪/無薪假
    freeze_months = impact.get('income_freeze_months', 0)
    if freeze_months > 0:
        expense_for_freeze = int((state['annual_expense'] / 12 * freeze_months) * 0.7)
        event_summary += f" 收入中斷 {freeze_months} 個月。啟動節流，需消耗 {expense_for_freeze} 元。"
        if state['emergency_fund'] >= expense_for_freeze:
            state['emergency_fund'] -= expense_for_freeze
            event_summary += " 幸好有充足預備金度過難關。"
        else:
            gap = expense_for_freeze - state['emergency_fund']
            state['emergency_fund'] = 0
            state['liquid_assets'] -= gap
            if state['liquid_assets'] >= 0:
                event_summary += f" 預備金不足，被迫賤賣投資水庫 {gap} 元。"
            else:
                state['is_bankrupt'] = True
                event_summary += f" 投資水庫清空且不足以負擔，被迫借貸 {-state['liquid_assets']} 元，宣告破產！"
                
    monthly_delta = impact.get('monthly_income_delta', 0)
    if monthly_delta != 0:
        state['annual_income'] += monthly_delta * 12
        if monthly_delta > 0:
            event_summary += f" 月收入增加 {monthly_delta} 元。"
        else:
            event_summary += f" 月收入減少 {-monthly_delta} 元。"
            
    # 處理固定支出增加 (如家庭開銷、通膨)
    expense_increase = impact.get('annual_expense_increase', 0)
    expense_multiplier = impact.get('annual_expense_multiplier', 1.0)
    
    if expense_multiplier != 1.0:
        old_expense = state['annual_expense']
        state['annual_expense'] = int(state['annual_expense'] * expense_multiplier)
        increase = state['annual_expense'] - old_expense
        event_summary += f" 每年生活固定支出上漲 {increase} 元。"
        
    if expense_increase != 0:
        state['annual_expense'] += expense_increase
        event_summary += f" 每年生活固定支出增加 {expense_increase} 元。"

    logs.append({
        'age': 28,
        'event': event_title,
        'choice': '事件觸發與應對',
        'summary': event_summary,
        'current_state': {
            'annual_income': state['annual_income'],
            'annual_expense': state['annual_expense'],
            'emergency_fund': state['emergency_fund'],
            'liquid_assets': state['liquid_assets'],
            'is_bankrupt': state['is_bankrupt']
        }
    })

    # 階段 4：32 歲人力資本重構與財務復甦
    # 經歷了 28 歲的波折後，到了 32 歲
    state["age"] = 32
    if state["is_bankrupt"] or state.get("liquid_assets", 0) < 0:
        state["is_bankrupt"] = True
        # 背負債務的情況下，4年來以 10% 的高利滾動債務
        # 假設每年勉強擠出 100,000 元還債
        debt = -state["liquid_assets"]
        for _ in range(4):
            debt = round(debt * 1.10) - 100000
            
        if debt > 0:
            state["liquid_assets"] = -debt
            state["emergency_fund"] = 0
        else:
            state["liquid_assets"] = -debt # which is positive now
            state["emergency_fund"] = 30000 # rebuild some emergency fund
            
        state["annual_income"] = 550000 # 薪水勉強回升，但不若順遂者，職涯受創
        
    else:
        # 平常情況下，資產隨 7% 複利增長並加上持續投入
        # 過去 4 年 (28~32歲)，每年持續投入 200,000 元
        for _ in range(4):
            state["liquid_assets"] = round((state["liquid_assets"] + 200000) * 1.07)
            
        # 順利進修，薪水隨機成長到 85 萬 ~ 100 萬
        if dynamic_mode:
            state["annual_income"] = random.randint(85, 100) * 10000
        else:
            state["annual_income"] = 1000000
            
    state["annual_expense"] = max(state["annual_expense"], 400000)
    
    if state["is_bankrupt"] and state["liquid_assets"] < 0:
        event_summary = f"這4年來背負著沉重債務，努力還款。目前主動收入回升至 55 萬，但仍有 {-state['liquid_assets']} 元的債務需清償。"
    elif state["is_bankrupt"] and state["liquid_assets"] >= 0:
        event_summary = f"歷經4年的省吃儉用與還債，終於重獲新生，還清所有債務。主動收入回升至 55 萬，準備重新出發。"
        state["is_bankrupt"] = False
    else:
        event_summary = f"透過專業進修，主動年收入躍升至 {state['annual_income']} 元。這使你得以建立更寬闊的 6-3-1 現金流水庫，將更多儲蓄注入投資。"
    
    logs.append({
        "age": 32,
        "event": "人力資本重構",
        "choice": "清償債務" if state["is_bankrupt"] or state.get("liquid_assets", 0) < 0 else "進修高端技能並跳槽轉職",
        "summary": event_summary,
        "current_state": {
            "annual_income": state["annual_income"],
            "liquid_assets": state["liquid_assets"],
            "emergency_fund": state["emergency_fund"]
        }
    })

    # 階段 5：45 歲 FIRE 進度驗收（結合通膨）
    state["age"] = 45
    # 根據薪水與開銷，決定每年的可投資金額 (假設扣除少數雜支，投入率 80%)
    annual_savings = max(0, state["annual_income"] - state["annual_expense"])
    annual_investment = int(annual_savings * 0.8)
    
    # 過去 13 年 (32~45歲)
    for _ in range(13):
        state["liquid_assets"] = round((state["liquid_assets"] + annual_investment) * 1.07)
        
    fire_status_45 = calculate_fire_status(state)
    
    logs.append({
        "age": 45,
        "event": "Coast FIRE 指標驗收",
        "choice": "評估是否能提早過上躺平生活",
        "fire_status": fire_status_45,
        "summary": f"45 歲資產滾動達 {state['liquid_assets']:,} 元。考量 {state['inflation_rate']*100}% 通膨，退休時的名目年支出將增至 {fire_status_45['inflation_impact']['nominal_expense_at_retire']:,} 元。對照之下，您的實質資產健康度如何？",
        "current_state": {
            "liquid_assets": state["liquid_assets"],
            "fire_status": fire_status_45
        }
    })

    # 階段 6：60 歲終極人生驗收
    state["age"] = 60
    
    # 若在 45 歲還未達 Coast FIRE，可能需繼續投入，若已達則讓其自然滾動
    # 為了簡化，我們假定這 15 年，如果還沒 FIRE，薪水可能不會成長，但如果 FIRE 了就躺平
    # 我們統一讓其繼續保持 annual_investment 投入，或選擇不再投入
    is_coast_fire = fire_status_45["coast_fire"]["achieved"]
    
    for _ in range(15):
        if is_coast_fire:
            # 已達 Coast FIRE，不再新投入資金
            state["liquid_assets"] = round(state["liquid_assets"] * 1.07)
        else:
            # 未達 Coast FIRE，繼續苦幹實幹投入
            state["liquid_assets"] = round((state["liquid_assets"] + annual_investment) * 1.07)
            
    fire_status_60 = calculate_fire_status(state)
    
    logs.append({
        "age": 60,
        "event": "終極財務自由驗收",
        "choice": "正式啟動提領計畫退休",
        "fire_status": fire_status_60,
        "summary": f"恭喜您到達 60 歲！最終投資水庫達 {state['liquid_assets']:,} 元。若扣除這 37 年來的通膨折現，您的實際購買力是否足夠支撐理想的晚年生活？",
        "current_state": {
            "liquid_assets": state["liquid_assets"],
            "fire_status": fire_status_60
        }
    })

    return {
        "final_state": state,
        "timeline_logs": logs
    }

if __name__ == "__main__":
    result = run_life_simulation_scenario("Dan", 23, dynamic_mode=True)
    print("Dynamic Life Simulation Test:")
    # Print a summary of the 28-year-old event
    for log in result["timeline_logs"]:
        print(f"Age {log['age']} - {log['event']}: {log['summary'][:150]}...")
