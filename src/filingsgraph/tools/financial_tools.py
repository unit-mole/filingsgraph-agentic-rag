from filingsgraph.finance.calculations import growth_rate,cagr,gross_margin,operating_margin,capex_change,revenue_mix,segment_growth,percentage_point_change
CALCULATION_FUNCTIONS={
 'growth_rate':growth_rate,'cagr':cagr,'gross_margin':gross_margin,'operating_margin':operating_margin,
 'capex_change':capex_change,'revenue_mix':revenue_mix,'segment_growth':segment_growth,'percentage_point_change':percentage_point_change,
}
def calculate(name:str,**kwargs)->float:
    if name not in CALCULATION_FUNCTIONS: raise KeyError(f'Unknown calculation: {name}')
    return float(CALCULATION_FUNCTIONS[name](**kwargs))
