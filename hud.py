from simplygame import *

def init(color_list=[(255,61,65,180), (95,95,211,180), (26,95,211,180)]):
    val_list = []
    for i in range(len(color_list)):
        bar_dict = {}
        bar_dict['cur'] = pygame.Surface((100,8), pygame.SRCALPHA)
        bar_dict['cur'].fill(color_list[i])
        bar_dict['max'] = pygame.Surface((100,4), pygame.SRCALPHA)
        bar_dict['max'].fill(color_list[i])
        bar_dict['bg'] = pygame.Surface((100+4,12), pygame.SRCALPHA)
        bar_dict['bg'].fill((0,0,0,180))
        bar_dict['color'] = color_list[i]
        val_list.append(bar_dict)
    return val_list
        
def render(display, rect_dict, x, y):
    chunk_width = 0
    for i in range(len(rect_dict)):
        display.blit(rect_dict[i]['bg'], (x-2,y+chunk_width))
        display.blit(rect_dict[i]['max'], (x+rect_dict[i]['cur'].get_width(), y+4+chunk_width))
        display.blit(rect_dict[i]['cur'], (x,y+2+chunk_width))
        chunk_width += rect_dict[i]['bg'].get_height()

def update(rect_dict, val_list):
    global color_list
    for i in range(len(rect_dict)):
        w = rect_dict[i]['cur'].get_width() * val_list[i]/100
        rect_dict[i]['cur'] = pygame.transform.scale(rect_dict[i]['cur'], (w, rect_dict[i]['cur'].get_height()))
        rect_dict[i]['max'] = pygame.Surface((round(100-w),rect_dict[i]['max'].get_height()), pygame.SRCALPHA)
        rect_dict[i]['max'].fill(rect_dict[i]['color'])