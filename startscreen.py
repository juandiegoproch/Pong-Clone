import pygame
import json
from helpers import *

def start_screen(screen):
    #sound
    background_track = pygame.mixer.Sound("Audio/Music/bg_score.ogg")
    background_track.play(loops=-1)
    # variables
    clock = pygame.time.Clock()
    display_player_qty = 5
    background = pygame.image.load("Images/Background.png.").convert()
    rect_back = pygame.image.load("Images/men.2.png").convert()
    imm = pygame.image.load("Images/start_button2.png").convert()


    #Fetch Data from highscores json
    scores = {}
    with open("saves/player_scores.json",) as scores_file:
        scores = json.load(scores_file)

    # Sub-Mainloop
    while True:
        #draws
        screen.blit(background, [0, 0])

        for player in range(display_player_qty):
            playerid = str(player)
            
            player_highscore = str(scores[playerid]["highscore"])
            player_name = scores[playerid]["name"]
            
            screen.blit(rect_back, (50 ,(player*80)+75))

            draw_text(screen, player_name, 20, 60, (player*80)+90)
            draw_text(screen, player_highscore, 20, 650, (player*80)+90)

        start_button = screen.blit(imm, (100, 500, 600, 80))
        draw_text(screen, "Inicio", 20, 370, 525)
        #event fetch
        events = pygame.event.get()
        #Event processing:
        for ev in events:
            # Quit event
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            #Click event
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                pos = pygame.mouse.get_pos()
                if start_button.collidepoint(pos):
                    background_track.fadeout(3000)
                    return 1
        
        #flip screen
        pygame.display.flip()
        clock.tick(60)
