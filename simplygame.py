import pygame
from pygame.locals import *
from consts import *
import sys
import os
import io

def get_between(s, first, last):
    start = s.index(first) + len(first)
    end = s.index(last, start)
    return s[start:end]

def print_text(font, display, text, x, y, color=(255,255,255), bg_color=None, alpha=255, scale=1.0, center=True):
    str_list = []
    temp_i = -1
    for i in range(len(text)):
        if text[i] == "\n":
            str_list.append(text[temp_i+1:i])
            temp_i = i
    str_list.append(text[temp_i+1:])

    for i in range(len(str_list)):
        if bg_color is None:
            text_surface = font.render(str_list[i], True, color)
        else:
            text_surface = font.render(str_list[i], True, color, bg_color)
        text_surface.set_alpha(alpha)
        text_surface = pygame.transform.scale(text_surface, [text_surface.get_width()*scale, text_surface.get_height()*scale])
        text_rect = text_surface.get_rect()
        text_rect.x = x
        text_rect.y = y+(i*text_rect.height)
        if center:
            text_rect.midtop = (x, y+((i+1)*text_rect.height))
        display.blit(text_surface, text_rect)

def get_text_size(font, text, scale=1.0):
    text_surface = font.render(text, True, (0,0,0))
    text_rect = text_surface.get_rect()
    return (text_rect.width*scale, text_rect.height*scale)


def load_texture_dictionary(path, scale=1.0):
    tex_dict = []
    flist = sorted(os.listdir(path))
    for fname in flist:
        tex_dict.append(pygame.image.load(path + fname).convert_alpha())
        if scale != 1.0:
            tex_dict[-1] = pygame.transform.scale(tex_dict[-1], ((tex_dict[-1].get_width() * scale), (tex_dict[-1].get_height() * scale)))
    return tex_dict

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def blur(surface, qt):
    radius = 1.0/float(qt)
    size = surface.get_size()
    scale_size = (int(size[0]*radius), int(size[1]*radius))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, size)
    return surf

def new_rectEX(width, height, color):
    rect = pygame.Surface((width,height), pygame.SRCALPHA)
    rect.fill(color)
    return rect

def smooth_camera(camera, player_rect, display, l, r, j):
    if not r and not l:
        if camera[0] > player_rect.x-180:
            camera[0] -= 2.4
        if camera[0] < player_rect.x-180:
            camera[0] += 2.4
    if not j:
        if camera[1] > player_rect.y-100:
            camera[1] -= 2.0
        if camera[1] < player_rect.y-100:
            camera[1] += 2.0

def dt_value(dt, value):
    return value