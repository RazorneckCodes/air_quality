# air_quality
Indoor air quality sensor BME680 and MHZ-19B are providing the data. An arduino nano is used to the read the data via serial and i2c interface. It provides the data to it's usb port. You can test it easy with the serial monitor inside the arduino ide.

A raspberry pi can request the data from the arduino via usb and writes it to the local/remote influxdb. The configuration for the docker containers is also show. On the pi I use the python script as a cron job to run it regularly. If you are also running grafana you can easily visualize the data in your browser.
