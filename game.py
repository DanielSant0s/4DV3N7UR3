from simplygame import *

def init(w_name, w, h):
    global scan_line
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption(w_name)
    screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN if w == 0 else 0)
    display = pygame.Surface((250*(screen.get_width()/screen.get_height()), 250))
    return clock, screen, display

def draw(display, screen):
    global scan_line
    surf = pygame.transform.scale(display, [screen.get_width(), screen.get_height()])
    screen.blit(surf, (0, 0))
    pygame.display.update()

def deinit():
    pygame.quit()