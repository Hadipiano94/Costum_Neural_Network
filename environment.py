from data import *


class World:
    def __init__(self):
        self.pixels_list = []
        for xcor in range(0, WORLD_WIDTH):
            column_list = []
            for ycor in range(0, WORLD_HEIGHT):
                pixel = Pixel((xcor, ycor))
                column_list.append(pixel)
            self.pixels_list.append(column_list)


class Pixel:
    # by is either "creature" or "obstacle"
    def __init__(self, position, available=True, by=None):
        self.position = position
        self.available = available
        self.occupied_by = by
