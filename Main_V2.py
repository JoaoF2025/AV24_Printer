import serial
import numpy as np
import time
import tkinter as tk
from tkinter import Canvas

#Printer and Arduino variables

arduino_port = 'COM12'
printer_port = 'COM10'
baud_rate = 115200

# Main application class
class DrawingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Set the title and size of the main window
        self.title("Drawing App")
        self.geometry("800x600")
        
        # Create and pack the left frame for buttons
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Create and pack the plotter frame for the canvas
        self.plotter_frame = tk.Frame(self, bd=2, relief=tk.SOLID)  # Added border
        self.plotter_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create and pack the bottom frame for coordinate display
        self.coord_frame = tk.Frame(self)
        self.coord_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add buttons to the left frame
        self.home_button = tk.Button(self.left_frame, text="Home", command=self.home)
        self.home_button.pack(padx=20, pady=20)
        
        self.free_drawing_button = tk.Button(self.left_frame, text="Free Drawing", command=self.free_drawing)
        self.free_drawing_button.pack(padx=20, pady=20)
        
        self.game_mode_button = tk.Button(self.left_frame, text="Game Mode", command=self.game_mode)
        self.game_mode_button.pack(padx=20, pady=20)
        
        # Create and pack the canvas (whiteboard) in the plotter frame
        self.canvas = Canvas(self.plotter_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind mouse motion events to canvas for drawing and coordinate display
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Motion>", self.show_coordinates)
        
        # Create and pack the coordinate display label in the bottom frame
        self.coord_label = tk.Label(self.coord_frame, text="XYZ Coordinates: (X: 0, Y: 0)")
        self.coord_label.pack(pady=5)
        
    # Placeholder method for Home button functionality
    def home(self):
        pass
    
    # Placeholder method for Free Drawing button functionality
    def free_drawing(self):
        pass
    
    # Placeholder method for Game Mode button functionality
    def game_mode(self):
        pass
    
    # Method to draw on the canvas
    def draw(self, event):
        # Get the current mouse coordinates, adjusting for bottom-left origin
        x, y = event.x, self.canvas.winfo_height() - event.y
        # Draw a small oval (circle) at the mouse coordinates
        self.canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, fill="black")
        
    # Method to display mouse coordinates on the label
    def show_coordinates(self, event):
        # Get the current mouse coordinates, adjusting for bottom-left origin
        x, y = event.x, self.canvas.winfo_height() - event.y
        # Update the coordinate label with the current coordinates
        self.coord_label.config(text=f"XYZ Coordinates: (X: {x}, Y: {y})")
        

# Function to send a G-code command and receive the response
def send_gcode(command, printer):
    printer.write(command.encode())
    time.sleep(0.5)  # Give the printer some time to process the command
    response = printer.readline().decode().strip()
    return response



def main():
    pass
    
    

if __name__ == '__main__':
    main()
        # Create an instance of the DrawingApp class
    app = DrawingApp()
    # Run the application main loop
    app.mainloop()