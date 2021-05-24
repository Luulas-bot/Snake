# Imports
import pygame
import random
import sys
import time 

# Importe de las constantes globales
from constants import (row, col, tail_list, screen, background, titulo_snake, press_play_button,
play_button, press_quit_button, quit_button, clock, point_list_count, point_list, width, WHITE, height,
x_pos_point_list, y_pos_point_list, time_limit, pause, play_game_background, sound_button, canceled_sound_button,
pressed_sound_button) 

# Inicializacion de pygame
pygame.init()

# Musica de fondo
pygame.mixer.music.load("audios/chiptune_4.mp3")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.03)

# Clase de la snake
class Snake(pygame.sprite.Sprite):
    
    def __init__(self, initial_pos):
        super().__init__()
        self.image = pygame.image.load("images/head_snake.png")
        self.rect = self.image.get_rect()
        
        self.previous_position_x = self.rect.x + 1 * row
        self.previous_position_y = self.rect.y
        self.initial_pos = initial_pos
        self.rect.x = self.initial_pos[0]
        self.rect.y = self.initial_pos[1]

    # Se actualiza todo el tiempo y se sobreescribe en una variable la posición previa de la snake    
    def update(self):
        self.previous_x = self.rect.x
        self.previous_y = self.rect.y
        
# Clase de la cola
class Tail(pygame.sprite.Sprite):
    
    def __init__(self, x, y, initial_position):
        super().__init__()
        self.image = pygame.image.load("images/body_snake.png")
        self.rect = self.image.get_rect()
        self.rect.x = initial_position[0]
        self.rect.y = initial_position[1]
        
        self.previous_x = self.rect.x + 1
        self.previous_y = self.rect.y
        
    # Se toman los valores de la posición actual de la cola y se escriben en una variable además
    # de actualizar los valores en sí mismos de la posición de la cola
    def update_with_position(self, new_x, new_y):
        self.previous_x = self.rect.x
        self.previous_y = self.rect.y

        self.rect.x = new_x
        self.rect.y = new_y
          
# Clase de los puntos que aparecen en pantalla que tiene que devorar la snake
class Points(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Point.png")
        self.rect = self.image.get_rect()
        
    # Define la posición de los puntos
    def pos(self, x, y):    
        self.rect.x = x * row
        self.rect.y = y * col

# Creo las clases y las añado a una lista de sprites general
snake = Snake([450, 330])
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(snake)
first_tail = Tail(snake.previous_position_x, snake.previous_position_y, [snake.previous_position_x, snake.previous_position_y])
all_tails = [first_tail]
tails_hit_list = pygame.sprite.Group()
tails_hit_list.add(first_tail)
for tail in all_tails:
    all_sprites_list.add(tail)
tail_list_count = pygame.sprite.Group()
tail_list_count.add(tail)

# Pantalla del menú principal
def main_menu():
    
    global pressed_sound_button
    
    # Variables de la funcion
    pygame.mouse.set_visible(1)
    done = False
    
    # Hitbox de los botones del menú principal
    play_game_button = pygame.Rect((280, 360), (300, 100))
    quit_game_button = pygame.Rect(300, 470, 250, 60)
    sound_game_button = pygame.Rect(810, 620, 60, 60)
    
    # Variable del boton presionado. Define si esta presionado o no.
    pressed_button = False
    pressed_quit_button = False
    
    # Bucle principal de la funcion
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()    
            
            # Click en los botones del menu
            mx, my = pygame.mouse.get_pos()
            if play_game_button.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0] == 1:  
                    pressed_button = True
            if event.type == pygame.MOUSEBUTTONUP:
                if play_game_button.collidepoint((mx, my)):
                    play_game()
            if quit_game_button.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0] == 1:  
                    pressed_quit_button = True
            if event.type == pygame.MOUSEBUTTONUP:
                if quit_game_button.collidepoint((mx, my)):
                    sys.exit()
            if sound_game_button.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0] == 1:
                    if pressed_sound_button == False:
                        pressed_sound_button = True
                        pygame.mixer.music.pause()  
                    elif pressed_sound_button == True:    
                        pressed_sound_button = False
                        pygame.mixer.music.unpause()
                    
        # Mostrar por pantalla el background y el titulo
        screen.blit(background, (0, 0))
        screen.blit(titulo_snake, (130, 30))
        
        # Elegir si mostrar por pantalla el boton presionado o no
        if pressed_button == True:
            screen.blit(press_play_button, (280, 360))            
        else:
            screen.blit(play_button, (280, 360))
        if pressed_quit_button == True:
            screen.blit(press_quit_button, (300, 440))            
        else:
            screen.blit(quit_button, (300, 440))
        if pressed_sound_button == True:
            screen.blit(canceled_sound_button, (810, 620))
        else:
            screen.blit(sound_button, (810, 620))
                        
        # Se actualiza la pantalla a 60 frames por segundo
        pygame.display.flip()
        clock.tick(60)

# Pantalla del juego en sí
def play_game():
    
    # Hacer las variables que se van a usar globales dentro de la función
    global time_limit
    global pause
    global point_coords
    
    # Hace no visible el mouse
    pygame.mouse.set_visible(1)
    done = False
    
    # Establecer las variables para reconocer si una tecla está presionada o no
    snake_left_bool = True
    snake_right_bool = False
    snake_up_bool = False
    snake_down_bool = False 
    
    # Texto de la pausa
    font = pygame.font.SysFont("Comic", 25, bold = True)
    text1 = font.render("PRESS 'P' TO PAUSE AND UNPAUSE", True, WHITE)
    
    if len(point_list_count) == 0:    
        create_point()
        
    # Variable que setea el timer a 0 para contar el tiempo desde 0.
    start_time = time.time()
        
    # Bucle principal de la funcion
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            # Registra los eventos de presionar las teclas y hace verdadero o falso los boleanos que definen que tecla esta presionada
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if snake_down_bool == False:
                        snake_up_bool = True
                        snake_left_bool = False
                        snake_right_bool = False
                        snake_down_bool = False
                        snake.image = pygame.image.load("images/head_snake_up.png")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if snake_up_bool == False:
                        snake_up_bool = False
                        snake_left_bool = False
                        snake_right_bool = False
                        snake_down_bool = True
                        snake.image = pygame.image.load("images/head_snake_down.png")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if snake_right_bool == False:    
                        snake_up_bool = False
                        snake_left_bool = True
                        snake_right_bool = False
                        snake_down_bool = False
                        snake.image = pygame.image.load("images/head_snake.png")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                     if snake_left_bool == False:   
                        snake_up_bool = False
                        snake_left_bool = False
                        snake_right_bool = True
                        snake_down_bool = False
                        snake.image = pygame.image.load("images/head_snake_right.png")
            
            # Registra si se presiona la 'p' para entrar en la función de pausado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_menu()
                                
        
        # Lista de las colisiones entre la serpiente y los puntos
        point_hit_list = pygame.sprite.spritecollide(snake, point_list, True)
        tails_collide_list = pygame.sprite.spritecollide(snake, tails_hit_list, True)
        
        # Si la lista de colisiones devuelve "True" se llama a la funcion para crear otro punto
        if point_hit_list:
            add_new_tail()
            create_point()
            
        # Crea un timer que maneja la velocidad a la que se maneja la serpiente
        elapsed_time_list = []
        elapsed_time = time.time() - start_time
        if elapsed_time > time_limit:
            time_limit += 0.27
            elapsed_time_list.append(1)
        
        # Si la lista de colisiones entre la cola y la cabeza devuelve 'True' se llama a la función 'game_over'
        if tails_collide_list:
            time_limit = 0
            return game_over()
        
        # Si se unpausea el juego, se le suma al time_limit todo el tiempo que perdió en la pausa.
        # De este modo es como si el timer comenzara de 0.
        if pause == False:
            time_limit += elapsed_time - time_limit
            pause = True
        
        # Separa a los boleanos previamente creados y los lleva con sus funciones, al ritmo que se añaden enteros a la lista de tiempo
        for e in elapsed_time_list:
            if snake_up_bool == True:
                update_snake_position(0, -1)   
            elif snake_down_bool == True:
                update_snake_position(0, 1)      
            elif snake_left_bool == True:   
                update_snake_position(-1, 0)       
            elif snake_right_bool == True:
                update_snake_position(1, 0)   

            # Por cada cola en la lista de colas se actualiza la posición de las colas
            for tail in tail_list_count:
                update_tail_position()

        # Se dibuja el fondo por pantalla        
        screen.blit(play_game_background, (0, 0))
        
        # Si la snake toca algun borde se llama a la función 'game_over'
        if snake.rect.x < 0 or snake.rect.x > 870:
            elapsed_time = 0
            time_limit = 0
            return game_over()
        if snake.rect.y < 0 or snake.rect.y > 670:
            elapsed_time = 0
            time_limit = 0
            return game_over()
        
        # Se Muetran por pantalla todos los sprites en la lista de sprites
        all_sprites_list.update()
        all_sprites_list.draw(screen)        

        screen.blit(text1, (560, 10))

        pygame.display.flip()
        clock.tick(30)
        
# Función que no se usa en el juego en sí, sin embargo fue utilizada en la creación
# para visualizar mejor el movimiento de la snake. Crea una grilla de 30x30 pixeles.
def draw_grid():
    
    for i in range(0, width, row):
        pygame.draw.line(screen, WHITE, (i, 0), (i, height))
        
    for j in range(0, height, col):
        pygame.draw.line(screen, WHITE, (0, j), (width, j))
        
# Actualiza la posicion de la snake
def update_snake_position(update_x, update_y):
        snake.rect.x += update_x * row
        snake.rect.y += update_y * col
        
# Actualiza la posicion de cada cola leyendo la posición anterior de la cola de enfrente.
def update_tail_position():
    first_tail.update_with_position(snake.previous_x, snake.previous_y)
    for tail1, tail2 in zip(all_tails[:-1], all_tails[1:]):
        tail2.update_with_position(tail1.previous_x, tail1.previous_y)
           
# Crea una nueva cola
def add_new_tail():
    last_tail = all_tails[-1]
    new_tail = Tail(last_tail.previous_x, last_tail.previous_y, [first_tail.rect.x, first_tail.rect.y]) 
    all_tails.append(new_tail)
    all_sprites_list.add(new_tail)
    tails_hit_list.add(new_tail)

# Funcion que crea los puntos y los añade a la lista de todos los sprites
def create_point():
    global first_tail
    global new_tail
    
    pos_point_x = random.choice(x_pos_point_list) 
    pos_point_y = random.choice(y_pos_point_list)
    point = Points()
    point.pos(pos_point_x, pos_point_y)
    point_collide_list_tails = pygame.sprite.spritecollide(point, tails_hit_list, False)
    point_collide_list_snake = pygame.sprite.spritecollide(snake, point_list, False)
    if point_collide_list_tails or point_collide_list_snake == True:
        create_point()
    else:
        all_sprites_list.add(point)
        point_list.add(point)
        point_list_count.append(1)
    
# Pantalla del Game Over
def game_over():
    snake.rect.x = 450
    snake.rect.y = 330
    
    # Textos
    font = pygame.font.SysFont("Comic", 150, bold = True)
    font2 = pygame.font.SysFont("Comic", 60, bold = True) 
    font3 = pygame.font.SysFont("Comic", 50, bold = True) 
    text1 = font.render('GAME OVER', True, WHITE)
    text2 = font2.render("PRESS 'R' TO RESTART", True, WHITE)
    text3 = font3.render("PRESS 'Q' TO QUIT TO MAIN MENU", True, WHITE)
    
    # Resetea la orientacion de la cabeza hacia la izquierda
    snake.image = pygame.image.load("images/head_snake.png")
    
    game_over = True
    
    # Bucle principal de la función
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            # Si se aprieta 'r' se llama a la función 'play_game'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    all_sprites_list.empty()
                    tails_hit_list.empty()
                    all_tails.clear()
                    all_sprites_list.add(snake)
                    all_sprites_list.add(first_tail)
                    all_tails.append(first_tail)
                    point_list_count.clear()
                    play_game()
            
            # Si se aprieta la 'q' se llama a la función 'main_menu'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    all_sprites_list.empty()
                    tails_hit_list.empty()
                    all_tails.clear()
                    all_sprites_list.add(snake)
                    all_sprites_list.add(first_tail)
                    all_tails.append(first_tail)
                    point_list_count.clear()
                    main_menu()
        
        # Se dibujan los textos por pantalla
        screen.blit(text1, (75, 170)) 
        screen.blit(text2, (170, 370)) 
        screen.blit(text3, (100, 450)) 
        
        pygame.display.flip()
        clock.tick(60)

# Menú de pausa    
def pause_menu():
    global pause
    
    # Bucle principal
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            # Si se aprieta la 'p' se sale del bucle y vuelve al juego
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
                
        pygame.display.flip()
        clock.tick(30) 

main_menu()

