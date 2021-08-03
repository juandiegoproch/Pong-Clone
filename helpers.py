import pygame

pygame.font.init()
#fuente = pygame.font.Font("Blockt.ttf", 30)
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
blue = (0,0,255)

def draw_text(surface,text,size,x,y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, red)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

class ball:
    def __init__(self, xpos, ypos, dirx, diry):
        self.xpos = xpos
        self.ypos = ypos
        self.diry = diry
        self.dirx = dirx
        self.collision_timer = 0
        self.infield = True
        self.consecutive_checks_hit = 0
def doesnt_collide(pointx,pointy,rects):
    for i in rects:
        if i.collidepoint(pointx,pointy):
            return False
    return True

    
