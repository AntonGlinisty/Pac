import pygame
from Globals import Globals
from Grid import Grid
from Pacman import Pacman
from Treatment import Treatment


class Game():

    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    pacman = Pacman()
    all_sprites.add(pacman)
    GRID = Grid()
    GRID.DrawGrid()
    mouse = 0
    button = 0
    motion = Globals.LEFT
    potential = Globals.STOP
    direction = Globals.LEFT
    treatment = Treatment()
    while Globals.running:
        gridCord = GRID.ScreenToGrid(pacman.rect.center)
        gridCord_LU = GRID.ScreenToGrid((pacman.rect.x, pacman.rect.y))
        gridCord_RU = GRID.ScreenToGrid((pacman.rect.x + 39, pacman.rect.y))
        gridCord_LD = GRID.ScreenToGrid((pacman.rect.x, pacman.rect.y + 39))
        gridCord_RD = GRID.ScreenToGrid((pacman.rect.x + 39, pacman.rect.y + 39))
        clock.tick(Globals.fps)
        all_sprites.add(pacman)
        all_sprites.update()
        all_sprites.draw(Globals.screen)
        GRID.PacmanLocation(pacman.rect.center, motion)
        (motion, potential, mouse) = treatment.InputEvents(GRID, gridCord_LU, gridCord_RU, gridCord_LD,
                                                           gridCord_RD, pacman, mouse, potential, motion, button)
        motion = treatment.Potential(potential, motion, GRID, gridCord_LU, gridCord_RU, gridCord_LD, gridCord_RD)
        pygame.display.update()
        pacman.Delete()
        treatment.PacmanMovement(motion, pacman)
        motion = treatment.PacmanObstacle(motion, GRID, gridCord_LU, gridCord_RU, gridCord_LD, gridCord_RD, pacman)
        treatment.PacmanTeleport(pacman)
        (motion, direction) = treatment.PacmanChangeDir(motion, direction, pacman)
    GRID.GridSave()

    pygame.quit()
