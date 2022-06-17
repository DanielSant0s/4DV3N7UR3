from simplygame import *
from map_system import *

import anim
import hud

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

def lose_life(life, life_lost):
    life = life - life_lost
    life_lost = 0
    return life, life_lost

def draw_char(display, rect, camera, state):
    backup = rect.copy()
    if state['side'] == LEFT:
        rect.x = rect.x-rect.width
        display.blit(pygame.transform.flip(state['sprite'], True, False), World2Screen(rect, camera), (((state['sprite'].get_width()/state['lim'])*state['prog']),0,(state['sprite'].get_width()/state['lim']), state['sprite'].get_height())) 
    else:
        display.blit(state['sprite'], World2Screen(rect, camera), (((state['sprite'].get_width()/state['lim'])*state['prog']),0,(state['sprite'].get_width()/state['lim']), state['sprite'].get_height()))
    return backup


def test_rect_rect(p_rect, c_rect):
    if p_rect.colliderect(c_rect):
        return True
    return False

def proccess_char_collisions(char):
    if char['collisions']['bottom']:
        if char['state']['sprite'] == char['anim']['jump']['sprite']:
            if char['moves'][0] or char['moves'][1]:	
                anim.change(char['anim'], char['state'], 'run')
            else:
                anim.change(char['anim'], char['state'], 'idle')
        char['y_momentum'] = 0
        char['air_timer'] = 0
    else:
        char['air_timer'] += 1

    if char['collisions']['left']:
        char['blocks'][0] = True
        if char['y_momentum'] >= 0:
            char['moves'][0] = False
    else:
        char['blocks'][0] = False

    if char['collisions']['right']:
        char['blocks'][1] = True
        if char['y_momentum'] >= 0:
            char['moves'][1] = False
    else:
        char['blocks'][1] = False

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

def move_char(char, ms):
    char['movement'] = [0, 0]
    if char['moves'][1]:
        char['movement'][0] += dt_value(ms, 2.0)
    if char['moves'][0]:
        char['movement'][0] -= dt_value(ms, 2.0)
    char['movement'][1] += char['y_momentum']
    char['y_momentum'] += 0.2
    if char['y_momentum'] > 3:
        char['y_momentum'] = 3
        if char['state']['sprite'] != char['anim']['jump']['sprite']:
            anim.change(char['anim'], char['state'], 'jump')


def process_enemy_ai(enemy, player, player_rect, player_state, player_y_momentum, life, ms, g_hud):
    enemy['cooldown'] -= ms

    if enemy['blocks'][0] == True:
        enemy['moves'][0] = False
        enemy['moves'][1] = True
        enemy['state']['side'] = RIGHT
    elif enemy['blocks'][1] == True:
        enemy['moves'][0] = True
        enemy['moves'][1] = False
        enemy['state']['side'] = LEFT

    if enemy['moves'][0] or enemy['moves'][1]:
        if enemy['state']['sprite'] == enemy['anim']['idle']['sprite']:
            anim.change(enemy['anim'], enemy['state'], 'run')

    if test_rect_rect(player_rect, enemy['rect']):
        if enemy['cooldown'] <= 0 and not enemy['atk_lock'] and life > 0:
            anim.change(enemy['anim'], enemy['state'], 'run_attack')
            anim.change(player, player_state, 'hurt')
            hud.update(g_hud, (int(life), 100, 100))
            life = lose_life(life, 15)[0]
            if enemy['moves'][0] == True:
                player_rect.x -= 30
            elif enemy['moves'][1] == True:
                player_rect.x += 30
            player_y_momentum -= 2.5
            enemy['cooldown'] = 2000
            enemy['atk_lock'] = True

    elif enemy['rect'].y == player_rect.y and enemy['cooldown'] <= 0:
        if enemy['rect'].x < player_rect.x:
            enemy['moves'][1] = True
            enemy['moves'][0] = False
            enemy['state']['side'] = RIGHT
        elif enemy['rect'].x > player_rect.x:
            enemy['moves'][1] = False
            enemy['moves'][0] = True
            enemy['state']['side'] = LEFT

    if enemy['anim']['run_attack']['sprite'] == enemy['state']['sprite'] or enemy['anim']['hurt']['sprite'] == enemy['state']['sprite']:
        if (enemy['state']['prog'] == enemy['state']['lim']-1 and enemy['state']['side'] == RIGHT) or (enemy['state']['prog'] == 1 and enemy['state']['side'] == LEFT):
            anim.change(enemy['anim'], enemy['state'], 'run')

    return player_y_momentum, life

def register_enemy(enemies, char_name, posx, posy, speed_list, frames_list):
    enemy = {}
    enemy['anim'] = anim.new(char_name, speed_list, frames_list, True)
    enemy['state'] = {'sprite': enemy['anim']['idle']['sprite'], 'prog': 0, 'lim': enemy['anim']['idle']['frames'], 'speed': enemy['anim']['idle']['speed'], 'side': RIGHT}
    enemy['rect'] = pygame.Rect(posx, posy, enemy['state']['sprite'].get_width()/enemy['state']['lim']/2, enemy['state']['sprite'].get_height())
    enemy['moves'] = [False, True]
    enemy['blocks'] = [False, False]
    enemy['collisions'] = None
    enemy['movement'] = None
    enemy['y_momentum'] = 0
    enemy['air_timer'] = 0
    enemy['time_acc'] = 0
    enemy['sfx_acc'] = 0
    enemy['cooldown'] = 0
    enemy['atk_lock'] = False
    enemy['life'] = 100
    enemies.append(enemy)

def damage_enemy(player_rect, enemy, damage, x=30, y=2.5):
    if test_rect_rect(player_rect, enemy['rect']) and enemy['life'] > 0:
        anim.change(enemy['anim'], enemy['state'], 'hurt')
        enemy['life'] = lose_life(enemy['life'], damage)[0]
        if enemy['moves'][0] == True:
            enemy['rect'].x -= x
        elif enemy['moves'][1] == True:
            enemy['rect'].x += x
        enemy['moves'][0] = False
        enemy['moves'][1] = False
        enemy['y_momentum'] -= y