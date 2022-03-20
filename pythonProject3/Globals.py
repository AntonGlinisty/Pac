import os
import pygame

class Globals():
    width = 1200
    height = 600
    fps = 60

    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)

    RIGHT = "to the right"
    LEFT = "to the left"
    UP = "to up"
    DOWN = "to down"
    STOP = "stop"

    speed = 2
    running = True

    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'images')
    player_img_right = pygame.image.load(os.path.join(img_folder, 'pixil-frame.right.png'))
    player_img_left = pygame.image.load(os.path.join(img_folder, 'pixil-frame.left.png'))
    player_img_up = pygame.image.load(os.path.join(img_folder, 'pixil-frame.up.png'))
    player_img_down = pygame.image.load(os.path.join(img_folder, 'pixil-frame.down.png'))

    pacman_size = player_img_left.get_width() // 7.5, player_img_left.get_height() // 7.5
    pacman_side = pacman_size[0]
    cell_side = pacman_side
    cell_w_count = int(width / cell_side)
    cell_h_count = int(height / cell_side)

    pygame.init()
    screen = pygame.display.set_mode((width, height))