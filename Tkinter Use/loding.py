import tkinter as tk
from tkinter import ttk

def start_loading():
    # Create a new window for the loading screen
    loading_window = tk.Toplevel(root)
    loading_window.title("Loading...")

    # Add a progress bar to the loading screen
    progress_bar = ttk.Progressbar(loading_window, mode="indeterminate")
    progress_bar.pack(padx=20, pady=20)

    # Start the progress bar animation
    progress_bar.start()

    # Simulate a time-consuming task (you can replace this with your actual task)
    root.after(3000, lambda: stop_loading(loading_window, progress_bar))

def stop_loading(loading_window, progress_bar):
    # Stop the progress bar animation
    progress_bar.stop()

    # Close the loading window
    loading_window.destroy()

# Create the main Tkinter window
root = tk.Tk()
root.title("Tkinter Loading Example")

# Create a button to start the loading screen
start_button = tk.Button(root, text="Start Loading", command=start_loading)
start_button.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()
