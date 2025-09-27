from src.business_logic.calculations import calculate_total_cost

def test_calculate_total_cost():
    assert calculate_total_cost(100000, 10) == 1000000
