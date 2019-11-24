from enum import Enum
from sense_hat import SenseHat

class Compass:
  class Direction(Enum):
    N = 1
    NE = 2
    E = 3
    SE = 4
    S = 5
    SW = 6
    W = 7
    NW = 8

  direction_ranges = {
    Direction.N: (337.5, 360),
    Direction.N: (0, 22.5), 
    Direction.NE: (22.5, 67.5), 
    Direction.E: (67.5, 112.5), 
    Direction.SE: (112.5, 157.5),
    Direction.S: (157.5, 202.5),
    Direction.SW: (202.5, 247.5),
    Direction.W: (247.5, 292.5),
    Direction.NW: (292.5, 337.5)
  }

  direction_colors = {
    Direction.N: (0, 0, 255),
    Direction.NE: (255, 255, 0),
    Direction.E: (0, 255, 0),
    Direction.SE: (0, 255, 0),
    Direction.S: (255, 0, 0),
    Direction.SW: (255, 255, 0),
    Direction.W: (255, 255, 255),
    Direction.NW: (255, 255, 255)
  }

  def isWithinRange(self, degrees, range):
    return range[0] <= degrees < range[1]

  def show(self):  
    sense_hat = SenseHat()

    degrees_from_north = sense_hat.get_compass()
    
    direction = self.Direction.N
  
    for direction, range in self.direction_ranges.items(): 
      if self.isWithinRange(degrees_from_north, range):
        direction = direction
        break;
    
    degrees_180 = degrees_from_north if degrees_from_north <= 180 else degrees_from_north - 360 
    # print(degrees_from_north, direction.name, self.direction_colors[direction])
    sense_hat.show_message("{} {:.1f}".format(direction.name, degrees_180), text_colour=self.direction_colors[direction])

