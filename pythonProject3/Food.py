import pygame
from Grid import Grid
from Globals import Globals


class Food(Grid):
    def DrawFood(self, gridCord, button):
        screenCord = Grid.GridToScreen(Grid, gridCord)
        rect = pygame.Rect((screenCord[0], screenCord[1], Globals.cell_side, Globals.cell_side))
        if button == 0:
            pygame.draw.rect(Globals.screen, Globals.black, rect)
        if button == 3:
            pygame.draw.circle(Globals.screen, Globals.yellow, (screenCord[0] + Globals.cell_side//2,
                                                                            screenCord[1] + Globals.cell_side//2), 5)
        if button == 4:
            pygame.draw.circle(Globals.screen, Globals.black, (screenCord[0] + Globals.cell_side//2,
                                                                            screenCord[1] + Globals.cell_side//2), 5)

    def DrawAllFood(self):
        for line_counter in range(int(Globals.height//Globals.cell_side)):
            for column_counter in range(int(Globals.width//Globals.cell_side)):
                self.DrawFood((column_counter, line_counter), int(self.grid[line_counter][column_counter]))
