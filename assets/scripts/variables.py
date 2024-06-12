import tkinter as tk
from tkinter import font

with open('assets/data/winfo.txt') as f:
    string = f.read().splitlines()

with open('assets/data/font.txt') as f:
    string_1 = f.read().splitlines()

with open('assets/data/docinfo.txt') as f:
    string_2 = f.read().splitlines()

with open('assets/data/int.txt') as f:
    string_3 = f.read().splitlines()

doc_info = [int(string_2[0]), int(string_2[1])]
interface = [int(string_3[0]), int(string_3[1]), int(string_3[2])]

theme = open('assets/data/theme.txt', 'r').read()

width = int(string[0])
height = int(string[1])

active_font = [string_1[0], int(string_1[1])]
QFont = None

root = tk.Tk()

x = int((root.winfo_screenwidth() / 2) - (width / 2))
y = int(((root.winfo_screenheight() - 120) / 2) - (height / 2))

fonts = font.families()
num = len(fonts)
index = fonts.index(active_font[0])
file_loc = []
for i in range(0, 10000):
    file_loc.append('')

tab_number = 0
tab_count = 1

app = None
main_window = None
