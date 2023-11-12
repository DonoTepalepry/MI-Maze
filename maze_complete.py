import pygame, math
import random
import heapq
from functools import total_ordering


def start():
    grid_cells = None
    RES = WIDTH, HEIGHT = 800, 700
    TILE = 50  # change size of tiles to make maze larger or smaller
    cols, rows = WIDTH // TILE, HEIGHT // TILE
    Set = False
    start_tile = None
    end_tile = None
    start_cell = None
    end_cell = None
    goal = False
    solution = None
    show_heur = True
    pygame.init()
    sc = pygame.display.set_mode(RES)
    clock = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', 16)

    @total_ordering
    class Cell:
        def __init__(self, x, y):
            self.x, self.y = x, y
            self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
            self.gen_visited = False
            self.thickness = 4
            self.heuristic = 0
            self.neighbors = {'top': None, 'right': None, 'bottom': None, 'left': None}
            self.neighbors_str = None

            self.astar_frontier = False
            self.astar_explored = False
            self.astar_path = False

        def __eq__(self, other):
            return (self.x, self.y) == (other.x, other.y)

        def __lt__(self, other):
            return (self.x, self.y) < (other.x, other.y)

        def __hash__(self) -> int:
            return (self.x) + (self.y << 2)

        def __str__(self):
            neighbors = []
            if self.neighbors['top']:
                neighbors.append('t')
            if self.neighbors['bottom']:
                neighbors.append('b')
            if self.neighbors['left']:
                neighbors.append('l')
            if self.neighbors['right']:
                neighbors.append('r')

            self.neighbors_str = ','.join(neighbors)

            return f'"Cell id: {self.x},{self.y}"'

        def __repr__(self) -> str:
            return self.__str__()

        def draw(self, sc):
            x, y = self.x * TILE, self.y * TILE

            if self.astar_path:
                pygame.draw.rect(sc, pygame.Color('crimson'), pygame.Rect(x, y, TILE, TILE))
            elif self.astar_explored:
                pygame.draw.rect(sc, pygame.Color('chocolate1'), pygame.Rect(x, y, TILE, TILE))
            elif self.astar_frontier:
                pygame.draw.rect(sc, pygame.Color('darkgoldenrod1'), pygame.Rect(x, y, TILE, TILE))

            if self.walls['top']:
                pygame.draw.line(sc, pygame.Color('dark green'), (x, y), (x + TILE, y), self.thickness)
            if self.walls['right']:
                pygame.draw.line(sc, pygame.Color('dark green'), (x + TILE, y), (x + TILE, y + TILE), self.thickness)
            if self.walls['bottom']:
                pygame.draw.line(sc, pygame.Color('dark green'), (x + TILE, y + TILE), (x, y + TILE), self.thickness)
            if self.walls['left']:
                pygame.draw.line(sc, pygame.Color('dark green'), (x, y + TILE), (x, y), self.thickness)
            if self.heuristic and show_heur:
                huer = font.render(f'{self.heuristic:.2f}', True, (255, 255, 255))
                sc.blit(huer, (x + 5, y + TILE // 2))

        def check_cell(self, x, y):
            find_index = lambda x, y: x + y * cols
            if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
                return False
            return self.grid_cells[find_index(x, y)]

        def check_gen_neighbors(self):
            self.grid_cells = grid_cells
            neighbors = []  # create empty list called neighbors
            top = self.check_cell(self.x, self.y - 1)  # check if top is open
            right = self.check_cell(self.x + 1, self.y)  # check if right is open
            bottom = self.check_cell(self.x, self.y + 1)  # check if bottom is open
            left = self.check_cell(self.x - 1, self.y)  # check if left is open
            if top and not top.gen_visited:  # if top is open and has not been visited then add it to neighbors list
                neighbors.append(top)
            if right and not right.gen_visited:  # same but right
                neighbors.append(right)
            if bottom and not bottom.gen_visited:  # same
                neighbors.append(bottom)
            if left and not left.gen_visited:  # same
                neighbors.append(left)
            return random.choice(neighbors) if neighbors else False
            # ^ choses a random neighbor then not sure here but if neighbors true it does nothing otherwise set neigbors to false?

        def check_valid_neighbors(
                self):  # checks if you can travel to the neigboring cell and if so will add it to self.neigbors
            self.grid_cells = grid_cells
            top = self.check_cell(self.x, self.y - 1)  # check if top is open
            right = self.check_cell(self.x + 1, self.y)  # check if right is open
            bottom = self.check_cell(self.x, self.y + 1)  # check if bottom is open
            left = self.check_cell(self.x - 1, self.y)  # check if left is open
            if top and not self.walls['top']:
                self.neighbors['top'] = top
            if bottom and not self.walls['bottom']:
                self.neighbors['bottom'] = bottom
            if left and not self.walls['left']:
                self.neighbors['left'] = left
            if right and not self.walls['right']:
                self.neighbors['right'] = right

    def remove_walls(current, next):
        dx = current.x - next.x
        if dx == 1:
            current.walls['left'] = False
            next.walls['right'] = False
        elif dx == -1:
            current.walls['right'] = False
            next.walls['left'] = False
        dy = current.y - next.y
        if dy == 1:
            current.walls['top'] = False
            next.walls['bottom'] = False
        elif dy == -1:
            current.walls['bottom'] = False
            next.walls['top'] = False

    def draw_gui(x, y, ready):
        m_pos = pygame.mouse.get_pos()
        m_pos = m_pos[0] // TILE, m_pos[1] // TILE
        pos = font.render(f"Pos: {m_pos}", True, (255, 255, 255))
        sc.blit(pos, (x, y))
        if start_tile:
            spos = font.render("Start: " + str(start_tile), True, (255, 255, 255))
            sc.blit(spos, (x, y + 20))
        if end_tile:
            epos = font.render("End: " + str(end_tile), True, (255, 255, 255))
            sc.blit(epos, (x, y + 40))
        if ready:
            pos = font.render(f"Ready", True, (255, 255, 255))
            sc.blit(pos, (x + 100, y))

    def distance(cell, finish):
        m_pos = cell.x, cell.y
        mx, my = m_pos[0], m_pos[1]
        dist = math.sqrt((mx - finish[0]) ** 2 + (my - finish[1]) ** 2)
        return dist

    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]

    current_cell = grid_cells[0]

    astar_explored = set()
    astar_queue = []

    stack = []
    colors, color = [], 40
    gen_neighbors = False
    while True:
        sc.fill(pygame.Color('dark cyan'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        [cell.draw(sc) for cell in grid_cells]
        if not current_cell.gen_visited:
            current_cell.gen_visited = True

        if start_tile:
            pygame.draw.circle(sc, 'GREEN', pstart, 10)

        if end_tile:
            pygame.draw.circle(sc, 'GOLD', pend, 10)

        next_cell = current_cell.check_gen_neighbors()
        if next_cell:
            stack.append(current_cell)
            colors.append((min(color, 255), 10, 100))
            color += 1
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()
        elif not gen_neighbors:
            # gonna add more connectivity to

            gen_neighbors = True
            for cell in grid_cells:
                cell.check_valid_neighbors()
                # print(cell)

        draw_gui(10, 10, gen_neighbors)

        if Set == 0:
            if pygame.mouse.get_pressed()[0]:
                pstart = pygame.mouse.get_pos()
                start_tile = pstart[0] // TILE, pstart[1] // TILE
                start_cell = grid_cells[start_tile[0] + start_tile[1] * cols]
                starttup = (0, [start_cell], start_cell)
                heapq.heappush(astar_queue, starttup)
                Set = Set + 1
                pygame.time.wait(500)
        elif Set == 1:
            if pygame.mouse.get_pressed()[0]:
                pend = pygame.mouse.get_pos()
                end_tile = pend[0] // TILE, pend[1] // TILE
                end_cell = grid_cells[end_tile[0] + end_tile[1] * cols]
                for cell in grid_cells:
                    cell.heuristic = distance(cell, end_tile)
                Set = Set + 1

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_r]:
            return True

        if pressed_keys[pygame.K_s]:
            show_heur = not show_heur

        if start_cell and end_cell and not solution:
            # print([(x[0], x[2]) for x in astar_queue])
            if astar_queue:
                astar_cost, astar_path, astar_cell = heapq.heappop(astar_queue)
                if astar_cell in astar_explored:
                    continue

                if astar_cell == end_cell:
                    solution = astar_path
                    for sol_cell in solution:
                        sol_cell.astar_path = True
                    print(solution)

                if not solution:
                    astar_explored.add(astar_cell)
                    astar_cell.astar_explored = True

                    astar_cost -= astar_cell.heuristic
                    neighbors = sorted(
                        [astar_cell.neighbors[key] for key in astar_cell.neighbors if astar_cell.neighbors[key]])
                    for next in neighbors:
                        next.astar_frontier = True
                        new_cost = astar_cost + 1 + next.heuristic
                        next_path = [x for x in astar_path]
                        next_path.append(next)

                        heapq.heappush(astar_queue, (new_cost, next_path, next))

        pygame.display.flip()
        if not solution and start_tile and end_tile:
            clock.tick(20)
        else:
            clock.tick(0)


while True:
    cont = start()
    if cont:
        continue
    else:
        break

# code graveyard

# endconv = grid_cells[end_tile[0] + end_tile[1] * cols]
# astar(c_cell, start_tile, endconv)
# print(endconv)
# if pressed_keys[pygame.K_UP] and c_cell.neighbors['top']:
#     c_cell = c_cell.neighbors['top']
# elif pressed_keys[pygame.K_DOWN] and c_cell.neighbors['bottom']:
#     c_cell = c_cell.neighbors['bottom']
# elif pressed_keys[pygame.K_RIGHT] and c_cell.neighbors['right']:
#     c_cell = c_cell.neighbors['right']
# elif pressed_keys[pygame.K_LEFT] and c_cell.neighbors['left']:
#     c_cell = c_cell.neighbors['left']
