#!/usr/bin/env python

# import the necessary packages
# from imutils.video import VideoStream
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

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str,
	default="DICT_ARUCO_ORIGINAL",
	help="type of ArUCo tag to detect")
args = vars(ap.parse_args())

# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
#	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
#	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
#	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
#	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

# verify that the supplied ArUCo tag exists and is supported by
# OpenCV
if ARUCO_DICT.get(args["type"], None) is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(
		args["type"]))
	sys.exit(0)

# load the ArUCo dictionary and grab the ArUCo parameters
print("[INFO] detecting '{}' tags...".format(args["type"]))
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters_create()

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
#vs = VideoStream(src=0).start() # change camera
#cap=cv2.VideoCapture(1)

#time.sleep(2.0)

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 600 pixels
	#frame = vs.read()
	#frame = imutils.resize(frame, width=1000)
	
	frames = pipeline.wait_for_frames()
	# 深度与颜色对齐
	aligned_frames = align.process(frames)
        # 获得相机内参
        # profile = aligned_frames.get_profile()
        #intrinsics = profile.as_video_stream_profile().get_intrinsics()
        #pinhole_camera_intrinsic = o3d.camera.PinholeCameraIntrinsic(
        #    intrinsics.width, intrinsics.height, intrinsics.fx, intrinsics.fy, intrinsics.ppx, intrinsics.ppy)

        # 获得对齐的帧
	depth_frame = aligned_frames.get_depth_frame()
	color_frame = aligned_frames.get_color_frame()
	frame = np.asanyarray(color_frame.get_data())
	h,w,_=frame.shape

    # detect ArUco markers in the input frame
	(corners, ids, rejected) = cv2.aruco.detectMarkers(frame,
		arucoDict, parameters=arucoParams)

	# verify *at least* one ArUco marker was detected
	if len(corners) > 0:
		# flatten the ArUco IDs list
		ids = ids.flatten()

		# loop over the detected ArUCo corners
		for (markerCorner, markerID) in zip(corners, ids):
			# extract the marker corners (which are always returned
			# in top-left, top-right, bottom-right, and bottom-left
			# order)
			corners = markerCorner.reshape((4, 2))
			(topLeft, topRight, bottomRight, bottomLeft) = corners

			# convert each of the (x, y)-coordinate pairs to integers
			topRight = (int(topRight[0]), int(topRight[1]))
			bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
			bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
			topLeft = (int(topLeft[0]), int(topLeft[1]))

			# draw the bounding box of the ArUCo detection
			cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
			cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
			cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
			cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)

			# compute and draw the center (x, y)-coordinates of the
			# ArUco marker
			cX = int((topLeft[0] + bottomRight[0]) / 2.0)
			cY = int((topLeft[1] + bottomRight[1]) / 2.0)
			cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)

			# draw the ArUco marker ID on the frame
			cv2.putText(frame, str(markerID)+"_("+str(cX)+","+str(cY)+")",
				(topLeft[0], topLeft[1] - 15),
				cv2.FONT_HERSHEY_SIMPLEX,
				0.5, (0, 255, 0), 2)
				
			tx=-(cX-w/2)
			# 基于竖直平面
			#ty=(bottomRight[0]-topLeft[0])-50
			# 基于水平面
			ty=(cY-h/2)
			
			
			tz=-(cY-h/2)
			
			if abs(tx)<30:
				tx=0
			if abs(ty)<30:
				ty=0
			if abs(tz)<30:
				tz=0
			k=1000
			tx=tx/k
			ty=ty/k
			tz=tz/k
			
			cv2.putText(frame, "move_("+str(tx)+","+str(ty)+","+str(tz)+")",
				(20, 20),
				cv2.FONT_HERSHEY_SIMPLEX,
				0.5, (255, 0, 0), 2)
		
		if tx==0:
			x_=0
		elif tx != 0:
			x_=tx/abs(tx)/50
			
		if ty==0:
			y_=0
		elif ty!=0:
			y_=ty/abs(ty)/50
		
		target[0]+=x_
		target[1]+=y_
		#target[2]+=tz
		
		rtde_c.moveL(target, 0.25, 0.5, True)
		time.sleep(1)
		# Stop the movement before it reaches target
		#rtde_c.stopL(0.5)
		
	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF


	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
# Stop the RTDE control script
rtde_c.stopScript()
#vs.stop()
