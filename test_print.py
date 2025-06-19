import subprocess
import os
import time
import pyautogui

def save_webpage(url):
    # Mở Chrome với URL chỉ định
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Đường dẫn Chrome
    subprocess.Popen([chrome_path, url])
    
    # Chờ trình duyệt mở
    time.sleep(5)
    
    # Thực hiện thao tác bàn phím
    try:
        # Nhấn Ctrl+S để mở dialog lưu
        pyautogui.hotkey('ctrl', 's')
        time.sleep(2)
        
        # Lấy đường dẫn thư mục hiện tại
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Nhập đường dẫn
        pyautogui.write(current_dir)
        time.sleep(2)
        
        # Nhấn Enter để lưu
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write('data.html')
        time.sleep(1)
        pyautogui.press('enter')
        print(f"Đã lưu trang web vào thư mục: {current_dir}")
        
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

# Sử dụng

save_webpage("https://csfloat.com/search?category=2&rarity=3&sort_by=lowest_price&max_float=0.09&collection=set_community_35&max_price=150")