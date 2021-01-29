#! /usr/bin/python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

bridge = CvBridge()

def image_callback(msg):

    try:
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError, e:
        print(e)
    else:
        time = msg.header.stamp
        cv2.imwrite('/home/legion/catkin_ws/save_images/'+str(time)+'.png', cv2_img)
        print("Saved an image!")
        rospy.sleep(1)


def main():
    rospy.init_node('image_listener')
    image_topic = "/usb_cam/image_raw"
    # image_topic = "/cv_camera/image_raw" # topic na robocie w M321
    rospy.Subscriber(image_topic, Image, image_callback)
    rospy.spin()

if __name__ == '__main__':
    main()