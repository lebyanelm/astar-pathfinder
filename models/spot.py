# dependencies
from models.colors import COLORS
import pygame

"""
To help keep track of positions.
Represents a node, and able to keep track other spots
that are around it.
"""


class Spot:
    def __init__(self, row: int, col: int, width: int, total_rows: int, total_width: int):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = COLORS['BLACK']
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.total_width = total_width
        self.is_changeable = True

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == COLORS['RED']

    def is_open(self):
        return self.color == COLORS['BLACK']

    def is_barrier(self):
        return self.color == COLORS['GREY']

    def is_path(self):
        return self.color == COLORS['PURPLE']

    def check_is_edge(self):
        if self.x < self.width or (self.x + self.width) == self.total_width:
            self.make_barrier()
            self.is_changeable = False # prevent changes to this spot
        elif self.y < self.width or (self.y + self.width) == self.total_width:
            self.make_barrier()
            self.is_changeable = False # prevent changes to this spot

    def is_start(self):
        return self.color == COLORS['ORANGE']

    def is_end(self):
        return self.color == COLORS['TURQUOISE']

    def reset(self):
        self.color = COLORS['BLACK']

    def make_closed(self):
        self.color = COLORS['RED']

    def make_open(self):
        self.color = COLORS['GREEN']

    def make_barrier(self):
        self.color = COLORS['GREY']

    def make_start(self):
        self.color = COLORS['ORANGE']

    def make_end(self):
        self.color = COLORS['TURQUOISE']

    def make_path(self):
        self.color = COLORS['PURPLE']

    def draw(self, win):
        self.check_is_edge()
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []

        possible_neighbors = (
            # top
            (self.row - 1, self.col),
            # right
            (self.row, self.col + 1),
            # bottom
            (self.row + 1, self.col),
            # left
            (self.row, self.col - 1),
        )

        """Filter out the valid rows and colums to prevent KeyError"""
        for neighbor in possible_neighbors:
            if (-1 < neighbor[0] < self.total_rows) \
                    and -1 < neighbor[1] < self.total_rows:
                spot = grid[neighbor[0]][neighbor[1]]
                if not spot.is_barrier():
                    self.neighbors.append(spot)

    def __lt__(self, other):
        return False
