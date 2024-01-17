import random
class Directions:
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

for i in range(100):
     random.seed(i)
     _directions = {Directions.NORTH: (0, 1),
                   Directions.SOUTH: (0, -1),
                   Directions.EAST:  (1, 0),
                   Directions.WEST:  (-1, 0),
                   Directions.STOP:  (0, 0)}
     _directionsAsList = _directions.items()
     _directionsAsList = sorted(_directionsAsList, key=lambda x:x[0])
     print(list(_directionsAsList))

