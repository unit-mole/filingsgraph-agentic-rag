from __future__ import annotations

def _nz(v:float,name:str)->float:
    v=float(v)
    if v==0: raise ZeroDivisionError(f"{name} cannot be zero")
    return v

def growth_rate(previous:float,current:float)->float: return (float(current)-float(previous))/_nz(previous,"previous")*100.0
def year_over_year_change(previous:float,current:float)->float: return growth_rate(previous,current)
def cagr(begin:float,end:float,years:int)->float:
    if years<=0: raise ValueError("years must be positive")
    return ((float(end)/_nz(begin,"begin"))**(1.0/years)-1.0)*100.0
def gross_margin(gross_profit:float,revenue:float)->float: return float(gross_profit)/_nz(revenue,"revenue")*100.0
def operating_margin(operating_income:float,revenue:float)->float: return float(operating_income)/_nz(revenue,"revenue")*100.0
def capex_change(previous:float,current:float)->float: return growth_rate(previous,current)
def revenue_mix(segment_revenue:float,total_revenue:float)->float: return float(segment_revenue)/_nz(total_revenue,"total_revenue")*100.0
def segment_growth(previous:float,current:float)->float: return growth_rate(previous,current)
def percentage_point_change(previous_percent:float,current_percent:float)->float: return float(current_percent)-float(previous_percent)
