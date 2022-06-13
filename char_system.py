import pygame
from pygame.locals import *
import sys
import os
import io

from simplygame import *
from map_system import *
from consts import *

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
    return int(life), life_lost

def draw_char(display, rect, camera, state):
    backup = rect.copy()
    if state['side'] == LEFT:
        rect.x = rect.x-rect.width
        display.blit(pygame.transform.flip(state['sprite'], True, False), World2Screen(rect, camera), (((state['sprite'].get_width()/state['lim'])*state['prog']),0,(state['sprite'].get_width()/state['lim']), state['sprite'].get_height())) 
    else:
        display.blit(state['sprite'], World2Screen(rect, camera), (((state['sprite'].get_width()/state['lim'])*state['prog']),0,(state['sprite'].get_width()/state['lim']), state['sprite'].get_height()))
    return backup

    
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