// ROS node for controlling regulator board for SUTD
// soft gripper

// Author : Snehal Jain

#include <ros.h>
#include <rosserial_arduino/Adc.h>

ros::NodeHandle nh;
rosserial_arduino::Adc adc_msg
ros::Publisher pub("gripper_sensor",&adc_msg);

int senPin[6] = {14,15,16,17,18,19};

int averageSense(int pin){
	int v=0;
	for(int i=0; i<4; i++){
		v+=analogRead(pin);
		return v/4;
	}
}

void setup() {
  // put your setup code here, to run once:
  for (int i=0;i<6;i++){
    pinMode(senPin[i],INPUT);
  }
  pinMode(13, OUTPUT);
  nh.initNode();
  nh.advertise(pub);
}

void loop() {
  // put your main code here, to run repeatedly:
  adc_msg.adc0 = averageSense(senPin[0]);
  adc_msg.adc1 = averageSense(senPin[1]);
  adc_msg.adc2 = averageSense(senPin[2]);
  adc_msg.adc3 = averageSense(senPin[3]);
  adc_msg.adc4 = averageSense(senPin[4]);
  adc_msg.adc5 = averageSense(senPin[5]);

  pub.publish(&adc_msg);
  delay(250);
  nh.spinOnce();
}