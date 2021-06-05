#include "MHZ19.h"
#include <Arduino.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"

#define RX_PIN 2
#define TX_PIN 3
#define BAUDRATE 9600

Adafruit_BME680 bme;
MHZ19 myMHZ19;
SoftwareSerial mySerial(RX_PIN, TX_PIN);   
String req = "";

void setup() {
  Serial.begin(9600);
  mySerial.begin(BAUDRATE);            
  myMHZ19.begin(mySerial);
  myMHZ19.autoCalibration();    
  
  if (!bme.begin()) {
    Serial.println("Could not find a valid BME680 sensor, check wiring!");
    while (1);
  }
  // Set up oversampling and filter initialization
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150); // 320*C for 150 ms
}

void loop() {
  if (Serial.available() > 0) {
    req = Serial.readStringUntil('\n');
    bme.performReading(); 
    if (req == "co2") {
      // Exponential equation for Raw & CO2 relationship
      Serial.println(myMHZ19.getCO2());
    }
    else if (req == "temp") {  
      Serial.println(bme.temperature); // Request Temperature (as Celsius)
    }
    else if (req == "hum") {   
      Serial.println(bme.humidity); // Request humidity in %
    }
    else if (req == "res") {   
      Serial.println(bme.gas_resistance / 1000.0); // Request Gas Resistance in kOhms
    }
  }
}
