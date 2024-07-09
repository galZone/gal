import argparse
import imutils
import time
import cv2
import sys
import pyrealsense2 as rs
import numpy as np

import rtde_control
import rtde_receive
import time

# ur connect
rtde_c = rtde_control.RTDEControlInterface("192.168.1.101")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.1.101")
init_q = rtde_r.getActualQ()

time.sleep(0.2)


init_pose1=[0.01380, -0.55444, 0.47962, -0.017976, -3.06226, 0.14979]
rtde_c.moveL(init_pose1, 0.25, 0.5, True)
time.sleep(3)

# Target in the Z-Axis of the TCP
target = rtde_r.getActualTCPPose()

# realsense connect
pipeline=rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
# 设置对齐对象，让Depth对齐RGB
align_to = rs.stream.color
align =  rs.align(align_to)

# start streaming
pipeline.start(config)

