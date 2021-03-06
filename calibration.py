def calibration(sensorValue):
    #linear calibration:y = 1.2097x-53.206; R square value=0.99
    #the highest calibrated value of humidity will be capped at 67.64 %RH due to the sensor itself
    #this calibration equation best fits for 55 to 65 %RH interval by the mechanic hydro meter
    #every sensor differs, needs to check by yourself
    calibratedValue = 1.2097*sensorValue - 53.206
    return calibratedValue    
