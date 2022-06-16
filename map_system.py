import os
import pygame
from pygame.locals import *

def Map2Screen(rect, camera):
    rect[0] -=camera[0]
    rect[1] -=camera[1]
    return rect

def World2Screen(rect, camera):
    return (rect.x-camera[0], rect.y-camera[1])

def Screen2World(rect, camera):
    rect.x +=camera[0]
    rect.y +=camera[1]
    return rect


def loopBackground(display, bg, h_speed, v_speed, side_state):
    posx_ptr = ['posx', 'posx2']
    for i in range(len(bg)):
        for ptr in posx_ptr:
            if(side_state[1]):
                bg[i][ptr] -= h_speed*((i+1)/10)
                if (bg[i][ptr] < -(bg[i]['data'].get_width()-0.5)):
                  bg[i][ptr] = (bg[i]['data'].get_width()-0.5)
            elif(side_state[0]):
                bg[i][ptr] += h_speed*((i+1)/10)
                if (bg[i][ptr] > (bg[i]['data'].get_width()-0.5)):
                  bg[i][ptr] = -(bg[i]['data'].get_width()-0.5)
            if v_speed < 0 or v_speed > 2.9:
               bg[i]['posy'] -= v_speed/2
            if bg[i]['posy'] < display.get_height()-bg[i]['data'].get_height():
                bg[i]['posy'] = display.get_height()-bg[i]['data'].get_height()
            if bg[i]['posy'] > 0:
                bg[i]['posy'] = 0

            display.blit(bg[i]['data'], (bg[i][ptr], bg[i]['posy']))

def render_map(display, tileset, tile_size, map, camera):
    tile_rects = []
    y = 0
    for row in map:
        x = 0
        for tile in row:
            tile_coords = Map2Screen([x * tile_size, y * tile_size], camera)
            if tile != 0:
                display.blit(tileset[tile-1], tile_coords)
                tile_rects.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
            x += 1
        y += 1
    return tile_rects

def render_objects(display, tileset, tile_size, map, camera):
    tile_rects = []
    y = 0
    for row in map:
        x = 0
        for tile in row:
            tile_coords = Map2Screen([x * tile_size, y * tile_size], camera)
            if tile != 0:
                display.blit(tileset[tile-1], tile_coords)
            x += 1
        y += 1
