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
        self.data = {}

        # Frames for each step
        self.frames = []
        self.create_steps()
        self.show_step(0)

        # Result labels
        self.profit_label = tk.Label(root, text="", font=("Arial", 12))
        self.profit_label.pack(pady=5)
        self.daily_label = tk.Label(root, text="", font=("Arial", 12))
        self.daily_label.pack(pady=5)

        # Figure for chart
        self.fig = plt.Figure(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

    def create_steps(self):
        # Step 0: grams per packet
        frame0 = tk.Frame(self.root)
        tk.Label(frame0, text="Enter grams per packet:", font=("Arial", 12)).pack(side="left")
        self.grams_entry = tk.Entry(frame0)
        self.grams_entry.pack(side="left")
        self.add_icon(frame0, "assets/images/tea_packaging.jpg")
        tk.Button(frame0, text="Next", command=lambda: self.next_step(0)).pack(side="left")
        frame0.pack(pady=5)
        self.frames.append(frame0)

        # Step 1: cost per gram
        frame1 = tk.Frame(self.root)
        tk.Label(frame1, text="Enter cost per gram:", font=("Arial", 12)).pack(side="left")
        self.cost_entry = tk.Entry(frame1)
        self.cost_entry.pack(side="left")
        self.add_icon(frame1, "assets/images/tea_logo.png")
        tk.Button(frame1, text="Next", command=lambda: self.next_step(1)).pack(side="left")
        frame1.pack(pady=5)
        self.frames.append(frame1)

        # Step 2: price per gram
        frame2 = tk.Frame(self.root)
        tk.Label(frame2, text="Enter price per gram:", font=("Arial", 12)).pack(side="left")
        self.price_entry = tk.Entry(frame2)
        self.price_entry.pack(side="left")
        self.add_icon(frame2, "assets/images/tea_field.jpg")
        tk.Button(frame2, text="Next", command=lambda: self.next_step(2)).pack(side="left")
        frame2.pack(pady=5)
        self.frames.append(frame2)

        # Step 3: shipping cost per gram
        frame3 = tk.Frame(self.root)
        tk.Label(frame3, text="Enter shipping cost per gram:", font=("Arial", 12)).pack(side="left")
        self.shipping_entry = tk.Entry(frame3)
        self.shipping_entry.pack(side="left")
        tk.Button(frame3, text="Next", command=lambda: self.next_step(3)).pack(side="left")
        frame3.pack(pady=5)
        self.frames.append(frame3)

        # Step 4: packaging cost per gram
        frame4 = tk.Frame(self.root)
        tk.Label(frame4, text="Enter packaging cost per gram:", font=("Arial", 12)).pack(side="left")
        self.packaging_entry = tk.Entry(frame4)
        self.packaging_entry.pack(side="left")
        tk.Button(frame4, text="Next", command=lambda: self.next_step(4)).pack(side="left")
        frame4.pack(pady=5)
        self.frames.append(frame4)

        # Step 5: packets per day
        frame5 = tk.Frame(self.root)
        tk.Label(frame5, text="Enter packets sold per day:", font=("Arial", 12)).pack(side="left")
        self.packets_entry = tk.Entry(frame5)
        self.packets_entry.pack(side="left")
        tk.Button(frame5, text="Calculate", command=self.calculate_result).pack(side="left")
        frame5.pack(pady=5)
        self.frames.append(frame5)

    def add_icon(self, frame, path):
        try:
            img = Image.open(path)
            img = img.resize((30, 30))
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(frame, image=photo)
            label.image = photo  # keep reference
            label.pack(side="left", padx=5)
        except Exception as e:
            print(f"Could not load icon {path}: {e}")

    def show_step(self, index):
        for i, f in enumerate(self.frames):
            if i == index:
                f.pack()
            else:
                f.pack_forget()

    def next_step(self, index):
        self.show_step(index + 1)

    def calculate_result(self):
        try:
            grams = float(self.grams_entry.get())
            cost = float(self.cost_entry.get())
            price = float(self.price_entry.get())
            shipping = float(self.shipping_entry.get())
            packaging = float(self.packaging_entry.get())
            packets = int(self.packets_entry.get())
        except ValueError:
            messagebox.showerror("Error", "All inputs must be numbers!")
            return

        result = calculate_profit(cost, price, shipping, packaging, grams, packets)

        self.profit_label.config(text=f"Profit per packet: {result['profit_per_packet']}")
        self.daily_label.config(text=f"Daily profit: {result['daily_profit']}")

        # Chart
        days = list(range(1, 8))
        daily_profits = [result['daily_profit']] * 7
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
        write_json(output_path, [result])
        messagebox.showinfo("Saved", f"Results saved to {output_path}")


# --- Run app ---
root = tk.Tk()
app = TeaApp(root)
root.mainloop()
