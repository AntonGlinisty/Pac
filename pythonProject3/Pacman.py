import pygame
from Globals import Globals

class Pacman(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Globals.player_img_left, Globals.pacman_size)
        self.image.set_colorkey(Globals.white)
        self.rect = self.image.get_rect()
        self.rect.x = Globals.pac_spawnkord_x
        self.rect.y = Globals.pac_spawnkord_y

    def Delete(self):
        rect = pygame.Rect((self.rect.x, self.rect.y, Globals.pacman_side, Globals.pacman_side))
        pygame.draw.rect(Globals.screen, Globals.black, rect)

