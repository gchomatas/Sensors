#!/usr/bin/python3 -u

import time
import quaternion
from  madgwick import MadgwickAHRS

from sense_hat import SenseHat

heading = MadgwickAHRS()
sense = SenseHat()

while True:
  gyro = [value for key,value in sense.get_gyroscope_raw().items()]
  accel = [value for key,value in sense.get_accelerometer_raw().items()]
  compass = [value for key,value in sense.get_compass_raw().items()]
  heading.update(gyro, accel, compass)
  ahrs = heading.quaternion.to_euler_angles()
  roll = ahrs[0]
  pitch = ahrs[1]
  yaw = ahrs[2]
  #(p,r,y) = heading.quaternion.to_euler_angles()
  print(pitch, roll, yaw)
  time.sleep(0.1)

