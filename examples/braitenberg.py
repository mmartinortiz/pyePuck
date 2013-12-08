#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       braitenberg.py
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

#		-- Braitenberg --
#
#		Simple program to evade collisions according to Braitenberg method
#

from ePuck import ePuck
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
	
	log('Connecting with the ePuck')
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
		robot.enable('proximity')
		
		log('Conection complete. CTRL+C to stop')
		log('Library version: ' + robot.version)
	
	except Exception, e:
		error(e)
		sys.exit(1)
		
	try:
		matrix = ( (150, -35), (100, -15), (80, -10), (-10, -10),
        (-10, -10), (-10, 80), (-30, 100), (-20, 150) )
		while True:
			# Important: when you execute 'step()', al sensors
			# and actuators are updated. All changes you do on the ePuck
			# will be effectives after this method, not before
			robot.step()

			# Now, we can get updated information from the sensors
			prox_sensors = robot.get_proximity()

			# The Braitenberg algorithm is really simple, it simply computes the
			# speed of each wheel by summing the value of each sensor multiplied by
			# its corresponding weight. That is why each sensor must have a weight 
			# for each wheel.
			wheels = [0, 0]
			for w, s in ((a, b) for a in range(len(wheels)) for b in range(len(prox_sensors))):
				# We need to recenter the value of the sensor to be able to get
				# negative values too. This will allow the wheels to go 
				# backward too.
				wheels[w] += matrix[s][w] * (1.0 - (prox_sensors[s] / 512))
			
			# Now, we set the motor speed. Remember that we need to execute 'step()'
			# for make this command effective
			robot.set_motors_speed(wheels[0], wheels[1])
			
	except KeyboardInterrupt:
		log('Stoping the robot. Bye!')
		robot.close()
		sys.exit()
	except Exception, e:
		print e

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
	
