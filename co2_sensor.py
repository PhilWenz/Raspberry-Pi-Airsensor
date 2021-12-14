import time
import board
import busio
import adafruit_ccs811
import math
class Sensor:
    def __init__(self) -> None:
        self.i2c= busio.I2C(board.SCL, board.SDA)
        self.ccs811 = adafruit_ccs811.CCS811(self.i2c)
        while not self.ccs811.data_ready:
            pass
        
        temp = self.ccs811.temperature
        self.ccs811.temp_offset = temp - 25
        print("Setup Done")
        
    def get_values(self, times):
        index = 0

        while True:

            index+=1
            
            co2_avg = 0
            co2_values = []

            tvoc_avg = 0
            tvoc_values = []

            temp_avg = 0
            temp_values = []
            

            for i in range(0,times):
                #get co2 values for average and stdv
                co2_current = self.ccs811.eco2
                co2_avg += co2_current
                co2_values.append(co2_current)
                
                #get tvoc values for average and stdv
                tvoc_current = self.ccs811.tvoc
                tvoc_avg += tvoc_current
                tvoc_values.append(tvoc_current)

                #get temp 
                temp_current = self.ccs811.temperature
                temp_avg += temp_current
                temp_values.append(temp_current)
                
                time.sleep(0.5)

            if index == 10 or Sensor.calc_stdv(co2_values) < 1000 and Sensor.calc_stdv(tvoc_values) < 100 and Sensor.calc_stdv(temp_values) < 10:
                break
            else:
                print("Messfehler! Messung wird wiederholt.")

        return co2_avg/times, tvoc_avg/times, temp_avg/times

        


    def calc_stdv(values):
        #calc mean
        mean = sum(values)/len(values)

        stdv = 0
        for v in values:
            stdv += math.pow((v-mean),2)

        return math.sqrt(stdv/len(values))
