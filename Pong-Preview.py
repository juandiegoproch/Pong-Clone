import sys
import pygame
import random
import time

tamano_obst = 30
collision_timeout = 10

pygame.init()
#Colores
negro = (0,0,0)
blanco = (255,255,255)
#Variables de la Pantalla
pantalla_x = 800
pantalla_y = 600
tamanho_pantalla = (pantalla_x, pantalla_y)
#Dimensiones de las paletas
ancho_jugador = 15
alto_jugador = 90
#Dimensiones de la pantalla
pantalla = pygame.display.set_mode(tamanho_pantalla)
#Reloj: FPS
reloj = pygame.time.Clock()
#Coordenadas del jugador 1
jugador1_x = 50
jugador1_y = 300 - (alto_jugador//2)
#Movimientos de los jugadores
mov_jugador1 = 0
#Coordenadas de la pelota
pelota_x = 400
pelota_y = 300
mov_pelota_x = 3
mov_pelota_y = 3
#Rapidez
fast = 60
#Puntaje para rapidez
incremento = 0
#Marcador
player1p = 0
def draw_text(surface,text,size,x,y):
    font = pygame.font.SysFont("serif",size)
    text_surface = font.render(text,True,blanco)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface,text_rect)
#Flag: bandera de fin del juego
game_over = False
game_over_not_quit = False
collider_timer = 0
# Generar obstaculos
obstaculos = []
for x in range(200,800,tamano_obst):
    for y in range(50,600,tamano_obst):
        if random.randint(0,20) == 1:
            obstaculos.append((x,y))
while not game_over:
    # Hasta que el jugador decida romper el bucle: salir del juego
    for evento in pygame.event.get():
        # print(evento)
        #Si sale del juego
        if evento.type == pygame.QUIT:
            game_over = True
        #Si el usuario mantiene presionada una tecla
        if evento.type == pygame.KEYDOWN:
            #Jugador 1
            if evento.key == pygame.K_w:
                mov_jugador1 = -3
            if evento.key == pygame.K_s:
                mov_jugador1 = 3
        #Si el usuario deja de presionar una tecla
        if evento.type == pygame.KEYUP:
            #Jugador 1
            if evento.key == pygame.K_w:
                mov_jugador1 = 0
            if evento.key == pygame.K_s:
                mov_jugador1 = 0

    #Rebote: pelota
    if pelota_y > 600:
        pelota_y = 0
    if pelota_y < 0:
        pelota_y = 600
    if pelota_x > 800:
        mov_pelota_x *=-1
    #Si la pelota sale por el lado izquierdo o derecho es porque alguien perdió
    if pelota_x < 0:
        game_over_not_quit = True
        
    #Mover a los jugadores
    jugador1_y += mov_jugador1
    #Mover a la pelota
    pelota_x += mov_pelota_x
    pelota_y += mov_pelota_y

    #------------------------------------------------------------------------
    # Dibujos
    # ------------------------------------------------------------------------
    # Pintar fondo
    pantalla.fill(negro)
    #Dibujar jugador 1
    jugador1 = pygame.draw.rect(pantalla, blanco, (jugador1_x, jugador1_y, ancho_jugador, alto_jugador))
    obstaculos_hitboxes = []
    #Dibujar obstaculos
    for obst in obstaculos:
        obstaculos_hitboxes.append(pygame.draw.rect(pantalla, blanco, (obst[0], obst[1], tamano_obst, tamano_obst)))
    #Dibujamos la pelota
    pelota = pygame.draw.circle(pantalla, blanco, (pelota_x, pelota_y), 10)
    if game_over_not_quit:
        draw_text(pantalla, "GAME OVER", 100, 400,250)
    #Colisiones
    if pelota.colliderect(jugador1) and not collider_timer:
        mov_pelota_x*=-1
        mov_pelota_y+= random.random()*random.randint(-3,3)
        mov_pelota_x+= random.random()*random.randint(-3,3)
        collider_timer = collision_timeout
    for obst in obstaculos_hitboxes:
        if pelota.colliderect(obst) and not collider_timer:
            center_x = obst.x+tamano_obst//2
            center_y = obst.y+tamano_obst//2
            """
            Ver cual de los ejes es el que más cerca está del centro, rebotar en ese eje
            """

            delta_x = abs(pelota_x - center_x)
            delta_y = abs(pelota_y - center_y)

            if delta_x >= delta_y:

                mov_pelota_x *=-1
                mov_pelota_x += random.random()*random.randint(-1,1)
                mov_pelota_y += random.random()*random.randint(-1,1)
            else:
                
                mov_pelota_y *=-1
                mov_pelota_x += random.random()*random.randint(-1,1)
                mov_pelota_y += random.random()*random.randint(-1,1)

            collider_timer = collision_timeout

    if collider_timer > 0: collider_timer-=1
    #Actualización de pantalla
    
    #FPS
    if incremento % 2 == 0 and incremento != 0:
        fast = fast + 20
        incremento = incremento - 2
    reloj.tick(fast)

    draw_text(pantalla,str(player1p),25,50,10)
    pygame.display.flip()
pygame.quit()
