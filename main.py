import pygame
from pygame.locals import *

from map_system import *
from char_system import *
from simplygame import *
from consts import *
import game
import anim
import hud
import ui

clock, screen, display = game.init('4DV3N7UR3', 0, 0)

scan = new_rectEX(display.get_width(), 1, (0,0,0,0))

global_camera = [-180.0, -100.0]

fps_limit = 60
menu_lim = 60

bg_dict = load_texture_dictionary('Map/Background/', 1.5)
bg = []
for i in range(len(bg_dict)):
    bg.append({'data':bg_dict[i], 'posx':0, 'posy':display.get_height()-bg_dict[i].get_height(), 'posx2':-(bg_dict[i].get_width()-0.5)})

tilelist = load_texture_dictionary('Map/Tiles/')
TILE_SIZE = 32

frames_lst = [6, 8, 8, 6, 6, 6, 2, 4, 4, 6, 6, 6]
speeds_lst = [8.0, 8.0, 8.0, 1.0, 1.0, 4.0, 1.0, 1.0, 1.0, 1.0, 4.0, 2.5]

player = anim.new('Punk', speeds_lst, frames_lst)
biker = anim.new('Biker', speeds_lst, frames_lst)
cyborg = anim.new('Cyborg', speeds_lst, frames_lst)

font = pygame.font.Font('Font/PixeloidMono-1G8ae.ttf', 9)

game_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0,  0,  0,  0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0,  0,  0,  0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0,  0,  0,  0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 77, 77,77, 77, 77],
            [0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 18,18,0, 0, 0, 0, 0, 0, 18,18,5, 0,  0,  0,  0,  0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0,  0,  0,  0,  0],
            [5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0,  0,  0,  0,  0],
            [2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0,  0,  0,  0,  0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0,  0,  0,  0,  0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0,  0,  0,  0,  0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0,  0,  0,  0,  0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0,  0,  0,  0,  0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0,  0,  0,  0,  0]]

moving_right = False
moving_left = False
blocked_right = False
blocked_left = False

player_y_momentum = 0
air_timer = 0

ms = 0
time_acc = 0

anim_state = {'sprite': player['idle']['sprite'], 'prog': 0, 'lim': player['idle']['frames'], 'speed': player['idle']['speed'], 'side': RIGHT}

player_rect = pygame.Rect(50, 50, anim_state['sprite'].get_width()/anim_state['lim']/2, anim_state['sprite'].get_height())
test_rect = pygame.Rect(100,100,100,50)

dashd = False
jumping = False

life = 100
life_lost = 0

mouse_pos = pygame.mouse.get_pos()

fullscreen = True

game_hud = hud.init()

hud.update(game_hud, (life, 20, 20))

game_state = MAIN_MENU

dark_overlay = new_rectEX(display.get_width(), display.get_height(), (0,0,0,128))

video_modes = [(640,480), (800,600), (1024,768), (1280,720), (1366, 768), (1280,1024), (1600,900), (1920,1080)]

menu_ptr = {'ptr': 0, 'lim': 4, 'store':None}
options_ptr = [{'ptr': 0, 'lim': 4, 'store':[0,1,0,0]}, {'ptr': 0, 'lim': 7, 'store':None}]

new_mode = (screen.get_width(),screen.get_height())

game_running= True

def move_player(ml, mr, bl, br, y_momentum, camera, player, state, ms):
    player_movement = [0, 0]
    if mr:
        player_movement[0] += dt_value(ms, 2.0)
        if not br:
            camera[0] += dt_value(ms, 2.0)
    if ml:
        player_movement[0] -= dt_value(ms, 2.0)
        if not bl:
            camera[0] -= dt_value(ms, 2.0)
    player_movement[1] += y_momentum
    y_momentum += 0.2
    if y_momentum < 0:
        camera[1] += y_momentum
    if y_momentum > 3:
        y_momentum = 3
        camera[1] += y_momentum
        if state['sprite'] != player['jump']['sprite']:
            anim.change(player, state, 'jump')
    return player_movement, y_momentum

while game_running: # game loop
    if game_state == MAIN_MENU:
        loopBackground(display, bg, dt_value(ms, 2.0), 0, (False, True))
        display = blur(display, 2.8)

        display.blit(dark_overlay, (0,0))
        print_text(font, display, "4DV3N7UR3", display.get_width()/2, -25, (255,255,255), center=True, scale=4)

        main_labels = ["Start Game", "Options", "Creator", "Exit"]
        ui.draw_menu(display, font, main_labels, menu_ptr['ptr'], display.get_width()/2, 50.0, (255,255,255), (95,95,185), 2.5)
        
        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                game_running = False
            if event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[K_RETURN]:
                    if menu_ptr['ptr'] == 0:
                        game_state = GAME_RUNNING
                    elif menu_ptr['ptr'] == 1:
                        game_state = OPTIONS_MENU
                        for i in range(len(video_modes)):
                            if new_mode in video_modes:
                                if video_modes[i] == new_mode:
                                    options_ptr[1]['ptr'] = i
                                    break
                            else:
                                video_modes.append(new_mode)
                                options_ptr[1]['ptr'] = 8
                                break
                        options_ptr[0]['store'][0] = options_ptr[1]['ptr']
                    elif menu_ptr['ptr'] == 3:
                        game_running = False
                ui.process_menu_commands({'dec':keys[K_UP], 'inc':keys[K_DOWN]}, menu_ptr)

    elif game_state == OPTIONS_MENU:
        loopBackground(display, bg, dt_value(ms, 2.0), 0, (False, True))
        display = blur(display, 2.8)

        display.blit(dark_overlay, (0,0))
        print_text(font, display, "Options", display.get_width()/2, -25, (255,255,255), center=True, scale=4)
        opt_labels = [f"Resolution: {new_mode[0]}x{new_mode[1]}", f"Fullscreen: {fullscreen}", f"FPS Limit: {menu_lim}", "Back"]
        ui.draw_menu(display, font, opt_labels, options_ptr[0]['ptr'], display.get_width()/2, 50.0, (255,255,255), (95,95,185), 2.5)

        if options_ptr[0]['ptr'] == 0:
            options_ptr[1]['lim'] = len(video_modes)
            new_mode = video_modes[options_ptr[1]['ptr']]
        elif options_ptr[0]['ptr'] == 1:
            options_ptr[1]['lim'] = 2
            fullscreen = bool(options_ptr[1]['ptr'])
        elif options_ptr[0]['ptr'] == 2:
            options_ptr[1]['lim'] = 1
            if options_ptr[1]['ptr'] == 0:
                menu_lim = 60
        elif options_ptr[0]['ptr'] == 3:
            options_ptr[1]['lim'] = 0

        if options_ptr[1]['ptr'] > options_ptr[1]['lim']:
            options_ptr[1]['ptr'] = 0
        elif options_ptr[1]['ptr'] < 0:
            options_ptr[1]['ptr'] = options_ptr[1]['lim']

        for event in pygame.event.get():
            if event.type == QUIT:
                game_running = False
            if event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[K_RETURN]:
                    if options_ptr[0]['ptr'] == 0:
                        screen = pygame.display.set_mode(new_mode, pygame.FULLSCREEN if fullscreen else 0)
                        display = pygame.Surface((250*(new_mode[0]/new_mode[1]), 250))
                    if options_ptr[0]['ptr'] == 1:
                        if not fullscreen:
                            screen = pygame.display.set_mode(new_mode)
                            display = pygame.Surface((250*(new_mode[0]/new_mode[1]), 250))
                        else:
                            screen = pygame.display.set_mode(new_mode, pygame.FULLSCREEN)
                            display = pygame.Surface((250*(screen.get_width()/screen.get_height()), 250))
                    if options_ptr[0]['ptr'] == 2:
                        fps_limit = menu_lim
                    if options_ptr[0]['ptr'] == 3:
                        game_state = MAIN_MENU
                ui.process_menu_commands([{'dec':keys[K_UP], 'inc':keys[K_DOWN]}, {'dec':keys[K_LEFT], 'inc':keys[K_RIGHT]}], options_ptr)
    elif game_state == GAME_RUNNING:
        loopBackground(display, bg, dt_value(ms, 1.5), player_y_momentum, (moving_left, moving_right))
        time_acc = anim.update(anim_state, time_acc)
        tile_rects = render_map(display, tilelist, TILE_SIZE, game_map, global_camera)

        hud.render(display, game_hud, 10, 10)

        player_movement, player_y_momentum = move_player(moving_left, moving_right, blocked_left, blocked_right, player_y_momentum, global_camera, player, anim_state, ms)

        #mouse_pos = pygame.mouse.get_pos()
        #pygame.draw.rect(display, (255, 0, 0), (mouse_pos[0]/(screen.get_width()/display.get_width()), mouse_pos[1]/(screen.get_height()/display.get_height()), 5, 5))

        player_rect, collisions = move(player_rect, player_movement, tile_rects)

        if collisions['bottom']:
            jump_mode = 0
            if anim_state['sprite'] == player['jump']['sprite']:
                if moving_right or moving_left:
                    anim.change(player, anim_state, 'run')
                else:
                    anim.change(player, anim_state, 'idle')
            player_y_momentum = 0
            if life_lost > 0:
                hud.update(game_hud, (life, 50, 50))
                life, life_lost = lose_life(life, life_lost)
            air_timer = 0
            dashd = False
            jumping = False
        else:
            air_timer += 1

        if air_timer > 120:
                life_lost += 0.3

        if collisions['left']:
            blocked_left = True
            if player_y_momentum >= 0:
                moving_left = False
                global_camera[0] -= dt_value(ms, 2.0)
        else:
            blocked_left = False
        if collisions['right']:
            blocked_right = True
            if player_y_momentum >= 0:
                moving_right = False
                global_camera[0] += dt_value(ms, 2.0)
        else:
            blocked_right = False

        player_rect = draw_char(display, player_rect, global_camera, anim_state)

        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                game_running = False
            if event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[K_RIGHT]:
                    moving_right = True
                    anim.change(player, anim_state, 'run', RIGHT)
                    if keys[K_LEFT]:
                        moving_left = True
                        anim.change(player, anim_state, 'run', LEFT)
                if keys[K_LEFT]:
                    moving_left = True
                    anim.change(player, anim_state, 'run', LEFT)
                    if keys[K_RIGHT]:
                        moving_left = True
                        anim.change(player, anim_state, 'run', RIGHT)
                if keys[K_BACKSPACE]:
                    global_camera = [player_rect.x-100, player_rect.y-100]
                if keys[K_UP]:
                    if air_timer > 15 and not dashd:
                        dashd = True
                        jumping = True
                        anim.change(player, anim_state, 'doublejump')
                        player_y_momentum = -6.5
                    else:
                        jumping = True
                        anim.change(player, anim_state, 'jump')
                        if air_timer < 6:
                            player_y_momentum = -6
                if keys[K_LALT] and keys[K_RETURN]:
                    if fullscreen:
                        screen = pygame.display.set_mode((640,480),0,32)
                        fullscreen = False
                        display = pygame.Surface((250*(640/480), 250))

                    else:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        fullscreen = True
                        display = pygame.Surface((250*(screen.get_width()/screen.get_height()), 250))
                if keys[K_LCTRL]:
                    anim.change(player, anim_state, 'attack1')
                if keys[K_z]:
                    anim.change(player, anim_state, 'attack2')
                if keys[K_x]:
                    anim.change(player, anim_state, 'attack3')

            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False
                    if not jumping:
                        anim.change(player, anim_state, 'idle', RIGHT)
                    if keys[K_LEFT]:
                        anim.change(player, anim_state, 'run', LEFT)
                if event.key == K_LEFT:
                    moving_left = False
                    if not jumping:
                        anim.change(player, anim_state, 'idle', LEFT)
                    if keys[K_RIGHT]:
                        anim.change(player, anim_state, 'run', RIGHT)
                if event.key == K_LCTRL or event.key == K_x or event.key == K_z:
                    anim.change(player, anim_state, 'idle')

        smooth_camera(global_camera, player_rect, display, moving_right, moving_left, jumping)

    for i in range(250):
        display.blit(scan, (0, i*2))
    game.draw(display, screen)
    ms = clock.tick(fps_limit)
    time_acc += ms

game.deinit()