import tkinter as tk

root = tk.Tk()
root.geometry("600x400")
root.resizable(False, False)


def start(count=0):
    if count < 11:
        lab.config(text=count)
        root.after(1000, start, count + 1)


button = tk.Button(root, text='Go', command=lambda: start())
button.pack()

lab = tk.Label(root, text='Not Start')
lab.pack()

root.mainloop()
