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
        self.current_step = 0

        # Frames for each step
        self.frames = []
        self.create_steps()
        self.show_step(0)

        # Result labels
        self.total_cost_label = tk.Label(root, text="", font=("Arial", 12))
        self.total_cost_label.pack(pady=5)
        self.profit_label = tk.Label(root, text="", font=("Arial", 12))
        self.profit_label.pack(pady=5)
        self.daily_profit_label = tk.Label(root, text="", font=("Arial", 12))
        self.daily_profit_label.pack(pady=5)
        self.daily_cost_label = tk.Label(root, text="", font=("Arial", 12))
        self.daily_cost_label.pack(pady=5)

        # Chart
        self.fig = plt.Figure(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

    def create_steps(self):
        # Each step: price + grams with icons
        entries = [
            ("Enter purchase price:", "assets/images/price_icon.png", "assets/images/weight_icon.png"),
            ("Enter shipping cost:", "assets/images/shipping_icon.png", "assets/images/weight_icon.png"),
            ("Enter packaging cost:", "assets/images/packaging_icon.png", "assets/images/weight_icon.png"),
            ("Enter selling price:", "assets/images/sell_icon.png", "assets/images/weight_icon.png")
        ]

        self.price_entries = []
        self.gram_entries = []

        for i, (label_text, price_icon, gram_icon) in enumerate(entries):
            frame = tk.Frame(self.root)
            tk.Label(frame, text=label_text, font=("Arial", 12)).pack(side="left")

            price_entry = tk.Entry(frame, width=10)
            price_entry.pack(side="left")
            self.add_icon(frame, price_icon)

            gram_entry = tk.Entry(frame, width=10)
            gram_entry.pack(side="left")
            self.add_icon(frame, gram_icon)

            tk.Button(frame, text="Next" if i < len(entries)-1 else "Next", command=lambda idx=i: self.next_step(idx)).pack(side="left")
            frame.pack(pady=5)
            self.frames.append(frame)

            self.price_entries.append(price_entry)
            self.gram_entries.append(gram_entry)

        # Step: packets per day
        frame_packets = tk.Frame(self.root)
        tk.Label(frame_packets, text="Packets sold per day:", font=("Arial", 12)).pack(side="left")
        self.packets_entry = tk.Entry(frame_packets, width=10)
        self.packets_entry.pack(side="left")
        tk.Button(frame_packets, text="Calculate", command=self.calculate_result).pack(side="left")
        frame_packets.pack(pady=5)
        self.frames.append(frame_packets)

    def add_icon(self, frame, path):
        try:
            img = Image.open(path)
            img = img.resize((25, 25))
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(frame, image=photo)
            label.image = photo  # keep reference
            label.pack(side="left", padx=2)
        except Exception as e:
            print(f"Could not load icon {path}: {e}")

    def show_step(self, index):
        for i, f in enumerate(self.frames):
            f.pack_forget()
        self.frames[index].pack()

    def next_step(self, index):
        self.show_step(index + 1)

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

        grams = grams_purchase  # assume all weights equal for simplicity, یا می‌توانید متوسط بگیرید

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
        ax.plot(days, daily_profits, marker='o')
        ax.set_title("Daily Profit")
        ax.set_xlabel("Day")
        ax.set_ylabel("Profit")
        self.canvas.draw()

        # Save to JSON
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


# --- Run app ---
root = tk.Tk()
app = TeaApp(root)
root.mainloop()
