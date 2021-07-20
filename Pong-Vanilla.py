import sys
import pygame
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
jugador2_x = 750-ancho_jugador
jugador2_y = 300 - (alto_jugador//2)
#Movimientos de los jugadores
mov_jugador1 = 0
mov_jugador2 = 0
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
player2p = 0
def draw_text(surface,text,size,x,y):
    font = pygame.font.SysFont("serif",size)
    text_surface = font.render(text,True,blanco)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface,text_rect)
#Flag: bandera de fin del juego
game_over = False
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
            #Jugador 2
            if evento.key == pygame.K_UP:
                mov_jugador2 = -3
            if evento.key == pygame.K_DOWN:
                mov_jugador2 = 3
        #Si el usuario deja de presionar una tecla
        if evento.type == pygame.KEYUP:
            #Jugador 1
            if evento.key == pygame.K_w:
                mov_jugador1 = 0
            if evento.key == pygame.K_s:
                mov_jugador1 = 0
            # Jugador 2
            if evento.key == pygame.K_UP:
                mov_jugador2 = 0
            if evento.key == pygame.K_DOWN:
                mov_jugador2 = 0

    #Rebote: pelota
    if pelota_y > 600 or pelota_y <0:
        mov_pelota_y *=-1
    #Si la pelota sale por el lado izquierdo o derecho es porque alguien perdió
    if pelota_x>800:
        pelota_x = 400
        pelota_y = 300
        incremento += 1
        player1p += 1
        #Si sale de la pantalla, invertimos la dirección
        mov_pelota_x*=-1
        mov_pelota_y*=-1
    if pelota_x<0:
        pelota_x = 400
        pelota_y = 300
        incremento += 1
        player2p += 1
        #Si sale de la pantalla, invertimos la dirección
        mov_pelota_x*=-1
        mov_pelota_y*=-1
    #Mover a los jugadores
    jugador1_y += mov_jugador1
    jugador2_y += mov_jugador2
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
    #Dibujar jugador 2
    jugador2 = pygame.draw.rect(pantalla, blanco, (jugador2_x, jugador2_y, ancho_jugador, alto_jugador))
    #Dibujamos la pelota
    pelota = pygame.draw.circle(pantalla, blanco, (pelota_x, pelota_y), 10)
    #Colisiones
    if pelota.colliderect(jugador1) or pelota.colliderect(jugador2):
        mov_pelota_x*=-1

    #Actualización de pantalla

    #FPS
    if incremento % 2 == 0 and incremento != 0:
        fast = fast + 20
        incremento = incremento - 2
    reloj.tick(fast)

    draw_text(pantalla,str(player1p),25,50,10)
    draw_text(pantalla, str(player2p), 25, 750, 10)
    pygame.display.flip()
pygame.quit()
