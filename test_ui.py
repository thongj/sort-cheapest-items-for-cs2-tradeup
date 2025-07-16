import tkinter as tk
from tkinter import ttk

def calculate_average():
    float_vals = []
    price_vals = []

    for entry in float_entries:
        val = entry.get()
        if val:
            try:
                float_vals.append(float(val))
            except ValueError:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Lỗi: Float không hợp lệ -> {val}\n")
                return

    for entry in price_entries:
        val = entry.get()
        if val:
            try:
                price_vals.append(float(val))
            except ValueError:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Lỗi: Price không hợp lệ -> {val}\n")
                return

    avg_float = sum(float_vals) / len(float_vals) if float_vals else 0
    avg_price = sum(price_vals) / len(price_vals) if price_vals else 0

    min_val = float(min_val_var.get())
    max_val = float(max_val_var.get())

    try:
        max_output_val = float(max_output_entry.get())
    except ValueError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Lỗi: max_output_val không hợp lệ\n")
        return

    # In kết quả ra khung Text
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Số lượng float nhập: {len(float_vals)}\n")
    result_text.insert(tk.END, f"Số lượng price nhập: {len(price_vals)}\n")
    result_text.insert(tk.END, f"Trung bình Float: {avg_float:.4f}\n")
    result_text.insert(tk.END, f"Trung bình Price: {avg_price:.4f}\n")
    result_text.insert(tk.END, f"Min float chọn: {min_val}\n")
    result_text.insert(tk.END, f"Max float chọn: {max_val}\n")
    result_text.insert(tk.END, f"Max output value nhập: {max_output_val}\n")

# ==== UI Setup ====
root = tk.Tk()
root.title("Tính trung bình Float & Price")
root.geometry("1150x500")

# ===== Float entries =====
tk.Label(root, text="Float Values:").grid(row=0, column=0, sticky="w", padx=5)
float_entries = []
for i in range(10):
    entry = tk.Entry(root, width=10)
    entry.grid(row=0, column=i+1, padx=3)
    float_entries.append(entry)

# ===== Price entries =====
tk.Label(root, text="Price Values:").grid(row=1, column=0, sticky="w", padx=5)
price_entries = []
for i in range(10):
    entry = tk.Entry(root, width=10)
    entry.grid(row=1, column=i+1, padx=3)
    price_entries.append(entry)

# ===== Min val =====
tk.Label(root, text="Min Float Value:").grid(row=2, column=0, sticky="w", pady=10, padx=5)
min_val_var = tk.StringVar(value="0")
for i, val in enumerate(["0", "0.02", "0.06"]):
    tk.Radiobutton(root, text=val, variable=min_val_var, value=val).grid(row=2, column=i+1, sticky="w")

# ===== Max val =====
tk.Label(root, text="Max Float Value:").grid(row=3, column=0, sticky="w", pady=10, padx=5)
max_val_var = tk.StringVar(value="1")
for i, val in enumerate(["0.8", "0.9", "1"]):
    tk.Radiobutton(root, text=val, variable=max_val_var, value=val).grid(row=3, column=i+1, sticky="w")

# ===== Max output val entry =====
tk.Label(root, text="Max Output Value:").grid(row=4, column=0, sticky="w", pady=10, padx=5)
max_output_entry = tk.Entry(root, width=10)
max_output_entry.grid(row=4, column=1)

# ===== Button =====
calc_button = tk.Button(root, text="Tính trung bình", command=calculate_average)
calc_button.grid(row=5, column=0, columnspan=5, pady=10)

# ===== Kết quả Text box =====
result_text = tk.Text(root, height=8, width=100)
result_text.grid(row=6, column=0, columnspan=12, padx=10, pady=10)

root.mainloop()
