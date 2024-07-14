import tkinter as tk
from tkinter import Canvas
import serial
import time

# Replace 'COM3' with the appropriate COM port for Arduino and 'COM4' for 3D printer
arduino_port = 'COM12'
printer_port = 'COM11'
baud_rate = 115200

# Establish serial connection to Arduino
try:
    arduino_ser = serial.Serial(arduino_port, baud_rate, timeout=2)
    print("Arduino OK")
except serial.SerialException as e:
    print(f"Failed to connect to Arduino: {e}")
    arduino_ser = None

# Establish serial connection to 3D printer
try:
    printer_ser = serial.Serial(printer_port, baud_rate, timeout=2)
    print("3D Printer OK")
except serial.SerialException as e:
    print(f"Failed to connect to 3D Printer: {e}")
    printer_ser = None

# Global variables to store previous coordinates
prev_x, prev_y = None, None
pointer = None

# Constants for canvas size and scaling factor
CANVAS_MARGIN = 20
MAX_COORD = 200
canvas_width, canvas_height = MAX_COORD + CANVAS_MARGIN * 2, MAX_COORD + CANVAS_MARGIN * 2
scaling_factor = 1.0

# Function to initialize the main window
def init_window():
    global root, canvas, coord_label_x, coord_label_y, coord_label_z, scaling_factor

    root = tk.Tk()
    root.title("Drawing App")
    
    # Maximize window
    root.state('zoomed')  # For Windows
    # For other platforms, use: root.attributes('-fullscreen', True)
    
    # Create and pack the left frame for buttons
    left_frame = tk.Frame(root, width=200)
    left_frame.pack(side=tk.LEFT, fill=tk.Y)
    
    # Create and pack the plotter frame for the canvas
    plotter_frame = tk.Frame(root, bd=2, relief=tk.SOLID)  # Added border
    plotter_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Create and pack the right frame for coordinate display
    coord_frame = tk.Frame(root, width=200)
    coord_frame.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Add buttons to the left frame
    button_font = ("Arial", 18)
    home_button = tk.Button(left_frame, text="Home", command=home, font=button_font)
    home_button.pack(padx=20, pady=20)
    
    game_mode_button = tk.Button(left_frame, text="Game Mode", command=game_mode, font=button_font)
    game_mode_button.pack(padx=20, pady=20)

    clean_canvas_button = tk.Button(left_frame, text="Clean", command=clean_canvas, font=button_font)
    clean_canvas_button.pack(padx=20, pady=20)

    close_button = tk.Button(left_frame, text="Close", command=close_program, font=button_font)
    close_button.pack(padx=20, pady=20)
    
    # Create and pack the canvas (whiteboard) in the plotter frame
    canvas = Canvas(plotter_frame, bg="white")
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.bind("<Configure>", resize_canvas)
    
    # Create and pack the coordinate display labels in the right frame
    coord_label_font = ("Courier", 18)  # Use a monospace font
    coord_label_width = 10  # Set a fixed width to accommodate three digits
    coord_label_x = tk.Label(coord_frame, text="X: 000", font=coord_label_font, anchor="w", width=coord_label_width)
    coord_label_x.pack(pady=5, padx=20, anchor="w")

    coord_label_y = tk.Label(coord_frame, text="Y: 000", font=coord_label_font, anchor="w", width=coord_label_width)
    coord_label_y.pack(pady=5, padx=20, anchor="w")

    coord_label_z = tk.Label(coord_frame, text="Z: 000", font=coord_label_font, anchor="w", width=coord_label_width)
    coord_label_z.pack(pady=5, padx=20, anchor="w")

    # Update scaling factor based on the initial canvas size
    canvas.update_idletasks()  # Ensure canvas is updated to its final size
    resize_canvas(None)

# Function for Home button functionality
def home():
    global canvas
    # Change the background color of the canvas
    send_gcode(f"G28\n",printer_ser)

# Placeholder function for Game Mode button functionality
def game_mode():
    send_gcode(f"G01 Z5 F5000\n", printer_ser)
    send_gcode(f"G01 X0 Y65\n", printer_ser)
    #send_gcode(f"G01 Z0\n", printer_ser)
    send_gcode(f"G01 X200 Y65\n", printer_ser)
    canvas.create_line(0* scaling_factor + CANVAS_MARGIN, (MAX_COORD - 65) * scaling_factor + CANVAS_MARGIN, 200* scaling_factor + CANVAS_MARGIN, (MAX_COORD -65) * scaling_factor + CANVAS_MARGIN, fill="black", width=2)
    #send_gcode(f"G01 Z2\n", printer_ser)
    send_gcode(f"G01 X200 Y130\n", printer_ser)
    #send_gcode(f"G01 Z0\n", printer_ser)
    send_gcode(f"G01 X0 Y130\n", printer_ser)
    canvas.create_line(200* scaling_factor + CANVAS_MARGIN, (MAX_COORD - 130) * scaling_factor + CANVAS_MARGIN, 0* scaling_factor + CANVAS_MARGIN, (MAX_COORD - 130) * scaling_factor + CANVAS_MARGIN, fill="black", width=2)
    #send_gcode(f"G01 Z2\n", printer_ser)
    send_gcode(f"G01 X65 Y0\n", printer_ser)
    #send_gcode(f"G01 Z0\n", printer_ser)
    send_gcode(f"G01 X65 Y200\n", printer_ser)
    canvas.create_line(65* scaling_factor + CANVAS_MARGIN, (MAX_COORD - 0) * scaling_factor + CANVAS_MARGIN, 65* scaling_factor + CANVAS_MARGIN, (MAX_COORD - 200) * scaling_factor + CANVAS_MARGIN, fill="black", width=2)
    #send_gcode(f"G01 Z2\n", printer_ser)
    send_gcode(f"G01 X130 Y200\n", printer_ser)
    #send_gcode(f"G01 Z0\n", printer_ser)
    send_gcode(f"G01 X130 Y0\n", printer_ser)
    canvas.create_line(130* scaling_factor + CANVAS_MARGIN, (MAX_COORD - 200) * scaling_factor + CANVAS_MARGIN, 130* scaling_factor + CANVAS_MARGIN, (MAX_COORD - 0) * scaling_factor + CANVAS_MARGIN, fill="black", width=2)
    #send_gcode(f"G01 Z2 \n", printer_ser)
    send_gcode(f"G02 X200 Y200 \n", printer_ser)



def clean_canvas():
    global canvas
    send_gcode(f"G01 Z10\n", printer_ser)
    send_gcode(f"G28 X Y\n", printer_ser)
    canvas.delete("all")

# Function to close the program
def close_program():
    global root
    root.destroy()

# Function to decode Arduino data
def decoder(arduino_data):
    # Split the data by commas
    parts = arduino_data.split(',')
    
    # Assign coordinates
    x = int(parts[0].strip())
    y = int(parts[1].strip())
    z = int(parts[2].strip())
    
    return x, y, z

# Function to send a G-code command and receive the response
def send_gcode(command, printer):
    printer.write(command.encode())
    time.sleep(0.5)  # Give the printer some time to process the command
    response = printer.readline().decode().strip()
    return response

# Function to handle canvas resizing
def resize_canvas(event):
    global canvas_width, canvas_height, scaling_factor, canvas
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    scaling_factor = min(canvas_width, canvas_height) / (MAX_COORD + CANVAS_MARGIN * 2)
    print(f"Canvas resized: width={canvas_width}, height={canvas_height}, scaling_factor={scaling_factor}")

# Function to draw on the canvas using decoded coordinates
def draw(x, y, z):
    global canvas, prev_x, prev_y, scaling_factor, pointer
    # Adjust coordinates for canvas size and scaling
    adjusted_x = x * scaling_factor + CANVAS_MARGIN
    adjusted_y = (MAX_COORD - y) * scaling_factor + CANVAS_MARGIN  # Inverting y-axis for bottom-left origin
    # Draw a line from the previous coordinates to the current coordinates with a thicker line
    if prev_x is not None and prev_y is not None:
        canvas.create_line(prev_x, prev_y, adjusted_x, adjusted_y, fill="black", width=2)
    # Update previous coordinates
    prev_x, prev_y = adjusted_x, adjusted_y
    # Update pointer position
    if pointer:
        canvas.delete(pointer)
    pointer = canvas.create_oval(adjusted_x - 2, adjusted_y - 2, adjusted_x + 2, adjusted_y + 2, outline="red", fill="red")
    # Update coordinates display
    show_coordinates(x, y, z)

# Function to display coordinates on the label
def show_coordinates(x, y, z):
    global coord_label_x, coord_label_y, coord_label_z
    # Update the coordinate labels with the current coordinates
    coord_label_x.config(text=f"X: {x:03d}")
    coord_label_y.config(text=f"Y: {y:03d}")
    coord_label_z.config(text=f"Z: {z:03d}")

# Function to read from Arduino and update the GUI
def update_data():
    global arduino_ser

    if arduino_ser is not None and arduino_ser.is_open:
        try:
            # Ask for information
            arduino_ser.write(b'T')
            print("Requesting data from Arduino...")

            # Read a line of data from the Arduino
            arduino_data = arduino_ser.readline().decode('utf-8').strip()
            
            if arduino_data:
                print(f'Received from Arduino: {arduino_data}')
                    
                try:
                    x, y, z = decoder(arduino_data)
                    draw(x, y, z)
                    send_gcode(f"G01 X{x} Y{y} Z{z}\n", printer_ser)
                    print(f"Parsed coordinates: X={x}, Y={y}, Z={z}")
                        
                except ValueError as e:
                    print(f"Error parsing coordinates: {e}")
                    
            else:
                print("No data received from Arduino.")
                        
        except serial.SerialException as e:
            print(f'Serial error: {e}')
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    # Schedule the next call to this function
    root.after(100, update_data)  # Adjust the delay as needed

# Main entry point for the application
if __name__ == "__main__":
    # Initialize the main window and components
    init_window()
    
    send_gcode(f"G28\n", printer_ser)

    # Start the periodic data update
    root.after(1000, update_data)
    
    # Run the application main loop
    root.mainloop()
