import pygame, math
import random
import heapq
from functools import total_ordering
def start():
    grid_cells = None
    RES = WIDTH, HEIGHT = 800, 700
    TILE = 100          #change size of tiles to make maze larger or smaller
    cols, rows = WIDTH // TILE, HEIGHT // TILE
    Set = False
    start_tile = None
    end_tile = None
    c_cell = None
    goal = False
    pygame.init()
    sc = pygame.display.set_mode(RES)
    clock = pygame.time.Clock()

    @total_ordering
    class Cell:
        def __init__(self, x, y):
            self.x, self.y = x, y
            self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
            self.visited = False
            self.thickness = 4
            self.heuristic = 0
            self.neighbors = {'top': None, 'right': None, 'bottom': None, 'left': None}
            self.been_there = False

        def __eq__(self, other):
            return (self.x, self.y) == (other.x, other.y)
        def __lt__(self, other):
            return (self.x, self.y) < (other.x, other.y)

        def draw(self, sc):
            x, y = self.x * TILE, self.y * TILE

            if self.walls['top']:
                pygame.draw.line(sc, pygame.Color('dark green'), (x, y), (x + TILE, y), self.thickness)
            if self.walls['right']:
                pygame.draw.line(sc, pygame.Color('dark green'), (x + TILE, y), (x + TILE, y + TILE), self.thickness)
            if self.walls['bottom']:
                pygame.draw.line(sc, pygame.Color('dark green'), (x + TILE, y + TILE), (x, y + TILE), self.thickness)
            if self.walls['left']:
                pygame.draw.line(sc, pygame.Color('dark green'), (x, y + TILE), (x, y), self.thickness)
            if self.heuristic:
                huer = font.render(f'{self.heuristic:.2f}', True, (255, 255, 255))
                sc.blit(huer, (x, y + TILE // 2))

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
            if top and not top.visited:  # if top is open and has not been visited then add it to neighbors list
                neighbors.append(top)
            if right and not right.visited:  # same but right
                neighbors.append(right)
            if bottom and not bottom.visited:  # same
                neighbors.append(bottom)
            if left and not left.visited:  # same
                neighbors.append(left)
            return random.choice(neighbors) if neighbors else False
            # ^ choses a random neighbor then not sure here but if neighbors true it does nothing otherwise set neigbors to false?

        def check_valid_neighbors(self):  # checks if you can travel to the neigboring cell and if so will add it to self.neigbors
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

        def print_neighbors(self):
            neighbors = []
            if self.neighbors['top']:
                neighbors.append('top')
            if self.neighbors['bottom']:
                neighbors.append('bottom')
            if self.neighbors['left']:
                neighbors.append('left')
            if self.neighbors['right']:
                neighbors.append('right')

            neighbors_str = ' '.join(neighbors)
            print(f'Cell id: {self.x},{self.y}. Neighbors: {neighbors_str}')

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

    font = pygame.font.Font('freesansbold.ttf', 16)

    def draw_gui(x, y):
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

    def distance(cell, finish):
        m_pos = cell.x, cell.y
        mx, my = m_pos[0], m_pos[1]
        dist = math.sqrt((mx - finish[0]) ** 2 + (my - finish[1]) ** 2)
        return dist

    def astar(cells, start, goal):
        if start == goal:
            return[]
        explored = set()
        queue = []
        starttup = (0, [start], start)
        heapq.heappush(queue, starttup)

        while queue:
            print(heapq.heappop(queue))
            cost, path, cell = heapq.heappop(queue)
            if cell in explored:
                continue

            if cell == goal:
                return path

            explored.add(cell)

            cost -= cell.heuristic
            neighbors = sorted([x for x in cells.neighbors(cell)])
            for next in neighbors:
                new_cost = cost + 1 + cell.heuristic
                next_path = [x for x in path]
                next_path.append(next)

                heapq.heappush(queue, (new_cost, next_path, next))

    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]

    current_cell = grid_cells[0]
    stack = []
    colors, color = [], 40
    gen_neighbors = False
    while True:
        sc.fill(pygame.Color('dark cyan'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        [cell.draw(sc) for cell in grid_cells]
        current_cell.visited = True

        # uncomment below thing to solve
        # [pygame.draw.rect(sc, colors[i], (cell.x * TILE + 5, cell.y * TILE + 5, TILE - 10, TILE - 10), border_radius=12) for i, cell in enumerate(stack)]

        if start_tile:
            pygame.draw.circle(sc, 'GREEN', pstart, 10)
            if c_cell:
                pygame.draw.rect(sc, pygame.Color('red'),
                                 (c_cell.x * TILE + 4, c_cell.y * TILE + 4, TILE - 6, TILE - 6))
        if end_tile:
            pygame.draw.circle(sc, 'GOLD', pend, 10)
            if (c_cell.x == end_tile[0]) and (c_cell.y == end_tile[1]):
                goal = True
                print('goal')
        next_cell = current_cell.check_gen_neighbors()
        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            colors.append((min(color, 255), 10, 100))
            color += 1
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()
        elif not gen_neighbors:
            gen_neighbors = True
            for cell in grid_cells:
                cell.check_valid_neighbors()
                cell.print_neighbors()

        draw_gui(10, 10)

        if Set == 0:
            if pygame.mouse.get_pressed()[0]:
                pstart = pygame.mouse.get_pos()
                start_tile = pstart[0] // TILE, pstart[1] // TILE
                c_cell = grid_cells[start_tile[0] + start_tile[1] * cols]
                Set = Set + 1
                pygame.time.wait(500)
        elif Set == 1:
            if pygame.mouse.get_pressed()[0]:
                pend = pygame.mouse.get_pos()
                end_tile = pend[0] // TILE, pend[1] // TILE
                # for cell in grid_cells:
                #     cell.heuristic = distance(cell, end_tile)
                Set = Set + 1

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_r]:
            start()

        if c_cell and not goal and end_tile:
            ...
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

# replace start_tile and end_tile, convert the x and y cords into cell hint hint lambda function
            if c_cell.neighbors['top']:
                if random.randint(0, 100) < 36:
                    c_cell = c_cell.neighbors['top']
            if c_cell.neighbors['right']:
                if random.randint(0, 100) < 36:
                    c_cell = c_cell.neighbors['right']
            if c_cell.neighbors['bottom']:
                if random.randint(0, 100) < 36:
                    c_cell = c_cell.neighbors['bottom']
            if c_cell.neighbors['left']:
                if random.randint(0, 100) < 36:
                    c_cell = c_cell.neighbors['left']

        pygame.display.flip()
        if next_cell:
            clock.tick(100)
        else:
            clock.tick(20)

start()