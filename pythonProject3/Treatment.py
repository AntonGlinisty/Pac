from Globals import Globals
import pygame

class Treatment():

    def InputEvents(self, GRID, gridCord_LU, gridCord_RU, gridCord_LD,
                                            gridCord_RD, pacman, mouse, potential, motion, button):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Globals.running = False
            elif event.type == pygame.KEYDOWN:
                (motion, potential, mouse) = self.Keydown(event, motion, potential, GRID, gridCord_LU,
                                                               gridCord_RU, gridCord_LD, gridCord_RD, pacman, mouse)
            if mouse == 1 and event.type == pygame.MOUSEBUTTONDOWN:
                self.Mousedown(event, GRID, button)
        return (motion, potential, mouse)

    def Keydown(self, event, motion, potential, GRID, gridCord_LU,
                                            gridCord_RU, gridCord_LD, gridCord_RD, pacman, mouse):
        if event.key == pygame.K_LEFT:
            if (GRID.grid[gridCord_LU[1]][gridCord_LU[0] - 1] == 1
                    or GRID.grid[gridCord_LD[1]][gridCord_LD[0] - 1]):
                potential = Globals.LEFT
            else:
                motion = Globals.LEFT
                potential = Globals.LEFT
        elif event.key == pygame.K_RIGHT:
            if gridCord_RU[0] + 1 < 30:
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
        elif event.key == pygame.K_o:
            print(gridCord_LU, gridCord_RU, gridCord_LD, gridCord_RD)
            print((pacman.rect.x, pacman.rect.y), (pacman.rect.x + 39, pacman.rect.y),
                  (pacman.rect.x, pacman.rect.y + 39), (pacman.rect.x + 39, pacman.rect.y + 39))
        elif event.key == pygame.K_u:
            if mouse == 0:
                mouse = 1
            else:
                mouse = 0
        return (motion, potential, mouse)

    def Mousedown(self, event, GRID, button):
        gridCord = GRID.ScreenToGrid(event.pos)
        if event.button == 1:
            GRID.grid[gridCord[1]][gridCord[0]] = 1
            button = 1
        elif event.button == 3:
            GRID.grid[gridCord[1]][gridCord[0]] = 0
            button = 0
        GRID.DrawCell(gridCord, button)

    def Potential(self, potential, motion, GRID, gridCord_LU, gridCord_RU, gridCord_LD, gridCord_RD):
        if potential != motion:
            if potential == Globals.LEFT and (GRID.grid[gridCord_LU[1]][gridCord_LU[0] - 1] == 0
                                and GRID.grid[gridCord_LD[1]][gridCord_LD[0] - 1] == 0):
                motion = potential

            if potential == Globals.RIGHT and (GRID.grid[gridCord_RU[1]][gridCord_RU[0] + 1] == 0
                                and GRID.grid[gridCord_RD[1]][gridCord_RD[0] + 1] == 0):
                motion = potential

            if potential == Globals.UP and (GRID.grid[gridCord_LU[1] - 1][gridCord_LU[0]] == 0
                                and GRID.grid[gridCord_RU[1] - 1][gridCord_RU[0]] == 0):
                motion = potential

            if potential == Globals.DOWN and (GRID.grid[gridCord_LD[1] + 1][gridCord_LD[0]] == 0
                                and GRID.grid[gridCord_RD[1] + 1][gridCord_RD[0]] == 0):
                motion = potential
        return motion

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
        if pacman.rect.x + 40 <= 0:
            pacman.rect.x = 1200
        elif pacman.rect.x >= 1200:
            pacman.rect.x = -40

    def PacmanChangeDir(self, motion, direction, pacman):
        if motion == Globals.LEFT:
            if direction == Globals.LEFT:
                pass
            elif direction == Globals.RIGHT:
                pacman.image = pygame.transform.rotate(pacman.image, 180)
                direction = Globals.LEFT
            elif direction == Globals.UP:
                pacman.image = pygame.transform.rotate(pacman.image, 90)
                direction = Globals.LEFT
            elif direction == Globals.DOWN:
                pacman.image = pygame.transform.rotate(pacman.image, 270)
                direction = Globals.LEFT
        elif motion == Globals.RIGHT:
            if direction == Globals.RIGHT:
                pass
            elif direction == Globals.LEFT:
                pacman.image = pygame.transform.rotate(pacman.image, 180)
                direction = Globals.RIGHT
            elif direction == Globals.DOWN:
                pacman.image = pygame.transform.rotate(pacman.image, 90)
                direction = Globals.RIGHT
            elif direction == Globals.UP:
                pacman.image = pygame.transform.rotate(pacman.image, 270)
                direction = Globals.RIGHT
        elif motion == Globals.UP:
            if direction == Globals.UP:
                pass
            elif direction == Globals.DOWN:
                pacman.image = pygame.transform.rotate(pacman.image, 180)
                direction = Globals.UP
            elif direction == Globals.RIGHT:
                pacman.image = pygame.transform.rotate(pacman.image, 90)
                direction = Globals.UP
            elif direction == Globals.LEFT:
                pacman.image = pygame.transform.rotate(pacman.image, 270)
                direction = Globals.UP
        elif motion == Globals.DOWN:
            if direction == Globals.DOWN:
                pass
            elif direction == Globals.UP:
                pacman.image = pygame.transform.rotate(pacman.image, 180)
                direction = Globals.DOWN
            elif direction == Globals.LEFT:
                pacman.image = pygame.transform.rotate(pacman.image, 90)
                direction = Globals.DOWN
            elif direction == Globals.RIGHT:
                pacman.image = pygame.transform.rotate(pacman.image, 270)
                direction = Globals.DOWN
        pacman.image.set_colorkey(Globals.white)
        return (motion, direction)

    def PacmanObstacle(self, motion, GRID, gridCord_LU, gridCord_RU, gridCord_LD, gridCord_RD, pacman):
        if motion == Globals.LEFT and (GRID.grid[gridCord_LU[1]][gridCord_LU[0] - 1] == 1
                               or GRID.grid[gridCord_LD[1]][gridCord_LD[0] - 1] == 1) and pacman.rect.x % 40 == 0:
            motion = Globals.STOP
        if gridCord_RU[0] + 1 < 30:
            if motion == Globals.RIGHT and (GRID.grid[gridCord_RU[1]][gridCord_RU[0] + 1] == 1
                                   or GRID.grid[gridCord_RD[1]][gridCord_RD[0] + 1] == 1) and pacman.rect.x % 40 == 0:
                motion = Globals.STOP
        if motion == Globals.UP and (GRID.grid[gridCord_LU[1] - 1][gridCord_LU[0]] == 1
                               or GRID.grid[gridCord_RU[1] - 1][gridCord_RU[0]] == 1) and pacman.rect.y % 40 == 0:
            motion = Globals.STOP
        if motion == Globals.DOWN and (GRID.grid[gridCord_LD[1] + 1][gridCord_LD[0]] == 1
                               or GRID.grid[gridCord_RD[1] + 1][gridCord_RD[0]] == 1) and pacman.rect.y % 40 == 0:
            motion = Globals.STOP
        return motion