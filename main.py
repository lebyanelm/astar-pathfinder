"""A* PATH FINDING ALGORITHIM"""
import pygame
from queue import PriorityQueue
from models.spot import Spot
from models.colors import COLORS

# PYGAME DISPLAY WINDOW SETUP
WIDTH = 400
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('A* PATH FINDING ALGORITHM')

"""For calculating the path to figure out the path to an end point. Using manhatten distance."""
def h(p1: int, p2: int):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def draw_path(came_from, current, draw_inner):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw_inner()


def astar_algorithm(draw_inner, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))

    came_from = {}

    g_score = {spot: float('inf') for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float('inf') for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            draw_path(came_from, end, draw_inner)

            """Reset the rest of the spots"""
            for row in grid:
                for spot in row:
                    if not spot.is_open() and not spot.is_path() and not spot.is_barrier():
                        spot.reset()
            return True

        for neighber in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighber]:
                came_from[neighber] = current
                g_score[neighber] = temp_g_score
                f_score[neighber] = temp_g_score + h(neighber.get_pos(), end.get_pos())
                if neighber not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighber], count, neighber))
                    open_set_hash.add(neighber)
                    neighber.make_open()

        draw_inner()
        if current != start:
              current.make_closed()

    return False


"""For drawing the grid on the pygame window to show the state of the algorithm"""
def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows, width)
            grid[i].append(spot)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, COLORS['GREY'], (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, COLORS['GREY'], (j * gap, 0), (j * gap, width))


"""Main draw function"""
def draw(win, grid, rows, width):
    win.fill(COLORS['BLACK'])

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)

    pygame.display.update()


"""
When a mouse click happens, we would want to get the position
of the mouse click to know which spot has been clicked.
"""
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    ROWS = 20
    grid = make_grid(ROWS, width)

    # Algorithm states
    start = None
    end = None

    run = True
    started = False

    while run:
        """Start drawing the spots and grid on the window"""
        draw(win, grid, ROWS, width)

        """Listen for events that get fired off when user interacts"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    print('Started.')
                    """Start running the algorithm"""
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    astar_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                """Cancels the algorithm and restarts everything"""
                if event.key == pygame.K_c:
                    grid = make_grid(ROWS, width)
                    start = None
                    end = None
                    started = False
            """So that when the algorithm has started prevent any changes to the board"""
            # if started:
            #     continue

            if pygame.mouse.get_pressed()[0]:
                """Left mouse click"""

                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)

                spot = grid[row][col]
                spot.update_neighbors(grid)
                if not start and spot.is_open():
                    start = spot
                    start.make_start()

                elif not end and spot.is_open():
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                """Right mouse click"""

                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)

                spot = grid[row][col]
                # check if the spot are part of the start or end nodes to reset it
                if start == spot or end == spot:
                    if start == spot:
                        start = None
                    else:
                        end = None
                    spot.reset()

                # if not start or end, check if that node is a barrier to reset the spot
                elif spot.is_barrier() and spot.is_changeable:
                    spot.reset()

    pygame.quit()


main(WINDOW, WIDTH)
