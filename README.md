# gripper_teleop
ROS Packages for the SUTD Gripper teleoperation. Consists of 3 main modules:

1) Gripper driver : for acquiring gripper sensor data and sending vacuum commands

2) CNN-based classification package : classifies input gesture image to 9 gripper command classes

3) Wearable driver : interfaces with driver and sends force information for operator feedback

# Requirements
- Ubuntu 18.04
- ROS Melodic
- OpenCV
- Tensorflow2
- Python 3.7
- Other dependencies: matplotlib, sklearn, numpy

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

5) Launch the node - example launch files to support various EZGripper configurations.  

	$ roslaunch ezgripper_driver joy.launch
	  // joy.launch is configured for a single servo gripper (dual) and the USB interface
	  
	$ roslaunch ezgripper_driver joy2.launch
	  // joy2.launch is configured for two independent servos (quad independent) and the USB interface
	  
	$ roslaunch ezgripper_driver joy2sync.launch
	  // joy2sync.launch controls two servos as if it were a single servo (quad dependent) and the USB interface
	  
	$ roslaunch ezgripper_driver joy_tcp.launch
	  // joy_tcp.launch controls a single servo via TCP instead of USB
	
## Dynamic Reconfigure

Using ROS dynamic_reconfigure, inputs to the teleoperation system can be given during runtime:

1) grasp_mode - selects actuation mode for SUTD Soft gripper


## TroubleShooting

Serial connection issues:

	Error message: 'Serial' object has no attribute 'setParity'  --- this message indicates you have a new version of serial library that causes issues.  Do the following command to load an older pySerial library.
	$ sudo pip install "pySerial>=2.0,<=2.9999"
	
	Error message: permission denied (get accurate error message).  This indicates the user does not have privellages to use the /dev/ttyUSBx.  The solution is to add the <user> to the "dialout" group.  After executing the following command, reboot.
	$ sudo adduser <user> dialout
	reboot
