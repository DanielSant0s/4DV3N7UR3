from simplygame import *
from random import randint

def new(char_name, speed_list, frames_list, random=False):
    anim_dict = {}
    if random:
        rand_color = (randint(60,255),randint(60,255),randint(60,255))
    flist = sorted(os.listdir("Char/"+char_name+"/"))
    for i in range(len(flist)):
        name = get_between(flist[i], char_name+"_", ".png")
        anim_sprite = pygame.image.load("Char/"+char_name+"/" + flist[i]).convert_alpha()
        if random:
            anim_sprite.fill(rand_color, special_flags=pygame.BLEND_MULT)
        anim_dict[name] = {'sprite': anim_sprite, 'speed': speed_list[i], 'frames': frames_list[i]}
    return anim_dict

def change(char, state, anim, side=None):
    if side is not None:
        state['side'] = side
    if state['side'] == LEFT:
        state['prog'] = char[anim]['frames']-1
        if char[anim]['frames'] == 2:
            state['prog'] = 0
    else:
        state['prog'] = 0
    state['lim'] = char[anim]['frames']
    state['speed'] = char[anim]['speed']
    state['sprite'] = char[anim]['sprite']

def update(state, time_acc, life):
    if time_acc*state['speed'] > 600:
        if state['side'] == RIGHT:
            if state['prog'] <= state['lim']:
                    state['prog'] += 1
            if state['prog'] >= state['lim']:
                state['prog'] = 0
                if life <= 0:
                    state['prog'] = state['lim']-1
        else:
            if state['prog'] >= 0:
                    state['prog'] -= 1
            if state['prog'] <= 0:
                state['prog'] = state['lim']-1
                if life <= 0:
                    state['prog'] = 0
        time_acc = 0
    return time_acc