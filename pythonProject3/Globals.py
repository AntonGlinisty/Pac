import os
import pygame

class Globals():
    width = 1200
    field_height = 600
    height = 680
    fps = 60

    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    fuchsia = (255, 0, 255)

    RIGHT = "to the right"
    LEFT = "to the left"
    UP = "to up"
    DOWN = "to down"
    STOP = "stop"

    speed = 2
    running = True

    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'images')
    player_img_right = pygame.image.load(os.path.join(img_folder, 'pix.right.png'))
    player_img_left = pygame.image.load(os.path.join(img_folder, 'pix.left.png'))
    player_img_up = pygame.image.load(os.path.join(img_folder, 'pix.up.png'))
    player_img_down = pygame.image.load(os.path.join(img_folder, 'pix.down.png'))
    player_img_mouth = pygame.image.load(os.path.join(img_folder, 'pixil-frame-0.png'))
    red_gh_left = pygame.image.load(os.path.join(img_folder, 'red_l.png'))
    heart = pygame.image.load(os.path.join(img_folder, 'toppng.com-8-bit-heart-pixel-heart-673x601.png'))
    heart = pygame.transform.scale(heart, (60, 60))

    pacman_size = player_img_left.get_width() // 7.5, player_img_left.get_height() // 7.5
    pacman_side = pacman_size[0]
    ghosts_size = pacman_size
    ghosts_side = pacman_side
    cell_side = pacman_side
    cell_w_count = int(width / cell_side)
    cell_h_count = int(height / cell_side)

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    surf = pygame.Surface((300, 80))
    surf.fill(black)

    mou_op_freq = 5
    mou_cl_freq = 10

    pac_spawnkord_x = 640
    pac_spawnkord_y = 520
    r_gh_spawnkord_x = 640
    r_gh_spawnkord_y = 120


    bonus1 = 100
    score_disp_width = 50
    score_disp_coords = (10, 620)

    marker1 = True
    sf = pygame.Surface((width, height))
