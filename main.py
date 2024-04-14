import time
from machine import I2C, Pin
from RTC import RTC

time.sleep(0.1) # Wait for USB to become ready
print("Hello world")

# Setup the I2C peripheral
i2c = I2C(0, sda = Pin(0), scl = Pin(1), freq=400000)


# Scan the I2C bus for connected devices
devices = i2c.scan()

if devices:
    print(f"Device found with address: 0x{devices[0]:02X}")
else:
    print("No I2C devices found")

device_address = devices[0]


# Implement the RTC library and use it to initialise the RTC to 11:57:23 03/02/2024 then print out the time every second forever
initial_date = '03/02/2024'
initial_time = '11:57:23'

rtc = RTC(i2c, device_address, initial_date, initial_time)

# Main loop
while True:
    # Read date and time
    current_time = rtc.get_datetime()

    # Display date and time
    hour = current_time[0]
    minute = current_time[1]
    second = current_time[2]
    date = current_time[3]
    month = current_time[4]
    year = current_time[5]
    print("{:02d}/{:02d}/{:04d} {:02d}:{:02d}:{:02d}".format(date, month, year, hour, minute, second))

    # Delay for 1 second
    time.sleep(1)
