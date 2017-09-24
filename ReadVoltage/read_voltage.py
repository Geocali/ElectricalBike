#! /usr/bin/python

import gspread
from oauth2client.service_account import *
import pandas as pd

import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:
##CLK  = 18
##MISO = 23
##MOSI = 24
##CS   = 25
##mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp1 = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
mcp2 = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE + 1))
Vref = 5

R = [{'R1':0,'R2':1}]
R.append({'R1':1000,'R2':1000})
R.append({'R1':10000,'R2':1000})
R.append({'R1':10000,'R2':1000})
R.append({'R1':10000,'R2':1000})
R.append({'R1':10000,'R2':1000})
R.append({'R1':10000,'R2':1000})
R.append({'R1':10000,'R2':1000})
R.append({'R1':10000,'R2':1000})
R.append({'R1':10000,'R2':1000})

print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>5} | {1:>5} | {2:>5} | {3:>5} | {4:>5} | {5:>5} | {6:>5} | {7:>5} | {8:>5} | {9:>5} |'.format(*range(10)))
print('-' * 81)

# prepare the google spreadsheet
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('ElectricalBike-f269de0cf54e.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open("VoltageMeasures").sheet1

cell_list = wks.range('A1:K20')
for cell in cell_list:
    cell.value = ''
wks.update_cells(cell_list)
wks.update_cell(1, 1, 'Time')
for i in range(10):
    wks.update_cell(1, i + 2, 'VoltageBattery' + str(i + 1))

# Main program loop.
k = 0
t0 = time.time()
delta_k = 10 # every delta_k measures, the result is stored in the google spreadsheet
while True:
    # Read all the ADC channel values in a list.
    values = [0]*10
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        value = float(mcp1.read_adc(i)) * Vref / 1024
        values[i] = round(value*(R[i]['R1']+R[i]['R2'])/R[i]['R2'], 2)
    
    for i in range(2):
        value = float(mcp2.read_adc(i)) * Vref / 1024
        values[i + 8] = round(value*(R[i + 8]['R1']+R[i + 8]['R2'])/R[i + 8]['R2'], 2)
    # Print the ADC values.
    print('| {0:>5} | {1:>5} | {2:>5} | {3:>5} | {4:>5} | {5:>5} | {6:>5} | {7:>5} | {8:>5} | {9:>5} |'.format(*values))
    
    # save the result in a google spreadsheet
    k = k + 1
    if float(k) /delta_k == k/delta_k:
        wks.update_cell(k/delta_k + 1, 1, str(round(time.time() - t0, 1)).replace(".", ","))
        for i in range(10):
            if i == 0 :
                voltage = str(round(values[i], 2)).replace(".", ",")
            else:
                voltage = str(round(values[i] - values[i - 1], 2)).replace(".", ",")
            wks.update_cell(k/delta_k + 1, i + 2, voltage)
    
    # save the result in a csv file

    
    # Pause for half a second.
    time.sleep(0.5)
