import tkinter as tk
from tkinter import messagebox
import time

def calculate_x():
    try:
        # Lấy giá trị f_min và f_max
        f_min = float(f_min_entry.get())
        f_max = float(f_max_entry.get())
        
        # Lấy giá trị các item
        items = []
        for entry in item_entries:
            items.append(float(entry.get()))
        
        # Tính toán kết quả
        sum_items = sum(items)
        x = ((sum_items * (f_max - f_min)) / 10) + f_min
        
        # Hiển thị kết quả
        #result_label.config(text=f"Kết quả X = {x:.12f}")
        for i in range(10):
            result_label.config(text=f"{i}")
            time.sleep(1)
        
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ vào tất cả các ô")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Tính toán giá trị X")
root.geometry("400x500")

# Tạo frame chứa các ô nhập f_min và f_max
f_frame = tk.Frame(root)
f_frame.pack(pady=10)

tk.Label(f_frame, text="f_min:").pack(side=tk.LEFT)
f_min_entry = tk.Entry(f_frame, width=10)
f_min_entry.pack(side=tk.LEFT, padx=5)

tk.Label(f_frame, text="f_max:").pack(side=tk.LEFT)
f_max_entry = tk.Entry(f_frame, width=10)
f_max_entry.pack(side=tk.LEFT, padx=5)

# Tạo frame chứa các ô nhập item0 đến item9
items_frame = tk.Frame(root)
items_frame.pack(pady=10)

item_entries = []
for i in range(10):
    frame = tk.Frame(items_frame)
    frame.pack()
    tk.Label(frame, text=f"item{i}:").pack(side=tk.LEFT)
    entry = tk.Entry(frame, width=10)
    entry.pack(side=tk.LEFT, padx=5)
    item_entries.append(entry)

# Nút tính toán
calculate_button = tk.Button(root, text="Tính X", command=calculate_x)
calculate_button.pack(pady=10)

# Hiển thị kết quả
result_label = tk.Label(root, text="Kết quả X = ", font=('Arial', 12))
result_label.pack(pady=10)

# Chạy ứng dụng
root.mainloop()