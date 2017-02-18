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
FILENAME = "test"

class Spreadsheet():
	def __init__(self):
		print 'Started spreadsheet class.'
		self.row = 0
#		self.open()
			
	def open(self, filename, mode):
		# mode is just for filewrite compatibility and is discarded so far.
		self.filename = filename
		scope = ['https://spreadsheets.google.com/feeds']
		credentials = ServiceAccountCredentials.from_json_keyfile_name(authfile, scope)
		gc = gspread.authorize(credentials)
		wks = gc.open(filename)
		self.sheet = wks.get_worksheet(0)
		
	def header(self):
		val = []
		val.append('Time')
		val.append('Ping(ms)')
		val.append('Download(Mb/s)')
		val.append('Upload(Mb/s)')
		return(val)
	
	def write(self, val):
		self.open(self.filename, "w")		# otherwise the authorisation times out
		self.row += 1
		col = 0
		for nextval in val:
			col += 1
			self.sheet.update_cell(self.row, col, nextval)			
		return(0)
	
if __name__ == '__main__':
	print 'Google Spreadsheet test.'
	s = Spreadsheet()
	s.open(FILENAME, "w")
	val = []
	val.append(time.strftime('%d %b'))	# date in top row
	s.write(val)
	val = []
	val = s.header()
	s.write(val)
	print 'Written to spreadsheet - test.'
	
	