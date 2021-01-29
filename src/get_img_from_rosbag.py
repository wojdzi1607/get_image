#!/usr/bin/python

PKG = 'get_image'
import roslib; roslib.load_manifest(PKG)
import rosbag
import rospy
import cv2 as cv
from cv_bridge import CvBridge, CvBridgeError
import os
import sys

class ImageCreator():
    def __init__(self):
        if len(sys.argv) < 3:
            save_dir = str('/home/legion/catkin_ws/from_script/')
            filename = str('/home/legion/catkin_ws/2020-12-15-11-55-34.bag')
            rospy.loginfo("Bag filename = %s", filename)
        else:
            save_dir = os.path.join(sys.path[0], sys.argv[1])
            filename = os.path.join(sys.path[0], sys.argv[2])
            rospy.loginfo("Bag filename = %s", filename)

        self.bridge = CvBridge()

        # Open bag file.
        with rosbag.Bag(filename, 'r') as bag:
            timestr_last = 0
            for topic, msg, t in bag.read_messages():
                # if topic == "/cv_camera/image_raw": # topic na robocie w M321
                if topic == "/usb_cam/image_raw":
                    try:
                        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
                    except CvBridgeError, e:
                        print(e)

                    timestr = int("%.0f" % msg.header.stamp.to_sec())
                    if timestr != timestr_last:
                        image_name = str(save_dir) + str(timestr) + ".png"
                        print('save ', image_name)
                        cv.imwrite(image_name, cv_image)
                    timestr_last = timestr

def main():
    rospy.init_node(PKG)
    try:
        image_creator = ImageCreator()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()