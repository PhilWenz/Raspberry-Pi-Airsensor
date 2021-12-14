import time
import board
import busio
import adafruit_ccs811
 
i2c= busio.I2C(board.SCL, board.SDA)
ccs811 = adafruit_ccs811.CCS811(i2c)
while not ccs811.data_ready:
    pass
        
temp = ccs811.temperature
ccs811.temp_offset = temp - 25
print("Setup Done")

while True:
    print("CO2: {} PPM, TVOC: {} PPM, Temp: {} C"
        .format(ccs811.eco2, ccs811.tvoc, ccs811.temperature))
    time.sleep(0.5)