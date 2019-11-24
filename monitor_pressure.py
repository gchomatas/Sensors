#!/usr/bin/python3

from sense_hat import SenseHat
import os
import time

class SensorReadings:

  def __init__(self, sense_hat):
    self.temprerature_humidity_sensor = sense_hat.get_temperature_from_humidity()
    self.temperature_pressure_sensor = sense_hat.get_temperature_from_pressure()
    self.humidity = sense_hat.get_humidity()
    self.pressure = sense_hat.get_pressure()

  def print(self):
    print("temperature from humidity sensor: {} C".format(self.temprerature_humidity_sensor))
    print("temperature from pressure sensor: {} C".format(self.temperature_pressure_sensor))
    print("humidity: {}".format(self.humidity))
    print("pressure: {}".format(self.pressure))

  def display(self, sense_hat):
    sense_hat.show_message("T:{:.1f} C".format(self.temprerature_humidity_sensor), text_colour=red)
    sense_hat.show_message("H:{:.1f}".format(self.humidity), text_colour=blue)
    sense_hat.show_message("P:{:.2f}".format(self.pressure), text_colour=green)


class SensorDataPersister:
  PRESSURE_READINGS_FILENAME = 'pressure.csv'
  TEMPERATURE_READINGS_FILENAME = 'temperature.csv'

  def __init__(self, sensor_data_dir):
    self.sensor_data_dir = sensor_data_dir
    self.pressure_readings_file_path = os.path.join(self.sensor_data_dir, self.PRESSURE_READINGS_FILENAME)

  def write_pressure(self, sensor_readings):
    with open(self.pressure_readings_file_path, "a") as pressure_data:
      pressure_data.write("{} {}\n".format(int(time.time() * 1000), sensor_readings.pressure))
 
  def write_changed_pressure(self, sensor_readings_previous, sensor_readings_next, tolerance):
    pressure_previous = sensor_readings_previous.pressure
    pressure_next = sensor_readings_next.pressure
    
    if (not self.isclose(pressure_previous, pressure_next, tolerance)):
      with open(self.pressure_readings_file_path, "a") as pressure_data:
        pressure_data.write("{} {}\n".format(int(time.time() * 1000), sensor_readings_next.pressure))
        return True
    
    return False
  
  def isclose(self, reading_a, reading_b, tolerance):
    print(abs(reading_a - reading_b))
    return abs(reading_a - reading_b) <= tolerance

sense_hat = SenseHat()
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
sensor_data_persister = SensorDataPersister("/home/pi/sense-hat-examples/python-sense-hat/SensorData")

sensor_readings_previous = SensorReadings(sense_hat)
sensor_data_persister.write_pressure(sensor_readings_previous)

while True:
  sensor_readings_next = SensorReadings(sense_hat)
  sensor_readings_next.print()

  if (sensor_data_persister.write_changed_pressure(sensor_readings_previous, sensor_readings_next, 0.1)):
    sensor_readings_next.display(sense_hat)
    sensor_readings_previous = sensor_readings_next
  
  time.sleep(30)


