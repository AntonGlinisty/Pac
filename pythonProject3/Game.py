import sys

import pygame
from Globals import Globals
from Grid import Grid
from Pacman import Pacman
from Treatment import Treatment
from Food import Food
from Ghosts import Ghosts
from collections import deque
from datetime import datetime


class Game():

    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    pacman = Pacman()
    #blinky = Blinky()
    blinky = Ghosts('blinky')
    # pinky = Ghosts(pinky)
    # inky = Ghosts(inky)
    # clyde = Ghosts(clyde)
    all_sprites.add(pacman)
    all_sprites.add(blinky)
    GRID = Grid()
    FOOD = Food()
    GRID.DrawGrid()
    FOOD.DrawAllFood()
    U_block = 0
    I_block = 0
    button = 0
    motion = Globals.LEFT
    potential = Globals.STOP
    direction = Globals.LEFT
    treatment = Treatment()
    i = 0
    score = 0

    gridCord_b = GRID.ScreenToGrid(blinky.rect.center)



    # graph = {}
    # for y, row in enumerate(GRID.grid):
    #     for x, col in enumerate(row):
    #         if col != 1:
    #             graph[(x, y)] = graph.get((x, y), []) + Ghosts.Get_next_nodes(blinky, x, y, GRID)
    # goal = gridCord_b
    # queue = deque([gridCord_b])
    # visited = {gridCord_b: None}




    while Globals.running:
        gridCord_b = GRID.ScreenToGrid(blinky.rect.center)
        gridCord = GRID.ScreenToGrid(pacman.rect.center)
        gridCord_LU = GRID.ScreenToGrid((pacman.rect.x, pacman.rect.y))
        gridCord_RU = GRID.ScreenToGrid((pacman.rect.x + int(Globals.pacman_side) - 1, pacman.rect.y))
        gridCord_LD = GRID.ScreenToGrid((pacman.rect.x, pacman.rect.y + int(Globals.pacman_side) - 1))
        gridCord_RD = GRID.ScreenToGrid((pacman.rect.x + int(Globals.pacman_side) - 1,
                                         pacman.rect.y + int(Globals.pacman_side) - 1))
        clock.tick(Globals.fps)
        all_sprites.update()
        all_sprites.draw(Globals.screen)
        (GRID, score) = treatment.PacmanEat(motion, GRID, pacman, gridCord_LU, gridCord_RU,
                                                                                gridCord_LD, gridCord_RD, score)
        GRID.PacmanLocation(pacman.rect.center, motion)
        (motion, potential, U_block, I_block) = treatment.InputEvents(GRID, FOOD, gridCord_LU, gridCord_RU, gridCord_LD,
                                                    gridCord_RD, pacman, U_block, I_block, potential, motion, button)

        motion = treatment.Potential(potential, motion, GRID, gridCord_LU,
                                                      gridCord_RU, gridCord_LD, gridCord_RD, pacman)

        Grid.Score(GRID, score)
        # path_segment = Ghosts.funkforgame(blinky, gridCord_b, gridCord, graph, GRID, visited, goal, gridCord_RU)


        pygame.display.update()
        pacman.Delete()
        # blinky.Delete()

        # Ghosts.WayMaking(blinky, path_segment, gridCord)
        treatment.PacmanMovement(motion, pacman)
        motion = treatment.PacmanObstacle(motion, GRID, gridCord_LU, gridCord_RU, gridCord_LD, gridCord_RD, pacman)
        treatment.PacmanTeleport(pacman)
        (motion, direction) = treatment.PacmanChangeDir(motion, direction, pacman)
        treatment.PacmanMouth(direction, pacman, i)
        i = treatment.Counter(i)
    nextgoal = (0, 0)
    i = 0
    score = 0
    gridCord_b = GRID.ScreenToGrid(blinky.rect.center)
    graph = {}
    for y, row in enumerate(GRID.grid):
        for x, col in enumerate(row):
            if col != 1:
                graph[(x, y)] = graph.get((x, y), []) + Ghosts.Get_next_nodes(blinky, x, y, GRID)
    goal = gridCord_b
    queue = deque([gridCord_b])
    visited = {gridCord_b: None}
    listofPacpassed = []
    live = 3
    marker = marker2 = True
    while Globals.running:
        if marker:
            gridCord_b = GRID.ScreenToGrid(blinky.rect.center)
            gridCord = GRID.ScreenToGrid(pacman.rect.center)
            gridCord_LU = GRID.ScreenToGrid((pacman.rect.x, pacman.rect.y))
            gridCord_RU = GRID.ScreenToGrid((pacman.rect.x + int(Globals.pacman_side) - 1, pacman.rect.y))
            gridCord_LD = GRID.ScreenToGrid((pacman.rect.x, pacman.rect.y + int(Globals.pacman_side) - 1))
            gridCord_RD = GRID.ScreenToGrid((pacman.rect.x + int(Globals.pacman_side) - 1,
                                             pacman.rect.y + int(Globals.pacman_side) - 1))
            if len(listofPacpassed) != 0:
                if listofPacpassed[len(listofPacpassed) - 1] != gridCord:
                    listofPacpassed.append(gridCord)
            else:
                listofPacpassed.append(gridCord)
            clock.tick(Globals.fps)
            all_sprites.update()
            all_sprites.draw(Globals.screen)
            (GRID, score) = treatment.PacmanEat(motion, GRID, pacman, gridCord_LU, gridCord_RU,
                                                                                    gridCord_LD, gridCord_RD, score)
            GRID.PacmanLocation(pacman.rect.center, motion)
            (motion, potential, U_block, I_block) = treatment.InputEvents(GRID, FOOD, gridCord_LU, gridCord_RU, gridCord_LD,
                                                        gridCord_RD, pacman, U_block, I_block, potential, motion, button)

            motion = treatment.Potential(potential, motion, GRID, gridCord_LU,
                                                          gridCord_RU, gridCord_LD, gridCord_RD, pacman)

            Grid.Score(GRID, score)

            nextgoal = blinky.Nextgoal(gridCord_b, listofPacpassed, graph, GRID, visited, goal, gridCord_RU, nextgoal, i)
            live, marker2 = blinky.Catcher((pacman.rect.x, pacman.rect.y), (blinky.rect.x, blinky.rect.y), live, marker2)
            print(live)
            GRID.Hearts(3)

            pygame.display.update()
            pacman.Delete()
            blinky.Delete()

            Ghosts.WayMaking(blinky, nextgoal)
            treatment.PacmanMovement(motion, pacman)
            motion = treatment.PacmanObstacle(motion, GRID, gridCord_LU, gridCord_RU, gridCord_LD, gridCord_RD, pacman)
            treatment.PacmanTeleport(pacman)
            (motion, direction) = treatment.PacmanChangeDir(motion, direction, pacman)
            treatment.PacmanMouth(direction, pacman, i)
            i = treatment.Counter(i)
            if marker2:
                if live == 2 or live == 1:
                    marker = False
                    marker2 = False
                    motion = Globals.LEFT
                    start = datetime.now().second
                if live == 0:
                    Globals.running = False

            GRID.GridSave()
        if marker == False:
            clock.tick(Globals.fps)
            f1 = pygame.font.SysFont('calibri', 70)
            text1 = f1.render('You are dead', True, Globals.red)
            Globals.screen.blit(Globals.sf, (0, 0))
            Globals.screen.blit(text1, (Globals.width // 3, Globals.height // 8 * 3))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Globals.running = False
            if datetime.now().second - start == 3:
                marker = True
                GRID.DrawGrid()
                FOOD.DrawAllFood()
                pacman.rect.x = Globals.pac_spawnkord_x
                pacman.rect.y = Globals.pac_spawnkord_y
                blinky.rect.x = Globals.r_gh_spawnkord_x
                blinky.rect.y = Globals.r_gh_spawnkord_y
            pygame.display.update()

    pygame.quit()
