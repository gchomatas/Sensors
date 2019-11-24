class SensorReadings:

  def __init__(self, sense_hat):
    self.temprerature_humidity_sensor = sense_hat.get_temperature_from_humidity()
    self.temperature_pressure_sensor = sense_hat.get_temperature_from_pressure()
    self.humidity = sense_hat.get_humidity()
    self.pressure = sense_hat.get_pressure()

  def printReadings(self):
    print("temperature from humidity sensor: {} C".format(self.temprerature_humidity_sensor))
    print("temperature from pressure sensor: {} C".format(self.temperature_pressure_sensor))
    print("humidity: {}".format(self.humidity))
    print("pressure: {}".format(self.pressure))

  def display(self, sense_hat):
    sense_hat.show_message("T:{:.1f} C".format(self.temprerature_humidity_sensor), text_colour=red)
    sense_hat.show_message("H:{:.1f}".format(self.humidity), text_colour=blue)
    sense_hat.show_message("P:{:.2f}".format(self.pressure), text_colour=green)

  def getAsMap(self):
    return {"temperature_humidity_sensor": self.temprerature_humidity_sensor, "temperature_pressure_sensor": self.temperature_pressure_sensor, "humidity": self.humidity, "pressure": self.pressure}
