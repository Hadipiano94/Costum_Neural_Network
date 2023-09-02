from data import *
from random import choice, randint


class Brain:
    def __init__(
            self,
            first_cell=None,
            last_cell=None,
            cells_list=None,
            cells_number=None,
            connections_list=None,
            connections_number=None,
            reproduction=None,
            is_positioned=False,
            color=None
    ):
        self.speed = None
        if color is None:
            self.make_color()
        else:
            self.color = color
        self.is_positioned = is_positioned

        if reproduction is None:
            reproduction = randint(0, 10)
        self.reproduction = reproduction

        self.cells_number = cells_number
        self.cells_list = []
        if cells_list is None:
            if self.cells_number is not None:
                for num in range(self.cells_number):
                    cell = Cell(
                        cell_type=choice(cell_type_list),
                        cell_index=num
                    )
                    self.cells_list.append(cell)
        else:
            self.cells_list = cells_list

        self.connections_number = connections_number
        self.connections_list = []
        if connections_list is None:
            if self.connections_number is not None:
                for _ in range(self.connections_number):
                    self.connections_list.append(
                        (randint(0, self.cells_number - 1),
                         randint(0, self.cells_number - 1))
                    )
        else:
            self.connections_list = connections_list

        if first_cell is None:
            self.first_cell = choice(self.cells_list)
        else:
            self.first_cell = first_cell

        if last_cell is None:
            self.last_cell = choice(self.cells_list)
        else:
            self.last_cell = last_cell

    def make_color(self):
        # temporarily like this
        self.color = ["#" + ''.join([choice('ABCDEF0123456789') for i in range(6)])]
        # old_method = choice([color_dict[i] for i in color_dict.keys()])
        return

    def think(self, possible_pixels_list):
        # possible_pixels_list has 9 members,
        # starting from the current pixel and going clock-wise from the top left neighbour
        left_pixels_list = possible_pixels_list.copy()
        count = 0
        while len(left_pixels_list) > 1 and count < 2 * len(self.connections_list):
            for num in range(0, len(left_pixels_list)):
                # print(left_pixels_list, z)
                decision = self.cell_netter(num)
                # print(decision)
                if not decision:
                    try:
                        left_pixels_list.remove(left_pixels_list[num])
                    except IndexError:
                        pass
            count += 1
        # print(len(left_pixels_list))
        new_position = left_pixels_list[randint(0, len(left_pixels_list) - 1)].position
        return new_position

    def cell_netter(self, number):
        # gets a number and returns True or False
        number_copy = number
        current_cell = self.first_cell
        number_copy = current_cell.result(number_copy)
        # print(number_copy)
        count = 0
        connected = True
        while current_cell != self.last_cell and count <= len(self.connections_list) and connected:
            connected = False
            for connection in self.connections_list:
                if current_cell.cell_index == connection[0]:
                    try:
                        current_cell = self.cells_list[connection[1]]
                        number_copy = current_cell.result(number_copy)
                        # print(number_copy)
                        connected = True
                    except IndexError:
                        pass
            count += 1
        # print(count, current_cell == self.last_cell)
        if number_copy == 1:
            return True
        elif number_copy == 0:
            return False
        else:
            return choice([True, False])

    def copy(self):
        return Brain(
            first_cell=self.first_cell.copy(),
            last_cell=self.last_cell.copy(),
            cells_list=[cell.copy() for cell in self.cells_list],
            cells_number=self.cells_number,
            connections_list=self.connections_list,
            connections_number=self.connections_number,
            reproduction=self.reproduction,
            is_positioned=self.is_positioned,
            color=self.color
        )


class Cell:
    def __init__(self, cell_type: str, cell_index: int):
        self.cell_type = cell_type
        self.cell_index = cell_index

    def copy(self):
        return Cell(self.cell_type, self.cell_index)

    def result(self, number):
        try:
            if self.cell_type == "n":
                return number
            if self.cell_type == "n-1":
                return number - 1
            if self.cell_type == "n+1":
                return number + 1
            if self.cell_type == "n//2":
                return number // 2
            if self.cell_type == "n>4-0,n<=4-1":
                if number > 4:
                    return 0
                else:
                    return 1
            if self.cell_type == "n<4-0,n>=4-1":
                if number < 4:
                    return 0
                else:
                    return 1
            if self.cell_type == "n<4-n>4,n>4-n<4":
                if number < 4:
                    return randint(4, 8)
                else:
                    return randint(0, 3)
            if self.cell_type == "abs(n-9)":
                return abs(number - 9)
            if self.cell_type == "abs(n-7)":
                return abs(number - 7)
            if self.cell_type == "abs(n-5)":
                return abs(number - 5)
            if self.cell_type == "abs(n-2)":
                return abs(number - 2)
            if self.cell_type == "0":
                return 0
            if self.cell_type == "1":
                return 1
            if self.cell_type == "1-0,0-1":
                if number == 1:
                    return 0
                elif number == 0:
                    return 1
            if self.cell_type == "--0,+-1":
                if number <= 0:
                    return 0
                else:
                    return 1
        except TypeError:
            return choice([True, False])
