import pygame
from pygame.locals import *

from simplygame import *
from map_system import *
from consts import *

import anim

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

#Função que recebe a quantidade de vida e a vida perdida, e então desconta a vida perdida do total de vida, zera o contador de vida perdida e retorna o total de vida
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

def proccess_char_collisions(collisions, char, char_state, char_y_momentum, air_timer, block_list, move_list):
    if collisions['bottom']:
        if char_state['sprite'] == char['jump']['sprite']:
            if move_list[0] or move_list[1]:
                anim.change(char, char_state, 'run')
            else:
                anim.change(char, char_state, 'idle')
        char_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    if collisions['left']:
        block_list[0] = True
        if char_y_momentum >= 0:
            move_list[0] = False
    else:
        block_list[0] = False

    if collisions['right']:
        block_list[1] = True
        if char_y_momentum >= 0:
            move_list[1] = False
    else:
        block_list[1] = False

    return char_y_momentum, air_timer

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

def move_char(move_list, y_momentum, char, state, ms):
    char_movement = [0, 0]
    if move_list[1]:
        char_movement[0] += dt_value(ms, 2.0)
    if move_list[0]:
        char_movement[0] -= dt_value(ms, 2.0)
    char_movement[1] += y_momentum
    y_momentum += 0.2
    if y_momentum > 3:
        y_momentum = 3
        if state['sprite'] != char['jump']['sprite']:
            anim.change(char, state, 'jump')
    return char_movement, y_momentum
