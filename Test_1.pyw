import tkinter as tk
import start

"""
先创建400x500的初始窗口
"""

game_mode = 1

root = tk.Tk()
root.geometry('247x287')
a = start.Application(root)
root.mainloop()
