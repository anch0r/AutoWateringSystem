import sys
import time
import urllib
import Adafruit_DHT
import RPi.GPIO as GPIO
import logging
from ValveControl import closeValve, watering30sec
from ThreadDispatcher import threadDispatcher

sensorType = Adafruit_DHT.DHT22
sensorPin = 4   #GPIO 04(pin #7)
tempCalibrationOffset = -0.0    #sensor calibration,based on mechanic temp/hydro meter
humidCalibrationOffset = -4.0
timeCalibration = -1.0       #timing error calibration
dataUploadTimeout = 300.0    #upload sensor data to ThingSpeak every 5 minutes
wateringTimeout = 3600.0     #watering timeout(1 hour)
thingSpeakApiKey = ''
thingSpeakParams = None
humidity = None
temperature = None
hotTemp = 25.0
warmTemp = 20.0
chillTemp = 15.0
warmTempWateringDelay = 3600.0    #delay additional 1 hour in warm seasons
chillTempWateringDelay = 10800.0  #delay additional 3 hour in chill seasons

#DHT22 sensor initialize
sensor = Adafruit_DHT.DHT22
pin = sensorPin

#timer initialize
dataUploadTimer = time.time()
wateringTimer =  time.time()
 
try:
    while True:
        loopTimer = time.time()
        #avoid using time.sleep() for timing out in main thread
        if ((loopTimer - dataUploadTimer) >= dataUploadTimeout):
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            temperature += tempCalibrationOffset
            humidity += humidCalibrationOffset
            if humidity is not None and temperature is not None:
                print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
                thingSpeakParams = urllib.parse.urlencode({'field1': temperature, 'field2': humidity, 'key': thingSpeakApiKey})
                threadDispatcher('UPLOAD_DATA',thingSpeakParams)                
                dataUploadTimer = time.time() + timeCalibration               
        if humidity is not None and humidity < 60.0 and temperature is not None:
            if temperature >= hotTemp and (loopTimer - wateringTimer) >= wateringTimeout:           
                print('humidity < 60%, watering 30 sec...\n')
                threadDispatcher('WATERING')
                wateringTimer = time.time()
            if (warmTemp <= temperature < hotTemp) and (loopTimer - wateringTimer) >= (wateringTimeout + warmTempWateringDelay):           
                print('humidity < 60%, watering 30 sec...\n')
                threadDispatcher('WATERING')
                wateringTimer = time.time()
            if (chillTemp <= temperature < warmTemp) and (loopTimer - wateringTimer) >= (wateringTimeout + chillTempWateringDelay):           
                print('humidity < 60%, watering 30 sec...\n')
                threadDispatcher('WATERING')
                wateringTimer = time.time()
        if (humidity is not None and (humidity < 0.0 or humidity > 100.0)) or (temperature is not None and (temperature < 0.0 or temperature > 50.0)):
            print('sensor misfunction, force close valve')
            closeValve()
            
except KeyboardInterrupt:
    closeValve()    #probably not thread-safe, must check
    print('DHT22 watering system stpped')
    
except Exception as e:
    closeValve()    #probably not thread-safe, must check
    print('unexpected error occured')
    logging.error(e)

finally:
    GPIO.cleanup()
