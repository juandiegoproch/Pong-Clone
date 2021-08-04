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
    powerup_pertick_probability = 0.01
    ball_iframe = 3
    xmovement_addition = 3
    player_speed = 6
    weird_bounce_chance = 0.1
    extra_size_player = 160
    weird_tp_chance = 0.005
    
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

    # Sound effect handles
    

    #player variables
    player_standard = pygame.image.load("Sprites/Player_textures/paleta.png")
    player_extended = pygame.image.load("Sprites/Player_textures/paleta_extended.png")
    player_icon = None
    player_posx = 30
    player_posy = 250

    player_sizex = 30
    player_sizey = 80

    player_yspeed = 0

    points = 0
    points_multiplier = 0
    default_ballspeed = 3
    if diff == 0:
        player_speed = 6
        default_ballspeed = 3
        points_multiplier = 1
        ball_iframe = 3
    elif diff == 1:
        player_speed = 9
        default_ballspeed = 6
        points_multiplier = 1.5
        ball_iframe = 4
    elif diff == 2:
        player_speed = 12
        default_ballspeed = 9
        points_multiplier = 2
        ball_iframe = 5
    ball_speed = default_ballspeed
    
    # Balls array
    balls = [ball(400,300,default_ballspeed,-default_ballspeed)]
    # powerup list

    powerups = []

    #powerup_Textures
        #Power id's
        # 1. Size increment
        # 2. Multiply ball
        # 3. Ball_speed +
        # 4. Ball_speed -
        # 5. x2 points
        # 6. ignore obstacles (600 frames)
        # 7. +1 life
    powerups_textures = [
        pygame.image.load("Sprites/power_ups/extra_size.png"),
        pygame.image.load("Sprites/power_ups/ball_multiply.png"),
        pygame.image.load("Sprites/power_ups/ballspeed+.png"),
        pygame.image.load("Sprites/power_ups/ballspeed-.png"),
        pygame.image.load("Sprites/power_ups/x2_score.png"),
        pygame.image.load("Sprites/power_ups/phase.png"),
        pygame.image.load("Sprites/power_ups/extra_live.png"),
        pygame.image.load("Sprites/Obstacles/obstacle.png"),
        ]
    
    #
    
    # Ambientes
    ambientes = [pygame.image.load("Images/Forest2.jpg"),
                 pygame.image.load("Images/Mountains.jpg"),
                 pygame.image.load("Images/desert.png"),
                 pygame.image.load("Images/tundra.jpg"),
                 pygame.image.load("Images/Space.jpg"),
                 pygame.image.load("Images/Ocean2.png"),
    ]
    musicas = [
        pygame.mixer.Sound("Audio/Music/bg_forest.ogg"),
        pygame.mixer.Sound("Audio/Music/bg_montana.ogg"),
        pygame.mixer.Sound("Audio/Music/bg_desierto.ogg"),
        pygame.mixer.Sound("Audio/Music/bg_tundra.ogg"),
        pygame.mixer.Sound("Audio/Music/bg_espacio.ogg"),
        pygame.mixer.Sound("Audio/Music/bg_ocean.ogg")

        ]
    # seleccionar ambientes y musica!
    bg_music = None
    landscape = None
    DiffAmbientProb = None
    if diff == 0:
        DiffAmbientProb = random.randint(0, 2)
    if diff == 1:
        DiffAmbientProb = random.randint(2, 3)
    if diff == 2:
        DiffAmbientProb = random.randint(4, 5)
    bg_music = musicas[DiffAmbientProb]
    bg_music.play(loops=-1)
    landscape = ambientes[DiffAmbientProb]


    obstacles = []

    while True:
        
        #update player pos
        
        player_posy += player_yspeed
        
        #update ball positions
        
        for i in balls:
            i.xpos += int(i.dirx) 
            i.ypos += int(i.diry)
        
        #on wall collide:
        for i in balls:
            # do for all balls, add a bit to xpos to avoid vertical travel that is VERY annoying
            if i.dirx < (i.diry*10):
                i.dirx+= 0.01
                i.dirx*=1.005
                ball_speed_magnitude = (i.diry**2 + i.dirx**2)**0.5
                i.diry = (i.diry/ball_speed_magnitude)*ball_speed
                i.dirx = (i.dirx/ball_speed_magnitude)*ball_speed
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
                #if it should bounce
                if not i.consecutive_checks_hit:
                    #if it hasn´t bounced allready
                    collision_timer = ball_iframe
                    i.dirx = (i.dirx* -1)
                    i.xpos = screensize[0]-3


                    #points
                    points += points_multiplier*(2 if has_double_points else 1)
            else:
                i.consecutive_checks_hit = False
                
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

        #draw_power_up text
        pwupstr =  "Power Up: "+current_power_up
        draw_text(screen,pwupstr,20,50,10)
        
        #Draw Player
        if player_sizey <= 85:
            screen.blit(player_standard,(player_posx,player_posy))
        else:
            screen.blit(player_extended,(player_posx,player_posy))
        player_hitbox = pygame.Rect((player_posx,player_posy,player_sizex,player_sizey))
        

        #draw_obstacles:
        obstacle_hitboxes = []
        for i in obstacles:
            hitbox = pygame.draw.rect(screen,white,(i[0]+obstacle_x_init,i[1],obstacle_size,obstacle_size))
            obstacle_hitboxes.append(hitbox)

        #draw_balls
        for i in balls:
            pygame.draw.circle(screen, black, (i.xpos, i.ypos), ball_radius)
        
        # draw powerups:
        to_blit = [(powerups_textures[p[1]-1],(p[0].x,p[0].y)) for p in powerups]
        screen.blits(to_blit)
            
                             
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
            if doesnt_collide(pygame.Rect(powerup_x,powerup_y,obstacle_size,obstacle_size),powerups):
                if random.random() <= 0.7:
                    powerups.append((pygame.Rect(powerup_x,powerup_y,obstacle_size,obstacle_size),8))
                else:
                    powerups.append((pygame.Rect(powerup_x,powerup_y,obstacle_size,obstacle_size),power))
                
        
        
        # ball/obstacle/player collision
        for bll in balls:
            #ball is on playing field:
            if bll.xpos > player_posx + player_sizex:
                bll.infield = True
            #player collision handler
            if bll.ypos > player_posy and bll.ypos < player_posy+player_sizey and bll.xpos <= player_posx + player_sizex and bll.xpos >= player_posx and bll.infield:
                #speed update
                bll.dirx -= xmovement_addition # ball.dirx is allways negative +(-) to increment it!
                bll.dirx *= -1
                bll.diry += player_yspeed
                bll.collision_timer = ball_iframe
                #speed normalize
                ball_speed_magnitude = (bll.diry**2 + bll.dirx**2)**0.5
                bll.diry = (bll.diry/ball_speed_magnitude)*ball_speed
                bll.dirx = (bll.dirx/ball_speed_magnitude)*ball_speed
                bll.infield = False
            #obstacle collisison handler
            has_hit = False
            for obst in obstacle_hitboxes:
                if obst.collidepoint(bll.xpos,bll.ypos) and (not bll.collision_timer) and not(bll.consecutive_checks_hit):
                    has_hit = True
                    bll.consecutive_checks_hit +=1
                    bll.collision_timer = ball_iframe 
                    obst_centerx, obst_centery = obst.center
                    deltay = abs(obst_centerx - bll.xpos)
                    deltax = abs(obst_centery - bll.ypos)
                    # weird bounce: bounce to a side with lots-a-speed!
                    weird_bounce_x = random.choice([-10,10]) if random.random() < weird_bounce_chance else 0 
                    weird_bounce_y = random.choice([-10,10]) if random.random() < weird_bounce_chance else 0
                    if deltay < deltax:
                        bll.diry += abs(random.randint(-1,1)*random.random())*bll.diry*abs(1/bll.diry)
                        bll.diry *= -1
                    else:
                        bll.dirx += abs(random.randint(-1,1)*random.random()+xmovement_addition)*bll.dirx*abs(1/bll.dirx)
                        bll.dirx *= -1 + (random.randint(-2,2)*random.random())
                    # normalize speed
                    ball_speed_magnitude = (bll.diry**2 + bll.dirx**2)**0.5
                    bll.diry = (bll.diry/ball_speed_magnitude)*ball_speed
                    bll.dirx = (bll.dirx/ball_speed_magnitude)*ball_speed
                    del(obst)
            if not(has_hit):
                bll.consecutive_checks_hit = 0

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
                        player_sizey = extra_size_player
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
                    player_yspeed = -player_speed
                if ev.key == pygame.K_s:
                    player_yspeed =  player_speed
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
            bg_music.fadeout(10000)
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
