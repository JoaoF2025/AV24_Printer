import serial
import time

arduino_port = 'COM12'
baud_rate = 115200


# Establish serial connection to Arduino
arduino_ser = serial.Serial(arduino_port, baud_rate, timeout=2)
print("Arduino OK")

user_input = input("Press Enter to continue or Space to perform another action...")

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


    def coordinates():
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
                        
                    except ValueError as e:
                        print(f"Error parsing coordinates: {e}")
                        
                time.sleep(0.1)  # Adjust the delay as needed


        except serial.SerialException as e:
            print(f'Serial error: {e}')
        except KeyboardInterrupt:
            print("Program stopped by User")


    def main():
        coordinates()

if __name__ == "__main__":
    main()