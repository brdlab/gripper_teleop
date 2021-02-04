// ROS node for controlling regulator board for SUTD
// soft gripper

// Author : Snehal Jain

#include <ros.h>
#include <std_msgs/UInt16.h>
#include <std_msgs/String.h>

ros::NodeHandle nh;

// Analog Output pins for controlling regulator
int regPin[2] = {10,11};

// Regulator callback function to set voltage
void aperture_cb( const std_msgs::UInt16& cmd_msg)
{
  analogWrite(regPin[0],(cmd_msg.data*255/80));
  digitalWrite(13, HIGH-digitalRead(13));
}

// Regulator callback function to set voltage
void grip_cb( const std_msgs::UInt16& cmd_msg)
{
  analogWrite(regPin[1],(cmd_msg.data*255/80));
  digitalWrite(13, HIGH-digitalRead(13));
}

ros::Subscriber<std_msgs::UInt16> aperture("aperture_pressure", aperture_cb);
ros::Subscriber<std_msgs::UInt16> grip("gripper_pressure",grip_cb);

void setup() {
  // put your setup code here, to run once:
  for (int i=0;i<2;i++){
    pinMode(regPin[i],OUTPUT);
    analogWrite(regPin[i],0);
  }
  nh.initNode();
  nh.subscribe(aperture);
  nh.subscribe(grip);
}

void loop() {
  // put your main code here, to run repeatedly:

  nh.spinOnce();
  delay(500);
}