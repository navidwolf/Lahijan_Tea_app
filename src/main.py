import os
from business_logic.calculations import calculate_profit
from utils.helpers import read_json, write_json
from bidi.algorithm import get_display
import arabic_reshaper

def rtl(text):
    """تبدیل متن فارسی برای نمایش درست راست به چپ"""
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

def get_project_root():
    """مسیر ریشه پروژه را پیدا می‌کند (پوشه بالای src و data)"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def main():
    print(rtl("=== اپلیکیشن مدیریت فروش چای لاهی‌جان (خودکار) ===\n"))

    project_root = get_project_root()
    input_path = os.path.join(project_root, "data", "input_samples.json")
    output_path = os.path.join(project_root, "data", "output_examples.json")

    # خواندن داده‌ها از JSON
    try:
        inputs = read_json(input_path)
    except FileNotFoundError:
        print(rtl(f"فایل '{input_path}' یافت نشد. لطفاً آن را بسازید."))
        return
    except Exception as e:
        print(rtl(f"خطا در خواندن فایل: {str(e)}"))
        return

    results = []

    for entry in inputs:
        try:
            result = calculate_profit(
                cost_per_gram=entry["cost_per_gram"],
                price_per_gram=entry["price_per_gram"],
                shipping_per_gram=entry["shipping_per_gram"],
                packaging_per_gram=entry["packaging_per_gram"],
                grams_per_packet=entry["grams_per_packet"],
                packets_per_day=entry["packets_per_day"]
            )
            results.append(result)

            # نمایش نتیجه در کنسول
            print(rtl(f"\nسود هر پاکت: {result['profit_per_packet']} تومان"))
            print(rtl(f"سود روزانه: {result['daily_profit']} تومان"))

        except KeyError as ke:
            print(rtl(f"کلید {ke} در ورودی یافت نشد!"))
        except Exception as e:
            print(rtl(f"خطا در محاسبه: {str(e)}"))

    # ذخیره نتایج در JSON
    write_json(output_path, results)
    print(rtl(f"\nتمام نتایج در فایل '{output_path}' ذخیره شد."))

if __name__ == "__main__":
    main()
