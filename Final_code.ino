#include <Wire.h> //i2c library

#define TOF10120 0x52 //TOF10120 모듈의 I2C 주소 - A4: blue line, A5: green line
#define VOLTS_PER_UNIT .0049F // (.0049 for 10 bit A-D)

char Sensor = A0; //Connect sensor to A0
int Ic; //Sensor ADC Value Storage Variables
float volts;
float cm;

int laser;
int ultra;
int i;
int sum_laser = 0;
int sum_Ic = 0;
int num1 = 8;
int num2 = 4;
int count = 0;
int lock = 0;
int reset = 0;

void setup() {
  Wire.begin(); //I2C library starts
  Serial.begin(9600); //Debugging Serial Monitol starts
}

void loop() {
  POINT:
  for(i=0;i<num1;i++) {
    laser = ReadDistance();
    sum_laser+=laser;
  }
  for(i=0;i<num2;i++) {
    Ic = analogRead(Sensor); // Store analog values in sensor storage variables
    volts = (float)Ic * VOLTS_PER_UNIT; // Convert analog values in volts
    cm = 60.495 * pow(volts,-1.1904); // Calculation of the distance in cm according to the measured
    sum_Ic+=cm;
  }
  sum_laser/=num1;
  sum_Ic/=(num2+2);
  
  if(((0.1*sum_laser) < sum_Ic) && (sum_laser < 600)) {
    lock --;
    if(lock >= 1) {
      goto POINT;
    }
    while(1) {
      if(sum_laser > 700)
      {
        count = count + 1;
        break;
      }
      sum_laser = ReadDistance();
    }
  }
  else if(((0.1*sum_laser) > sum_Ic) && (sum_Ic < 60)) {
    lock = 10;
    while(1) {
      if(sum_Ic > 70)
      {
        count = count - 1;
        break;
      }
      Ic = analogRead(Sensor); // Store analog values in sensor storage variables
      volts = (float)Ic * VOLTS_PER_UNIT; // Convert analog values in volts
      sum_Ic = 60.495 * pow(volts,-1.1904); // Calculation of the distance in cm according to the measured
    }
  }
  Serial.println(count);
  reset += 1;
  if(reset > 20000) // approximately 20 minutes 
  {
    reset = 0;
    count = 0;
  }
  delay(50);
}

void SensorRead(unsigned char addr,unsigned char* datbuf,unsigned char cnt) {
  unsigned short result=0; 
  Wire.beginTransmission(TOF10120);
  Wire.write(byte(addr));  
  Wire.endTransmission();
  Wire.requestFrom(TOF10120, (int)cnt);
  if (cnt <= Wire.available()) {
    *datbuf++ = Wire.read();
    *datbuf++ = Wire.read();
  }
}

int ReadDistance() { // Function to read distance data to TOF10120 module    
    unsigned short distance;
    unsigned char i2c_rx_buf[2]; //Read 2 bytes from 0x00 on the module
    SensorRead(0x00,i2c_rx_buf,2);
    
    //Combine two bytes read into one variable
    distance=i2c_rx_buf[0]; // i2c_rx_buf[0] : Top Byte
    distance=distance<<8;
    distance|=i2c_rx_buf[1]; // i2c_rx_buf[1] : Sub bytes
    return distance;
}