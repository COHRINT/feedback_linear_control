#!/usr/bin/env python3

from nav_msgs.msg import Odometry
import rospy
import numpy as np
from std_msgs.msg import Float64



class FLController:
	def __init__(self):

		self.measurment = np.array([0.0,0.0,0.0,0.0])	#measurment will be an array of [x,y,x_dot,y_dot]

		rospy.Subscriber("measurement_test",Odometry,self.measurment_callback)

		self.left_pub = rospy.Publisher("left_wheel_vel_cmd",Float64, queue_size=10)
		self.right_pub = rospy.Publisher("right_wheel_vel_cmd",Float64, queue_size=10)

		self.controller()


	
	def measurment_callback(self,msg):
		self.measurment[0] = msg.pose.pose.position.x
		self.measurment[1] = msg.pose.pose.position.y
		self.measurment[2] = msg.twist.twist.linear.x
		self.measurment[3] = msg.twist.twist.linear.y


	
	def controller(self):

		rate = rospy.Rate(100)			#change this depending on what rate you want your controller to run at. Number is in Hz

		while not rospy.is_shutdown():
			
			left_vel = 0.0
			right_vel = 0.0


			#TODO: Your controller code here


			self.left_pub.publish(left_vel)
			self.right_pub.publish(right_vel)
			rate.sleep()


if __name__=="__main__":
	rospy.init_node("feedback_linear_control")

	FLController()


		