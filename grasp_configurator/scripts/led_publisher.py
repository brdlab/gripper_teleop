#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt16
from payload import payload_dict
import math

gripper_pressure = None
new_msg = False

def level_clamp(n):
	return 4 if n>4 else n

def pressure_cb(data):
	global gripper_pressure, new_msg
	gripper_pressure = data
	new_msg = True


def led_gen_manual():
	while not rospy.is_shutdown():
		#pressure = raw_input('Enter mode (A/G) with pressure or (Q)uit')
		if rospy.has_param('/grasp_mode/led_level'):
			led = int(rospy.get_param('/grasp_mode/led_level'))
			rospy.loginfo("LED_LEVEL is %d", led)
		else:
			rospy.loginfo("LED_LEVEL hasn't been published yet")
			led = 0
		level_pub.publish(led)
		rate.sleep()

def led_gen_auto():
	global gripper_pressure, new_msg
	rospy.Subscriber('gripper_pressure', UInt16, pressure_cb)
	previous_index = 0
	pressure_limit = 80
	led = 0
	while not rospy.is_shutdown():
		# Obtain payload parameter from ROS ParamServer
		if rospy.has_param('/grasp_mode/payload_select'):
			payload_index = int(rospy.get_param('/grasp_mode/payload_select'))
		else:
			rospy.loginfo("Running in free mode")
			payload_index = 0

		# Check if index has changed, if yes, update limits list
		if (payload_index!=previous_index):
			for item in payload_dict:
				if item["index"] == payload_index:
					pressure_limit = item["limit"]
					name = item["name"]
					rospy.loginfo("Payload set to %s", name)
		
		# Derive LED_LEVEL from pressure_limit and gripper_pressure topic
		if new_msg:
			pressure = gripper_pressure.data
			pfac = (pressure*4)/pressure_limit
			pfac = math.ceil(pfac)
			pfac = level_clamp(pfac)
			led = pfac

		level_pub.publish(led)
		new_msg = False
		previous_index = payload_index
		rate.sleep()

if __name__ == '__main__':
	level_pub = rospy.Publisher('led_level', UInt16, queue_size=20)
	rospy.init_node('glove_level', anonymous=True)
	rate = rospy.Rate(1)
	try:
		led_gen_auto()
	except rospy.ROSInterruptException:
		pass