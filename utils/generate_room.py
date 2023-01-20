import random

rooms = {}


def roomgeneration(room_amount):

  Room(None, 0, 0)    # Create start room
  last_room = None

  for i in range(room_amount * 2):  # Generate x rooms
    _, current_room = random.choice(list(rooms.items()))  # Select random room

    for j in range(5):  # 5 attempts per room
      x = current_room.x + random.randint(-1, 1)
      if x == current_room.x:
        y = current_room.y + random.randint(-1, 1)
      else:
        y = 0  # Prevent diagonals

      # Check if room exist
      if (x, y) in rooms:
        continue

      last_room = Room(current_room, x, y)

  # Print map
  for y in range(-10, 10):
    for x in range(-10, 10):
      if x == 0 and y == 0:
        print("0", end="")
      elif last_room.x == x and last_room.y == y:
        print("M", end="")
      else:
        if (x, y) in rooms:
          print("X", end="")
        else:
          print(" ", end="")

    print("")

  printed_room = last_room
  path_list = []
  while printed_room != None:
    path_list.append((printed_room.x, printed_room.y))
    printed_room = printed_room.previous

  return rooms, last_room

  """"
  # Print path
  for y in range(-10, 10):
    for x in range(-10, 10):
      print("0", end="")
      elif last_room.x == x and last_room.y == y:
        print("M", end="")
      elif (x, y) in path_list:
        print("X", end="")
      else:
        print(" ", end="")

    print("")
"""

class Room:
  def __init__(self, previous, x, y):
    self.previous = previous
    self.x = x
    self.y = y
    self.visited = False
    # if [self.x, self.y] != [0, 0]:
    room_rng = random.randint(1, 10)
    if room_rng == 1:
        self.contains = "trap"
    if 2 <= room_rng <= 4:
        self.contains = "chest"
    if room_rng >= 5:
        self.contains = "monster"
    if self.x == 0:
      if self.y == 0:
        self.contains = None
    rooms[(x, y)] = self  # Add to rooms dictionary
    # else:
      # self.contains = None
   
