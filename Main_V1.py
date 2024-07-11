# Adicionar plotter virtual;
# Adicionar modo jogo do galo
# Meter o código bonitinho


import serial
import time

# Replace 'COM3' with the appropriate COM port for Arduino and 'COM4' for 3D printer
arduino_port = 'COM12'
printer_port = 'COM10'
baud_rate = 115200

# Establish serial connection to Arduino
arduino_ser = serial.Serial(arduino_port, baud_rate, timeout=2)
print("Arduino OK")

# Establish serial connection to 3D printer
printer_ser = serial.Serial(printer_port, baud_rate,timeout=2)
print("Printer OK")

# Ligar steppers
gcode1 = f"M17 \n"
printer_ser.write(gcode1.encode())
print("M17 Sent")

# Sistema de coordenadas absoluto
gcode1 = f"G90 \n"
printer_ser.write(gcode1.encode())
print("G90 Sent")

#Homing a todos os eixos
gcode2 = f"G28 \n"
printer_ser.write(gcode2.encode())
print("G28 Sent")

#Definir feedrate
gcode3 = f"G01 X0 F1000 \n"
printer_ser.write(gcode3.encode())
print("feedrate set")

user_input = input("Press Enter to continue or Space to perform another action...")

# Function to send a G-code command and receive the response
def send_gcode(command, printer):
    printer.write(command.encode())
    time.sleep(0.5)  # Give the printer some time to process the command
    response = printer.readline().decode().strip()
    return response

if user_input == '':
    x = 0
    y = 0
    z = 0

    x_old = x
    y_old = y
    z_old = z

    # Traduzir a info recebida do arduino
    def decoder(arduino_data):
        # Dividir pelas vírgulas
        parts = arduino_data.split(',')

        # Atribuir coordenadas
        x = int(parts[0].strip())
        y = int(parts[1].strip())
        z = int(parts[2].strip())

        return x, y, z

    try:
        while True:
            #Ask for information
            arduino_ser.write(b'T')
            print('pi')


            # Read a line of data from the Arduino
            arduino_data = arduino_ser.readline().decode('utf-8').strip()

            
            if arduino_data:
                print(f'Received from Arduino: {arduino_data}')
                
                try:
                    x, y, z = decoder(arduino_data)
                    print(f"Parsed coordinates: X={x}, Y={y}, Z={z}")
                    
                    # Verificar se algo mudou
                    if not x == x_old or not y == y_old or not z == z_old:
                        send_gcode(f"G01 X{x} Y{y} Z{z} F5000\n",printer_ser)
                        x_old = x
                        y_old = y
                        z_old = z
                        time.sleep(0.1)
                    
                except ValueError as e:
                    print(f"Error parsing coordinates: {e}")
            
            time.sleep(0.1)  # Adjust the delay as needed
            
    except serial.SerialException as e:
        print(f'Serial error: {e}')
    except KeyboardInterrupt:
        print("Program stopped by User")
    finally:
        printer_ser.close()

elif user_input == ' ':
    
    send_gcode(f"G01 Z2 F5000\n", printer_ser)
    send_gcode(f"G01 X10 Y10 Z0\n", printer_ser)
    send_gcode(f"G02 X10 Y10 I0 J5\n", printer_ser)
    send_gcode(f"G01 Z2\n", printer_ser)
    send_gcode(f"G01 X20 Y10 Z0\n", printer_ser)
    send_gcode(f"G02 X20 Y10 I0 J5\n", printer_ser)
    send_gcode(f"G01 Z5\n", printer_ser)
    send_gcode(f"G01 X10 Y20 Z0\n", printer_ser)
    send_gcode(f"G01 Y40 \n", printer_ser)
    send_gcode(f"G02 X20 Y40 I5 J0\n", printer_ser)
    send_gcode(f"G01 Y20 \n", printer_ser)
    