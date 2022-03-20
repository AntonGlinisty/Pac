from Globals import Globals
import pygame

class Grid():

    def __init__(self):
        self.grid = [[int(0)] * Globals.cell_w_count for i in range(Globals.cell_h_count)]
        self.GridFilling()

    def GridFilling(self):
        file_line_counter = -1
        line_symbol_counter = -1
        with open("new.txt", "r") as f:
            for line in f.readlines():
                file_line_counter += 1
                for symbol in line:
                    line_symbol_counter += 1
                    if line_symbol_counter == 30:
                        break
                    if int(symbol) == int(2):
                        self.grid[file_line_counter][line_symbol_counter] = 0
                    else:
                        self.grid[file_line_counter][line_symbol_counter] = int(symbol)
                line_symbol_counter = -1

    def PrintGrid(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                print(self.grid[i][j], end=' ')
            print()

    def ScreenToGrid(self, screenCord):
        return (screenCord[0]//40, screenCord[1]//40)

    def GridToScreen(self, gridCord):
        return (gridCord[0] * Globals.cell_side, gridCord[1] * Globals.cell_side)

    def DrawCell(self, gridCord, button):
        screenCord = self.GridToScreen(gridCord)

        rect = pygame.Rect((screenCord[0], screenCord[1], Globals.cell_side, Globals.cell_side))
        if button == 0:
            pygame.draw.rect(Globals.screen, Globals.black, rect)
        elif button == 1:
            pygame.draw.rect(Globals.screen, Globals.blue, rect)

    def DrawGrid(self):
        for line_counter in range(15):
            for column_counter in range(30):
                self.DrawCell((column_counter, line_counter), int(self.grid[line_counter][column_counter]))

    def PacmanLocation(self, screenCord, motion):
        gridCord = self.ScreenToGrid(screenCord)
        if gridCord[0] + 1 < 30:
            self.grid[gridCord[1]][gridCord[0]] = 2
            if motion == Globals.LEFT and self.grid[gridCord[1]][gridCord[0] + 1] == 2:
                self.grid[gridCord[1]][gridCord[0] + 1] = 0
            elif motion == Globals.RIGHT and self.grid[gridCord[1]][gridCord[0] - 1] == 2:
                self.grid[gridCord[1]][gridCord[0] - 1] = 0
            elif motion == Globals.UP and self.grid[gridCord[1] + 1][gridCord[0]] == 2:
                self.grid[gridCord[1] + 1][gridCord[0]] = 0
            elif motion == Globals.DOWN and self.grid[gridCord[1] - 1][gridCord[0]] == 2:
                self.grid[gridCord[1] - 1][gridCord[0]] = 0

    def GridSave(self):
        f = open('new.txt', 'w+')
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                a = self.grid[i][j]
                f.write(str(a))
            f.write('\n')
