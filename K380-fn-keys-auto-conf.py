#!/usr/bin/env python3
#coding: utf-8
"""
(ROOT RQUIRED)
This script watches K380's connection.
Every time its reconnection is detected, run fn_on.sh to normalize the fn-key configuration.
"""

import os
import re
import signal
from time import sleep
import subprocess as sp
import sys

def main():
	"""
	main function
	"""
	def signal_handler(num, frame):	#pylint: disable=W0613
		proc.kill()
		sys.exit(0)
	
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	#Get K380's MAC address.
	s = sp.run(('bt-device', '-l'), stdout=sp.PIPE).stdout.decode('utf-8')
	match = re.search(r'Keyboard K380 \((([0-9,A-F]{2}:){5}[0-9,A-F]{2})\)', s)
	if match:
		mac = match.groups()[0]
	else:
		print('Error: Keyboard K380 is not paired.')
		sys.exit(1)

	#If K380 is already connected, then run fn_on.sh to certainly normalize the fn-key configuration.
	proc = sp.Popen('bluetoothctl', stdin=sp.PIPE, stdout=sp.PIPE)
	s = proc.communicate('info {0}\nexit'.format(mac).encode('utf-8'))[0].decode('utf-8')
	if re.search(r'Device {0}[\s\S]*Connected: ((yes|no))'.format(mac), s).groups()[0] == 'yes':
		sp.run('./fn_on.sh')

	#Run fn_on.sh every time K380's reconnection is detected.
	proc = sp.Popen('bluetoothctl', stdin=sp.PIPE, stdout=sp.PIPE)
	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGTERM, signal_handler)
	while True:
		s = proc.stdout.readline().decode('utf-8')
		if mac in s and 'Connected: yes' in s:
			sleep(0.5)	#a short wait is necessary
			sp.run('./fn_on.sh')

if __name__ == '__main__':
	main()
