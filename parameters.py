import pygame
import pygame_menu


def colors(color: str) -> tuple[int, int, int]:
    colors_list = {
        'red': (255, 0, 0),
        'orange': (255, 165, 0),
        'yellow': (255, 255, 0),
        'green': (0, 128, 0),
        'blue': (0, 0, 255),
        'indigo': (75, 0, 130),
        'violet': (127, 0, 255),
        'white': (255, 255, 255),
        'gray': (128, 128, 128),
        'black': (0, 0, 0),
    }
    return colors_list[color]


pygame.init()


users_settings = {}
change = False

with open('resources\\users_settings', 'r') as us:
    settings = us.read().split('\n')

for string in settings:
    string = string.split(': ')
    users_settings[string[0]] = string[1]


dis_width = 1020
dis_height = 750
menu_width = 750
menu_height = 500
leaderboard_width = 750
leaderboard_height = 650

snake_block = 30
snake_speed = 13
difficulty = 'Normal'
nickname = 'default'

arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10, 15))

font_style = pygame.font.SysFont('bahnschrift', 30)
score_font = pygame.font.SysFont('comicsansms', 50)

dis = pygame.display.set_mode([dis_width, dis_height])

clock = pygame.time.Clock()
