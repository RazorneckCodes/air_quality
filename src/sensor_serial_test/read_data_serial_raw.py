#!/usr/bin/env python3
import serial
import time
from influxdb import InfluxDBClient

def read_data(command): 
    try:
        req = command + "\n"
        ser.write(req.encode())
        line = ser.readline(100).decode('utf-8').rstrip()
        return float(line)
    except:
        #If RPi usb crashes, this will fix it
        s = serial.Serial('/dev/ttyS0', 9600, timeout=5)
        s.close()

def con_influx():
    user = ''
    password = ''
    dbname = ''
    host = 'localhost'
    port = 8086
    client = InfluxDBClient(host, port, user, password, dbname, ssl=True, verify_ssl=True)
    return client


def send_db(co2, temp, hum, res):
    client = con_influx()
    json = [
        {
            "measurement": "air_quality",
            "tags": {
                "location": "",
                "room": "",
                "dimension temp": "°C", 
                "dimension hum": "%",
                "dimension gas resistance": "kOhms",
                "dimension co2": ""
            },
            "time": int(time.time()),
            "fields": {
                "temperature": temp,
                "humidity": hum,
                "gas resistance": res,
                "co2": co2
            }
        }
    ]
    client.write_points(json, time_precision='s')

if __name__ == '__main__':
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) #search interface name at py
        ser.flush()
        time.sleep(2) #time to open up the serial connection

        co2 = read_data("co2")
        humidity = read_data("hum")
        temperature = read_data("temp")
        gas_resistance = read_data("res")
        send_db(co2, temperature, humidity, gas_resistance)

