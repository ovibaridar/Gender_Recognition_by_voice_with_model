import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("600x400")
root.resizable(False, False)

# Initialize a variable to track the current theme
current_theme = "forest-dark"
font = ("Times New Roman CE", 10)

# Variable to track whether an image is displayed in frame2
image_displayed = False


def toggle():
    global current_theme
    if current_theme == "forest-dark":
        if "forest-light" not in style.theme_names():
            root.tk.call('source', 'forest-light.tcl')
        style.theme_use('forest-light')
        current_theme = "forest-light"
    else:
        style.theme_use('forest-dark')
        current_theme = "forest-dark"


def start(count=0):
    lab1.config(text='Recording Start...')
    if count < 11:
        lab2.config(text=count)
        root.after(1000, start, count + 1)


style = ttk.Style(root)
if "forest-dark" not in style.theme_names():
    root.tk.call('source', 'forest-dark.tcl')
style.theme_use('forest-dark')

frame1 = ttk.Frame(root, height=400, width=600)
frame1.pack()
mode = ttk.Checkbutton(frame1, style="Switch", command=toggle)
mode.place(x=550, y=10)

button_create = ttk.Button(text='Check', width=15, command=start)
button_create.place(x=140, y=130)

frame2 = ttk.Frame(frame1, height=200, width=200, relief="groove", borderwidth=2)
frame2.propagate(0)
frame2.place(x=380, y=80)

lab1 = ttk.Label(frame2, text='')
lab1.pack()

lab2 = ttk.Label(frame2, text='')
lab2.place(x=100, y=100)

root.mainloop()
