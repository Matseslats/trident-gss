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
import machine
import onewire, ds18x20

# the device is on GPIO3
dat = machine.Pin(3)

# create the onewire object
ds = ds18x20.DS18X20(onewire.OneWire(dat))

# scan for devices on the bus
roms = ds.scan()
print('found devices:', roms)

# loop 10 times and print all temperatures
for i in range(10):
    print('temperatures:', end=' ')
    ds.convert_temp()
    time.sleep_ms(750)
    for rom in roms:
        print(ds.read_temp(rom), end=' ')
    print()


"""Eller:
import time
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()

while True:
    temperature = sensor.get_temperature()
    print("The temperature is %s celsius" % temperature)
    time.sleep(1)
    """