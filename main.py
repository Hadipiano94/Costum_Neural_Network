import turtle as tr
from tkinter import messagebox
import _tkinter
from time import sleep
from datetime import datetime
from data import *
from objects import Creature, Obstacle
from environment import World
from brain import Brain, Cell
from other import Writer
from random import randint, choice


"""Functions-------------------------------------------------------------------------------------------"""


def update_environment(position, available: bool, by=None):
    world.pixels_list[position[0]][position[1]].available = available
    world.pixels_list[position[0]][position[1]].occupied_by = by


def possible_pixels_list_maker(position):
    possible_pixels_list = []
    for (w, h) in possible_pixels_address_list:
        try:
            if world.pixels_list[position[0] + w][position[1] + h].available \
                    and position[0] + w >= 0 \
                    and position[1] + h >= 0:
                possible_pixels_list.append(world.pixels_list[position[0] + w][position[1] + h])
        except IndexError:
            pass
    return possible_pixels_list


def reset_environment():
    global world
    for column in world.pixels_list:
        for pixel in column:
            pixel.available = True
            pixel.occupied_by = None
    return


def delete_creatures():
    global creatures_list
    creatures_list.clear()
    return


def delete_obstacles():
    global world_obstacles
    world_obstacles.clear()
    return


"""Setting Up the Screen and make all the Creatures and Obstacles--------------------------------------"""


# try is for cases you close the window in the middle of the operation,
# so that tkinter doesn't raise an exception
try:
    # making the screen and registering pixel and obstacles shapes
    screen = tr.Screen()
    screen.setup(
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        startx=100,
        starty=50
    )
    screen.register_shape("pixel", pixel_latitude)
    for obstacle in obstacles_list:
        screen.register_shape(obstacle["name"], obstacle["latitude"])

    screen.tracer(0)

    # make the environment (the world)
    world = World()

    # to give them to the next generation
    chosen_previous_generation_brains_list = []

    creatures_list = []
    world_obstacles = []
    redemption_area_copy = REDEMPTION_AREA.copy()

    # start of the generation
    generation_count = 1
    while generation_count <= GENERATION_NUMBER:

        reset_environment()
        delete_creatures()
        delete_obstacles()
        screen.clear()
        screen.tracer(0)

        # check for the last generation's information for creating new creatures
        if generation_count == 1:
            # make new creatures and update the environment
            for i in range(NUMBER_OF_CREATURES):
                creature = Creature(
                    brain=Brain(
                        cells_number=5,
                        connections_number=3,
                    ),
                    # speed=randint(1, 2),
                )
                update_environment(creature.position, available=False, by="creature")
                creatures_list.append(creature)
        else:
            for brain in chosen_previous_generation_brains_list:
                for _ in range(brain.reproduction):
                    creature = Creature(
                        brain=brain.copy(),
                        speed=brain.speed,
                    )
                    update_environment(creature.position, available=False, by="creature")
                    creatures_list.append(creature)

            for _ in range(int(len(creatures_list) * MUTATED_CELL_CONSTANT)):

                old_brain = choice(chosen_previous_generation_brains_list)
                new_brain = old_brain.copy()

                # modifications
                new_brain.cells_number += 1
                new_brain.cells_list.append(Cell(
                    cell_type=choice(cell_type_list),
                    cell_index=len(old_brain.cells_list))
                )
                new_brain.connections_number += 1
                new_brain.connections_list.append(
                    (
                        randint(0, old_brain.cells_number),
                        randint(0, old_brain.cells_number)
                    )
                )
                new_brain.reproduction += 1

                new_speed = old_brain.speed

                creature = Creature(
                    brain=new_brain,
                    speed=new_speed,
                )
                update_environment(creature.position, available=False, by="creature")
                creatures_list.append(creature)

        if len(creatures_list) > POPULATION_LIMIT:
            for _ in range(len(creatures_list) - POPULATION_LIMIT):
                # randomly choosing the victim
                poor_creature = creatures_list[randint(0, len(creatures_list) - 1)]
                # make it invisible
                poor_creature.hideturtle()
                # send it away!
                poor_creature.goto(-WORLD_WIDTH//2 - 20, -WORLD_HEIGHT//2)
                # clear its place
                update_environment(poor_creature.position, available=True, by=None)
                # remove it from creatures_list
                creatures_list.remove(poor_creature)

        # make obstacles and update environment.
        # remember, position is the top left point of the object.
        world_obstacles = [
            # Obstacle((150, 300), "1x100"),
            # Obstacle((100, 250), "1x100"),
            # Obstacle((100, 300), "100x1"),
            # Obstacle((200, 350), "1x100"),
        ]
        for obstacle in world_obstacles:
            for pixel_position in obstacle.pixels_positions_list:
                update_environment(pixel_position, available=False, by="obstacle")

        # draw world's borderline and texts
        writer = Writer()
        writer.draw_border()
        writer.write_info(
            generation_count,
            len(creatures_list),
            int(sum([brain.reproduction for brain
                     in chosen_previous_generation_brains_list]) * MUTATED_CELL_CONSTANT),
            len(chosen_previous_generation_brains_list)
        )
        writer.draw_redemption_area(redemption_area_copy)

        # show everything
        screen.update()

        # move creatures
        move_count = 0
        while move_count < GENERATION_MOVES:
            start_time = datetime.now().time()
            start_second = start_time.second
            start_microsecond = start_time.microsecond / 1000000
            for creature in creatures_list:
                for _ in range(creature.speed):
                    # make previous position available in the environment
                    update_environment(creature.position, available=True, by=None)
                    # creature moves and gets a new position
                    creature.move(possible_pixels_list_maker(creature.position))
                    update_environment(creature.position, available=False, by="creature")
            move_count += 1
            end_time = datetime.now().time()
            end_second = end_time.second
            end_microsecond = end_time.microsecond / 1000000
            sleep_time = MOVE_TIME - ((end_second - start_second) + (end_microsecond - start_microsecond))
            if sleep_time < 0:
                sleep_time = 0
            sleep(sleep_time)
            # show the move
            screen.update()

        # collecting the survived brains for the next generation
        chosen_previous_generation_brains_list.clear()
        for creature in creatures_list:
            if redemption_area_copy["location"][0] <= creature.position[0] <= redemption_area_copy["location"][0] + redemption_area_copy["size"][0] \
                    and redemption_area_copy["location"][1] <= creature.position[1] <= redemption_area_copy["location"][1] + redemption_area_copy["size"][1]:
                creature.brain.speed = creature.speed
                chosen_previous_generation_brains_list.append(creature.brain.copy())

        generation_count += 1

        # extinction
        start_over = False
        if not chosen_previous_generation_brains_list:
            writer.write_extinct()
            if messagebox.askyesno("Start Over?", "Do you want to start a new World?"):
                generation_count = 1
                start_over = True
            else:
                raise SystemExit

        if not start_over:
            # to reduce the chance of survival
            if redemption_area_copy["size"][0] > GENERATION_HARDENER_CONSTANT \
                    and redemption_area_copy["size"][1] > GENERATION_HARDENER_CONSTANT:
                redemption_area_copy["size"] = (
                    redemption_area_copy["size"][0] - GENERATION_HARDENER_CONSTANT,
                    redemption_area_copy["size"][1] - GENERATION_HARDENER_CONSTANT
                )
                redemption_area_copy["location"] = (
                    redemption_area_copy["location"][0] + GENERATION_HARDENER_CONSTANT,
                    redemption_area_copy["location"][1]
                )
            writer.write_next_generation()

        else:
            redemption_area_copy = REDEMPTION_AREA.copy()

        sleep(1)

    screen.mainloop()

# in case you close the window
except tr.Terminator:
    pass
except _tkinter.TclError:
    pass
