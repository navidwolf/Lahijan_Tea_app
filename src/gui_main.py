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
        self.root.geometry("800x700")

        # Background image
        try:
            self.bg_image = Image.open("assets/images/background.jpg").resize((800,700))
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.background = tk.Label(root, image=self.bg_photo)
            self.background.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"No background image: {e}")

        # Entries
        self.price_entries = []
        self.gram_entries = []

        inputs = [
            ("Purchase price", "assets/images/price_icon.png", "assets/images/weight_icon.png"),
            ("Shipping cost", "assets/images/shipping_icon.png", "assets/images/weight_icon.png"),
            ("Packaging cost", "assets/images/packaging_icon.png", "assets/images/weight_icon.png"),
            ("Selling price", "assets/images/sell_icon.png", "assets/images/weight_icon.png")
        ]

        y_pos = 20
        for label_text, price_icon, gram_icon in inputs:
            frame = tk.Frame(root, bg="#fdf6e3", bd=2, relief="groove")
            frame.place(x=50, y=y_pos, width=700, height=50)

            tk.Label(frame, text=label_text, font=("Arial", 12, "bold"), bg="#fdf6e3").pack(side="left", padx=5)
            price_entry = tk.Entry(frame, width=10, font=("Arial", 11), bd=2, relief="groove")
            price_entry.pack(side="left", padx=5)
            self.add_icon(frame, price_icon)

            tk.Label(frame, text="for", font=("Arial", 12, "bold"), bg="#fdf6e3").pack(side="left", padx=5)
            grams_entry = tk.Entry(frame, width=10, font=("Arial", 11), bd=2, relief="groove")
            grams_entry.pack(side="left", padx=5)
            self.add_icon(frame, gram_icon)

            tk.Label(frame, text="grams", font=("Arial", 12, "bold"), bg="#fdf6e3").pack(side="left", padx=5)

            self.price_entries.append(price_entry)
            self.gram_entries.append(grams_entry)
            y_pos += 70

        # Packets per day
        frame_packets = tk.Frame(root, bg="#fdf6e3", bd=2, relief="groove")
        frame_packets.place(x=50, y=y_pos, width=700, height=50)
        tk.Label(frame_packets, text="Packets sold per day:", font=("Arial", 12, "bold"), bg="#fdf6e3").pack(side="left", padx=5)
        self.packets_entry = tk.Entry(frame_packets, width=10, font=("Arial", 11), bd=2, relief="groove")
        self.packets_entry.pack(side="left", padx=5)
        tk.Button(frame_packets, text="Calculate", font=("Arial", 10, "bold"), bg="#2196F3", fg="white",
                  command=self.calculate_result).pack(side="right", padx=5)

        # Results
        self.result_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="ridge")
        self.result_frame.place(x=50, y=y_pos+70, width=700, height=100)
        self.total_cost_label = tk.Label(self.result_frame, text="", font=("Arial", 12), bg="#ffffff")
        self.total_cost_label.pack(pady=2)
        self.profit_label = tk.Label(self.result_frame, text="", font=("Arial", 12), bg="#ffffff")
        self.profit_label.pack(pady=2)
        self.daily_profit_label = tk.Label(self.result_frame, text="", font=("Arial", 12), bg="#ffffff")
        self.daily_profit_label.pack(pady=2)
        self.daily_cost_label = tk.Label(self.result_frame, text="", font=("Arial", 12), bg="#ffffff")
        self.daily_cost_label.pack(pady=2)

        # Chart
        self.fig = plt.Figure(figsize=(7, 2))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().place(x=50, y=y_pos+180)

        # Footer
        footer = tk.Frame(root, bg="#eee", height=30)
        footer.pack(side="bottom", fill="x")
        tk.Label(footer, text="© 2025 Lahijan Tea App | GitHub: navidwolf", font=("Arial", 10), bg="#eee").pack()

    def add_icon(self, frame, path):
        try:
            img = Image.open(path).resize((30,30))
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(frame, image=photo, bg="#fdf6e3")
            label.image = photo
            label.pack(side="left", padx=3)
        except Exception as e:
            print(f"Could not load icon {path}: {e}")

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

        grams = grams_purchase
        total_cost_per_packet = price_purchase + shipping + packaging
        profit_per_packet = selling_price - total_cost_per_packet
        daily_profit = profit_per_packet * packets_per_day
        daily_cost = total_cost_per_packet * packets_per_day

        self.total_cost_label.config(text=f"Total cost per packet: {total_cost_per_packet}")
        self.profit_label.config(text=f"Profit per packet: {profit_per_packet}")
        self.daily_profit_label.config(text=f"Daily profit: {daily_profit}")
        self.daily_cost_label.config(text=f"Daily cost: {daily_cost}")

        # Chart
        days = list(range(1, 8))
        daily_profits = [daily_profit] * 7
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.plot(days, daily_profits, marker='o', color="#FF5722")
        ax.set_title("Daily Profit")
        ax.set_xlabel("Day")
        ax.set_ylabel("Profit")
        self.canvas.draw()

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
root = tk.Tk()
app = TeaApp(root)
root.mainloop()
