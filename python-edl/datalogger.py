# Temp: GPIO3
temppin = 3
# Steg 1: Få temp data, manglende resistor mellom data og VCC?
# Steg 2: Send data
# Steg 3: Programmer ATTINY for å videresende data
# Steg 4: Programmer ATTINY for å slå av og på pi
# Steg 5: Få rot data
# Steg 6: PID kontroll

# Få temp data


import time
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()

while True:
    temperature = sensor.get_temperature()
    print("The temperature is %s celsius" % temperature)
    time.sleep(1)

    
