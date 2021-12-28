#! /usr/bin/env python3

#linear.x = 앞+,뒤-
#linear.y = 속도??
#linear.z = 오른쪽 바퀴
#angular.x = 없음
#angular.y = 없음
#angular.z = 왼쪽+ , 오른쪽-
from numpy.core.numeric import count_nonzero
from geometry_msgs import msg
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np
import time, math

def callback(data):
    con = Twist()
    pub.publish(con)
    go_ranges = data.ranges[0:10]
    left_ranges = data.ranges[85:95]
    right_ranges = data.ranges[265:275]


    w_point = np.array(go_ranges)
    l_point = np.array(left_ranges)
    r_point = np.array(right_ranges)

    w = np.count_nonzero(w_point >= 0.2)
    l = np.count_nonzero(l_point >= 0.22)
    r = np.count_nonzero(r_point >= 0.2)
    print(w, l, r)

    if w > 0.0 :
        con.angular.z = 0.0
        con.linear.x = 0.2
        pub.publish(con)
        if l == 0:
            con.angular.z = 0
            pub.publish(con)

        if r == 0:
            con.angular.z = 0
            pub.publish(con)
        else :
            pass

    elif w == 0:
        if l == 0:
                relative_angle = math.radians(47)
                angular_speed = -1.0 
                duration = relative_angle / abs(angular_speed)
                time2end = rospy.Time.now() + rospy.Duration(duration)
                con.angular.z = angular_speed
                while rospy.Time.now() < time2end:
                    pub.publish(con)
                # rospy.sleep(1)
                con.linear.x = 0.0
                con.angular.z = 0.0
        elif w == 0:
            if r == 0:
                relative_angle = math.radians(47)
                angular_speed = 1.0
                duration = relative_angle / abs(angular_speed)
                time2end = rospy.Time.now() + rospy.Duration(duration)
                con.angular.z = angular_speed
                while rospy.Time.now() < time2end:
                    pub.publish(con)
                # rospy.sleep(1)
                con.linear.x = 0.0
                con.angular.z = 0.0
        else :
            con.linear.x = 0.0
        pub.publish(con)

if __name__ == '__main__':
    rospy.init_node('parking')
    sub = rospy.Subscriber('/scan', LaserScan, callback)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rospy.spin()
