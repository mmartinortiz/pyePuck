#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       line_follower.py
#       
#       Copyright 2010 Manuel Martín Ortiz <mmartinortiz@gmail.com>
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

#		-- Photo Taker --
#
#		Simple program to take pictures of the camera while turning on itself
#

from ePuck import ePuck
import sys
import re
import time

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

	print('Connecting with the ePuck')
	try:
		# First, create an ePuck object.
		# If you want debug information:
		#~ robot = ePuck(mac, debug = True)
		# ele:
		robot = ePuck(mac)

		# Second, connect to it
		robot.connect()

		# You can enable various sensors at the same time. Take a look to
		# to DIC_SENSORS for know the name of the sensors
		robot.enable('camera', 'motor_position')

		# We have to set the camera parameters
		robot.set_camera_parameters('RGB_365', 40, 40, 8)
		
		log('Conection complete. CTRL+C to stop')
		log('Library version: ' + robot.version)
	
	except Exception, e:
		error(e)
		sys.exit(1)
		
	try:
		counter = 0
		while True:
			# Important: when you execute 'step()', al sensors
			# and actuators are updated. All changes you do on the ePuck
			# will be effectives after this method, not before
			robot.step()

			image = robot.get_image()

			if image != None:
				# Do something with the image
				robot.save_image('ePuck-' + str(counter) + '.png')
				counter += 1

			# Set the motors speed and position
			robot.set_motors_speed(100,-100)
			robot.set_motor_position(0,0)

			# Make a 'step()' and the robot will move
			robot.step()

			while robot.get_motor_position()[0] < 270:
				# Keep turning on itself
				robot.step()

			# Stop the robot (don't forget the 'step()')
			robot.stop()
			robot.step()

			# Sleep, otherwise we will not see the stop
			time.sleep(1)
					
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
		
