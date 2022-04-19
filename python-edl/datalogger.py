# Temp: GPIO3
# scp C:\Users\matsh\Documents\cansat\software\gss\trident-gss\python-edl\datalogger.py trident@10.0.0.15:/home/trident
temppin = 3
# Steg 1: Få temp data, manglende resistor mellom data og VCC?
# Steg 2: Send data
# Steg 3: Programmer ATTINY for å videresende data
# Steg 4: Programmer ATTINY for å slå av og på pi
# Steg 5: Få rot data
# Steg 6: PID kontroll

# Få temp data


import time
# from w1thermsensor import W1ThermSensor

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.output(24,GPIO.HIGH)
# sensor = W1ThermSensor()


while True:
    # temperature = sensor.get_temperature()
    # print("The temperature is %s celsius" % temperature)
    time.sleep(1)
    GPIO.output(23,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(23,GPIO.LOW)


