def calibration(sensorValue):
    #linear calibration:y=1.7029x-89.128; R square value =0.9782
    #every sensor differs, needs to check by yourself
    calibratedValue = 1.7029*sensorValue - 89.128
    return calibratedValue    
