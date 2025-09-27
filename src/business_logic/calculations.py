def calculate_profit(cost_per_gram, price_per_gram, shipping_per_gram, packaging_per_gram, grams_per_packet, packets_per_day):
    """
    محاسبه سود هر پاکت و سود روزانه
    """
    total_cost_per_packet = (cost_per_gram + shipping_per_gram + packaging_per_gram) * grams_per_packet
    profit_per_packet = (price_per_gram * grams_per_packet) - total_cost_per_packet
    daily_profit = profit_per_packet * packets_per_day

    return {
        "profit_per_packet": round(profit_per_packet, 2),
        "daily_profit": round(daily_profit, 2)
    }
