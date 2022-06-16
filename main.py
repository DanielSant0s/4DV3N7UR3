from char_system import *
from simplygame import *
import game
import ui

clock, screen, display = game.init('4DV3N7UR3', 0, 0)

scan = new_rectEX(display.get_width(), 1, (20,0,100,25))

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
speeds_lst = [8.0, 8.0, 8.0, 1.0, 4.0, 4.0, 4.0, 1.0, 1.0, 1.0, 4.0, 4.0]

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

cyborg_moves = [False, True]
cyborg_blocks = [False, False]
player_moves = [False, False]
player_blocks = [False, False]

player_y_momentum = 0
cyborg_y_momentum = 0
air_timer = 0
cyborg_air_timer = 0

ms = 0
time_acc = 0
time_acc2 = 0
sfx_acc = 0
attack_cooldown = 0
atk_lock = False

game_paused = False

anim_state = {'sprite': player['idle']['sprite'], 'prog': 0, 'lim': player['idle']['frames'], 'speed': player['idle']['speed'], 'side': RIGHT}
cyborg_state = {'sprite': cyborg['idle']['sprite'], 'prog': 0, 'lim': cyborg['idle']['frames'], 'speed': cyborg['idle']['speed'], 'side': RIGHT}

player_rect = pygame.Rect(50, 50, anim_state['sprite'].get_width()/anim_state['lim']/2, anim_state['sprite'].get_height())
cyborg_rect = pygame.Rect(850, 180, cyborg_state['sprite'].get_width()/cyborg_state['lim']/2, cyborg_state['sprite'].get_height())
test_rect = pygame.Rect(100,100,100,50)

dashd = False
jumping = False

life = 100
life_lost = 0

cyborg_life = 100

mouse_pos = pygame.mouse.get_pos()

fullscreen = True

game_hud = hud.init()

hud.update(game_hud, (life, 100, 100))

game_state = MAIN_MENU

dark_overlay = new_rectEX(display.get_width(), display.get_height(), (0,0,0,128))

video_modes = [(640,480), (800,600), (1024,768), (1280,720), (1366, 768), (1280,1024), (1600,900), (1920,1080)]

menu_ptr = {'ptr': 0, 'lim': 4, 'store':None}
options_ptr = [{'ptr': 0, 'lim': 4, 'store':[0,1,0,0]}, {'ptr': 0, 'lim': 7, 'store':None}]

new_mode = (screen.get_width(),screen.get_height())

tile_rects = []

game_running = True

attack = False

dash_sound = pygame.mixer.Sound("Sfx/Jump/Jump__004.wav")
jump_sound = pygame.mixer.Sound("Sfx/Jump/Jump__002.wav")
punch_sound = pygame.mixer.Sound("Sfx/Punch2/Punch2__001.wav")
walk_sound = pygame.mixer.Sound("Sfx/Footstep/Footstep__007.wav")

pygame.mixer.music.load("Sfx/galactic-trek.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

while game_running: # game loop
    if game_state == MAIN_MENU:
        loopBackground(display, bg, dt_value(ms, 2.0), 0, (False, True))
        display = blur(display, 2.8)

        display.blit(dark_overlay, (0,0))
        print_text(font, display, "4DV3N7UR3", display.get_width()/2, -25, (255,255,255), scale=4)

        main_labels = ["Start Game", "Options", "Creator", "Exit"]
        ui.draw_menu(display, font, main_labels, menu_ptr['ptr'], display.get_width()/2, 50.0, (255,255,255), (95,95,185), 2.5)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                game_running = False
            if event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[K_RETURN]:
                    if menu_ptr['ptr'] == 0:
                        pygame.mixer.music.set_volume(0.1)
                        game_state = GAME_RUNNING
                        life = 100
                        anim.change(player, anim_state, 'idle', RIGHT)
                        player_rect = pygame.Rect(50, 50, anim_state['sprite'].get_width()/anim_state['lim']/2, anim_state['sprite'].get_height())
                        global_camera = [-180.0, -100.0]
                        hud.update(game_hud, (life, 100, 100))

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
        print_text(font, display, "Options", display.get_width()/2, -25, (255,255,255), scale=4)
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
        if (player_moves[0] or player_moves[1]) and sfx_acc*anim_state['speed'] > 1800 and air_timer < 10:
            walk_sound.play()
            sfx_acc = 0

        if not game_paused:
            time_acc = anim.update(anim_state, time_acc, life)
            time_acc2 = anim.update(cyborg_state, time_acc2, cyborg_life)

            cyborg_movement, cyborg_y_momentum = move_char(cyborg_moves, cyborg_y_momentum, cyborg, cyborg_state, ms)

            player_movement, player_y_momentum = move_player(player_moves[0], player_moves[1], player_blocks[0], player_blocks[1], player_y_momentum, global_camera, player, anim_state, ms)

            #mouse_pos = pygame.mouse.get_pos()
            #pygame.draw.rect(display, (255, 0, 0), (mouse_pos[0]/(screen.get_width()/display.get_width()), mouse_pos[1]/(screen.get_height()/display.get_height()), 5, 5))

            player_rect, collisions = move(player_rect, player_movement, tile_rects)

            cyborg_rect, e_collisions = move(cyborg_rect, cyborg_movement, tile_rects)
            cyborg_y_momentum, cyborg_air_timer = proccess_char_collisions(e_collisions, cyborg, cyborg_state, cyborg_y_momentum, cyborg_air_timer, cyborg_blocks, cyborg_moves)

            if collisions['bottom']:
                jump_mode = 0
                if anim_state['sprite'] == player['jump']['sprite']:
                    if player_moves[1] or player_moves[0]:
                        anim.change(player, anim_state, 'run')
                    else:
                        anim.change(player, anim_state, 'idle')
                player_y_momentum = 0
                if life_lost > 0:
                    hud.update(game_hud, (int(life), 100, 100))
                    life, life_lost = lose_life(life, life_lost)
                air_timer = 0
                dashd = False
                jumping = False
            else:
                air_timer += 1

            if air_timer > 120:
                    life_lost += 0.3

            if collisions['left']:
                player_blocks[0] = True
                if player_y_momentum >= 0:
                    player_moves[0] = False
                    global_camera[0] -= dt_value(ms, 2.0)
            else:
                player_blocks[0] = False
            if collisions['right']:
                player_blocks[1] = True
                if player_y_momentum >= 0:
                    player_moves[1] = False
                    global_camera[0] += dt_value(ms, 2.0)
            else:
                player_blocks[1] = False

            if anim_state['sprite'] == player['run_attack']['sprite']:
                if (anim_state['side'] == RIGHT and anim_state['lim']-1 == anim_state['prog']) or (anim_state['side'] == LEFT and 0 == anim_state['prog']):
                    if player_moves[0] or player_moves[1]:
                        anim.change(player, anim_state, 'run')
                    else:
                        anim.change(player, anim_state, 'idle')

            if cyborg_life > 0:
                player_y_momentum, attack_cooldown, life, atk_lock = process_enemy_ai([cyborg, cyborg_rect, cyborg_state], player, player_rect, anim_state, player_y_momentum, life, cyborg_moves, cyborg_blocks, attack_cooldown, ms, game_hud, atk_lock)
                atk_lock = False
            elif cyborg_state['sprite'] != cyborg['death']['sprite']:
                anim.change(cyborg, cyborg_state, 'death')


            if life < 0 and not anim_state['sprite'] == player['death']['sprite']:
                anim.change(player, anim_state, 'death')
            if anim_state['sprite'] == player['death']['sprite']:
                if (anim_state['side'] == RIGHT and anim_state['lim']-1 == anim_state['prog']) or (anim_state['side'] == LEFT and 0 == anim_state['prog']):
                    game_state = GAME_OVER

            smooth_camera(global_camera, player_rect, display, player_moves[1], player_moves[0], jumping)

        for event in pygame.event.get(): # event loop
            if event.type == QUIT: # check for window quit
                game_running = False
            if event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if not game_paused:
                    if keys[K_RIGHT]:
                        player_moves[1] = True
                        anim.change(player, anim_state, 'run', RIGHT)
                        if keys[K_LEFT]:
                            player_moves[0] = True
                            anim.change(player, anim_state, 'run', LEFT)
                    if keys[K_LEFT]:
                        player_moves[0] = True
                        anim.change(player, anim_state, 'run', LEFT)
                        if keys[K_RIGHT]:
                            player_moves[0] = True
                            anim.change(player, anim_state, 'run', RIGHT)
                    if keys[K_BACKSPACE]:
                        global_camera = [player_rect.x-100, player_rect.y-100]
                    if keys[K_UP]:
                        if air_timer > 15 and not dashd:
                            pygame.mixer.Sound.play(dash_sound)
                            dashd = True
                            jumping = True
                            anim.change(player, anim_state, 'doublejump')
                            player_y_momentum = -6.5
                        else:
                            pygame.mixer.Sound.play(jump_sound)
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
                        pygame.mixer.Sound.play(punch_sound)
                        if test_rect_rect(player_rect, cyborg_rect) and cyborg_life > 0:
                            anim.change(cyborg, cyborg_state, 'hurt')
                            cyborg_life = lose_life(cyborg_life, 15)[0]
                            cyborg_moves[0] = False
                            cyborg_moves[1] = False
                            if cyborg_moves[0] == True:
                                cyborg_rect.x -= 30
                            elif cyborg_moves[1] == True:
                                cyborg_rect.x += 30
                            cyborg_y_momentum -= 2.5
                        anim.change(player, anim_state, 'run_attack')
                    if keys[K_z]:
                        anim.change(player, anim_state, 'attack2')
                    if keys[K_x]:
                        anim.change(player, anim_state, 'attack3')
                if keys[K_ESCAPE]:
                    game_paused = not game_paused

            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    player_moves[1] = False
                    if not jumping:
                        anim.change(player, anim_state, 'idle', RIGHT)
                    if keys[K_LEFT]:
                        anim.change(player, anim_state, 'run', LEFT)
                if event.key == K_LEFT:
                    player_moves[0] = False
                    if not jumping:
                        anim.change(player, anim_state, 'idle', LEFT)
                    if keys[K_RIGHT]:
                        anim.change(player, anim_state, 'run', RIGHT)


        loopBackground(display, bg, dt_value(ms, 1.5), player_y_momentum, (player_moves[0], player_moves[1]))
        tile_rects = render_map(display, tilelist, TILE_SIZE, game_map, global_camera)
        player_rect = draw_char(display, player_rect, global_camera, anim_state)
        print_text(font, display, f"{cyborg_life}", World2Screen(cyborg_rect, global_camera)[0]+cyborg_rect.width/(4 if cyborg_state['side'] == LEFT else 1.35), World2Screen(cyborg_rect, global_camera)[1], (255,255,255), scale=0.8)

        cyborg_rect = draw_char(display, cyborg_rect, global_camera, cyborg_state)
        hud.render(display, game_hud, 10, 10)
        print_text(font, display, f"Player coordinates: {player_rect.x},{player_rect.y}", display.get_width()/2, 5, (255,255,255))

        if game_paused:
            player_y_momentum = 0
            player_moves[0], player_moves[1] = False, False
            display = blur(display, 3.5)

    elif game_state == GAME_OVER:
        display.fill((0,0,0))
        print_text(font, display, "GAME OVER", display.get_width()/2, -15, (255,255,255), scale=4)
        print_text(font, display, "Press ENTER to return to the main menu", display.get_width()/2, 150, (255,255,255))

        for event in pygame.event.get():
            if event.type == QUIT:
                game_running = False
            if event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if not game_paused:
                    if keys[K_RETURN]:
                        game_state = MAIN_MENU


    for i in range(125):
        display.blit(scan, (0, i*2))
    game.draw(display, screen)
    ms = clock.tick(fps_limit)
    time_acc += ms
    time_acc2 += ms
    sfx_acc += ms
game.deinit()