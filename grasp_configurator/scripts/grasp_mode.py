#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt16

from dynamic_reconfigure.server import Server
from grasp_configurator.cfg import GraspConfig

def callback(config, level):
	rospy.loginfo("""Reconfigure Request: Grasp mode - {grasping_mode}, Payload - {payload_select}""". format(**config))
	return config

if __name__ == '__main__':
	rospy.init_node("grasp_config", anonymous = False)
	srv = Server(GraspConfig, callback)
	rospy.spin()
