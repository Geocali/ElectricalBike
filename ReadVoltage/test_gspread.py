import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('ElectricalBike-f269de0cf54e.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open("VoltageMeasures").sheet1
for i in range(10):
    wks.update_cell(1, i + 1, 'VoltageBattery' + str(i + 1))
