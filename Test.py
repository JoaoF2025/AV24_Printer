import serial
import time

printer_port = 'COM10'
baud_rate = 115200

# Establish serial connection to 3D printer
printer_ser = serial.Serial(printer_port, baud_rate,timeout=2)
print("Printer OK")

# Ligar steppers
gcode1 = f"M17 \n"
printer_ser.write(gcode1.encode())
print("M17 Sent")

# Sistema de coordenadas absoluto
gcode1 = f"G91 \n"
printer_ser.write(gcode1.encode())
print("G91 Sent")

#Homing a todos os eixos
gcode2 = f"G28 X Y\n"
printer_ser.write(gcode2.encode())
print("G28 Sent")

#Definir feedrate
gcode3 = f"G01 X0 F200 \n"
printer_ser.write(gcode3.encode())
print("feedrate set")


# Function to send a G-code command and receive the response
def send_gcode(command, printer):
    printer.write(command.encode())
    time.sleep(0.5)  # Give the printer some time to process the command
    response = printer.readline().decode().strip()
    return response