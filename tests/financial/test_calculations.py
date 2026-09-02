import pytest
from filingsgraph.finance.calculations import growth_rate, cagr, gross_margin, operating_margin, revenue_mix, percentage_point_change

def test_growth_rate(): assert growth_rate(100, 125) == 25
def test_growth_zero_raises():
    with pytest.raises(ZeroDivisionError): growth_rate(0, 1)
def test_cagr(): assert round(cagr(100, 121, 2), 6) == 10.0
def test_margins(): assert gross_margin(40, 100) == 40 and operating_margin(20, 100) == 20
def test_revenue_mix(): assert revenue_mix(25, 100) == 25
def test_percentage_points(): assert percentage_point_change(35, 37.5) == 2.5
