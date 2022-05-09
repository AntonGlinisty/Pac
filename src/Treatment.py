from Globals import Globals
import pygame
from Food import Food
from Grid import Grid

class Treatment():

    def InputEvents(self, GRID, FOOD, gridCord_LU, gridCord_RU, gridCord_LD,
                                            gridCord_RD, pacman, U_block, I_block, potential, motion, button):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Globals.running = False
            elif event.type == pygame.KEYDOWN:
                (motion, potential, U_block, I_block) = self.Keydown(event, motion, potential,
                                    GRID, gridCord_LU,gridCord_RU, gridCord_LD, gridCord_RD, pacman, U_block, I_block)
            if U_block == 1 and event.type == pygame.MOUSEBUTTONDOWN and I_block == 0:
                self.MouseDrawCell(event, GRID, button)
                I_block = 0
            elif I_block == 1 and event.type == pygame.MOUSEBUTTONDOWN and U_block == 0:
                self.MouseDrawFood(event, GRID, FOOD)

                U_block = 0
        return (motion, potential, U_block, I_block)

    def Keydown(self, event, motion, potential, GRID, gridCord_LU,
                                              gridCord_RU, gridCord_LD, gridCord_RD, pacman, U_block,I_block):
        if event.key == pygame.K_LEFT:
            if (GRID.grid[gridCord_LU[1]][gridCord_LU[0] - 1] == 1
                    or GRID.grid[gridCord_LD[1]][gridCord_LD[0] - 1]):
                potential = Globals.LEFT
            else:
                motion = Globals.LEFT
                potential = Globals.LEFT
        elif event.key == pygame.K_RIGHT:
            if gridCord_RU[0] + 1 < Globals.width // Globals.cell_side:
                if (GRID.grid[gridCord_RU[1]][gridCord_RU[0] + 1] == 1
                        or GRID.grid[gridCord_RD[1]][gridCord_RD[0] + 1] == 1):
                    potential = Globals.RIGHT
                else:
                    motion = Globals.RIGHT
                    potential = Globals.RIGHT
            else:
                motion = Globals.RIGHT
                potential = Globals.RIGHT
        elif event.key == pygame.K_UP:
            if (GRID.grid[gridCord_LU[1] - 1][gridCord_LU[0]] == 1
                    or GRID.grid[gridCord_RU[1] - 1][gridCord_RU[0]] == 1):
                potential = Globals.UP
            else:
                motion = Globals.UP
                potential = Globals.UP
        elif event.key == pygame.K_DOWN:
            if (GRID.grid[gridCord_LD[1] + 1][gridCord_LD[0]] == 1
                    or GRID.grid[gridCord_RD[1] + 1][gridCord_RD[0]] == 1):
                potential = Globals.DOWN
            else:
                motion = Globals.DOWN
                potential = Globals.DOWN
        (I_block, U_block) = self.MagicButtons(event, pacman, gridCord_LU, gridCord_RU, gridCord_LD, gridCord_RD,
                                               U_block, I_block, GRID)
        return (motion, potential, U_block, I_block)

    def MagicButtons(self, event, pacman, gridCord_LU, gridCord_RU, gridCord_LD, gridCord_RD, U_block, I_block, GRID):
        if event.key == pygame.K_o:
            print(gridCord_LU, gridCord_RU, gridCord_LD, gridCord_RD)
            print((pacman.rect.x, pacman.rect.y), (pacman.rect.x + Globals.pacman_side - 1, pacman.rect.y),
                  (pacman.rect.x, pacman.rect.y + Globals.pacman_side - 1), (pacman.rect.x + Globals.pacman_side - 1,
                                                                             pacman.rect.y + Globals.pacman_side - 1))
        elif event.key == pygame.K_u:
            if U_block == 0:
                U_block = 1
                I_block = 0
            else:
                U_block = 0
        elif event.key == pygame.K_i:
            if I_block == 1:
                I_block = 0
            else:
                I_block = 1
                U_block = 0
        elif event.key == pygame.K_p:
            Grid.GridSave(GRID)
        return (I_block, U_block)

    def MouseDrawCell(self, event, GRID, button):
        gridCord = GRID.ScreenToGrid(event.pos)
        if event.button == 1:
            GRID.grid[gridCord[1]][gridCord[0]] = 1
            button = 1
        elif event.button == Globals.yell_food_id:
            GRID.grid[gridCord[1]][gridCord[0]] = 0
            button = 0
        GRID.DrawCell(gridCord, button)

    def MouseDrawFood(self, event, GRID, FOOD):
        gridCord = GRID.ScreenToGrid(event.pos)
        if event.button == 1:
            if GRID.grid[gridCord[1]][gridCord[0]] != 1:
                GRID.grid[gridCord[1]][gridCord[0]] = Globals.yell_food_id
                button = Globals.yell_food_id
                FOOD.DrawFood(gridCord, button)
        elif event.button == Globals.yell_food_id:
            if GRID.grid[gridCord[1]][gridCord[0]] != 1:
                GRID.grid[gridCord[1]][gridCord[0]] = 0
                screenCord = GRID.GridToScreen(gridCord)
                rect = pygame.Rect((screenCord[0], screenCord[1], Globals.cell_side, Globals.cell_side))
                pygame.draw.rect(Globals.screen, Globals.black, rect)

    def Potential(self, potential, motion, GRID, gridCord_LU, gridCord_RU, gridCord_LD, gridCord_RD, pacman):
        if potential != motion:
            if potential == Globals.LEFT and (GRID.grid[gridCord_LU[1]][gridCord_LU[0] - 1] != 1
                                and GRID.grid[gridCord_LD[1]][gridCord_LD[0] - 1] != 1):
                motion = potential
            if potential == Globals.RIGHT and (GRID.grid[gridCord_RU[1]][gridCord_RU[0] + 1] != 1
                                and GRID.grid[gridCord_RD[1]][gridCord_RD[0] + 1] != 1):
                motion = potential
            if pacman.rect.x != Globals.width:
                if potential == Globals.UP and (GRID.grid[gridCord_LU[1] - 1][gridCord_LU[0]] != 1
                                    and GRID.grid[gridCord_RU[1] - 1][gridCord_RU[0]] != 1):
                    motion = potential
                if potential == Globals.DOWN and (GRID.grid[gridCord_LD[1] + 1][gridCord_LD[0]] != 1
                                    and GRID.grid[gridCord_RD[1] + 1][gridCord_RD[0]] != 1):
                    motion = potential
        return (motion)

    def PacmanMovement(self, motion, pacman):
        if motion == Globals.LEFT:
            pacman.rect.x -= Globals.speed
        elif motion == Globals.RIGHT:
            pacman.rect.x += Globals.speed
        elif motion == Globals.UP:
            pacman.rect.y -= Globals.speed
        elif motion == Globals.DOWN:
            pacman.rect.y += Globals.speed

    def PacmanTeleport(self, pacman):
        if pacman.rect.x + int(Globals.pacman_side) <= 0:
            pacman.rect.x = int(Globals.width)
        elif pacman.rect.x >= int(Globals.width):
            pacman.rect.x = -int(Globals.pacman_side)

    def PacmanChangeDir(self, motion, direction, pacman):
        if motion == Globals.LEFT:
            if direction == Globals.RIGHT:
                pacman.image = pygame.transform.rotate(pacman.image, Globals.pac_turn_ei)
            elif direction == Globals.UP:
                pacman.image = pygame.transform.rotate(pacman.image, Globals.pac_turn_nin)
            elif direction == Globals.DOWN:
                pacman.image = pygame.transform.rotate(pacman.image, Globals.pac_turn_sev)
        elif motion == Globals.RIGHT:
            if direction == Globals.LEFT:
                pacman.image = pygame.transform.rotate(pacman.image, Globals.pac_turn_ei)
            elif direction == Globals.DOWN:
                pacman.image = pygame.transform.rotate(pacman.image, Globals.pac_turn_nin)
            elif direction == Globals.UP:
                pacman.image = pygame.transform.rotate(pacman.image, Globals.pac_turn_sev)
        elif motion == Globals.UP:
            if direction == Globals.DOWN:
                pacman.image = pygame.transform.rotate(pacman.image, Globals.pac_turn_ei)
            elif direction == Globals.RIGHT:
                pacman.image = pygame.transform.rotate(pacman.image, Globals.pac_turn_nin)
            elif direction == Globals.LEFT:
                pacman.image = pygame.transform.rotate(pacman.image, Globals.pac_turn_sev)
        elif motion == Globals.DOWN:
            if direction == Globals.UP:
                pacman.image = pygame.transform.rotate(pacman.image, Globals.pac_turn_ei)
            elif direction == Globals.LEFT:
                pacman.image = pygame.transform.rotate(pacman.image, Globals.pac_turn_nin)
            elif direction == Globals.RIGHT:
                pacman.image = pygame.transform.rotate(pacman.image, Globals.pac_turn_sev)
        if motion != Globals.STOP:
            direction = motion
        return (motion, direction)

    def Counter(self, i):
        i += 1
        return i

    def PacmanMouth(self, direction, pacman, counter):
        if counter % Globals.mou_cl_freq == 0:
            pacman.image = pygame.transform.scale(Globals.player_img_mouth, Globals.pacman_size)
        if counter % Globals.mou_op_freq == 0 and not counter % Globals.mou_cl_freq == 0:
            if direction == Globals.LEFT:
                pacman.image = pygame.transform.scale(Globals.player_img_left, Globals.pacman_size)
            elif direction == Globals.RIGHT:
                pacman.image = pygame.transform.scale(Globals.player_img_right, Globals.pacman_size)
            elif direction == Globals.UP:
                pacman.image = pygame.transform.scale(Globals.player_img_up, Globals.pacman_size)
            elif direction == Globals.DOWN:
                pacman.image = pygame.transform.scale(Globals.player_img_down, Globals.pacman_size)

    def PacmanObstacle(self, motion, GRID, gridCord_LU, gridCord_RU, gridCord_LD, gridCord_RD, pacman):
        if motion == Globals.LEFT and (GRID.grid[gridCord_LU[1]][gridCord_LU[0] - 1] == 1
                                        or GRID.grid[gridCord_LD[1]] [gridCord_LD[0] - 1] == 1) \
                                                                    and pacman.rect.x % int(Globals.pacman_side) == 0:
            motion = Globals.STOP
        if gridCord_RU[0] + 1 < int(Globals.width//Globals.cell_side):
            if motion == Globals.RIGHT and (GRID.grid[gridCord_RU[1]][gridCord_RU[0] + 1] == 1
                                        or GRID.grid[gridCord_RD[1]][gridCord_RD[0] + 1] == 1) \
                                                                    and pacman.rect.x % int(Globals.pacman_side) == 0:
                motion = Globals.STOP
        if motion == Globals.UP and (GRID.grid[gridCord_LU[1] - 1][gridCord_LU[0]] == 1
                                        or GRID.grid[gridCord_RU[1] - 1][gridCord_RU[0]] == 1) \
                                                                    and pacman.rect.y % int(Globals.pacman_side) == 0:
            motion = Globals.STOP
        if motion == Globals.DOWN and (GRID.grid[gridCord_LD[1] + 1][gridCord_LD[0]] == 1
                                        or GRID.grid[gridCord_RD[1] + 1][gridCord_RD[0]] == 1) \
                                                                    and pacman.rect.y % int(Globals.pacman_side) == 0:
            motion = Globals.STOP
        return motion

    def PacmanEat(self, motion, GRID, pacman, gridCord_LU, gridCord_RU, gridCord_LD, gridCord_RD, score, foodcounter):
        if gridCord_RU[0] + 1 < int(Globals.width // Globals.cell_side):
            if motion == Globals.LEFT and GRID.grid[gridCord_LU[1]][gridCord_LU[0]] == Globals.yell_food_id:
                if pacman.rect.x % int(Globals.cell_side) == int(Globals.cell_side) // 2 + Globals.food_ind:
                    GRID.grid[gridCord_LU[1]][gridCord_LU[0]] = 0
                    Food.DrawFood(Food, gridCord_LU, Globals.black_food_id)
                    score += Globals.bonus1
                    foodcounter -= 1
            if motion == Globals.RIGHT and GRID.grid[gridCord_RU[1]][gridCord_RU[0]] == Globals.yell_food_id:
                if pacman.rect.x % int(Globals.cell_side) == int(Globals.cell_side) // 2 - Globals.food_ind:
                    GRID.grid[gridCord_RU[1]][gridCord_RU[0]] = 0
                    Food.DrawFood(Food, gridCord_RU, Globals.black_food_id)
                    score += Globals.bonus1
                    foodcounter -= 1
            if motion == Globals.UP and GRID.grid[gridCord_LU[1]][gridCord_LU[0]] == Globals.yell_food_id:
                if pacman.rect.y % int(Globals.cell_side) == int(Globals.cell_side) // 2 + Globals.food_ind:
                    GRID.grid[gridCord_LU[1]][gridCord_LU[0]] = 0
                    Food.DrawFood(Food, gridCord_LU, Globals.black_food_id)
                    score += Globals.bonus1
                    foodcounter -= 1
            if motion == Globals.DOWN and GRID.grid[gridCord_LD[1]][gridCord_LD[0]] == Globals.yell_food_id:
                if pacman.rect.y % int(Globals.cell_side) == int(Globals.cell_side) // 2 - Globals.food_ind:
                    GRID.grid[gridCord_RD[1]][gridCord_RD[0]] = 0
                    Food.DrawFood(Food, gridCord_RD, Globals.black_food_id)
                    score += Globals.bonus1
                    foodcounter -= 1
        return (GRID, score, foodcounter)
