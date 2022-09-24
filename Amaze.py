from tkinter import *
from tkinter import ttk
import random
import time


class Cell:
    def __init__(self):
        """
        A one square cell that makes up a Maze.

        === Attributes ===
        visited : This Cell's visit status.
        top : This Cell's top wall.
        bottom : This Cell's bottom wall.
        right : This Cell's right wall.
        left : This Cell's left wall.
        r : This Cell's row.
        c : This Cell's column.
        """
        visited : bool
        top : List[bool]
        bottom : List[bool]
        right : List[bool]
        left : List[bool]
        r : int
        c : int
        self.visited = False
        self.top = [False]
        self.bottom = [False]
        self.right = [False]
        self.left = [False]
        self.r = 0
        self.c = 0


class Maze:
    def __init__(self, dim_x, dim_y):
        """
        The maze.

        === Attributes ===
        dim_x : This maze's length.
        dim_y : This maze's width.
        array : This maze's array to store each Cell.
        window : This maze's window.
        canvas : This maze's canvas.

        """
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.array = []
        self.window = Tk()
        self.canvas = Canvas(self.window, width=self.dim_x * 50,
                             height=self.dim_y * 50,
                             background='#cfbeed')

    def make_cells(self):
        """
        Populate the array with Cell objects.
        """
        for r in range(self.dim_y):
            temp = []
            for c in range(self.dim_x):
                temp.append(Cell())
            self.array.append(temp)

    def link_cells(self):
        """
        Link all of the Cell objects.
        """
        for r in range(self.dim_y):
            for c in range(self.dim_x):
                current_cell = self.array[r][c]
                current_cell.c = c
                current_cell.r = r
                if c + 1 < self.dim_x:  # check right neighbor
                    neighbor_cell = self.array[r][c + 1]
                    neighbor_cell.left = current_cell.right  # link
                if r + 1 < self.dim_y:  # check bottom neighbor
                    neighbor_cell = self.array[r + 1][c]
                    neighbor_cell.top = current_cell.bottom  # link

    def make_maze(self):
        """
        Generate a randomized maze.
        """
        initial_cell = ['initial',
                        self.array[random.randint(0, self.dim_y - 1)][
                            random.randint(0, self.dim_x - 1)]]
        stack = []
        stack.append(initial_cell)
        while stack != []:
            current_cell = stack.pop()  # includes direction and Cell object
            # break wall if cell not visited
            if not current_cell[1].visited:
                if current_cell[0] == 'right':
                    current_cell[1].left[0] = True
                if current_cell[0] == 'left':
                    current_cell[1].right[0] = True
                if current_cell[0] == 'top':
                    current_cell[1].bottom[0] = True
                if current_cell[0] == 'bottom':
                    current_cell[1].top[0] = True
                choices = []
                # check neighbors
                if current_cell[1].r != 0:
                    if not self.array[current_cell[1].r - 1][
                        current_cell[
                            1].c].visited:  # check if top neighbor visited
                        choices.append(['top',
                                        self.array[current_cell[1].r - 1][
                                            current_cell[1].c]])
                if current_cell[1].r != self.dim_y - 1:
                    if not self.array[current_cell[1].r + 1][
                        current_cell[
                            1].c].visited:  # check if bottom neighbor visited
                        choices.append(['bottom',
                                        self.array[current_cell[1].r + 1][
                                            current_cell[1].c]])
                if current_cell[1].c != 0:
                    if not self.array[current_cell[1].r][
                        current_cell[
                            1].c - 1].visited:  # check if left neighbor visited
                        choices.append(['left', self.array[current_cell[1].r][
                            current_cell[1].c - 1]])
                if current_cell[1].c != self.dim_x - 1:
                    if not self.array[current_cell[1].r][
                        current_cell[
                            1].c + 1].visited:  # check if right neighbor visited
                        choices.append(['right', self.array[current_cell[1].r][
                            current_cell[1].c + 1]])
                current_cell[1].visited = True
            random.shuffle(choices)
            if choices != []:
                for i in range(len(choices)):  # append neighbors randomly
                    stack.append(choices[i])

    def draw_walls(self):
        """
        Draw the maze's wall.
        """
        self.canvas.grid(row=0, column=0)
        x = 0
        y = 0
        self.window.geometry("1000x1000+10+10")
        for r in range(self.dim_y):
            for c in range(self.dim_x):
                if not self.array[r][c].top[0]:
                    self.canvas.create_line(x, y, x + 20, y, fill='black')
                    time.sleep(0.004)
                if not self.array[r][c].bottom[0]:
                    self.canvas.create_line(x, y + 20, x + 20, y + 20,
                                            fill='black')
                    time.sleep(0.004)
                if not self.array[r][c].right[0]:
                    self.canvas.create_line(x + 20, y, x + 20, y + 20,
                                            fill='black')
                    time.sleep(0.004)
                if not self.array[r][c].left[0]:
                    self.canvas.create_line(x, y, x, y + 20, fill='black')
                    time.sleep(0.004)
                x += 20
                self.window.update()
            y += 20
            x = 0

    def color_cell(self, current_cell : Cell, color : str):
        """
        Color the given <current_cell> with <color>.
        :param current_cell: The current Cell Object
        :param color: The color of the Cell object.
        """
        self.canvas.create_rectangle(current_cell.c * 20 + 3,
                                     current_cell.r * 20 + 3,
                                     current_cell.c * 20 + 20 - 3,
                                     current_cell.r * 20 + 20 - 3, fill=color,
                                     outline="")
        self.window.update()

    def solve_djikstar(self, start_row, start_col, finish_row, finish_col):
        """
        Solve the maze from point <start_row>,<start_col> to point <finish_row>, <finish_col>.
        :param start_row: The  starting row of Maze.
        :param start_col: The starting column of Maze.
        :param finish_row: The finishing row of Maze.
        :param finish_col: The finishing col of Maze.
        """
        d = {}  # 0 = curr_cell #1 = cell_backward
        visited_cells = []
        queue = []
        current_cell = self.array[start_row][start_col]
        self.color_cell(self.array[start_row][start_col], "black")
        while self.array[finish_row][
            finish_col] not in visited_cells:  # finish_cell not yet visited
            if self.array[current_cell.r][current_cell.c].top[0] and \
                    self.array[current_cell.r - 1][
                        current_cell.c] not in visited_cells:
                d.setdefault(self.array[current_cell.r - 1][current_cell.c],
                             self.array[current_cell.r][current_cell.c])
                queue.append(self.array[current_cell.r - 1][current_cell.c])
            if self.array[current_cell.r][current_cell.c].bottom[0] and \
                    self.array[current_cell.r + 1][
                        current_cell.c] not in visited_cells:
                d.setdefault(self.array[current_cell.r + 1][current_cell.c],
                             self.array[current_cell.r][current_cell.c])
                queue.append(self.array[current_cell.r + 1][current_cell.c])
            if self.array[current_cell.r][current_cell.c].right[0] and \
                    self.array[current_cell.r][
                        current_cell.c + 1] not in visited_cells:
                d.setdefault(self.array[current_cell.r][current_cell.c + 1],
                             self.array[current_cell.r][current_cell.c])
                queue.append(self.array[current_cell.r][current_cell.c + 1])
            if self.array[current_cell.r][current_cell.c].left[0] and \
                    self.array[current_cell.r][
                        current_cell.c - 1] not in visited_cells:
                d.setdefault(self.array[current_cell.r][current_cell.c - 1],
                             self.array[current_cell.r][current_cell.c])
                queue.append(self.array[current_cell.r][current_cell.c - 1])
            if current_cell is self.array[finish_row][
                finish_col]:
                self.color_cell(current_cell, "black")
            else :
                self.color_cell(current_cell, "blue")
            time.sleep(0.02)
            visited_cells.append(current_cell)
            if queue != []:
                current_cell = queue.pop(0)

        # trace backwards
        current_cell = visited_cells[-1]
        while current_cell is not self.array[start_row][start_col]:
            self.color_cell(current_cell, "red")
            time.sleep(0.02)
            current_cell = d[current_cell]
        self.color_cell(current_cell, "red")
        time.sleep(0.02)
        print("Maze is solved! Close Window to exit or play again.")
        self.window.mainloop()


def main():
    """
    Run this program to play!
    """
    play = True
    while play:
        print("=== Maze Size ===")
        flag = True
        while flag:
            x = input("x (max is 100) : ")
            if x.isdigit():
                x = int(x)
                if int(x) > 100 :
                    print("Input out of range. Maximum input is 50!")
                else :
                    flag = False
            else:
                print("Invalid Input. Input must be an integer!")
        flag = True
        while flag:
            y = input("y (max is 50) : ")
            if y.isdigit():
                y = int(y)
                if int(y) > 50 :
                    print("Input out of range. Maximum input is 50!")
                else :
                    flag = False
            else:
                print("Invalid Input. Input must be an integer!")
        print("Stand by, Generating Maze........")
        M = Maze(x, y)
        M.make_cells()
        M.link_cells()
        M.make_maze()
        M.draw_walls()
        print("=== Start Point and Final Point ===")
        flag = True
        while flag:
            start_x = input("Start (x) : ")
            if not start_x.isdigit():
                print("Invalid Input. Input must be an integer!")
            else:
                if not 0 <= int(start_x) < x:
                    print(
                        "Input ouf range. Input must be between 0 up to {x}".format(
                            x=M.dim_x-1))
                else:
                    start_x = int(start_x)
                    flag = False
        flag = True
        while flag:
            start_y = input("Start (y) : ")
            if not start_y.isdigit():
                print("Invalid Input. Input must be an integer!")

            else:
                if not 0 <= int(start_y) < y:
                    print(
                        "Input ouf range. Input must be between 0 up to {y}".format(
                            y=M.dim_y-1))
                else:
                    start_y = int(start_y)
                    flag = False
        flag = True
        while flag:
            finish_x = input("Finish (x) : ")
            if not finish_x.isdigit():
                print("Invalid Input. Input must be an integer!")
            else:
                if not 0 <= int(finish_x) < x:
                    print(
                        "Input ouf range. Input must be between 0 up to {x}".format(
                            x=M.dim_x-1))
                else:
                    finish_x = int(finish_x)
                    flag = False

        flag = True
        while flag:
            finish_y = input("Finish (y) : ")
            if not finish_y.isdigit():
                print("Invalid Input. Input must be an integer!")
            else:
                if not 0 <= int(finish_y) < y:
                    print(
                        "Input ouf range. Input must be between 0 up to {y}".format(
                            y=M.dim_y-1))
                else:
                    finish_y = int(finish_y)
                    flag = False
        print("Solving maze with Djikstart Algorithm....")
        M.solve_djikstar(start_y, start_x, finish_y, finish_x)
        flag1 = True
        while flag1:
            print("Do you want to play again?")
            answer = input("Type Y or N : ")
            if answer == "N":
                play = False
                flag1 = False
            elif answer == "Y":
                flag1 = False


if __name__ == "__main__":
    main()
