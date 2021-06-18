#!/usr/bin/env python3

import rospy
from gazebo_msgs.srv import GetModelState, GetModelStateRequest
from nav_msgs.msg import Odometry
import numpy as np



class MeasurmentPub:
	def __init__(self):
		rospy.wait_for_service("/gazebo/get_model_state")
		self.get_model_srv = rospy.ServiceProxy(
		"/gazebo/get_model_state", GetModelState
		)
		self.model = GetModelStateRequest()
		self.model.model_name = rospy.get_namespace()[1:-1]		# This assumes namespace is in the format "/jackal_X/"

		self.pos_std = 0.1
		self.vel_std = 0.1

		self.measurment_pub = rospy.Publisher("measurement_test",Odometry,queue_size=10)

		self.run()
	
	def run(self):
		rate = rospy.Rate(100)
		while not rospy.is_shutdown():
			result = self.get_model_srv(self.model)
			o = Odometry()
			o.header.stamp = rospy.get_rostime()
			o.header.frame_id = "map"


			o.pose.pose.position.x = result.pose.position.x + np.random.normal(scale=self.pos_std)
			o.pose.pose.position.y = result.pose.position.y + np.random.normal(scale=self.pos_std)

			o.twist.twist.linear.x = result.twist.linear.x + np.random.normal(scale=self.vel_std)
			o.twist.twist.linear.y = result.twist.linear.y + np.random.normal(scale=self.vel_std)

			self.measurment_pub.publish(o)
			
			rate.sleep()




if __name__ == "__main__":
	rospy.init_node("fake_measurment")

	MeasurmentPub()
