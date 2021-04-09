from random import randint
import copy
import os
import keyboard
import getch
import time

clear = lambda : os.system('clear')


def change_color_to_green():
    print('\033[32m', end='')


def change_color_to_white():
    print('\033[0m', end='')
    
class Cell:
    def __init__(self, x = 1, y = 1, type = 'wall', visited = False):
        self.x = x
        self.y = y
        self.type = type # wall/path/cell/start/finish
        self.visited = visited
    
    
    def visit(self):
        self.visited = True


class Maze:
    def __init__(self, height = 1, width = 1):
        self.height = height
        self.width = width
        self.field = [None] * height
        for i in range(height):
            self.field[i] = [None] * width
        for i in range(height):
            for j in range(width):
                self.field[i][j] = Cell(i, j)
        for i in range(height):
            for j in range(width):
                if i % 2 and j % 2:
                    self.field[i][j] = Cell(i, j, 'cell')


def get_init_values(): # get height, width and algorithm for generating
    print('GENERATING A MAZE:')
    print('Choose the difficulty level of your maze(1, 2 or 3):')
    while True:
        change_color_to_green()
        level = int(input())
        change_color_to_white()
        clear()
        if level != 1 and level != 2 and level != 3:
            print('GENERATING A MAZE:')
            print('wrong level, try again:')
        else:
            break
            
    if level == 1:
        height = 13
        width = 13
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
    print('GENERATING A MAZE:')
    print('choose the algorithm for generating your maze(dfs or prima):')
    while True:
        change_color_to_green()
        algo = input()
        change_color_to_white()
        clear()
        if algo != 'dfs' and algo != 'prima':
            print('GENERATING A MAZE:')
            print('wrong algorithm, try again:')
        else:
            break
    return height, width, algo


def generate_maze_with_dfs_algorithm(height, width):
    maze = Maze(height, width)
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
    height = maze.height
    width = maze.width
    maze.field[1][0].type = 'start'
    maze.field[height - 2][width - 1].type = 'finish'
    cells = [Cell(1, 1)]
    add_to_neighbours = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    used = [0] * height
    for i in range(height):
        used[i] = [False] * width
    path_is_founded = False
    while not path_is_founded:
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
                path_is_founded = True
            break
    for cell in cells:
        maze.field[cell.x][cell.y].type = 'path'
    return maze


def generate_maze_with_prima_algorithm(height, width):
    maze = Maze(height, width)
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
                print("\033[46m->\033[0m", end='')
            elif maze.field[i][j].type == 'path':
                print("\033[46m  \033[0m", end='')
            elif maze.field[i][j].type == 'wall':
                print("\033[45m  \033[0m", end='')
            elif maze.field[i][j].type == 'cell':
                print("\033[47m  \033[0m", end='')
            elif maze.field[i][j].type == 'user':
                print("\033[41m  \033[0m", end='')
        print()
    print()


def print_menu():
    print('What do you want?')
    print('1. Generate a maze')
    print('2. See a solution to the maze')
    print('3. Try to solve the maze')
    print('4. Save the maze to the file')
    print('5. Get a maze from the file')
    print('6. Exit')


def generate_maze():
    height, width, algo = get_init_values()
    if algo == 'dfs':
        maze = generate_maze_with_dfs_algorithm(height, width)
    elif algo == 'prima':
        maze = generate_maze_with_prima_algorithm(height, width)
    print_maze(maze)
    return maze


def end_process():
    print('Thanks for using this generator!')
    print('\033[32mdeveloped by koreec\033[0m')


def print_solution_of_maze(main_maze):
    maze = copy.deepcopy(main_maze)
    maze = solve_maze(maze)
    print_maze(maze)


def wrong_command_error():
    print('Oh, no! Wrong command. Try one more time:\n')


def get_key():
    first_char = getch.getch()
    clear()
    time.sleep(0.001)
    
    if first_char == '\x1b':
        return {'[A': 'up', '[B': 'down', '[C': 'right', '[D': 'left'}[getch.getch() + getch.getch()]
    else:
        return first_char


def move_cell(maze, cells, cur_cell, add):
    newi = cur_cell[0] + add[0]
    newj = cur_cell[1] + add[1]
    if 0 <= newi < maze.height and 0 <= newj < maze.width:
        if maze.field[newi][newj].type == 'cell' or maze.field[newi][newj].type == 'finish' or maze.field[newi][newj].type == 'path':
            if len(cells) > 1 and cells[len(cells) - 2] == [newi, newj]:
                last_cell = cells.pop()
                if newi == maze.height - 2 and cur_cell[1] == maze.width - 1:
                    maze.field[cur_cell[0]][cur_cell[1]].type = 'finish'
                else:
                    maze.field[cur_cell[0]][cur_cell[1]].type = 'cell'

            else:
                cells.append([newi, newj])
                maze.field[newi][newj].type = 'path'
            cur_cell[0] += add[0]
            cur_cell[1] += add[1]


def try_to_solve_maze(main_maze):
    maze = copy.deepcopy(main_maze)
    height = maze.height
    width = maze.width
    maze.field[1][0].type = 'start'
    maze.field[height - 2][width - 1].type = 'finish'
    print('SOLVING A MAZE:')
    print('-use arrows to move')
    print('-type q to quit')
    maze.field[1][1].type = 'path'
    cur_cell = [1, 1]
    print_maze(maze)
    cells = [[1, 1]]
    while True:
        pressedKey = get_key()
        if pressedKey == 'q':
            break
        elif pressedKey == 'up':
            move_cell(maze, cells, cur_cell, [-1, 0])
        elif pressedKey == 'right':
            move_cell(maze, cells, cur_cell, [0, 1])
        elif pressedKey == 'left':
            move_cell(maze, cells, cur_cell, [0, -1])
        elif pressedKey == 'down':
            move_cell(maze, cells, cur_cell, [1, 0])
        print('SOLVING A MAZE:')
        print('-use arrows to move')
        print('-type q to quit')
        print_maze(maze)
    print_maze(maze)


def save_to_file(maze):
    print('Enter a filename:')
    filename = input()
    clear()
    f = open(filename, 'w')
    f.write(str(maze.height) + '\n')
    f.write(str(maze.width) + '\n')
    for i in range(maze.height):
        for j in range(maze.width):
            f.write(maze.field[i][j].type + '\n')
    f.close()
    print_maze(maze)
    print('Your maze was successfully saved to the ' + filename + '!')
    print()


def get_maze_from_file():
    print('Enter a filename:')
    filename = input()
    clear()
    f = open(filename, 'r')
    x = 0
    y = 0
    step = 0
    maze = Maze()
    for line in f:
        if step == 0:
            height = int(line)
        elif step == 1:
            width = int(line)
            maze = Maze(height, width)
        else:
            maze.field[x][y].type = line[:-1]
            y += 1
            if y == width:
                y = 0
                x += 1
        step += 1
    print_maze(maze)
    f.close()
    return maze


clear()
print_menu()
maze = Maze(1, 1)
the_first_time = True
while True:
    change_color_to_green()
    command = input()
    change_color_to_white()
    clear()
    if command == '1':
        the_first_time = False
        maze = generate_maze()
    elif command == '2':
        if the_first_time:
            wrong_command_error()
        else:
            print_solution_of_maze(maze)
    elif command == '3':
        if the_first_time:
            wrong_command_error()
        else:
            try_to_solve_maze(maze)
    elif command == '4':
        if the_first_time:
            wrong_command_error()
        else:
            save_to_file(maze)
    elif command == '5':
        the_first_time = False
        maze = get_maze_from_file()
    elif command == '6':
        end_process()
        break
    else:
        wrong_command_error()
    print_menu()