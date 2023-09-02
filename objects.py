import turtle as tr
from random import randint
from data import *


class Creature(tr.Turtle):
    def __init__(self, brain, color=None, speed=None, position=None):
        super().__init__()
        self.object_type = "creature"
        self.shape("pixel")
        self.penup()
        self.brain = brain

        if color is None:
            color = self.brain.color
        else:
            color = color_dict[color]
        self.color(color)

        if self.brain.is_positioned:
            position = self.brain.position
        else:
            if position is None:
                position = (randint(0, WORLD_WIDTH - 1), randint(0, WORLD_HEIGHT - 1))
        self.position = position

        # for any turtle movement we need to translate the position using turtle_position_dict
        turtle_position = turtle_position_dict[self.position]
        self.goto(x=turtle_position[0], y=turtle_position[1])

        # self.speed is not turtle's speed method, because we use tracer on screen.
        # it is how many moves turtle can make in one world move.
        if self.brain.speed is not None:
            speed = self.brain.speed
        else:
            if speed is None:
                # 1 move per 1 world move
                speed = 1
        self.speed = speed

    def move(self, possible_pixels_list):
        # move: new_position comes from the brain
        new_position = self.brain.think(possible_pixels_list)
        # update creature position
        self.position = new_position
        turtle_new_position = turtle_position_dict[new_position]
        self.goto(x=turtle_new_position[0], y=turtle_new_position[1])
        return


class Obstacle(tr.Turtle):
    def __init__(self, position, obstacle_name: str, orientation=0):
        # orientation in degrees relative to the horizontal right line
        # orientation doesn't work for now
        super().__init__()
        self.object_type = "obstacle"
        self.name = obstacle_name
        self.shape(obstacle_name)
        self.position = position
        self.setheading(orientation)
        self.pixels_positions_list = []
        width = int(self.name.split(sep="x")[0])
        height = int(self.name.split(sep="x")[1])
        for xcor in range(width):
            for ycor in range(height):
                self.pixels_positions_list.append((self.position[0] + xcor, self.position[1] + ycor))
        self.penup()
        self.hideturtle()

        # for any turtle movement we need to translate the position using turtle_position_dict
        turtle_position = turtle_position_dict[self.position]
        self.goto(x=turtle_position[0], y=turtle_position[1])
        self.showturtle()
