import json
from src.business_logic.calculations import (
    calculate_total_cost,
    calculate_final_price,
    calculate_profit,
)
from src.utils.helpers import format_currency
from src.config import CURRENCY


def run_with_inputs(price_per_kg, weight_kg, selling_price):
    """اجرای محاسبات برای ورودی مشخص"""
    total_cost = calculate_total_cost(price_per_kg, weight_kg)
    final_price = calculate_final_price(price_per_kg, weight_kg)
    profit = calculate_profit(selling_price, final_price)

    print("\n📊 گزارش:")
    print("هزینه کل (بدون مالیات):", format_currency(total_cost, CURRENCY))
    print("قیمت نهایی (با مالیات):", format_currency(final_price, CURRENCY))
    print("سود خالص:", format_currency(profit, CURRENCY))


def run_from_json():
    """اجرای محاسبات برای همه سناریوهای ذخیره شده در فایل JSON"""
    with open("data/input_samples.json", encoding="utf-8") as f:
        scenarios = json.load(f)["scenarios"]

    print("📂 اجرای برنامه با داده‌های نمونه از input_samples.json")

    for i, s in enumerate(scenarios, start=1):
        print(f"\n=== سناریو {i} ===")
        run_with_inputs(s["price_per_kg"], s["weight_kg"], s["selling_price"])


def run_from_user_input():
    """اجرای محاسبات با ورودی کاربر"""
    print("🌱 برنامه مدیریت کسب‌وکار چای لاهیجان 🌱")

    price_per_kg = float(input("قیمت هر کیلو چای (تومان): "))
    weight_kg = float(input("وزن چای (کیلوگرم): "))
    selling_price = float(input("قیمت فروش کل (تومان): "))

    run_with_inputs(price_per_kg, weight_kg, selling_price)


def main():
    print("📌 انتخاب حالت:")
    print("1. اجرای برنامه با ورودی کاربر")
    print("2. اجرای برنامه با داده‌های ذخیره شده در JSON")

    choice = input("انتخاب شما (1 یا 2): ").strip()

    if choice == "1":
        run_from_user_input()
    elif choice == "2":
        run_from_json()
    else:
        print("❌ انتخاب نامعتبر")


if __name__ == "__main__":
    main()
