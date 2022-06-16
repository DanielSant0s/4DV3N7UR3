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
speeds_lst = [8.0, 8.0, 8.0, 1.0, 4.0, 4.0, 4.0, 1.0, 1.0, 1.0, 4.0, 8.0]

player = anim.new('Punk', speeds_lst, frames_lst)
anim_state = {'sprite': player['idle']['sprite'], 'prog': 0, 'lim': player['idle']['frames'], 'speed': player['idle']['speed'], 'side': RIGHT}
player_rect = pygame.Rect(50, 50, anim_state['sprite'].get_width()/anim_state['lim']/2, anim_state['sprite'].get_height())
player_moves = [False, False]
player_blocks = [False, False]
player_y_momentum = 0
air_timer = 0
player_timers = [0, 0, 0, 0, 0]
dashd = False
jumping = False
old_life = 0
life = 100
life_lost = 0

font = pygame.font.Font('Font/PixeloidMono-1G8ae.ttf', 9)

enemies = []
register_enemy(enemies, 'Cyborg', 800, 180, speeds_lst, frames_lst)
register_enemy(enemies, 'Biker', 900, 180, speeds_lst, frames_lst)

ms = 0
sfx_acc = 0
game_paused = False

mouse_pos = pygame.mouse.get_pos()

fullscreen = True
game_hud = hud.init()
hud.update(game_hud, (life, 100, 100))
game_state = MAIN_MENU

dark_overlay = new_rectEX(display.get_width(), display.get_height(), (0,0,0,128))

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

while game_running:
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
                        for enemy in enemies:
                            enemy['life'] = 100

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

            for enemy in enemies:
                enemy['time_acc'] = anim.update(enemy['state'], enemy['time_acc'], enemy['life'])
                move_char(enemy, ms)
                enemy['rect'], enemy['collisions'] = move(enemy['rect'], enemy['movement'], tile_rects)
                proccess_char_collisions(enemy)

            player_timers[0] = anim.update(anim_state, player_timers[0], life)
            player_movement, player_y_momentum = move_player(player_moves[0], player_moves[1], player_blocks[0], player_blocks[1], player_y_momentum, global_camera, player, anim_state, ms)
            player_rect, collisions = move(player_rect, player_movement, tile_rects)

            #mouse_pos = pygame.mouse.get_pos()
            #pygame.draw.rect(display, (255, 0, 0), (mouse_pos[0]/(screen.get_width()/display.get_width()), mouse_pos[1]/(screen.get_height()/display.get_height()), 5, 5))

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

            if anim_state['sprite'] == player['run_attack']['sprite'] or anim_state['sprite'] == player['attack1']['sprite'] or anim_state['sprite'] == player['attack2']['sprite'] or anim_state['sprite'] == player['attack3']['sprite']:
                if (anim_state['side'] == RIGHT and anim_state['lim']-1 == anim_state['prog']) or (anim_state['side'] == LEFT and 1 == anim_state['prog']):
                    if player_moves[0] or player_moves[1]:
                        anim.change(player, anim_state, 'run')
                    else:
                        anim.change(player, anim_state, 'idle')

            for enemy in enemies:
                if enemy['life'] > 0:
                    player_y_momentum, life = process_enemy_ai(enemy, player, player_rect, anim_state, player_y_momentum, life, ms, game_hud)
                    enemy['atk_lock'] = False
                elif enemy['state']['sprite'] != enemy['anim']['death']['sprite']:
                    anim.change(enemy['anim'], enemy['state'], 'death')


            if life < 0 and not anim_state['sprite'] == player['death']['sprite']:
                anim.change(player, anim_state, 'death')
                player_moves[0] = False
                player_moves[1] = False
            if anim_state['sprite'] == player['death']['sprite']:
                if (anim_state['side'] == RIGHT and anim_state['lim']-1 == anim_state['prog']) or (anim_state['side'] == LEFT and 0 == anim_state['prog']):
                    game_state = GAME_OVER

            smooth_camera(global_camera, player_rect, display, player_moves[1], player_moves[0], jumping)

        for event in pygame.event.get():
            if event.type == QUIT:
                game_running = False
            if event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if not game_paused and life > 0:
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
                        if air_timer > 15 and not dashd and player_timers[4] > 16384:
                            pygame.mixer.Sound.play(dash_sound)
                            dashd = True
                            jumping = True
                            anim.change(player, anim_state, 'doublejump')
                            player_y_momentum = -6.5
                            player_timers[4] = 0
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
                        for enemy in enemies:
                            damage_enemy(player_rect, enemy, 15)
                        pygame.mixer.Sound.play(punch_sound)

                        if player_moves[0] or player_moves[1]:
                            anim.change(player, anim_state, 'run_attack')
                        else:
                            anim.change(player, anim_state, 'attack1')

                    if keys[K_z]:
                        pygame.mixer.Sound.play(punch_sound)
                        anim.change(player, anim_state, 'attack2')

                    if keys[K_x]:
                        if not player_moves[0] and not player_moves[1] and player_timers[3] > 16384:
                            for enemy in enemies:
                                damage_enemy(player_rect, enemy, 50)
                            pygame.mixer.Sound.play(punch_sound)
                            anim.change(player, anim_state, 'attack3')
                            player_timers[3] = 0

                if keys[K_ESCAPE]:
                    game_paused = not game_paused

            if event.type == KEYUP and not game_paused and life > 0:
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

        for enemy in enemies:
            if enemy['life'] > 0:
                print_text(font, display, f"{enemy['life']}", World2Screen(enemy['rect'], global_camera)[0]+enemy['rect'].width/(4 if enemy['state']['side'] == LEFT else 1.35), World2Screen(enemy['rect'], global_camera)[1], (255,255,255), scale=0.8)
            enemy['rect'] = draw_char(display, enemy['rect'], global_camera, enemy['state'])

        hud.render(display, game_hud, 10, 10)
        print_text(font, display, f"Player coordinates: {player_rect.x},{player_rect.y}", display.get_width()/2, 5, (255,255,255))

        if game_paused:
            player_y_momentum = 0
            player_moves[0], player_moves[1] = False, False
            display = blur(display, 3.5)

        player_timers[0] += ms

        if player_timers[4] < 16384:
            player_timers[4] += ms

        if player_timers[3] < 16384:
            if life-old_life == 0:
                player_timers[3] += ms*0.3
            else:
                player_timers[3] = 0

        hud.update(game_hud, (life, player_timers[4]/163.84, player_timers[3]/163.84))

        for enemy in enemies:
            enemy['time_acc'] += ms

        sfx_acc += ms

        old_life = life

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

game.deinit()