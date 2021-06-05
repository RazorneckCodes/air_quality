#!/usr/bin/env python3
import serial
import time
from influxdb import InfluxDBClient

def read_data(command): 
    try:
        req = command + "\n"
        ser.write(req.encode())
        line = ser.readline(10).decode('utf-8').rstrip()
        return float(line)
    except:
        return None
        #reset serial port and arduino
        #ser.close()
        #ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        #ser.flushInput()
        #ser.close()

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
    print(json)
    client.write_points(json, time_precision='s')

if __name__ == '__main__':
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        ser.flushInput()
        time.sleep(3) #time to open up serial monitor
        co2 = read_data("co2", ser)
        humidity = read_data("hum", ser)
        temperature = read_data("temp", ser)
        gas_resistance = read_data("res", ser)
        send_db(co2, temperature, humidity, gas_resistance)
        ser.close()

