import pygame
from Globals import Globals
from collections import deque
import random


class Ghosts(pygame.sprite.Sprite):

    def Type(self, type):
        if type == 'blinky':
            return Blinky()
        if type == 'inky':
            return Inky()
        if type == 'clyde':
            return Clyde()

    def Get_next_nodes(self, x, y, GRID):
        check_next_node = lambda x, y: True if 0 <= x < int(Globals.width//Globals.cell_side) \
             and 0 <= y < int(Globals.height//Globals.cell_side) and not GRID.grid[y][x] == 1 else False
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]

    def bfs(self, gridCord, mycords, graph):
        queue = deque([gridCord])
        visited = {gridCord: None}
        while queue:
            cur_node = queue.popleft()
            if cur_node == mycords:
                break
            next_nodes = graph[cur_node]
            for next_node in next_nodes:
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = cur_node
        return queue, visited

    def funkforgame(self, gridCord, mycords, graph, GRID, visited, goal):
        if GRID.grid[gridCord[1]][gridCord[0]] != 1:
            queue, visited = self.bfs(gridCord, mycords, graph)
            goal = mycords
        path_head, path_segment = goal, goal
        buf = []
        while path_segment and path_segment in visited:
            path_segment = visited[path_segment]
            buf.append(path_segment)
        return buf

    def Nextgoal(self, gridCord, listofPacpassed, graph, GRID, visited, goal, nextgoal):
        if self.rect.center[0] % Globals.cell_side == Globals.cell_side // 2:
            marker = True
        else:
            marker = False
        if marker:
            path_segment = self.funkforgame(gridCord, listofPacpassed[len(listofPacpassed) - 1],
                                                                                graph, GRID, visited, goal)[::-1]
            path_segment = path_segment[1:]
            if len(path_segment) > 1:
                nextgoal = path_segment[1]
            elif len(path_segment) == 0:
                cords = GRID.ScreenToGrid((self.rect.x, self.rect.y))
                if GRID.grid[cords[1] + 1][cords[0]] == 0:
                    nextgoal = (cords[0], cords[1] + 1)
                elif GRID.grid[cords[1] - 1][cords[0]] == 0:
                    nextgoal = (cords[0], cords[1] - 1)
                if self.rect.x < Globals.width:
                    if GRID.grid[cords[1]][cords[0] + 1] == 0:
                        nextgoal = (cords[0] + 1, cords[1])
                if self.rect.x > 0:
                    if GRID.grid[cords[1]][cords[0] - 1] == 0:
                        nextgoal = (cords[0] - 1, cords[1])
            else:
                nextgoal = path_segment[0]
        return nextgoal

    def GhostsPotential(self, nextgoal, gh_movement, Grid):
        nextscreen = Grid.GridToScreen(nextgoal)
        if self.rect.center[1] % Globals.cell_side == Globals.cell_side // 2 and self.rect.center[0] % \
                Globals.cell_side == Globals.cell_side // 2:
            if nextgoal[0] > Globals.width // Globals.cell_side or nextgoal[0] < 0:
                return gh_movement
            elif Grid.grid[nextgoal[1]][nextgoal[0]] == 1:
                gh_movement = Globals.STOP
                return gh_movement
        if self.rect.center[1] % Globals.cell_side == Globals.cell_side // 2 :
            if nextscreen[0] > self.rect.x:
                gh_movement = Globals.RIGHT
            elif nextscreen[0] < self.rect.x:
                gh_movement = Globals.LEFT
        if self.rect.center[0] % Globals.cell_side == Globals.cell_side // 2 :
            if nextscreen[1] > self.rect.y:
                gh_movement = Globals.DOWN
            elif nextscreen[1] < self.rect.y:
                gh_movement = Globals.UP
        return gh_movement

    def Catcher(self, pacmancords, ghostcords, live):
        if ((ghostcords[1] - pacmancords[1]) * (ghostcords[1] - pacmancords[1]) + (ghostcords[0] - pacmancords[0]) *
                (ghostcords[0] - pacmancords[0]) <= Globals.cell_side * Globals.cell_side):
            return live - 1, True
        return live, False

    def WayMaking(self, gh_movement):
        if gh_movement == Globals.UP:
            self.rect.y -= Globals.speed
        elif gh_movement == Globals.DOWN:
            self.rect.y += Globals.speed
        elif gh_movement == Globals.LEFT:
            self.rect.x -= Globals.speed
        elif gh_movement == Globals.RIGHT:
            self.rect.x += Globals.speed

    def RandomMode(self, GRID, nextgoal, gridCord, graph, visited, goal, cords):
        running = True
        cord1 = cords[0]
        cord2 = cords[1]
        while running:
            if GRID.ScreenToGrid((self.rect.x, self.rect.y)) == cords or cords == (0, 0):
                cord1 = random.randint(0, Globals.rand_x_max)
                cord2 = random.randint(1, Globals.rand_y_max)
                if GRID.grid[cord2][cord1] == 0:
                    if cord1 == Globals.up_hole_x and cord2 == Globals.up_hole_y or \
                            Globals.left_hole_x_min <= cord1 <= Globals.left_hole_x_max and \
                            Globals.left_hole_y_min <= cord2 <= Globals.left_hole_y_max or \
                            Globals.right_hole_x_min <= cord1 <= Globals.right_hole_x_max and \
                            Globals.right_hole_y_min <= cord2 <= Globals.right_hole_y_max or \
                            cord1 == Globals.down_hole_x and cord2 == Globals.down_hole_y:
                        continue
                if GRID.grid[cord2][cord1] == 1:
                    continue
            running = False
            path_segment = self.funkforgame(gridCord, (cord1, cord2), graph, GRID, visited, goal)[::-1]
            path_segment = path_segment[1:]
            cords = (cord1, cord2)
            if len(path_segment) > 1:
                nextgoal = path_segment[1]
            else:
                nextgoal = cords
        return nextgoal, cords

    def Delete(self):
        rect = pygame.Rect((self.rect.x, self.rect.y, Globals.pacman_side, Globals.pacman_side))
        pygame.draw.rect(Globals.screen, Globals.black, rect)

    def Alg(self, GRID, cords):
        graph = {}
        for y, row in enumerate(GRID.grid):
            for x, col in enumerate(row):
                if col != 1:
                    graph[(x, y)] = graph.get((x, y), []) + Ghosts.Get_next_nodes(self, x, y, GRID)
        goal = cords
        queue = deque([cords])
        visited = {cords: None}
        return graph, goal, queue, visited

    def InkyGoal(self, pacmotion, pacman, gridCord, graph, GRID, visited, goal, nextgoal):
        if self.rect.center[0] % Globals.cell_side == Globals.cell_side // 2:
            marker = True
        else:
            marker = False
        if marker:
            paccords = GRID.ScreenToGrid((pacman.rect.center))
            selfcords = GRID.ScreenToGrid((self.rect.center))
            if pacmotion == Globals.LEFT:
                path_segment = self.Leftgoal(GRID, paccords, selfcords, graph, goal, visited, gridCord)
            elif pacmotion == Globals.RIGHT:
                path_segment = self.Rightgoal(GRID, paccords, selfcords, graph, goal, visited, gridCord)
            elif pacmotion == Globals.UP:
                path_segment = self.Upgoal(GRID, paccords, selfcords, graph, goal, visited, gridCord)
            elif pacmotion == Globals.DOWN:
                path_segment = self.Downgoal(GRID, paccords, selfcords, graph, goal, visited, gridCord)
            else:
                path_segment = self.funkforgame(gridCord, paccords, graph, GRID, visited, goal)[::-1]
            nextgoal = self.GoalSearcher(path_segment, GRID, nextgoal)
        return nextgoal

    def Leftgoal(self, GRID, paccords, selfcords, graph, goal, visited, gridCord):
        if paccords[0] >= 2 and GRID.grid[paccords[1]][paccords[0] - 1] == \
                GRID.grid[paccords[1]][paccords[0] - 2] != 1 and (paccords[0] - 2, paccords[1]) != selfcords \
                and (paccords[0] - 1, paccords[1]) != selfcords and \
                (paccords[0] - Globals.inky_pred3, paccords[1]) != selfcords:
            path_segment = self.funkforgame(gridCord, (paccords[0] - 2, paccords[1]),
                                            graph, GRID, visited, goal)[::-1]
            path_segment.append((paccords[0] - 2, paccords[1]))
        elif paccords[0] >= 2 and GRID.grid[paccords[1]][paccords[0] - 1] != 1 and \
                GRID.grid[paccords[1]][paccords[0] - 2] == 1 and (paccords[0] - 1, paccords[1]) != selfcords \
                and (paccords[0] - 2, paccords[1]) != selfcords:
            path_segment = self.funkforgame(gridCord, (paccords[0] - 1, paccords[1]),
                                            graph, GRID, visited, goal)[::-1]
            path_segment.append((paccords[0] - 1, paccords[1]))
        else:
            path_segment = self.funkforgame(gridCord, paccords, graph, GRID, visited, goal)[::-1]
            path_segment.append(paccords)
        return path_segment

    def Rightgoal(self, GRID, paccords, selfcords, graph, goal, visited, gridCord):
        if paccords[0] <= Globals.right_x_max and GRID.grid[paccords[1]][paccords[0] + 1] == \
                GRID.grid[paccords[1]][paccords[0] + 2] != 1 and (paccords[0] + 2, paccords[1]) != selfcords \
                and (paccords[0] + 1, paccords[1]) != selfcords and \
                (paccords[0] + Globals.inky_pred3, paccords[1]) != selfcords:
            path_segment = self.funkforgame(gridCord, (paccords[0] + 2, paccords[1]),
                                            graph, GRID, visited, goal)[::-1]
            path_segment.append((paccords[0] + 2, paccords[1]))
        elif paccords[0] <= Globals.right_x_max and GRID.grid[paccords[1]][paccords[0] + 1] != 1 and \
                GRID.grid[paccords[1]][paccords[0] + 2] == 1 and (paccords[0] + 1, paccords[1]) != selfcords \
                and (paccords[0] + 2, paccords[1]) != selfcords:
            path_segment = self.funkforgame(gridCord, (paccords[0] + 1, paccords[1]),
                                            graph, GRID, visited, goal)[::-1]
            path_segment.append((paccords[0] + 1, paccords[1]))
        else:
            path_segment = self.funkforgame(gridCord, paccords, graph, GRID, visited, goal)[::-1]
            path_segment.append(paccords)
        return path_segment

    def Upgoal(self, GRID, paccords, selfcords, graph, goal, visited, gridCord):
        if paccords[1] >= 2 and GRID.grid[paccords[1] - 1][paccords[0]] == \
                GRID.grid[paccords[1] - 2][paccords[0]] != 1 and (paccords[0], paccords[1] - 2) != selfcords \
                and (paccords[0], paccords[1] - 1) != selfcords and \
                (paccords[0], paccords[1] - Globals.inky_pred3) != selfcords:
            path_segment = self.funkforgame(gridCord, (paccords[0], paccords[1] - 2),
                                            graph, GRID, visited, goal)[::-1]
            path_segment.append((paccords[0], paccords[1] - 2))
        elif paccords[1] >= 2 and GRID.grid[paccords[1] - 1][paccords[0]] != 1 and \
                GRID.grid[paccords[1] - 2][paccords[0]] == 1 and (paccords[0], paccords[1] - 1) != selfcords \
                and (paccords[0], paccords[1] - 2) != selfcords:
            path_segment = self.funkforgame(gridCord, (paccords[0], paccords[1] - 1),
                                            graph, GRID, visited, goal)[::-1]
            path_segment.append((paccords[0], paccords[1] - 1))
        else:
            path_segment = self.funkforgame(gridCord, paccords, graph, GRID, visited, goal)[::-1]
            path_segment.append(paccords)
        return path_segment

    def Downgoal(self, GRID, paccords, selfcords, graph, goal, visited, gridCord):
        if paccords[1] <= Globals.down_ink_max and GRID.grid[paccords[1] + 1][paccords[0]] == \
                GRID.grid[paccords[1] + 2][paccords[0]] != 1 and (paccords[0], paccords[1] + 2) != selfcords \
                and (paccords[0], paccords[1] + 1) != selfcords and \
                (paccords[0], paccords[1] + Globals.inky_pred3) != selfcords:
            path_segment = self.funkforgame(gridCord, (paccords[0], paccords[1] + 2),
                                            graph, GRID, visited, goal)[::-1]
            path_segment.append((paccords[0], paccords[1] + 2))
        elif paccords[1] <= Globals.down_ink_max and GRID.grid[paccords[1] + 1][paccords[0]] != 1 and \
                GRID.grid[paccords[1] + 2][paccords[0]] == 1 and (paccords[0], paccords[1] + 1) != selfcords \
                and (paccords[0], paccords[1] + 2) != selfcords:
            path_segment = self.funkforgame(gridCord, (paccords[0], paccords[1] + 1),
                                            graph, GRID, visited, goal)[::-1]
            path_segment.append((paccords[0], paccords[1] + 1))
        else:
            path_segment = self.funkforgame(gridCord, paccords, graph, GRID, visited, goal)[::-1]
            path_segment.append(paccords)
        return path_segment

    def StarterGoal(self, GRID, gridCord, graph, visited, goal, marker, clozer, nextgoal):
        GRID.grid[Globals.gh_start_y][Globals.gh_start_x] = 0
        GRID.DrawCell((Globals.gh_start_x, Globals.gh_start_y), GRID.grid[Globals.gh_start_x][Globals.gh_start_y])
        if nextgoal != (Globals.gh_start_x, Globals.gh_start_y - 1):
            path_segment = self.funkforgame(gridCord, (Globals.gh_start_x, Globals.gh_start_y + 1), graph, GRID,
                                            visited, goal)[::-1]
            path_segment = path_segment[1:]
            path_segment.append((Globals.gh_start_x, Globals.gh_start_y + 1))
            if len(path_segment) == 1:
                nextgoal = path_segment[0]
            else:
                nextgoal = path_segment[1]
            if GRID.ScreenToGrid((self.rect.center)) == (Globals.gh_start_x, Globals.gh_start_y + 1) and \
                    self.rect.x % Globals.cell_side == 0 and self.rect.y % Globals.cell_side == 0:
                nextgoal = (Globals.gh_start_x, Globals.gh_start_y - 1)
        if GRID.ScreenToGrid((self.rect.center)) == (Globals.gh_start_x, Globals.gh_start_y - 1) and \
                self.rect.x % Globals.cell_side == 0 and self.rect.y % Globals.cell_side == 0:
            marker = False
            clozer = False
            GRID.grid[Globals.gh_start_y][Globals.gh_start_x] = 1
            GRID.DrawCell((Globals.gh_start_x, Globals.gh_start_y), GRID.grid[Globals.gh_start_x][Globals.gh_start_y])
        return marker, nextgoal, clozer

    def GoalSearcher(self, path_segment, GRID, nextgoal):
        path_segment = path_segment[1:]
        if len(path_segment) > 1:
            nextgoal = path_segment[1]
        elif len(path_segment) == 0:
            cords = GRID.ScreenToGrid((self.rect.x, self.rect.y))
            if GRID.grid[cords[1] + 1][cords[0]] == 0:
                nextgoal = (cords[0], cords[1] + 1)
            elif GRID.grid[cords[1] - 1][cords[0]] == 0:
                nextgoal = (cords[0], cords[1] - 1)
            if self.rect.x < Globals.width:
                if GRID.grid[cords[1]][cords[0] + 1] == 0:
                    nextgoal = (cords[0] + 1, cords[1])
            if self.rect.x > 0:
                if GRID.grid[cords[1]][cords[0] - 1] == 0:
                    nextgoal = (cords[0] - 1, cords[1])
        else:
            nextgoal = path_segment[0]
        return nextgoal


class Blinky(Ghosts):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Globals.red_gh_left, Globals.ghosts_size)
        self.rect = self.image.get_rect()
        self.rect.x = Globals.r_gh_spawnkord_x
        self.rect.y = Globals.r_gh_spawnkord_y

class Inky(Ghosts):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Globals.inky, Globals.ghosts_size)
        self.rect = self.image.get_rect()
        self.rect.x = Globals.bl_gh_spawnkord_x
        self.rect.y = Globals.bl_gh_spawnkord_y

class Clyde(Ghosts):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Globals.clyde, Globals.ghosts_size)
        self.rect = self.image.get_rect()
        self.rect.x = Globals.or_gh_spawnkord_x
        self.rect.y = Globals.or_gh_spawnkord_y