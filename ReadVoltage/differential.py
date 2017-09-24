# !!!! enable SPI before using !!!

import time
#import pandas as pd

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
Vref = 5
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
voltages = []

print('Press Ctrl-C to quit...')
while True:
    # Grab the difference between channel 0 and 1 (i.e. channel 0 minus 1).
    # Note you can specify any value in 0-7 to grab other differences:
    #  - 0: Return channel 0 minus channel 1
    #  - 1: Return channel 1 minus channel 0
    #  - 2: Return channel 2 minus channel 3
    #  - 3: Return channel 3 minus channel 2
    #  - 4: Return channel 4 minus channel 5
    #  - 5: Return channel 5 minus channel 4
    #  - 6: Return channel 6 minus channel 7
    #  - 7: Return channel 7 minus channel 6
    value1 = round(float(mcp.read_adc_difference(0)) * Vref / 1024, 3)
    print('Voltage battery 1: {0} V'.format(value1))
    value2 = round(float(mcp.read_adc_difference(1)) * Vref / 1024, 3)
    print('Voltage battery 2: {0} V'.format(value2))
    voltages.append([time.time(), value1, value2])
    time.sleep(1)

#df = pd.DataFrame(voltages, columns=['time', 'voltage'])
#df.to_csv("voltages.csv")
