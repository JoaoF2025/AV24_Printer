import serial
import time

# Replace 'COM3' with the appropriate COM port for Arduino and 'COM4' for 3D printer
arduino_port = 'COM12'
printer_port = 'COM13'
baud_rate = 115200

# Establish serial connection to Arduino
arduino_ser = serial.Serial(arduino_port, baud_rate, timeout=2)
print("Arduino OK")

# Establish serial connection to 3D printer
printer_ser = serial.Serial(printer_port, baud_rate,timeout=2)
print("Printer OK")


gcode1 = f"M17 \n"
printer_ser.write(gcode1.encode())
print("M17 Sent")

gcode1 = f"G91 \n"
printer_ser.write(gcode1.encode())
print("G91 Sent")

gcode2 = f"G28 \n"
printer_ser.write(gcode2.encode())
print("G28 Sent")

gcode3 = f"G01 Z50 \n"
printer_ser.write(gcode3.encode())
print("G28 Sent")

gcode3 = f"G01 X50 Y50 Z70 \n"
printer_ser.write(gcode3.encode())
print("G28 Sent")


# Function to send a G-code command and receive the response
def send_gcode(command, printer):
    printer.write(command.encode())
    time.sleep(0.2)  # Give the printer some time to process the command
    response = printer.readline().decode().strip()
    return response
