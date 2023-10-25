import pygame
from random import choice
import webcolors

RES = WIDTH, HEIGHT = 800, 700
TILE = 50
cols, rows = WIDTH // TILE, HEIGHT // TILE
pos = 0
spos = 0
pstart = [1, 35]
pend = [1, 55]
cnt = 0
startSet = False
start_tile = None
end_tile = None
player_x, player_y = 0, 0
prev_x, prev_y = 0, 0


pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        self.thickness = 4

    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color('dark cyan'), (x + 2, y + 2, TILE - 2, TILE - 2))

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

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return self.grid_cells[find_index(x, y)]

    def check_neighbors(self):
        self.grid_cells = grid_cells
        neighbors = [] #create empty list called neigbors
        top = self.check_cell(self.x, self.y - 1)  #check if top is open
        right = self.check_cell(self.x + 1, self.y) #check if right is open
        bottom = self.check_cell(self.x, self.y + 1) #check if bottom is open
        left = self.check_cell(self.x - 1, self.y) #check if left is open
        if top and not top.visited: #if top is open and has not been visited then add it to neigbors list
            neighbors.append(top)
        if right and not right.visited: #same but right
            neighbors.append(right)
        if bottom and not bottom.visited: #same
            neighbors.append(bottom)
        if left and not left.visited: #same
            neighbors.append(left)
        return choice(neighbors) if neighbors else False
        # ^ choses a random neighbor then not sure here but if neighbors true it does nothing otherwise set neigbors to false?

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

def draw_gui(x,y):
    m_pos = pygame.mouse.get_pos()
    m_pos = m_pos[0] // TILE, m_pos[1] // TILE
    pos = font.render(f"Pos: {m_pos}", True, (255, 255, 255))
    sc.blit(pos, (x, y))
    if start_tile:
        spos = font.render("Start: " + str(start_tile), True, (255, 255, 255))
        sc.blit(spos, (x, y+20))
    if end_tile:
        epos = font.render("End: " + str(end_tile), True, (255, 255, 255))
        sc.blit(epos, (x, y+40))

grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]

current_cell = grid_cells[0]
stack = []
colors, color = [], 40

while True:

    sc.fill(pygame.Color('dark cyan'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    [cell.draw(sc) for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()

    # uncomment below thing to solve
    #[pygame.draw.rect(sc,colors[i],(cell.x * TILE +5,cell.y * TILE +5,TILE - 10, TILE - 10), border_radius=12) for i, cell in enumerate(stack)]

    if start_tile:
        pygame.draw.circle(sc, 'GREEN', pstart, 10)
    if end_tile:
        pygame.draw.circle(sc, 'GOLD', pend, 10)

    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        colors.append((min(color, 255), 10, 100))
        color += 1
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()

    draw_gui(10,10)

    if startSet == 0:
        if pygame.mouse.get_pressed()[0]:
            pstart = pygame.mouse.get_pos()
            start_tile = pstart[0] // TILE, pstart[1] // TILE
            startSet = startSet + 1
            pygame.time.wait(500)
    elif startSet == 1:
        if pygame.mouse.get_pressed()[0]:
            pend = pygame.mouse.get_pos()
            end_tile = pend[0] // TILE, pend[1] // TILE
            startSet = startSet + 1

    if end_tile:
        pygame.draw.line(sc, (255, 0, 0), (pstart[0], pstart[1]), (pend[0], pend[1]))

    inBounds = pygame.Rect(0+TILE, 0+TILE, WIDTH, HEIGHT).collidepoint(player_x + TILE, player_y + TILE)

    pressed_keys = pygame.key.get_pressed()
    if inBounds:
        if pressed_keys[pygame.K_UP] and not sc.get_at((player_x + (TILE // 2), player_y + 1))[:3] == (0, 100, 0):
            prev_x, prev_y = player_x, player_y
            player_y = player_y - TILE
            pygame.time.wait(250)
        elif pressed_keys[pygame.K_DOWN] and not sc.get_at((player_x + (TILE // 2), player_y + TILE - 1))[:3] == (0, 100, 0):
            prev_x, prev_y = player_x, player_y
            player_y = player_y + TILE
            pygame.time.wait(250)
        elif pressed_keys[pygame.K_RIGHT] and not sc.get_at((player_x + TILE - 1, player_y + (TILE // 2)))[:3] == (0, 100, 0):
            prev_x, prev_y = player_x, player_y
            player_x = player_x + TILE
            pygame.time.wait(250)
        elif pressed_keys[pygame.K_LEFT] and not sc.get_at((player_x, player_y + (TILE // 2)))[:3] == (0, 100, 0):
            prev_x, prev_y = player_x, player_y
            player_x = player_x - TILE
            pygame.time.wait(250)
    else:
        player_x = prev_x
        player_y = prev_y

    pygame.draw.rect(sc, pygame.Color('red'), (player_x + 4, player_y + 4, TILE - 6, TILE - 6))

    pygame.display.flip()
    clock.tick(100)