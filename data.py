

WORLD_WIDTH = 500
WORLD_HEIGHT = 500
WINDOW_EDGE = 20
WINDOW_WIDTH = WORLD_WIDTH + WINDOW_EDGE * 2
WINDOW_HEIGHT = WORLD_HEIGHT + WINDOW_EDGE * 2

NUMBER_OF_CREATURES = 100
GENERATION_MOVES = 500
GENERATION_NUMBER = 100
REDEMPTION_AREA = {
    "location": (400, 0),
    "size": (100, 100)
}
GENERATION_HARDENER_CONSTANT = 2
MUTATED_CELL_CONSTANT = 0.00
POPULATION_LIMIT = 100
# in seconds
MOVE_TIME = 0.01

# the main location of every rectangle (including "pixel")
# is on the far left upper point of it. for circles, it's the center.
pixel_latitude = ((0, 0), (1, 0), (1, 1), (0, 1))

obstacles_list = [
    {"name": "1x100", "latitude": ((0, 0), (100, 0), (100, 1), (0, 1))},
    {"name": "100x100", "latitude": ((0, 0), (100, 0), (100, 100), (0, 100))},
    {"name": "100x1", "latitude": ((0, 0), (1, 0), (1, 100), (0, 100))},
]

# maze_obstacle = [
#     Obstacle((150, 300), "1x100"),
#     Obstacle((100, 250), "1x100"),
#     Obstacle((100, 300), "100x1"),
#     Obstacle((200, 350), "1x100"),
# ]

# my pixel system starts from top left pixel and the first pixel is (0, 0)
turtle_position_dict = {}
for x in range(WORLD_WIDTH):
    for y in range(WORLD_HEIGHT):
        turtle_position_dict[(x, y)] = (-WORLD_WIDTH//2 + x, WORLD_HEIGHT//2 - y)

cell_type_list = [
    "n",
    "n-1",
    "n+1",
    "n//2",
    "n>4-0,n<=4-1",
    "n<4-0,n>=4-1",
    "n<4-n>4,n>4-n<4",
    "abs(n-9)",
    "abs(n-7)",
    "abs(n-5)",
    "abs(n-2)",
    "0",
    "1",
    "1-0,0-1",
    "--0,+-1",
]

possible_pixels_address_list = [
    (0, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0)
]

color_dict = {
    "black": "black",
    "green": "#19A44E",
    "blue": "#2059C3",
    "red": "#CB2525",
    "yellow": "#E5C904",
    "purple": "#C203BA",
    "orange": "#FF7800",
    "firouz": "#03B4C2"
}
