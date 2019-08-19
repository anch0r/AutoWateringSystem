import RPi.GPIO as GPIO
import time

powerOnTimeout = 0.5    #relay power-on timeout(0.5 sec)

#GPIO initialize
GPIO.setmode(GPIO.BOARD)
RELAY1 = 11
RELAY2 = 13

GPIO.setup(RELAY1, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(RELAY2, GPIO.OUT, initial=GPIO.HIGH)

def openValve():
    valvePowerOnTime = time.time()
    GPIO.output(RELAY1, GPIO.LOW)
    while True:
        valvePowerOffTime = time.time()
        if (valvePowerOffTime - valvePowerOnTime >= powerOnTimeout):
            GPIO.output(RELAY1, GPIO.HIGH)
            break
    return

def closeValve():
    valvePowerOnTime = time.time()
    GPIO.output(RELAY2, GPIO.LOW)
    while True:
        valvePowerOffTime = time.time()
        if (valvePowerOffTime - valvePowerOnTime >= powerOnTimeout):
            GPIO.output(RELAY2, GPIO.HIGH)
            break
    return

def watering30sec():
    try:
        openValve()
        time.sleep(30)
        closeValve()
        print('watering finished, close valve\n')
        return
    
    except Exception as e:
        closeValve()
        print('unexpected error occured when watering, force close valve\n')
        logging.error(e)
        return