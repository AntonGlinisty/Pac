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
    blinky = Ghosts.Type(Ghosts, 'blinky')
    inky = Ghosts.Type(Ghosts, 'inky')
    clyde = Ghosts.Type(Ghosts, 'clyde')
    all_sprites.add(inky)
    all_sprites.add(clyde)
    all_sprites.add(pacman)
    all_sprites.add(blinky)
    GRID = Grid()
    grid = Grid()
    FOOD = Food()
    GRID.DrawGrid()
    FOOD.DrawAllFood(GRID)
    U_block = 0
    I_block = 0
    button = 0
    motion = Globals.LEFT
    potential = Globals.STOP
    direction = Globals.LEFT
    treatment = Treatment()
    nextgoalbl = nextgoalcl = nextgoalin = (0, 0)
    iter_count = 1
    score = 0
    gridCord_i = GRID.ScreenToGrid(inky.rect.center)
    gridCord_b = GRID.ScreenToGrid(blinky.rect.center)
    gridCord_c = GRID.ScreenToGrid(clyde.rect.center)
    graphin, goalin, queuein, visitedin = inky.Alg(GRID, gridCord_i)
    graphbl, goalbl, queuebl, visitedbl = blinky.Alg(GRID, gridCord_b)
    graphcl, goalcl, queuecl, visitedcl = clyde.Alg(GRID, gridCord_b)
    listofPacpassed = []
    live = 3
    marker = marker2 = marker3 = marker4 = marker5 = marker6 = marker7 = marker8 = marker9 = marker10 = marker11 = \
        marker12 = True
    bl_movement = cl_movement = in_movement = Globals.STOP
    cordsbl = cordscl = cordsin = (0, 0)
    while Globals.running:
        if marker:
            gridCord_i = GRID.ScreenToGrid(inky.rect.center)
            gridCord_b = GRID.ScreenToGrid(blinky.rect.center)
            gridCord_c = GRID.ScreenToGrid(clyde.rect.center)
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
            if iter_count % Globals.cleaner_count == 0:
                GRID.RoundDrawer(gridCord_b, blinky)
                GRID.RoundDrawer(gridCord_c, clyde)
                GRID.RoundDrawer(gridCord_i, inky)

            FOOD.DrawAllFood(GRID)
            all_sprites.update()
            all_sprites.draw(Globals.screen)
            (GRID, score, Globals.foodcounter) = treatment.PacmanEat(motion, GRID, pacman, gridCord_LU, gridCord_RU,
                                                        gridCord_LD, gridCord_RD, score, Globals.foodcounter)
            GRID.PacmanLocation(pacman.rect.center, motion)
            (motion, potential, U_block, I_block) = treatment.InputEvents(GRID, FOOD, gridCord_LU, gridCord_RU,
                                        gridCord_LD, gridCord_RD, pacman, U_block, I_block, potential, motion, button)

            motion = treatment.Potential(potential, motion, GRID, gridCord_LU,
                                                          gridCord_RU, gridCord_LD, gridCord_RD, pacman)

            GRID.Score(score)
            (marker, marker4, iter_count, Globals.foodcounter, motion, score, marker7, marker8, marker9, marker10,
             marker11, marker12, live) = FOOD.EndCheacker(Globals.foodcounter, grid, FOOD, pacman, blinky, inky, clyde,
             marker, marker4, iter_count, motion, score, marker7, marker8, marker9, marker10, marker11, marker12, live)
            if iter_count % Globals.pas_mode == 0:
                if marker4:
                    marker4 = False
            if iter_count % Globals.agr_mode == 0:
                if marker4 == False:
                    marker4 = True

            live, marker2 = blinky.Catcher((pacman.rect.x, pacman.rect.y), (blinky.rect.x, blinky.rect.y), live)
            live, marker5 = clyde.Catcher((pacman.rect.x, pacman.rect.y), (clyde.rect.x, clyde.rect.y), live)
            live, marker6 = inky.Catcher((pacman.rect.x, pacman.rect.y), (inky.rect.x, inky.rect.y), live)

            GRID.Mode(marker4)
            GRID.Hearts(live)
            pygame.display.update()

            pacman.Delete()
            blinky.Delete()
            clyde.Delete()
            inky.Delete()

            if iter_count >= Globals.inky_out and marker11:
                marker12, nextgoalin, marker11 = inky.StarterGoal(GRID, gridCord_i, graphin, visitedin, goalin, marker12,
                                                                 marker11, nextgoalin)
                in_movement = inky.GhostsPotential(nextgoalin, in_movement, GRID)
                inky.WayMaking(in_movement)
            if marker12 == False:
                if marker4:
                    nextgoalin, cordsin = inky.RandomMode(GRID, nextgoalin, gridCord_i, graphin, visitedin, goalin,
                                                          cordsin)
                else:
                    nextgoalin = inky.InkyGoal(motion, pacman, gridCord_i, graphin, GRID, visitedin, goalin, nextgoalin)
                in_movement = inky.GhostsPotential(nextgoalin, in_movement, GRID)
                inky.WayMaking(in_movement)

            if iter_count >= Globals.clyde_out and marker8:
                marker7, nextgoalcl, marker8 = clyde.StarterGoal(GRID, gridCord_c, graphcl, visitedcl, goalcl, marker7,
                                                                 marker8, nextgoalcl)
                cl_movement = clyde.GhostsPotential(nextgoalcl, cl_movement, GRID)
                clyde.WayMaking(cl_movement)
            if marker7 == False:
                nextgoalcl, cordscl = clyde.RandomMode(GRID, nextgoalcl, gridCord_c, graphcl, visitedcl, goalcl, cordscl)
                cl_movement = clyde.GhostsPotential(nextgoalcl, cl_movement, GRID)
                clyde.WayMaking(cl_movement)

            if iter_count >= Globals.blinky_out and marker9:
                marker10, nextgoalbl, marker9 = blinky.StarterGoal(GRID, gridCord_b, graphbl, visitedbl, goalbl, marker10,
                                                                 marker9, nextgoalbl)
                bl_movement = blinky.GhostsPotential(nextgoalbl, bl_movement, GRID)
                blinky.WayMaking(bl_movement)
            if marker10 == False:
                if marker4:
                    nextgoalbl, cordsbl = blinky.RandomMode(GRID, nextgoalbl, gridCord_b, graphbl,
                                                            visitedbl, goalbl, cordsbl)
                else:
                    nextgoalbl = blinky.Nextgoal(gridCord_b, listofPacpassed, graphbl, GRID, visitedbl, goalbl,
                                                 nextgoalbl)
                bl_movement = blinky.GhostsPotential(nextgoalbl, bl_movement, GRID)
                blinky.WayMaking(bl_movement)

            treatment.PacmanMovement(motion, pacman)
            motion = treatment.PacmanObstacle(motion, GRID, gridCord_LU, gridCord_RU, gridCord_LD, gridCord_RD, pacman)
            treatment.PacmanTeleport(pacman)
            (motion, direction) = treatment.PacmanChangeDir(motion, direction, pacman)
            treatment.PacmanMouth(direction, pacman, iter_count)
            iter_count = treatment.Counter(iter_count)
            if marker2 or marker5 or marker6:
                if live == 2 or live == 1:
                    marker = marker2 = marker5 = marker6 = False
                    motion = Globals.LEFT
                    start = datetime.now().second
                if live == 0:
                    Globals.running = False
            GRID.GridSave()
        if marker == False:
            clock.tick(Globals.fps)
            Globals.screen.blit(Globals.sf, (0, 0))
            Globals.screen.blit(Globals.dead, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Globals.running = False
            if datetime.now().second - start >= 2:
                marker = True
                Globals.screen.blit(Globals.sf, (0, 0))
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
                iter_count = 1
                marker7 = marker8 = marker9 = marker10 = marker11 = marker12 = True
                marker4 = True
            pygame.display.update()

    pygame.quit()
