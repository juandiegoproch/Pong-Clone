import pygame
import json
import random
from helpers import *
import time


def gameplay_screen(screen,diff,player_name):
    #configs
    obstacle_size = 40
    obstacle_x_init = 200
    obstacle_probability = 0.05
    ball_radius = 10
    ball_speed = 3
    powerup_pertick_probability = 0.008
    ball_iframe = 3
    
    # FPS and screen stuff
    clock = pygame.time.Clock()
    screensize = screen.get_size()

    #timers
    deadtimer = 300

    #State variables
    dead = False
    has_extra_life = False
    has_extra_ball = False
    has_extra_size = False
    has_double_points = False
    ball_speed_modifier = 1
    ignores_obstacles = False

    current_power_up = "None"
    
    # Balls array
    balls = [ball(400,300,3,-3)]

    #player variables
    player_posx = 30
    player_posy = 250

    player_sizex = 30
    player_sizey = 80

    player_yspeed = 0

    points = 0
    points_multiplier = 0
    default_ballspeed = 3
    if diff == 0:
        default_ballspeed = 3
        points_multiplier = 1
        ball_iframe = 2
    elif diff == 1:
        default_ballspeed = 6
        points_multiplier = 1.5
        ball_iframe = 2
    elif diff == 2:
        default_ballspeed = 9
        points_multiplier = 2
        ball_iframe = 4
    ball_speed = default_ballspeed
    # powerup list

    powerups = []
    # Ambientes
    forest = pygame.image.load("Images/Forest2.jpg")
    mountains = pygame.image.load("Images/Mountains.jpg")
    desert = pygame.image.load("Images/desert.png")
    tundra = pygame.image.load("Images/tundra.gif")
    exosfera = pygame.image.load("Images/Space.jpg")
    ocean = pygame.image.load("Images/Ocean2.png")
    landscape = ""
    DiffAmbientProb = random.randint(1, 2)
    if diff == 1:
        DiffAmbientProb = random.randint(3, 4)
    if diff == 2:
        DiffAmbientProb = random.randint(5, 6)

    AmbientProb = DiffAmbientProb
    if AmbientProb == 1:
        landscape = forest
    elif AmbientProb == 2:
        landscape = mountains
    elif AmbientProb == 3:
        landscape = desert
    elif AmbientProb == 4:
        landscape = tundra
    elif AmbientProb == 5:
        landscape = ocean
    elif AmbientProb == 6:
        landscape = exosfera
    # Obstacle Generation:
    random.seed(100)
    obstacles = []
    for x in range((screensize[0]-obstacle_x_init)//obstacle_size):
        for y in range(screensize[1]//obstacle_size):
            if random.random() <= obstacle_probability:
                obstacles.append([x*obstacle_size, y*obstacle_size, -1])

    while True:
        
        #update player pos
        
        player_posy += player_yspeed
        
        #update ball positions
        
        for i in balls:
            i.xpos += i.dirx
            i.ypos += i.diry
        
        #on wall collide:
        for i in balls:
            #loose condition
            if i.xpos <= 0:
                if has_extra_life:
                    has_extra_life = False
                    i.dirx *=-1
                    current_power_up = "None"
                else:
                    dead = True

            
            #Bounce of wall
            if i.xpos >= screensize[0]:
                i.dirx *=-1
                points += points_multiplier*(2 if has_double_points else 1)
            # wrap arround!
            if i.ypos > screensize[1]:
                i.ypos = 0
            if i.ypos < 0:
                i.ypos = screensize[1]


        #draws
        screen.blit(landscape, [0, 0])

        #draw score:
        scorestr =  "Score: "+str(points)
        draw_text(screen,scorestr,20,720,10)

        #draw_power_up
        pwupstr =  "Power Up: "+current_power_up
        draw_text(screen,pwupstr,20,50,10)
        
        #Draw Player

        player_hitbox = pygame.draw.rect(screen,white,(player_posx,player_posy,player_sizex,player_sizey))

        #draw_obstacles:
        obstacle_hitboxes = []
        for i in obstacles:
            hitbox = pygame.draw.rect(screen,white,(i[0]+obstacle_x_init,i[1],obstacle_size,obstacle_size))
            obstacle_hitboxes.append(hitbox)

        #draw_balls
        for i in balls:
            pygame.draw.circle(screen, white, (i.xpos, i.ypos), ball_radius)
        
        # draw powerups:
        for i in powerups:
            pygame.draw.rect(screen,blue,i[0])
            
                             
        #spawn powerups
        if random.random() <= powerup_pertick_probability:
            #attempt to spawn a powerup
            powerup_x = random.randint(obstacle_x_init,screensize[0])
            powerup_y = random.randint(0,screensize[1])
            #Power id's
            # 1. Size increment
            # 2. Multiply ball
            # 3. Ball_speed +
            # 4. Ball_speed -
            # 5. x2 points
            # 6. ignore obstacles (600 frames)
            # 7. +1 life
            power = 7 if not random.randint(0,10) else random.randint(1,6)
            if doesnt_collide(powerup_x,powerup_y,obstacle_hitboxes):                             
                powerups.append((pygame.Rect(powerup_x,powerup_y,obstacle_size,obstacle_size),power))
        
        
        # ball/obstacle/player collision
        for bll in balls:
            #player collision handler
            if bll.ypos > player_posy and bll.ypos < player_posy+player_sizey and bll.xpos <= player_posx + player_sizex:
                #speed update
                bll.collision_timer = ball_iframe
                bll.dirx *= -1 + (random.randint(-1,1)*random.random()) + player_yspeed
                #speed normalize
                ball_speed_magnitude = (bll.diry**2 + bll.dirx**2)**0.5
                bll.diry = (bll.diry/ball_speed_magnitude)*ball_speed
                bll.dirx = (bll.dirx/ball_speed_magnitude)*ball_speed
            #obstacle collisison handler
            for obst in obstacle_hitboxes:
                if obst.collidepoint(bll.xpos,bll.ypos) and (not bll.collision_timer):
                    bll.collision_timer = ball_iframe
                    obst_centerx, obst_centery = obst.center
                    deltay = abs(obst_centerx - bll.xpos)
                    deltax = abs(obst_centery - bll.ypos)

                    if deltay < deltax:
                        bll.diry *= -1 + (random.randint(-1,1)*random.random())
                    else:
                        bll.dirx *= -1 + (random.randint(-1,1)*random.random())
                    # normalize speed
                    ball_speed_magnitude = (bll.diry**2 + bll.dirx**2)**0.5
                    bll.diry = (bll.diry/ball_speed_magnitude)*ball_speed
                    bll.dirx = (bll.dirx/ball_speed_magnitude)*ball_speed

            # power up collision
            for pwup in powerups:
                if pwup[0].collidepoint(bll.xpos,bll.ypos) and (not bll.collision_timer):
                    pwup_centerx, pwup_centery = pwup[0].center
                    deltay = abs(pwup_centerx - bll.xpos)
                    deltax = abs(pwup_centery - bll.ypos)
                    power = pwup[1]
                    powerups.remove(pwup)
                    
                    if deltay < deltax:
                        bll.diry *= -1 + (random.randint(-1,1)*random.random())
                        bll.dirx += (random.randint(-1,1)*random.random()) #to reduce infinibounce cases
                    else:
                        bll.dirx *= -1 + (random.randint(-1,1)*random.random())
                    # normalize speed
                    ball_speed_magnitude = (bll.diry**2 + bll.dirx**2)**0.5
                    bll.diry = (bll.diry/ball_speed_magnitude)*ball_speed
                    bll.dirx = (bll.dirx/ball_speed_magnitude)*ball_speed

                    # Powerup reset:
                    player_sizey = 80
                    balls = balls[0:1]
                    ball_speed = default_ballspeed
                    has_double_points = False
                    current_power_up = " None"
                    #Power id's
                    # 1. Size increment
                    # 2. Multiply ball
                    # 3. Ball_speed +
                    # 4. Ball_speed -
                    # 5. x2 points
                    # 6. ignore obstacles (600 frames)
                    # 7. +1 life
            
                    # do_powers_stuff
                    if power == 1:
                        #1. Size increment
                        player_sizey = 160
                        current_power_up = " + Tamaño"
                        
                    if power == 2:
                        
                        dir_x = random.randint(1,3)
                        dir_y = random.randint(1,3)
                        magnitude = (dir_x**2+dir_y**2)**0.5
                        
                        dir_x = dir_x/magnitude * ball_speed
                        dir_y = dir_y/magnitude * ball_speed

                        
                        balls.append(ball(pwup_centerx,pwup_centery,dir_x,dir_y))
                        
                        current_power_up = " + Pelotas"
                    if power == 3:
                        ball_speed = default_ballspeed * 0.75

                        current_power_up = " - Velocidad"
                        
                    if power == 4:
                        ball_speed = default_ballspeed * 2
                        current_power_up = " + Velocidad"

                    if power == 5:
                        has_double_points = True
                        current_power_up = " Puntos Dobles"

                    if power == 6:
                        ignores_obstacles = True
                        for bll in balls:
                            bll.collision_timer = 600
                        current_power_up = " Phase"
                    if power == 7:
                        has_extra_life = True
                        current_power_up = " Vida Extra"
            
            #decrement collision iframe
            if bll.collision_timer:
                bll.collision_timer -= 1
                if ignores_obstacles and bll.collision_timer <1:
                    current_power_up = " None"

        # Event Processing
        events = pygame.event.get()
        for ev in events:
            # Quit event
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            # player movement
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_w:
                    player_yspeed = -6
                if ev.key == pygame.K_s:
                    player_yspeed = 6
            #Si el usuario deja de presionar una tecla
            if ev.type == pygame.KEYUP:
                #Jugador 1
                if ev.key == pygame.K_w:
                    player_yspeed = 0
                if ev.key == pygame.K_s:
                    player_yspeed = 0
        
        if dead:
            draw_text(screen,"GAME OVER",120,50,250)
            deadtimer -=1
            if deadtimer <= 0:
                #TODO - LOG ON JSON
                highscores = {}
                with open("saves/player_scores.json") as scorefile:
                    highscores = json.load(scorefile)
                for i in highscores:
                    if highscores[i]["highscore"] < points:
                        highscores[i]["highscore"] = points
                        highscores[i]["name"] = player_name
                        break

                with open("saves/player_scores.json","w") as scorefile:
                    json.dump(highscores,scorefile)

                return 0
        
        pygame.display.flip()
        clock.tick(60)
