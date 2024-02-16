import pygame
import pygame_menu
import parameters
import resources


pygame.init()


def level_1(menu: pygame_menu.Menu, level: str) -> None:
    print('level 1')


def level_2(menu: pygame_menu.Menu, level: str) -> None:
    print('level 2')


levels = {
    'level_1': level_1,
    'level_2': level_2,
}
