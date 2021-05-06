import pygame

# Colores
WHITE = (255, 255, 255)
YELLOW = (247, 195, 47)
TRAS = (0, 0, 0, 0)
BLACK = (0, 0, 0)
LIME = (0, 255, 0)

# Variables globales
width = 900
height = 700
size = (width, height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Snake")
row = col = 30
gridwidth = width // row
gridheight = height // col

# Variables globales de la snake
speed_snake_x = 15
speed_snake_y = 11
time_limit = 0.27
tail_list = []
tail_pos_x = 0
tail_pos_y = 0

# Variables de los puntos
x_pos_point_list = list(range(29))
y_pos_point_list = list(range(22))
point_hit_list = []
point_list_count = []
point_list = pygame.sprite.Group()

# Variable del pause_menu
pause = True

# Imagenes
background = pygame.image.load("Snake_background.png")
play_game_background = pygame.image.load("play_background.png")
titulo_snake = pygame.image.load("Titulo_Snake.png")
titulo_snake.set_colorkey(YELLOW)
play_button = pygame.image.load("Play_Button.png")
play_button = pygame.transform.scale(play_button, (300, 120))
press_play_button = pygame.image.load("Press_Play_Button.png")
press_play_button = pygame.transform.scale(press_play_button, (300, 120))
quit_button = pygame.image.load("Quit_Button.png")
quit_button = pygame.transform.scale(quit_button, (250, 120))
press_quit_button = pygame.image.load("Press_Quit_Button.png")
press_quit_button = pygame.transform.scale(press_quit_button, (250, 120))
sound_button = pygame.image.load("sound_button.png")
sound_button = pygame.transform.scale(sound_button, (60, 60))
canceled_sound_button = pygame.image.load("canceled_sound_button.png")
canceled_sound_button = pygame.transform.scale(canceled_sound_button, (60, 60))
