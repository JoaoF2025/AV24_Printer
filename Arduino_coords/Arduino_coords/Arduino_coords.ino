/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/AnalogReadSerial
*/
int x = A0;
int y = A1;
int z = A2;

int x_val;
int y_val;
int z_val;

char command;

int print_max_x = 200;
int print_max_y = 200;
int print_max_z = 100;

String Output;


// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);
}

// the loop routine runs over and over again forever:
void loop() {

  if (Serial.available() > 0) {
    command = Serial.read();
   // if (command == 'T') {
      x_val = map(analogRead(A0), 0, 1023, 0, print_max_x);
      y_val = map(analogRead(A1), 0, 1023, 0, print_max_y);
      z_val = map(analogRead(A2), 0, 1023, 0, print_max_z);

      // Output
      Output = String(x_val) + "," + String(y_val) + "," + String(z_val);
      Serial.println(Output);
    
 //   }
  }
}
