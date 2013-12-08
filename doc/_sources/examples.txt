Examples
--------

There are some some elements that you should know:

* Sensors

You have to use the keys of this dictionary for indicate on "enable" function the sensor that you want to read::
	
	DIC_SENSORS = { 
		"accelerometer" : "a",
		"selector" : "c",
		"motor_speed" : "e",
		"camera" : "i",
		"floor"  : "m",
		"proximity" : "n",
		"light" : "o",
		"motor_position" : "q",
		"microphone" : "u"
	}
	

* Camera Modes and zoom	

You have to use the keys of this dictionary for indicate the operating mode of the camera::

	CAM_MODE = {
		"GREY_SCALE" : 0,
		"RGB_365" : 1,
		"YUV" : 2,
		"LINEAR_CAM" : 3
	}
	


You can use three diferents Zoom in the camera::

	CAM_ZOOM = (1, 4, 8)


**Line Follower** example
^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/line_follower.py

**Braitenberg** example
^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/braitenberg.py

**Photo Taker** example
^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/photo_taker.py

