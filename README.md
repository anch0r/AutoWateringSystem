# AutoWateringSystem
An auto watering system with temperature/humidity detection on Raspberry pi.

watering 30 sec if humidity < 60% RH, then delay 1 hour and check again.

delay additional 1 hour in warm seasons (20 <= temperature < 25 celsius)

delay additional 3 hour in chill seasons (15 <= temperature < 20 celsius)

upload sensor data to ThingSpeak.com every 5 minutes

## Hardware

Board:  Raspberry pi 3 model B+ 

Sensor: DHT22

A 2-way 5V relay

A 3.3V DC motor valve controller(directly connect to the faucet)

(motor spin clockwise → valve open, spin counterclockwise → valve close)

## Software Environment

OS: Raspbian July 2019(Kernel version: 4.19)

Python 3.7.4

## Wiring

![Imgur](https://i.imgur.com/tcpmOL1.png)

## Note

For my experience, the DHT22 sensor is not durable, always cracks in 3 or less months(especially in high humidity environment).

Failed to read data, no response, lost of accuracy even if manually calibration ...all like these.

I bought it 5 times from different vendors and still have no luck.

If you are considering a durable sensor, you may try another one like the BME280 but not this one.
