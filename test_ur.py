import rtde_control
import rtde_receive
import time

rtde_c = rtde_control.RTDEControlInterface("192.168.56.101")
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.56.101")
init_q = rtde_r.getActualQ()


time.sleep(0.2)
# Stop the movement before it reaches new_q

# Target in the Z-Axis of the TCP
target = rtde_r.getTargetTCPPose()
print("get:\n")
print(target)

target[2] += 0.05
print(target)


# Move asynchronously in cartesian space to target, we specify asynchronous behavior by setting the async parameter to
# 'True'. Try to set the async parameter to 'False' to observe a default synchronous movement, which cannot be stopped
# by the stopL function due to the blocking behaviour.
# rtde_c.moveL(target, 0.25, 0.5, True)
# time.sleep(1.2)
# # Stop the movement before it reaches target
# rtde_c.stopL(0.5)


# Stop the RTDE control script
# rtde_c.stopScript()