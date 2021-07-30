import pygame
import json
from helpers import *



def register_screen(screen):
    clock = pygame.time.Clock()
    background = pygame.image.load("Images/Background.png.").convert()
    name = ""
    listening_keyboard = 0
    difficulty = 0
    while True:
        screen.blit(background, [0, 0])

        #Name Stuff
        draw_text(screen,"Nombre: ",30,100,100)
        text_box = pygame.draw.rect(screen,white,((210,95,450,50)))
        draw_text(screen,name,30,250,100)
        #Play Button
        play_button = pygame.draw.rect(screen,white,((300,500,200,70)))
        draw_text(screen,"Jugar",30,360,510)

        #Difficulty
        diff1_button = pygame.draw.rect(screen, blue if difficulty == 0 else white,((100,220,300,50)))
        draw_text(screen,"Facil",30,110,230)
        diff2_button = pygame.draw.rect(screen, blue if difficulty == 1 else white,((100,280,300,50)))
        draw_text(screen,"Intermedio",30,110,300)
        diff3_button = pygame.draw.rect(screen, blue if difficulty == 2 else white,((100,340,300,50)))
        draw_text(screen,"Dificil",30,110,360)
        
        events = pygame.event.get()
        for ev in events:
            # Quit event
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Button Interaction
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                pos = pygame.mouse.get_pos()
                # listening keyboard
                if text_box.collidepoint(pos):
                    listening_keyboard = 1
                else:
                    listening_keyboard = 0
                # Get_Difficulty

                #easy
                if diff1_button.collidepoint(pos):
                    difficulty = 0
                #medium
                if diff2_button.collidepoint(pos):
                    difficulty = 1
                #hard
                if diff3_button.collidepoint(pos):
                    difficulty = 2

                # Play the game!

                if play_button.collidepoint(pos):
                    return difficulty, name, 2
            if ev.type == pygame.KEYDOWN:
                if listening_keyboard:
                    if ev.key == pygame.K_RETURN:
                        listening_keyboard = 0
                    elif ev.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name+= ev.unicode
                    

            # Fetch key press event
            
        
        pygame.display.flip()
        clock.tick(60)
    
