from simplygame import *

def process_menu_commands(event_dict, ptr_dict):
    if isinstance(ptr_dict, dict):
        if event_dict['dec']:
            if ptr_dict['store'] is not None:
                ptr_dict['store'][ptr_dict['ptr']] = ptr_dict['ptr']
            if ptr_dict['ptr'] == 0:
                ptr_dict['ptr'] = ptr_dict['lim'] - 1
            else:
                ptr_dict['ptr'] -= 1
            if ptr_dict['store'] is not None:
                ptr_dict['ptr'] = ptr_dict['store'][ptr_dict['ptr']]
        if event_dict['inc']:
            if ptr_dict['store'] is not None:
                ptr_dict['store'][ptr_dict['ptr']] = ptr_dict['ptr']
            if ptr_dict['ptr'] == ptr_dict['lim'] - 1:
                ptr_dict['ptr'] = 0
            else:
                ptr_dict['ptr'] += 1
            if ptr_dict['store'] is not None:
                ptr_dict['ptr'] = ptr_dict['store'][ptr_dict['ptr']]
        return
    for i in range(len(event_dict)):
        if event_dict[i]['dec']:
            if ptr_dict[i]['store'] is not None:
                ptr_dict[0]['store'][ptr_dict[0]['ptr']] = ptr_dict[1]['ptr']
            if ptr_dict[i]['ptr'] == 0:
                ptr_dict[i]['ptr'] = ptr_dict[i]['lim'] - 1
            else:
                ptr_dict[i]['ptr'] -= 1
            if ptr_dict[i]['store'] is not None:
                ptr_dict[1]['ptr'] = ptr_dict[0]['store'][ptr_dict[0]['ptr']]
        if event_dict[i]['inc']:
            if ptr_dict[i]['store'] is not None:
                ptr_dict[0]['store'][ptr_dict[0]['ptr']] = ptr_dict[1]['ptr']
            if ptr_dict[i]['ptr'] == ptr_dict[i]['lim'] - 1:
                ptr_dict[i]['ptr'] = 0
            else:
                ptr_dict[i]['ptr'] += 1
            if ptr_dict[i]['store'] is not None:
                ptr_dict[1]['ptr'] = ptr_dict[0]['store'][ptr_dict[0]['ptr']]
