#! /usr/bin/python3
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from compass import Compass
from signal import pause
import subprocess
import sys
import time

def adjust_orientation(orientation):
  pitch = adjust_degrees(orientation["pitch"])
  roll = adjust_degrees(orientation["roll"])
  yaw = adjust_degrees(orientation["yaw"])
  return {"pitch": pitch, "roll": roll, "yaw": yaw}

def adjust_degrees(degrees):
 return degrees if degrees <= 180 else degrees - 360

def get_cpu_temp():
  cpu_temp_string = subprocess.check_output("vcgencmd measure_temp", shell=True).decode()
  title_and_temp = cpu_temp_string.split("=")
  temp_and_unit = title_and_temp[1].split("'")
  return float(temp_and_unit[0])

sense = SenseHat()
compass = Compass()
#sense.set_rotation(180)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

def pushed_up(event):
    if event.action == ACTION_RELEASED:
      #print("up released")
      compass.show()
      
def pushed_down(event):
    if event.action == ACTION_RELEASED:
      #print("down released")
      
      temperature_humidity_sensor = sense.get_temperature_from_humidity()
      temperature_pressure_sensor = sense.get_temperature_from_pressure()
      cpu_temp = get_cpu_temp()
      temperature_calibrated = temperature_humidity_sensor - ((cpu_temp - temperature_humidity_sensor)*1.3)
      humidity = sense.get_humidity()
      pressure = sense.get_pressure()
      orientation = adjust_orientation(sense.get_orientation())
      timestamp = time.time()

      #print("{} temperature from humidity sensor: {:.1f} C".format(timestamp, temperature_humidity_sensor))
      #print("{} temperature from humidity sensor calibrated: {:.1f} C".format(timestamp, temperature_calibrated))
      #print("{} temperature from pressure sensor: {:.1f} C".format(timestamp, temperature_pressure_sensor))
      #print("{} humidity: {:.1f}".format(timestamp, humidity))
      #print("pitch: {:.2f}, roll: {:.2f}, yaw: {:.1f}".format(orientation["pitch"], orientation["roll"], orientation["yaw"]))
      #sys.stdout.flush()
      sense.show_message("T:{:.1f} C".format(temperature_humidity_sensor), text_colour=red)
      sense.show_message("CPU/T:{:.1f} C".format(cpu_temp), text_colour=red)
      sense.show_message("H:{:.1f}".format(humidity), text_colour=blue)
      sense.show_message("P:{:.1f}".format(pressure), text_colour=green)

def pushed_left(event):
    if event.action == ACTION_RELEASED:
      print("left released")     

def pushed_right(event):
    if event.action == ACTION_RELEASED:
      print("right released")

sense.stick.direction_up = pushed_up
sense.stick.direction_down = pushed_down
sense.stick.direction_left = pushed_left
sense.stick.direction_right = pushed_right
pause()

