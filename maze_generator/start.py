from random import randint

import os
clear = lambda : os.system('clear') # or clear for Linux

class Cell:
    def __init__(self, x = 1, y = 1, type = 'wall', visited = False):
        self.x = x
        self.y = y
        self.type = type
        self.visited = visited
    
    
    def visit(self):
        self.visited = True


class Maze:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = [None] * height
        for i in range(height):
            self.field[i] = [None] * width
        for i in range(height):
            for j in range(width):
                self.field[i][j] = Cell(i, j)
        for i in range(height):
            self.field[i][0].type = 'border'
            self.field[i][width - 1].type = 'border'
        for j in range(width):
            self.field[0][j].type = 'border'
            self.field[height - 1][j].type = 'border'


def get_init_values():
    print('choose the difficulty level of your maze(1, 2 or 3):')
    while True:
        level = int(input())
        clear()
        if level != 1 and level != 2 and level != 3:
            print('wrong level, try again:')
        else:
            break
            
    if level == 1:
        height = 9
        width = 9
    elif level == 2:
        height = 23
        width = 23
    else:
        height = 51
        width = 51
    if height % 2 == 0:
        height += 1
    if width % 2 == 0:
        width += 1
    print('choose the algorithm for generating your maze(dfs or prima):')
    while True:
        algo = input()
        clear()
        if algo != 'dfs' and algo != 'prima':
            print('wrong algorithm, try again:')
        else:
            break
    return height, width, algo


def generate_maze_with_dfs_algorithm(height, width):
    maze = Maze(height, width)
    for i in range(height):
        for j in range(width):
            if i % 2 and j % 2:
                maze.field[i][j] = Cell(i, j, 'cell')
    cells = [Cell(1, 1)]
    add_to_neighbours = [[0, 2], [0, -2], [2, 0], [-2, 0]]
    while len(cells):
        cur_cell = cells.pop()
        maze.field[cur_cell.x][cur_cell.y].visit()
        neighbours = []
        for add in add_to_neighbours:
            newi = cur_cell.x + add[0]
            newj = cur_cell.y + add[1]
            if 0 < newi < height and 0 < newj < width and not maze.field[newi][newj].visited:
                neighbours.append(maze.field[newi][newj])
        if len(neighbours):
            pos = randint(0, len(neighbours) - 1)
            cells.append(cur_cell)
            cells.append(neighbours[pos])
            maze.field[(cur_cell.x + neighbours[pos].x) // 2][(cur_cell.y + neighbours[pos].y) // 2].type = 'cell'
    return maze


def solve_maze(maze):
    maze.field[1][0].type = 'start'
    maze.field[height - 2][width - 1].type = 'finish'
    cells = [Cell(1, 1)]
    add_to_neighbours = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    used = [0] * height
    for i in range(height):
        used[i] = [False] * width
    path_founded = False
    while not path_founded:
        cur_cell = cells.pop()
        used[cur_cell.x][cur_cell.y] = True
        for add in add_to_neighbours:
            newi = cur_cell.x + add[0]
            newj = cur_cell.y + add[1]
            if used[newi][newj]:
                continue
            if maze.field[newi][newj].type != 'cell':
                continue
            cells.append(cur_cell)
            cells.append(maze.field[newi][newj])
            if newi == height - 2 and newj == width - 2:
                path_founded = True
            break
    for cell in cells:
        maze.field[cell.x][cell.y].type = 'path'
    return maze


def generate_maze_with_prima_algorithm(height, weight):
    maze = Maze(height, width)
    for i in range(height):
        for j in range(width):
            if i % 2 and j % 2:
                maze.field[i][j] = Cell(i, j, 'cell')
    cells = [maze.field[randint(0, (height // 2 - 1)) * 2 + 1][randint(0, (width // 2 - 1)) * 2 + 1]]
    add_to_neighbours = [[0, 2], [0, -2], [2, 0], [-2, 0]]
    maze.field[cells[0].x][cells[0].y].visit()
    while len(cells):
        rand_pos = randint(0, len(cells) - 1)
        cur_cell = cells.pop(rand_pos)
        neighbours = []
        for add in add_to_neighbours:
            newi = cur_cell.x + add[0]
            newj = cur_cell.y + add[1]
            if 0 < newi < height and 0 < newj < width and not maze.field[newi][newj].visited:
                neighbours.append(maze.field[newi][newj])
        if len(neighbours):
            pos = randint(0, len(neighbours) - 1)
            cells.append(cur_cell)
            cells.append(neighbours[pos])
            maze.field[neighbours[pos].x][neighbours[pos].y].visit()
            maze.field[(cur_cell.x + neighbours[pos].x) // 2][(cur_cell.y + neighbours[pos].y) // 2].type = 'cell'
    return maze


def print_maze(maze):
    print('Get your amazing maze:')
    for i in range(maze.height):
        for j in range(maze.width):
            if maze.field[i][j].type == 'start' or maze.field[i][j].type == 'finish':
                print("\033[31m->\033[0m", end='')
            elif maze.field[i][j].type == 'border':
                print("\033[46m  \033[0m", end='')
            elif maze.field[i][j].type == 'path':
                print("\033[41m  \033[0m", end='')
            elif maze.field[i][j].type == 'wall':
                print("\033[40m  \033[0m", end='')
            else:
                print("\033[47m  \033[0m", end='')
        print()


clear()
height, width, algo = get_init_values()
if algo == 'dfs':
    maze = generate_maze_with_dfs_algorithm(height, width)
else:
    maze = generate_maze_with_prima_algorithm(height, width)
print_maze(maze)
print('do you want to solve it?')
s = input()
clear()
if s == 'yes' or s == 'y' or s == 'YES':
    maze = solve_maze(maze)
print_maze(maze)
print('thanks for using this generator!')