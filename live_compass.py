#! /usr/bin/python3

from enum import Enum
from sense_hat import SenseHat

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

sense_hat = SenseHat()

def isWithinRange(degrees, range):
 return range[0] <= degrees < range[1]

old_direction = None

while True:
  degrees_from_north = sense_hat.get_compass()
  direction = Direction.N
  
  for direction, range in direction_ranges.items(): 
    if isWithinRange(degrees_from_north, range):
      direction = direction
      break;
  
  if direction != old_direction:
    #print(degrees_from_north, direction.name, direction_colors[direction])
    sense_hat.show_message(direction.name, text_colour=direction_colors[direction])
    old_direction = direction

