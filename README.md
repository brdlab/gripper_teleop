# gripper_teleop
ROS Packages for the SUTD Gripper teleoperation. Consists of 3 main modules:

1) Gripper driver : for acquiring gripper sensor data and sending vacuum commands

2) CNN-based classification package : classifies input gesture image to 9 gripper command classes

3) Wearable driver : interfaces with driver and sends force information for operator feedback

# Requirements
- Ubuntu 18.04
- ROS Melodic
- ROS dependencies - image_pipeline, intel_realsense (or any camera driver)
- OpenCV
- Tensorflow2
- Python 3.7
- Python dependencies: matplotlib, sklearn, numpy, pyserial

## Install the EZGripper ROS Driver (Indigo or Kinetic)

1) Install the python EZGripper library https://github.com/SAKErobotics/libezgripper

2) Install dependencies:

	$ sudo apt-get install ros-indigo-joystick-drivers
	
	or 
	
	$ sudo apt-get install ros-kinetic-joystick-drivers

3) Download code:

	$ cd ~/catkin_ws/src
	$ git clone https://github.com/SAKErobotics/EZGripper.git
	$ cd ..
	$ catkin_make

4) Setup parameters in joy.launch file
  - ~port - serial device (like "/dev/ttyUSB0") or tcp endpoint (like "192.168.0.200:5000") to use
  - ~baud - baud rate of the serial device, not used for tcp
  - grippers - definition of grippers on this serial bus: the gripper name to use for the action interface and the servo id of the gripper (several ids if several grippers are to be used as one group), for example {left:[9], right:[10,11]}.  By default, SAKE Robotics delivers its grippers with address 1 for Duals and 1 and 2 for Quads and 57kbps.

5) Launch files - 
	`$ roslaunch grasp_configurator glove_driver.launch`
Launches the wearable driver and dynamic reconfigure packages
	  
	`$ roslaunch vision_command glove_vision.launch`
Launches the camera node and gesture classification system
	  
	`$ roslaunch gripper_controller gripper_controller.launch`
Launches the gripper controller

## Dynamic Reconfigure

Using ROS dynamic_reconfigure, inputs to the teleoperation system can be given during runtime:

1) **grasp_mode** - selects actuation mode for SUTD Soft gripper ('int'; 0 (Default) - no grasping, 1 - Aperture Mode, 2 - Gripper Mode)
2) **payload_select** - select payload to be grasped ('enum'; Free Grasping (0) for no grasping force limits or Controlled Grasping (non-0) for force limits). Payload force definitions can be defined in scripts/payload.py
3) **hold_pressure** - sets pressure command to the previous available pressure command sent by gesture system ('bool')
4) **override_pressure** - allows manual override of gripper using dynamic_reconfigure ('bool')

## TroubleShooting

Serial connection issues:

	Error message: permission denied (get accurate error message).  This indicates the user does not have privellages to use the /dev/ttyUSBx.  The solution is to add the <user> to the "dialout" group.  After executing the following command, reboot.
	$ sudo adduser <user> dialout
	reboot

CVbridge issues: Download and compile cv_bridge in another workspace using `catkin build` according to [this guide](https://cyaninfinite.com/ros-cv-bridge-with-python-3/). Add the `source $[CATKIN_BUILD_WORKSPACE]/devel/setup.bash` to your `~/.bashrc` for convenience.
