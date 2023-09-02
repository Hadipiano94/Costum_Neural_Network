import turtle as tr
from data import *


class Writer(tr.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color("black")
        self.pensize(1)

    def draw_border(self):
        self.goto(-(WORLD_WIDTH//2 + 1), -(WORLD_HEIGHT//2 + 1))
        self.pendown()
        self.goto(-(WORLD_WIDTH//2 + 1), WORLD_HEIGHT//2 + 1)
        self.goto(WORLD_WIDTH//2 + 1, WORLD_HEIGHT//2 + 1)
        self.goto(WORLD_WIDTH//2 + 1, -(WORLD_HEIGHT//2 + 1))
        self.goto(-(WORLD_WIDTH//2 + 1), -(WORLD_HEIGHT//2 + 1))
        # reset
        self.penup()
        self.goto(0, 0)

    def write_info(self, generation_number, creatures_number, mutated_number, survived_brains_number):
        self.goto(-WORLD_WIDTH//2, WORLD_HEIGHT//2 + 3)
        self.write(f"Gen:{generation_number}", font=("Consolas", 9, "bold"))
        self.goto(-WORLD_WIDTH//2 + 55, WORLD_HEIGHT//2 + 3)
        self.write(f"Population:{creatures_number}", font=("Consolas", 9, "bold"))
        self.goto(-WORLD_WIDTH//2 + 180, WORLD_HEIGHT//2 + 3)
        self.write(f"Mutated:{mutated_number}", font=("Consolas", 9, "bold"))
        self.goto(-WORLD_WIDTH // 2 + 270, WORLD_HEIGHT // 2 + 3)
        self.write(f"Survived:{survived_brains_number}", font=("Consolas", 9, "bold"))
        # reset
        self.goto(0, 0)

    def write_extinct(self):
        self.goto(0, 0)
        self.write("EXTINCTED!", align="center", font=("Consolas", 20, "bold"))

    def write_next_generation(self):
        self.goto(0, 0)
        self.write("Next Generation...", align="center", font=("Consolas", 18, "bold"))

    def draw_redemption_area(self, redemption_area):
        turtle_position = turtle_position_dict[redemption_area["location"]]
        self.goto(turtle_position)
        self.color("red")
        self.pendown()
        self.setheading(0)
        self.forward(redemption_area["size"][0])
        self.setheading(270)
        self.forward(redemption_area["size"][1])
        self.setheading(180)
        self.forward(redemption_area["size"][0])
        self.setheading(90)
        self.forward(redemption_area["size"][1])
        # reset
        self.setheading(0)
        self.penup()
        self.pencolor("black")
        self.goto(0, 0)
