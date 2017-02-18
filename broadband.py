#!/usr/bin/python
# Measure broadband speed at intervals
# Uses speedtest program to gather the data.
# Uses google spreadsheets to store data.

import subprocess, StringIO, time, lcd, spreadsheet
INTERVAL = 5*60
NUMLOOPS = 12*2

def get_speeds(self):
	val = []
	try:
		string = subprocess.check_output(['speedtest', '--simple'])
		buf = StringIO.StringIO(string)
		for i in range(3):
			ping1 = buf.readline()
			ping2 = ping1.split()[1]
			val.append(int(float(ping2)))
	except:
		print 'Failed to execute speedtest. Network might be dead?'
		val.append(0)
		val.append(0)
		val.append(0)
	return(val)
	
if __name__ == '__main__':
	print 'Collecting broadband speeds and storing in spreadsheet.'
	s = spreadsheet.Spreadsheet()
	s.open()
	s.header()
	print 'Opened spreadsheet.'
	myLcd = lcd.Screen()
	myLcd.clear()
	myLcd.writerow(0, 'Broadband')
	for i in range(NUMLOOPS):
		val = s.get_speeds()
		t= time.strftime('%H:%M')
		print t, 'Ping=', val[0], 'ms. Download=', val[1], 'Mb/s', 'Upload=', val[2], 'Mb/s'
		string = t + ' ' + str(val[0]) + ' ' + str(val[1]) + ' ' + str(val[2])
		myLcd.writerow(1, '                ')
		myLcd.writerow(1, string)
		s.update(val)
		time.sleep(INTERVAL)
	print 'Finished looping. Exiting.'
	myLcd.writerow(0,'Finished')
	