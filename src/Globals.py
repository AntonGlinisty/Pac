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
    clyde = pygame.image.load(os.path.join(img_folder, 'clyde.png'))
    inky = pygame.image.load(os.path.join(img_folder, 'inky.png'))
    heart = pygame.image.load(os.path.join(img_folder, 'heart.png'))
    dead = pygame.image.load(os.path.join(img_folder, 'wasted1.jpg'))
    dead = pygame.transform.scale(dead, (width, height))
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
    surf = pygame.Surface((width, 80))
    surf.fill(black)

    mou_op_freq = 5
    mou_cl_freq = 10

    pac_spawnkord_x = 640
    pac_spawnkord_y = 520
    r_gh_spawnkord_x = 640
    r_gh_spawnkord_y = 240
    or_gh_spawnkord_x = 600
    or_gh_spawnkord_y = 240
    bl_gh_spawnkord_x = 680
    bl_gh_spawnkord_y = 240

    bonus1 = 100
    score_disp_width = 50
    score_disp_coords = (10, 620)
    mode_disp_coords = (430, 620)
    cleaning_coords = (0, 600)

    marker1 = True
    sf = pygame.Surface((width, height))
    foodcounter = 157

    blinky_out = 50
    clyde_out = 250
    inky_out = 500
    pas_mode = 500
    agr_mode = 1500
    cleaner_count = 20

    wastedtime = 2
    gh_start_x = 16
    gh_start_y = 4
    rand_x_max = 28
    rand_y_max = 13
    up_hole_x = 11
    up_hole_y = 11
    down_hole_x = 3
    down_hole_y = 3
    left_hole_x_min = 9
    left_hole_x_max = 11
    left_hole_y_min = 6
    left_hole_y_max = 7
    right_hole_x_min = 15
    right_hole_x_max = 17
    right_hole_y_min = 5
    right_hole_y_max = 6
    down_ink_max = 12
    right_x_max = 27

    food_size = 5
    lives_stat = 3
    food_count_stat = 157

    yell_food_id = 3
    black_food_id = 4
    heart_x_spawn = 900
    heart_ind = 100
    heart_y_spawn = 610
    round_x_max = 1140
    pac_turn_nin = 90
    pac_turn_ei = 180
    pac_turn_sev = 270

    food_ind = 4
    inky_pred3 = 3
    Background = 'images/muz2.mp3'