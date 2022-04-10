import pygame
from Globals import Globals
from collections import deque


class Ghosts(pygame.sprite.Sprite):
    def __init__(self, type):
        pygame.sprite.Sprite.__init__(self)
        self.GhostsType(type)

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

    def funkforgame(self, gridCord, mycords, graph, GRID, visited, goal, gridCord_RU):
        if gridCord_RU[0] + 1 < int(Globals.width // Globals.cell_side):
            if GRID.grid[gridCord[1]][gridCord[0]] == 0:
                queue, visited = self.bfs(gridCord, mycords, graph)
                goal = mycords
        path_head, path_segment = goal, goal
        buf = []
        while path_segment and path_segment in visited:
            path_segment = visited[path_segment]
            buf.append(path_segment)
        return buf

    def WayMaking(self, path_segment, gridCord):
        self.rect.x += Globals.speed

    def Delete(self):
        rect = pygame.Rect((self.rect.x, self.rect.y, Globals.pacman_side, Globals.pacman_side))
        pygame.draw.rect(Globals.screen, Globals.black, rect)



























    def GhostsType(self, type):
        if type == 'blinky':
            self.Blinky()
        # if type == 'pinky':
        #     return Pinky
        # if type == 'inky':
        #     return Inky
        # if type == 'clyde':
        #     return Clyde



    def Blinky(self):
        self.image = pygame.transform.scale(Globals.red_gh_left, Globals.ghosts_size)
        self.rect = self.image.get_rect()
        self.rect.x = Globals.r_gh_spawnkord_x
        self.rect.y = Globals.r_gh_spawnkord_y






# class Inky():
#
# class Pinky():
#
# class Clyde():

