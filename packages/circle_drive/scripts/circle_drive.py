#!/usr/bin/env python3
import sys
import rospy
import numpy as np
from duckietown.dtros import DTROS, NodeType
from duckietown_msgs.msg import Twist2DStamped

class MyNode(DTROS):

    def __init__(self, node_name):
        super(MyNode, self).__init__(node_name=node_name, node_type=NodeType.DEBUG)
        self.pub = rospy.Publisher("~car_cmd", Twist2DStamped, queue_size=1)

    def run(self):
        i = 0

        for _ in range(5):
            msg = Twist2DStamped()
            msg.v = 0.3
            msg.omega = 0.0
            self.pub.publish(msg)

        while not rospy.is_shutdown():
            msg = Twist2DStamped()
            msg.v = 0.2
            msg.omega = 1.6
            rospy.loginfo(f"Publishing message [{i}] -- {msg.omega}")
            self.pub.publish(msg)
            if i == 700:
                break
            i += 1
            sys.stdout.flush()
        msg = Twist2DStamped()
        msg.v = 0.0
        msg.omega = 0.0
        self.pub.publish(msg)

            
    def on_shutdown(self):
        """Shutdown procedure.

        Publishes a zero velocity command at shutdown."""
        msg = Twist2DStamped()
        msg.v = 0.0
        msg.omega = 0.0
        self.pub.publish(msg)

        super(MyNode, self).on_shutdown()

if __name__ == '__main__':
    # create the node
    node = MyNode(node_name='circle_drive_node')
    # run node
    node.run()
    # keep spinning
    rospy.spin()
