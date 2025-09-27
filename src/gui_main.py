import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from business_logic.calculations import calculate_profit
from utils.helpers import write_json
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class TeaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lahijan Tea Sales App")
        self.root.geometry("850x700")

        # Canvas و Scrollbar
        self.canvas = tk.Canvas(root, bg="#f0f0f0")
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scroll_frame = tk.Frame(self.canvas, bg="#fdf6e3")
        self.canvas.create_window((0,0), window=self.scroll_frame, anchor="nw")

        self.scroll_frame.bind("<Configure>", self.on_frame_configure)

        # Background image اختیاری
        try:
            self.bg_image = Image.open("assets/images/background.jpg").resize((850,700))
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            bg_label = tk.Label(self.scroll_frame, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"No background image: {e}")

        # ورودی‌ها
        self.price_entries = []
        self.gram_entries = []

        inputs = [
            ("Purchase price", "assets/images/price_icon.png", "assets/images/weight_icon.png"),
            ("Shipping cost", "assets/images/shipping_icon.png", "assets/images/weight_icon.png"),
            ("Packaging cost", "assets/images/packaging_icon.png", "assets/images/weight_icon.png"),
            ("Selling price", "assets/images/sell_icon.png", "assets/images/weight_icon.png")
        ]

        for i, (label_text, price_icon, gram_icon) in enumerate(inputs):
            self.add_input_row(i, label_text, price_icon, gram_icon)

        # Packets per day
        self.add_packets_row(len(inputs))

        # Calculate Button
        self.calc_button = tk.Button(self.scroll_frame, text="Calculate", font=("Arial", 12, "bold"),
                                     bg="#2196F3", fg="white", command=self.calculate_result)
        self.calc_button.grid(row=len(inputs)+1, column=0, columnspan=7, pady=10)

        # Results Frame
        self.result_frame = tk.Frame(self.scroll_frame, bg="#ffffff", bd=2, relief="ridge")
        self.result_frame.grid(row=len(inputs)+2, column=0, columnspan=7, padx=20, pady=5, sticky="ew")
        self.total_cost_label = tk.Label(self.result_frame, text="", font=("Arial", 12), bg="#ffffff")
        self.total_cost_label.pack(pady=2)
        self.profit_label = tk.Label(self.result_frame, text="", font=("Arial", 12), bg="#ffffff")
        self.profit_label.pack(pady=2)
        self.daily_profit_label = tk.Label(self.result_frame, text="", font=("Arial", 12), bg="#ffffff")
        self.daily_profit_label.pack(pady=2)
        self.daily_cost_label = tk.Label(self.result_frame, text="", font=("Arial", 12), bg="#ffffff")
        self.daily_cost_label.pack(pady=2)

        # Chart
        self.fig = plt.Figure(figsize=(8,2))
        self.canvas_chart = FigureCanvasTkAgg(self.fig, master=self.scroll_frame)
        self.canvas_chart.get_tk_widget().grid(row=len(inputs)+3, column=0, columnspan=7, pady=5)

        # Footer
        footer = tk.Frame(root, bg="#eee", height=30)
        footer.pack(side="bottom", fill="x")
        tk.Label(footer, text="© 2025 Lahijan Tea App | GitHub: navidwolf", font=("Arial", 10), bg="#eee").pack()

    def add_input_row(self, row_num, label_text, price_icon, gram_icon):
        # Column 0: Label
        tk.Label(self.scroll_frame, text=label_text, font=("Arial",12,"bold"), bg="#fdf6e3").grid(
            row=row_num, column=0, padx=5, pady=5, sticky="w")

        # Column 1: Entry قیمت
        price_entry = tk.Entry(self.scroll_frame, width=10, font=("Arial",11), bd=2, relief="groove")
        price_entry.grid(row=row_num, column=1, padx=5)
        self.add_icon_grid(row_num, 2, price_icon)

        # Column 3: Label "for"
        tk.Label(self.scroll_frame, text="for", font=("Arial",12,"bold"), bg="#fdf6e3").grid(
            row=row_num, column=3, padx=5)

        # Column 4: Entry گرم
        grams_entry = tk.Entry(self.scroll_frame, width=10, font=("Arial",11), bd=2, relief="groove")
        grams_entry.grid(row=row_num, column=4, padx=5)
        self.add_icon_grid(row_num, 5, gram_icon)

        # Column 6: Label "grams"
        tk.Label(self.scroll_frame, text="grams", font=("Arial",12,"bold"), bg="#fdf6e3").grid(
            row=row_num, column=6, padx=5)

        self.price_entries.append(price_entry)
        self.gram_entries.append(grams_entry)

    def add_packets_row(self, row_num):
        tk.Label(self.scroll_frame, text="Packets sold per day:", font=("Arial",12,"bold"), bg="#fdf6e3").grid(
            row=row_num, column=0, padx=5, pady=5, sticky="w")
        self.packets_entry = tk.Entry(self.scroll_frame, width=10, font=("Arial",11), bd=2, relief="groove")
        self.packets_entry.grid(row=row_num, column=1, padx=5)

    def add_icon_grid(self, row, column, path):
        try:
            img = Image.open(path).resize((30,30))
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(self.scroll_frame, image=photo, bg="#fdf6e3")
            label.image = photo
            label.grid(row=row, column=column, padx=3)
        except Exception as e:
            print(f"Could not load icon {path}: {e}")

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def calculate_result(self):
        try:
            price_purchase, grams_purchase = float(self.price_entries[0].get()), float(self.gram_entries[0].get())
            shipping, grams_shipping = float(self.price_entries[1].get()), float(self.gram_entries[1].get())
            packaging, grams_packaging = float(self.price_entries[2].get()), float(self.gram_entries[2].get())
            selling_price, grams_selling = float(self.price_entries[3].get()), float(self.gram_entries[3].get())
            packets_per_day = int(self.packets_entry.get())
        except ValueError:
            messagebox.showerror("Error", "All inputs must be numbers!")
            return

        total_cost_per_packet = price_purchase + shipping + packaging
        profit_per_packet = selling_price - total_cost_per_packet
        daily_profit = profit_per_packet * packets_per_day
        daily_cost = total_cost_per_packet * packets_per_day

        self.total_cost_label.config(text=f"Total cost per packet: {total_cost_per_packet}")
        self.profit_label.config(text=f"Profit per packet: {profit_per_packet}")
        self.daily_profit_label.config(text=f"Daily profit: {daily_profit}")
        self.daily_cost_label.config(text=f"Daily cost: {daily_cost}")

        # Chart
        days = list(range(1,8))
        daily_profits = [daily_profit]*7
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.plot(days, daily_profits, marker='o', color="#FF5722")
        ax.set_title("Daily Profit")
        ax.set_xlabel("Day")
        ax.set_ylabel("Profit")
        self.canvas_chart.draw()

        # Save JSON
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        output_path = os.path.join(project_root, "data", "output_examples.json")
        result = {
            "total_cost_per_packet": total_cost_per_packet,
            "profit_per_packet": profit_per_packet,
            "daily_profit": daily_profit,
            "daily_cost": daily_cost
        }
        write_json(output_path, [result])
        messagebox.showinfo("Saved", f"Results saved to {output_path}")

# Run
if __name__ == "__main__":
    root = tk.Tk()
    app = TeaApp(root)
    root.mainloop()
