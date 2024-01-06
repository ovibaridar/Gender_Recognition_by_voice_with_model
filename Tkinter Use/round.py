import tkinter as tk

def on_button_click():
    print("Button clicked!")

# Create the main Tkinter window
root = tk.Tk()
root.title("Round Button Example")

# Set the window size
root.geometry("200x300")

# Create a canvas to draw the round button
canvas = tk.Canvas(root, width=200, height=200, bg='white')
canvas.pack(pady=20)

# Draw the round button on the canvas with a black fill color
button_radius = 80
button_center = (100, 100)
button = canvas.create_oval(button_center[0] - button_radius, button_center[1] - button_radius,
                             button_center[0] + button_radius, button_center[1] + button_radius,
                             fill='white', outline='black')

# Add text to the button
button_text = canvas.create_text(button_center[0], button_center[1], text="Click Me", fill='white', font=('Arial', 12, 'bold'))

# Bind the button click event to a function
canvas.tag_bind(button, '<Button-1>', lambda event: on_button_click())

# Run the Tkinter event loop
root.mainloop()
