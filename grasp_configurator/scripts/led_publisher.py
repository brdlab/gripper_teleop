#!/usr/bin/env python

import rospy
from std_msgs.msg import UInt16
from std_msgs.msg import Float32
from payload import payload_dict
import math

gripper_pressure = None
gripper_force = None
new_msg = False
new_msg2 = False

def level_clamp(n):
	if n<0:
		return 0
	if n>4:
		return 4

def pressure_cb(data):
	global gripper_pressure, new_msg
	gripper_pressure = data
	new_msg = True

def force_cb(data):
	global gripper_force, new_msg2
	gripper_force = data
	new_msg2 = True

def led_gen():
	global gripper_pressure, new_msg
	global gripper_force, new_msg2
	rospy.Subscriber('gripper_pressure', UInt16, pressure_cb)
	rospy.Subscriber('gripper_force', Float32, force_cb)
	previous_index = 0
	limit = 80
	led = 0
	while not rospy.is_shutdown():
		# Obtain payload parameter from ROS ParamServer
		if rospy.has_param('/grasp_mode/teleoperation_mode'):
			teleop_index = int(rospy.get_param('/grasp_mode/teleoperation_mode'))
			payload_index = int(rospy.get_param('/grasp_mode/payload_select'))
		else:
			rospy.loginfo("Running in free mode")
			teleop_index = 0
			payload_index = 0

		# Check if index has changed, if yes, update limits list
		if (payload_index!=previous_index):
			for item in payload_dict:
				if item["index"] == payload_index:
					if teleop_index == 0:
						limit = item["plimit"]
					else:
						limit = item["flimit"]
					name = item["name"]
					rospy.loginfo("Payload set to %s", name)
		
		# Derive LED_LEVEL from pressure_limit and gripper_pressure topic
		if teleop_index == 0:
			if new_msg:
				pressure = gripper_pressure.data
				pfac = (pressure*4)/limit
				pfac = math.ceil(pfac)
				pfac = level_clamp(pfac)
				led = int(pfac)

		if teleop_index == 1:
			if new_msg2:
				force = gripper_force.data
				if force == None:
					force = 0 
				ffac = (force*4)/limit
				ffac = int(math.ceil(ffac))
				ffac = level_clamp(ffac)
				led = int(ffac)

		level_pub.publish(led)
		new_msg = False
		new_msg2 = False
		previous_index = payload_index
		rate.sleep()

if __name__ == '__main__':
	level_pub = rospy.Publisher('led_level', UInt16, queue_size=20)
	rospy.init_node('glove_level', anonymous=True)
	rate = rospy.Rate(1)
	try:
		led_gen()
	except rospy.ROSInterruptException:
		pass
