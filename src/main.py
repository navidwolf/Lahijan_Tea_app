from business_logic.calculations import calculate_profit
from utils.helpers import read_json, write_json
from config import DEFAULT_INPUT_PATH, DEFAULT_OUTPUT_PATH

def main():
    print("=== اپلیکیشن مدیریت فروش چای لاهی‌جان ===\n")
    
    # دریافت ورودی از کاربر
    try:
        cost_per_gram = float(input("قیمت خرید عمده هر گرم چای: "))
        price_per_gram = float(input("قیمت فروش هر گرم چای: "))
        shipping_per_gram = float(input("هزینه ارسال هر گرم چای: "))
        packaging_per_gram = float(input("هزینه بسته‌بندی هر گرم: "))
        grams_per_packet = float(input("تعداد گرم در هر پاکت: "))
        packets_per_day = int(input("تعداد پاکت فروش در روز: "))
    except ValueError:
        print("ورودی‌ها باید عدد باشند!")
        return

    # محاسبه سود
    result = calculate_profit(cost_per_gram, price_per_gram, shipping_per_gram, packaging_per_gram, grams_per_packet, packets_per_day)

    # نمایش نتیجه
    print(f"\nسود هر پاکت: {result['profit_per_packet']} تومان")
    print(f"سود روزانه: {result['daily_profit']} تومان")

    # ذخیره داده‌ها در فایل JSON
    write_json(DEFAULT_OUTPUT_PATH, [result])
    print(f"\nنتایج در فایل '{DEFAULT_OUTPUT_PATH}' ذخیره شد.")

if __name__ == "__main__":
    main()
