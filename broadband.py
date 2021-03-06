#!/usr/bin/python
# Measure broadband speed at intervals
# Uses speedtest program to gather the data.
# Uses google spreadsheets to store data.

import subprocess, StringIO, time, lcd, spreadsheet
INTERVAL = 10		# minutes
HOURS = 6
NUMLOOPS = 6 * HOURS

def get_speeds():
	val = []
	val.append(time.strftime('%H:%M'))
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
	print 'Sampling every', INTERVAL, 'minutes'
	print 'Running for', HOURS, 'hours' 
	subprocess.call(['ifconfig', 'wlan0', 'down'])
	print 'Wifi disabled'
	s = spreadsheet.Spreadsheet()
	s.open("test","w")
	list = []
	list.append(time.strftime('%d %b'))
	s.write(list)	# date in top row
	val = s.header()
	s.write(val)
	print 'Opened spreadsheet.'
	myLcd = lcd.Screen()
	myLcd.clear()
	myLcd.writerow(0, 'Broadband')
	for i in range(NUMLOOPS):
		val = get_speeds()
		string = str(val[0]) + ' ' + str(val[1]) + ' ' + str(val[2]) + ' ' + str(val[3])
		print string
		myLcd.writerow(1, '                ')
		myLcd.writerow(1, string)
		s.write(val)
		time.sleep(INTERVAL*60)
	print 'Finished looping. Exiting.'
	myLcd.writerow(0,'Finished')
	