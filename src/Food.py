import pygame
from Grid import Grid
from Globals import Globals


class Food(Grid):

    def DrawFood(self, gridCord, button):
        screenCord = Grid.GridToScreen(Grid, gridCord)

        if button == Globals.yell_food_id:
            pygame.draw.circle(Globals.screen, Globals.yellow, (screenCord[0] + Globals.cell_side // 2,
                                                            screenCord[1] + Globals.cell_side//2), Globals.food_size)
        if button == Globals.black_food_id:
            pygame.draw.circle(Globals.screen, Globals.black, (screenCord[0] + Globals.cell_side // 2,
                                                            screenCord[1] + Globals.cell_side // 2), Globals.food_size)

    def DrawAllFood(self, GRID):
        for line_counter in range(int(Globals.height//Globals.cell_side)):
            for column_counter in range(int(Globals.width//Globals.cell_side)):
                self.DrawFood((column_counter, line_counter), int(GRID.grid[line_counter][column_counter]))

    def EndCheacker(self, foodcounter, GRID, FOOD, pacman, blinky, inky, clyde, marker, marker4, i, motion, score,
                    marker7, marker8, marker9, marker10, marker11, marker12, live):
        if foodcounter == 0:
            Globals.screen.blit(Globals.sf, (0, 0))
            a = Food()
            b = Grid()
            FOOD = a
            GRID = b
            GRID.DrawGrid()
            FOOD.DrawAllFood(GRID)
            pacman.rect.x = Globals.pac_spawnkord_x
            pacman.rect.y = Globals.pac_spawnkord_y
            blinky.rect.x = Globals.r_gh_spawnkord_x
            blinky.rect.y = Globals.r_gh_spawnkord_y
            clyde.rect.x = Globals.or_gh_spawnkord_x
            clyde.rect.y = Globals.or_gh_spawnkord_y
            inky.rect.x = Globals.bl_gh_spawnkord_x
            inky.rect.y = Globals.bl_gh_spawnkord_y
            i = 1
            score = 0
            live = Globals.lives_stat
            foodcounter = Globals.food_count_stat
            motion = Globals.LEFT
            marker = marker4 = marker7 = marker8 = marker9 = marker10 = marker11 = marker12 = True
        return (marker, marker4, i, foodcounter, motion, score, marker7, marker8, marker9, marker10, marker11, marker12,
                live, GRID, FOOD)