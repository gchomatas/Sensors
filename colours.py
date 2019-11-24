#! /usr/bin/python3

import time
from sense_hat import SenseHat
from enum import Enum

class ColorState(Enum):
  ASC = 1
  DESC = 2
  STABLE_LOW = 3
  STABLE_HIGH = 4

sense = SenseHat()

sense.clear()

r = [255, ColorState.STABLE_HIGH]
g = [0, ColorState.ASC]
b = [0, ColorState.STABLE_LOW]

colors = [r,g,b]
cycles = [0, 0, 0]

def set_next_color():
  for index, color in enumerate(colors):
    if color[1] is ColorState.ASC:
      if color[0] < 255:
        colors[index] = [color[0] + 1, color[1]]
      else:
       colors[index] = [255, ColorState.STABLE_HIGH]
       cycles[index] = cycles[index] + 1
       set_next_descending(index)
    if color[1] is ColorState.DESC:
      if color[0] > 0:
        colors[index] = [color[0] - 1, color[1]]
      else:
       colors[index] = [0, ColorState.STABLE_LOW]
       set_next_ascending(index)

def set_next_descending(next_stable_index):
  index_of_next_descending_color = -1
  max_cycles = cycles[next_stable_index]
  for index, color in enumerate(colors):
    if index is next_stable_index:
      continue
    if color[0] is 255 and cycles[index] <= max_cycles:
      index_of_next_descending_color = index
      max_cycles = cycles[index]
 
  print("next descending: {}".format(index_of_next_descending_color))
  colors[index_of_next_descending_color] = [254, ColorState.DESC]

def set_next_ascending(next_stable_index):
  index_of_next_ascending_color = -1
  max_cycles = cycles[next_stable_index]
  for index, color in enumerate(colors):
    if index is next_stable_index:
      continue
    if color[0] is 0 and cycles[index] <= max_cycles:
      index_of_next_ascending_color = index
      max_cycles = cycles[index]
  
  print("next ascending: {}".format(index_of_next_ascending_color))
  colors[index_of_next_ascending_color] = [1, ColorState.ASC]


while True:
  set_next_color()
  sense.clear([colors[0][0], colors[1][0], colors[2][0]])
  #print([colors[0][0], colors[1][0], colors[2][0]])
  time.sleep(10/1000.0)
