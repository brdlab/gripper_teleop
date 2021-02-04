#!/usr/bin/python3

import rospy
import sys
from std_msgs.msg import String
from sensor_msgs.msg import Image
from std_msgs.msg import UInt16
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import os
import tensorflow as tf
#Simport tensorflow_datasets as tfds
import pathlib
import keras_preprocessing
from keras_preprocessing import image
from keras_preprocessing.image import ImageDataGenerator

predict_lookup = [0,5,10,20,40,50,60,70,80]

class VisionCommand(object):
	def __init__(self):
		self.frame = None
		self.br = CvBridge()
		self.glove_model = tf.keras.models.load_model('/home/snehal/Utility/ROS/gripper_ws/src/vision_command/scripts/glove_model')
		self.loop_rate = rospy.Rate(2)

		self.sub_cam = rospy.Subscriber("/camera/color/image_raw", Image, self.image_callback)
		self.pub_cam = rospy.Publisher("/vision/prediction_image", Image, queue_size=10)
		self.pub_gripper = rospy.Publisher("gripper_pressure", UInt16, queue_size=20)
		self.pub_aperture = rospy.Publisher("aperture_pressure", UInt16, queue_size=20)

	def image_callback(self, msg):
	#	rospy.loginfo("Image received")
		try:
			frame = self.br.imgmsg_to_cv2(msg)
		except CvBridgeError as e:
			rospy.logerr("CvBridge Error: {0}".format(e))
		cv2.rectangle(frame, (165,0), (585,320), (255,0,0), 5)
		predicted_kPa = self.image_predict(frame)
		cv2.putText(frame, (str(predicted_kPa)+" kPa"), (300,350), cv2.FONT_HERSHEY_SIMPLEX,
			1, (0,0,0), 2, cv2.LINE_AA)
		self.pub_cam.publish(self.br.cv2_to_imgmsg(frame, "rgb8"))
	#	rospy.loginfo("publishing image")
		if rospy.has_param('/grasp_mode/grasping_mode'):
			mode = rospy.get_param('/grasp_mode/grasping_mode')
		else:
			mode = 0
		if rospy.has_param('/grasp_mode/hold_pressure'):
			hold = rospy.get_param('/grasp_mode/hold_pressure')
		else:
			hold = False
		if rospy.has_param('/grasp_mode/override_pressure'):
			override = rospy.get_param('/grasp_mode/override_pressure')
		else:
			override = True
		if not override:
			cmd = predicted_kPa
			if not hold:
				vac = cmd
		else:
			if rospy.has_param('/grasp_mode/pressure_manual'):
				vac = rospy.get_param('/grasp_mode/pressure_manual')
			else:
				vac = 0
		if mode==2:
			#cmd = int(pressure[1:3])
			rospy.loginfo(str(vac)+"kPa ; system_time: " + str(rospy.get_time()))
			self.pub_gripper.publish(vac)
			self.pub_aperture.publish(vac)
		if mode==1:
			#cmd = int(pressure[1:3])
			rospy.loginfo(str(vac)+"kPa ; system_time: " + str(rospy.get_time()))
			self.pub_aperture.publish(vac)
			self.pub_gripper.publish(0)
		if mode==0:
			rospy.loginfo(str(0)+"kPa ; system_time: " + str(rospy.get_time()))
			self.pub_gripper.publish(0)
			self.pub_aperture.publish(0)

	def image_predict(self, frame):
		global predict_lookup
		test = frame[0:320,165:585]
		predict_array = np.array(test)
		predict_array = np.expand_dims(predict_array,axis=0)
		prediction = self.glove_model.predict(predict_array)
	#	prediction_pressure = sum(predict_lookup*prediction)
		prediction_pressure = int(predict_lookup[int(np.argmax(prediction))])
	#	rospy.loginfo("prediction: {}".format(prediction_pressure))
		return prediction_pressure

	def start(self):
		while not rospy.is_shutdown():
			self.loop_rate.sleep()

if __name__ == '__main__':
	rospy.init_node("vision_pressure_command", anonymous=True)
	my_node = VisionCommand()
	my_node.start()
