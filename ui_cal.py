import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
import itertools
import math
import time
import os
import keyboard

def filter_wrong_price_item(list_items):
    cleaned_list = [
    {"price": float(item["price"]), "float": float(item["float"])}
    for item in list_items
    ]

    fn_min_price = float('inf')
    mw_min_price = float('inf')
    ft_min_price = float('inf')
    ww_min_price = float('inf')
    bs_min_price = float('inf')
     
    for item in cleaned_list:
        if item['float'] <= 0.07:
            if item['price'] < fn_min_price:
                fn_min_price = item['price']
        elif item['float'] <= 0.15 :
            if item['price'] < mw_min_price:
                mw_min_price = item['price']
        elif item['float'] <= 0.38 :
            if item['price'] < ft_min_price:
                ft_min_price = item['price'] 
        elif item['float'] <= 0.45 :
            if item['price'] < ww_min_price:
                ww_min_price = item['price'] 
        elif item['price'] < bs_min_price:
            bs_min_price = item['price'] 
    filter_list_items=[]
    for item in cleaned_list:
        if item['float'] > 0.45:
            if item['price'] <= ww_min_price:
                filter_list_items.append(item)
        elif item['float'] > 0.38 :
            if item['price'] <= ft_min_price:
                filter_list_items.append(item)
        elif item['float'] > 0.15 :
            if item['price'] <= mw_min_price:
                filter_list_items.append(item)
        elif item['float'] > 0.07 :
            if item['price'] <= fn_min_price:
                filter_list_items.append(item)
        else:
            filter_list_items.append(item)

    return filter_list_items


    


def read_data(input_data):
    if os.path.isfile(input_data):
        with open(input_data, "r", encoding="utf-8") as file:
            html_content = file.read()
    else:
        html_content = input_data
    soup = BeautifulSoup(html_content, "html.parser")
    results = []
    
    for parent_div in soup.find_all("div"):
        price_div = parent_div.find("div", class_="price ng-star-inserted")
        float_div = parent_div.find("div", class_="mat-mdc-tooltip-trigger wear")
        if price_div and float_div:
            #price_text = price_div.get_text(strip=True).replace('$', '')
            price_text = price_div.get_text(strip=True).replace('€', '')
            float_text = float_div.get_text(strip=True)
            # Kiểm tra nếu price là số
            try:
                float(price_text)  # Nếu lỗi sẽ bị except
                results.append({
                    "price": price_text,
                    "float": float_text
                })
            except ValueError:
                pass  # Bỏ qua các giá trị không phải là số
    # Loại bỏ các dict trùng nhau
    unique_results = [dict(t) for t in {tuple(d.items()) for d in results}]
    # In kết quả
    #for item in unique_results:
    #    print(item)
    return unique_results
    
def find_best_combination_v2(float_list, f_min, f_max, input_item_list, max_output_float, item_look_for):
    sum_items = ((max_output_float - f_min)*10)/(f_max - f_min)
    
    #Làm sạch dữ liệu (chuyển sang số thực)
    cleaned_list = [
        {"price": float(item["price"]), "float": float(item["float"])}
        for item in float_list
    ]
    
    def _find_best_item(cleaned_list, aver_item_list, sum_items, item_look_for):
        print("find best item for item_look_for: ", item_look_for)    
        min_price = float('inf')
        best_items = []
        found_combo = []
        best_item = {}
        i=0
        total_cal = math.comb(len(cleaned_list), item_look_for)
        if item_look_for == 1:
            #print(f"Calculate C({len(cleaned_list)},{lookfor_item_count})")
            for combo in itertools.combinations(cleaned_list, item_look_for):
                #print(combo)
                float_sum =  sum(aver_item_list) + combo[0]['float']
                
                if float_sum <= sum_items:       
                    if combo[0]['price'] < min_price:
                        min_price = combo[0]['price']
                        best_item = combo[0]
                if best_item:
                    print(f"\r{i}/{total_cal}", end='')
                    #print(f"\r{i}/{total_cal} -> {round(min_price,2)} {best_item['float']}", end='')
                i+=1
            best_items.append(best_item)
            if not best_item:
                raise ValueError("❌ Không tìm thấy item nào phù hợp.")
            return best_items
        else:
            #print(f"Calculate C({len(cleaned_list)},{lookfor_item_count})")
            for combo in itertools.combinations(cleaned_list, item_look_for):

                float_sum =  sum(aver_item_list) + sum(item['float'] for item in combo)
                if float_sum <= sum_items:       
                    if sum(item['price'] for item in combo) < min_price:
                        min_price = sum(item['price'] for item in combo)
                        found_combo = combo        
                if found_combo:
                    c = [combo['float'] for combo in found_combo]
                    #print(f"\r{i}/{total_cal} -> {round(min_price,2)} {c}", end='')
                    print(f"\r{i}/{total_cal}", end='')
                i+=1
            for item in found_combo:
                best_items.append(item)
            if not best_items:
                raise ValueError("❌ Không tìm thấy item nào phù hợp.")
            return best_items

    average_float = (sum_items - sum(i for i in input_item_list))/(10 - len(input_item_list))
    best_combo = []
    
    while (10 - len(input_item_list) - len(best_combo)):
        lookfor_item_count = 10 - len(input_item_list) - len(best_combo)
        
        aver_item_list = input_item_list.copy()
        
        if len(best_combo):
            
            for item in best_combo:
                
                aver_item_list.append(item['float'])
        #print(aver_item_list)
        for b in range(10 - item_look_for - len(input_item_list) - len(best_combo)):
            aver_item_list.append(average_float)          
        #print(aver_item_list)
        if item_look_for <= lookfor_item_count:
            best_items = _find_best_item(cleaned_list, aver_item_list, sum_items, item_look_for)
        else:
            best_items = _find_best_item(cleaned_list, aver_item_list, sum_items, lookfor_item_count)
        for item in best_items:
            best_combo.append(item)
        cleaned_list = [item for item in cleaned_list if item not in best_combo]
        
        
    min_total_price = sum(combo['price'] for combo in best_combo)
    return  min_total_price, best_combo


#--------------------------------------------------------------------------------------------------
def find_best_combination_under_output(float_list, f_min, f_max, input_item_list, max_output_float):
    
    sum_items = ((max_output_float - f_min)*10)/(f_max - f_min)
    min_total_price = float('inf')
    best_combo = None
    lookfor_item_count = 10 - len(input_item_list)

    #Làm sạch dữ liệu (chuyển sang số thực)
    cleaned_list = [
        {"price": float(item["price"]), "float": float(item["float"])}
        for item in float_list
    ]
    i=0
    result = math.comb(len(cleaned_list), lookfor_item_count)
    print(f"Calculate C({len(cleaned_list)},{lookfor_item_count})")
    for combo in itertools.combinations(cleaned_list, lookfor_item_count):
        float_sum = sum(item["float"] for item in combo) + sum(item for item in input_item_list)

        if float_sum <= sum_items:
            total_price = sum(item["price"] for item in combo)          
            if total_price < min_total_price:
                min_total_price = total_price
                best_combo = combo
        if best_combo:
            c = [combo['float'] for combo in best_combo]
            print(f"\r{i}/{result} -> {round(min_total_price,2)} {c}", end='')
        
        i+=1
    return  min_total_price, best_combo
# ====================================================================================================



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

    #avg_float = sum(float_vals) / len(float_vals) if float_vals else 0
    #avg_price = sum(price_vals) / len(price_vals) if price_vals else 0

    min_val = float(min_val_var.get())
    max_val = float(max_val_var.get())
    max_output_val = float(max_output_entry.get())
    items_input_data = data_text.get()

    # In kết quả ra khung Text
    result_text.delete(1.0, tk.END)
    #result_text.insert(tk.END, f"Số lượng float nhập: {len(float_vals)}\n")



    ########################################################################

    input_item_list = float_vals #[0.07348132878542]
    input_item_list_price = price_vals #[0]
    max_output_float = max_output_val  #0.07
    f_min = min_val
    f_max = max_val
    #f_min = 0
    #f_min = 0.06
    #f_max = 0.8
    #f_max = 0.9
    #f_max = 1

    average_input_item_float = sum(item for item in input_item_list) / len(input_item_list) if input_item_list else 0
    sum_items = ((max_output_float - f_min)*10)/(f_max - f_min)
    if average_input_item_float > sum_items:
        print(input_item_list)
        raise ValueError(f"❌ input item float is so high, it should be less than: {sum_items}")
        
    
    
    float_list = read_data(items_input_data)
    #float_list = read_data('data.html')
    #for item in float_list:
    #    print(item)
    print("--->", float_list[0])
    
       
    
    float_list1 =[
    {'price': 1.46, 'float': 0.002061226172},
    {'price': 1.43, 'float': 0.002645419678},
    {'price': 1.45, 'float': 0.001405477757},
    {'price': 1.8, 'float': 0.001840411685},
    {'price': 1.94, 'float': 0.001097303815},
    {'price': 1.45, 'float': 0.002576614264},
    {'price': 1.44, 'float': 0.002686206717},
    {'price': 1.81, 'float': 0.001371751656},
    {'price': 1.7, 'float': 0.002176133916},
    {'price': 0.8, 'float': 0.003645419678},
    {'price': 1.6, 'float': 0.000345419678},
    ]
    
    

    filtered_items = float_list
    print("Data: ", len(filtered_items)," items")
    
    #max_price = 1.5
    #max_filter_float = (((max_output_val * 10)-input_val)/9) * 1.5
    #print("max_filter_float: ", max_filter_float)
    #filtered_items = [
    #    item for item in float_list 
    #    if float(item['price']) <= max_price and float(item['float']) <= max_filter_float
    #]
    
    final_items = filter_wrong_price_item(filtered_items)
    
    print("After filter: ",len(final_items)," items")

    for t in range(1,10 - len(input_item_list)):
        start_time = time.time()
        #best_price, best_combo  = find_best_combination_under_output(filtered_items, f_min, f_max, input_item_list, max_output_float)
        best_price, best_combo  = find_best_combination_v2(filtered_items, f_min, f_max, input_item_list, max_output_float, t)

        if best_combo:
            
            best_combo = sorted(best_combo, key=lambda x: (x['price'], x['float']))
            print()
            print("✅ Best found with total price:", round(best_price+sum(i for i in input_item_list_price), 2))
            print("Resulting output_val:", round((((sum(i for i in input_item_list) + sum(i["float"] for i in best_combo)) * (f_max - f_min)) / 10) + f_min,12))
            
            #result_text.insert(tk.END, f"finding combo for {t}\n")
            #result_text.insert(tk.END, f"✅ Best found with total price: , {round(best_price+sum(i for i in input_item_list_price), 2)}\n")
            #result_text.insert(tk.END, f"Resulting output_val:, {round((((sum(i for i in input_item_list) + sum(i['float'] for i in best_combo)) * (f_max - f_min)) / 10) + f_min,12)}\n")


            for item in best_combo:
                print(item)
                #result_text.insert(tk.END, f"{item}\n")
        else:
            print("❌ Không tìm được tổ hợp phù hợp.")
            #result_text.insert(tk.END, f"❌ Không tìm được tổ hợp phù hợp.\n")
        
        
        end_time = time.time()

        # Tính thời gian chạy (giây)
        execution_time = end_time - start_time
        print(f"Thời gian chạy: {execution_time:.4f} giây")
        print()
        #result_text.insert(tk.END, f"Thời gian chạy: {execution_time:.4f} giây\n")
        #result_text.insert(tk.END, f"\n")

# ==== UI Setup ====
root = tk.Tk()
root.title("Tính trung bình Float & Price")
root.geometry("1200x800")

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
min_val_var = tk.StringVar(value="0.06")
for i, val in enumerate(["0", "0.02", "0.06"]):
    tk.Radiobutton(root, text=val, variable=min_val_var, value=val).grid(row=2, column=i+1, sticky="w")

# ===== Max val =====
tk.Label(root, text="Max Float Value:").grid(row=3, column=0, sticky="w", pady=10, padx=5)
max_val_var = tk.StringVar(value="0.8")
for i, val in enumerate(["0.8", "0.9", "1"]):
    tk.Radiobutton(root, text=val, variable=max_val_var, value=val).grid(row=3, column=i+1, sticky="w")

# ===== Max output val entry =====
tk.Label(root, text="Max Output Value:").grid(row=4, column=0, sticky="w", pady=10, padx=5)
max_output_entry = tk.StringVar(value="0.07")
for i, val in enumerate(["0.07", "0.15", "0.38"]):
    tk.Radiobutton(root, text=val, variable=max_output_entry, value=val).grid(row=4, column=i+1, sticky="w")

# ===== Button =====
calc_button = tk.Button(root, text="Calculate", command=calculate_average)
calc_button.grid(row=5, column=0, columnspan=5, pady=10)


# ===== Kết quả Text box =====
result_text = tk.Text(root, height= 5, width=100)
result_text.grid(row=6, column=0, columnspan=12, padx=10, pady=10, sticky="w")

# ===== data box =====
tk.Label(root, text="path or html data:").grid(row=7, column=0, sticky="w", padx=5)
data_text = tk.Entry(root, width=100)
data_text.grid(row=8, column=0, columnspan=12, padx=10, pady=10, sticky="w")


root.mainloop()
