def calibration(sensorValue):
    #linear calibration:y=0.6594x+14.114; R2=0.998
    calibratedValue = 0.6594*sensorValue + 14.114
    return calibratedValue    
