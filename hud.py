from simplygame import *

def init(color_list=[(255,61,65,180), (95,95,211,180), (26,95,211,180)]):
    val_list = []
    for i in range(len(color_list)):
        bar_dict = {}
        bar_dict['cur'] = pygame.Surface((100,8), pygame.SRCALPHA)
        bar_dict['cur'].fill(color_list[i])
        bar_dict['max'] = pygame.Surface((100,4), pygame.SRCALPHA)
        bar_dict['max'].fill(color_list[i])
        bar_dict['bg'] = pygame.Surface((113+4,12), pygame.SRCALPHA)
        bar_dict['bg'].fill((0,0,0,180))
        bar_dict['color'] = color_list[i]
        life_sprite = pygame.image.load("UI/life.png").convert_alpha()
        bar_dict['l_sprite'] = pygame.transform.scale(life_sprite, ((life_sprite.get_width() * .4), (life_sprite.get_height() * .4)))
        dash_sprite = pygame.image.load("UI/dash.png").convert_alpha()
        bar_dict['d_sprite'] = pygame.transform.scale(dash_sprite, ((dash_sprite.get_width() * .4), (dash_sprite.get_height() * .4)))
        special_sprite = pygame.image.load("UI/special.png").convert_alpha()
        bar_dict['s_sprite'] = pygame.transform.scale(special_sprite, ((special_sprite.get_width() * .4), (special_sprite.get_height() * .4)))
        val_list.append(bar_dict)
    return val_list
        
def render(display, rect_dict, x, y):
    chunk_width = 0
    for i in range(len(rect_dict)):
        display.blit(rect_dict[i]['bg'], (x-2,y+chunk_width))
        display.blit(rect_dict[i]['max'], (x+rect_dict[i]['cur'].get_width(), y+4+chunk_width))
        display.blit(rect_dict[i]['cur'], (x,y+2+chunk_width))
        chunk_width += rect_dict[i]['bg'].get_height()
        display.blit(rect_dict[i]['l_sprite'], (112,12))
        display.blit(rect_dict[i]['d_sprite'], (112,23))
        display.blit(rect_dict[i]['s_sprite'], (112,34))

def update(rect_dict, val_list):
    for i in range(len(rect_dict)):
        rect_dict[i]['cur'] = pygame.Surface(((0 if val_list[i] <= 0 else val_list[i]),rect_dict[i]['cur'].get_height()), pygame.SRCALPHA)
        rect_dict[i]['cur'].fill(rect_dict[i]['color'])
        rect_dict[i]['max'] = pygame.Surface(((100 if val_list[i] <= 0 else 100-val_list[i]),rect_dict[i]['max'].get_height()), pygame.SRCALPHA)
        rect_dict[i]['max'].fill(rect_dict[i]['color'])