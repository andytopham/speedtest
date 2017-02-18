#!/usr/bin/python
# Uses google spreadsheets to store data.
# Google writing leverages gspread library. See: https://github.com/burnash/gspread
#  But the oauth stuff is not quite right....
# Requires oauth2 authorisation.
#  That means we need to create a security key file using google ui.
#  This is pointed to below as authfile. Needs to be in working dir.
#  Spreadsheet needs to share access to the strange email address in this authfile
#     - the service account email address.

import subprocess, StringIO, gspread, time
from oauth2client.service_account import ServiceAccountCredentials
authfile = 'My Project-3aa2e2c55ac0.json'

class Spreadsheet():
	def __init__(self):
		print 'Started spreadsheet class.'
		print 'Making sure we are not using the wifi!'
		subprocess.call(['ifconfig', 'wlan0', 'down'])
		print 'Wifi disabled'
		self.row=0
			
	def open(self):
		scope = ['https://spreadsheets.google.com/feeds']
		credentials = ServiceAccountCredentials.from_json_keyfile_name(authfile, scope)
		gc = gspread.authorize(credentials)
		wks = gc.open("test")
		self.sheet = wks.get_worksheet(0)
		
	def header(self):
		date = time.strftime('%d %b')
		self.row = 1
		cell = 'A'+str(self.row)
		self.sheet.update_acell(cell, date)
		self.row += 1
		cell = 'A'+str(self.row)
		self.sheet.update_acell(cell, 'Time')		
		cell = 'B'+str(self.row)
		self.sheet.update_acell(cell, 'Ping(ms)')		
		cell = 'C'+str(self.row)
		self.sheet.update_acell(cell, 'Download(Mb/s)')		
		cell = 'D'+str(self.row)
		self.sheet.update_acell(cell, 'Upload(Mb/s)')		
		return(0)

	def update(self, val):
		self.open()		# otherwise the authorisation times out
		self.row += 1
		t = time.strftime("%H:%M")
		self.sheet.update_cell(self.row, 1, t)
		for col in range(3):
			self.sheet.update_cell(self.row, col+2, val[col])			
		return(0)
	
if __name__ == '__main__':
	print 'Google Spreadsheet test.'
	s = Spreadsheet()
	s.open()
	s.header()
	print 'Written to spreadsheet - test.'
	