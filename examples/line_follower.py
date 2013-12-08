#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       line_follower.py
#       
#       Copyright 2011 Manuel Martín Ortiz <mmartinortiz@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

#		-- Line Follower --
#
# 		Program to follow a black line ober white floor
#
#		Requisite:
#			* ePuck with Webots' firmware 1.4.2
#			* ePuck.py Library (>= 0.9)
#			* Bluetooth device

from ePuck import ePuck
import time
import sys
import re

# You can use this dictionary to asociate an ePuck ID with its MAC Address
epucks = {
	'1797' : '10:00:E8:6C:A2:B6',
	'1903' : '10:00:E8:6C:A1:C7'
}

def log(text):
	"""	Show @text in standart output with colors """
	
	blue = '\033[1;34m'
	off = '\033[1;m'
	
	print(''.join((blue, '[Log] ', off, str(text))))
		
def error(text):
	red = '\033[1;31m'
	off = '\033[1;m'
	
	print(''.join((red, '[Error] ', off, str(text))))
	
def main(mac):
	
	global_speed = 180
	fs_speed = 0.6
	threshold = 1000

	log('Conecting with ePuck')
	try:
		# First, create an ePuck object.
		# If you want debug information:
		#~ robot = ePuck(mac, debug = True)
		# else:
		robot = ePuck(mac)

		# Second, connect to it
		robot.connect()
		
		# You can enable various sensors at the same time. Take a look to
		# to DIC_SENSORS for know the name of the sensors
		robot.enable('floor', 'proximity')

		leds_on = [0] * 8
		log('Conection complete. CTRL+C to stop')
		log('Library version: ' + robot.version)
	
		times_got = []
	except Exception, e:
		error(e)
		sys.exit(1)
		
	try:
		while True:
			# Important: when you execute 'step()', al sensors
			# and actuators are updated. All changes you do on the ePuck
			# will be effectives after this method, not before
			robot.step()
			
			# Now, we can get updated information from the sensors
			floor_sensors = robot.get_floor_sensors()
			prox_sensors = robot.get_proximity()
			
			# line_follower
			delta = floor_sensors[2] - floor_sensors[0]
			l_speed = global_speed - fs_speed * delta
			r_speed = global_speed + fs_speed * delta

			# Now, we set the motor speed. Remember that we need to execute 'step()'
			# for make this command effective
			robot.set_motors_speed(l_speed, r_speed)
			
			# leds on/off
			for index, s in enumerate(prox_sensors):
				if int(s) > threshold and leds_on[index] == 0:
					# Switch On
					robot.set_led(index, 1)
					leds_on[index] = 1
				elif int(s) < threshold and leds_on[index] == 1:
					# Switch Off
					robot.set_led(index, 0)
					leds_on[index] = 0
					
	except KeyboardInterrupt:
		log('Stoping the robot. Bye!')
		robot.close()
		sys.exit()
	except Exception, e:
		error(e)

	return 0

if __name__ == '__main__':
	X = '([a-fA-F0-9]{2}[:|\-]?){6}'
	if len(sys.argv) < 2:
		error("Usage: " + sys.argv[0] + " ePuck_ID | MAC Address")
		sys.exit()
	robot_id = sys.argv[1]
	
	if epucks.has_key(robot_id):
		main(epucks[robot_id])
		
	elif re.match(X, robot_id) != 0:
		main(robot_id)
	
	else:
		error('You have to indicate the MAC direction of the robot')
