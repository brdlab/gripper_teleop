#!/usr/bin/env python

import rospy
import math
from std_msgs.msg import Float32
from rosserial_arduino.msg import Adc
import numpy as np

sensor = np.zeros(6, dtype=float)
new_msg = False

def adc_cb(data):
	sensor_adc = None
	sensor_voltage = None
	global sensor, new_msg
	sensor_adc = [data.adc0, data.adc1, data.adc2, data.adc3, data.adc4, data.adc5]
	sensor_voltage = np.array(sensor_adc)*(5.0000/255.0000)
	for i in range(len(sensor_voltage)):
		sensor[i] =resistance_calc(sensor_voltage[i])
	new_msg = True

# Calculates resistance from voltage divider. voltage variable is voltage across sensor
def resistance_calc(voltage):
	known_resistance = 1000.0000
	supply_voltage = 5.0000
	return (round((known_resistance*(supply_voltage - voltage))/voltage, 2))

def force(original_resistance, new_resistance):
	E = 1931000
	w = 0.008
	h = 0.004
	v = 0.47

	f = (1-(original_resistance/new_resistance))*((E*h*w)/(2*(1-(v*v))))
	return (round(f,2))

# Return value in kohm
	return round((known_resistance*((supply_voltage-voltage)/voltage)*1/1000),2)

def adc_to_force():
	global sensor, new_msg
	rospy.Subscriber('gripper_sensor', Adc, adc_cb)

	# steady sensor resistance values in ohms
	original_resistance = [1500.00,2000.00,1500.00,1600.00,2400.00,1800.00]
	while not rospy.is_shutdown():
		total_force = 0
		# Start of loop
		if new_msg:
			for i in range(len(sensor)):
				total_force = total_force + force(original_resistance[i], sensor[i])
			total_force = round(total_force,3)
		force_pub.publish(total_force)

		# End of loop
		new_msg = False
		rate.sleep()

if __name__ == '__main__':
	force_pub = rospy.Publisher('gripper_force', Float32, queue_size=20)
	rospy.init_node('gripper_force', anonymous=True)
	rate = rospy.Rate(4)
	try:
		adc_to_force()
	except rospy.ROSInterruptException:
		pass