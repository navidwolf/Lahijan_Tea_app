from src.config import TAX_RATE, CURRENCY

def calculate_total_cost(price_per_kg, weight_kg):
    """محاسبه هزینه کل قبل از مالیات"""
    return price_per_kg * weight_kg

def calculate_final_price(price_per_kg, weight_kg):
    """محاسبه قیمت نهایی با مالیات"""
    total = calculate_total_cost(price_per_kg, weight_kg)
    tax = total * TAX_RATE
    return total + tax

def calculate_profit(selling_price, cost_price):
    """محاسبه سود خالص"""
    return selling_price - cost_price
