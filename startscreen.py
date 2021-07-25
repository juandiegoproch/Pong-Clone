import pygame
import json
from helpers import *

def start_screen(screen):
    # variables
    clock = pygame.time.Clock()
    display_player_qty = 5

    #Fetch Data from highscores json
    scores = {}
    with open("saves/player_scores.json",) as scores_file:
        scores = json.load(scores_file)
    
    # Sub-Mainloop
    while True:
        #draws
        screen.fill(black)
        for player in range(display_player_qty):
            playerid = str(player)
            
            player_highscore = str(scores[playerid]["highscore"])
            player_name = scores[playerid]["name"]
            
            pygame.draw.rect(screen,white,((50,(player*80)+50,700,70)))
            
            draw_text(screen,player_name,20,60,(player*80)+70)
            draw_text(screen,player_highscore,20,650,(player*80)+70)
        
        start_button = pygame.draw.rect(screen,white,((100,500,600,80)))
        draw_text(screen,"START",20,370,525)
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
                    return 1
        
        #flip screen
        pygame.display.flip()
        clock.tick(60)
    
