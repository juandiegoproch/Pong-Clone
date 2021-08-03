import pygame

from startscreen import *
from registerscreen import *
from gameplay import *

#init
pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
sizeof_screen = (800,600)


# Game Variables:
player_name = "PLACEHOLDER"
screen = pygame.display.set_mode(sizeof_screen)
runmode = 0
difficulty = 0
while True:
    if runmode == 0:
        #start screen
        runmode = start_screen(screen)

    if runmode == 1:
        #register
        difficulty, player_name, runmode = register_screen(screen)
    if runmode == 2:
        #game_code
        runmode = gameplay_screen(screen,difficulty,player_name)
    
