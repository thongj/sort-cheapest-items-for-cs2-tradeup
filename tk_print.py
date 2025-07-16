import tkinter as tk
import time
class App:
    def __init__(self, root):
        self.root = root
        self.text = tk.Text(root, height=10, width=40)
        self.text.pack()

        self.running = False
        self.counter = 0

        tk.Button(root, text="Bắt đầu", command=self.start_loop).pack()
        tk.Button(root, text="Dừng", command=self.stop_loop).pack()

    def start_loop(self):
        if not self.running:
            self.running = True
            self.counter = 0
            self.loop()

    def stop_loop(self):
        self.running = False

    def loop(self):
        if self.running and self.counter < 1000000:
            self.text.insert(tk.END, f"{self.counter}\n")
            self.counter += 1
            time.sleep(500)
            self.root.after(1, self.loop)  # gọi lại sau 1ms

root = tk.Tk()
App(root)
root.mainloop()
