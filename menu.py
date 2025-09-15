import pygame
import pygame_menu
import os
import sys
import parameters
import resources
import database
import adventure
from functions import set_difficulty, update_score, set_nickname
from game import game_loop


def menu_loop() -> None:
    def back_to_menu() -> None:
        if parameters.change is True:
            parameters.change = False
            os.execv(sys.executable, [sys.executable] + sys.argv)
        pygame.display.set_mode((parameters.menu_width, parameters.menu_height))  # Вернуть меню в центр экрана

    surface = pygame.display.set_mode((parameters.menu_width, parameters.menu_height))
    menu = pygame_menu.Menu('Welcome', parameters.menu_width, parameters.menu_height,
                            theme=pygame_menu.themes.THEME_SOLARIZED, onreset=back_to_menu)
    menu.add.text_input('Name: ', default='default', maxchar=20, onchange=set_nickname)
    menu.add.button('Play', game_loop, menu)
    menu.add.button('Adventure', select_level, menu)
    menu.add.button('Difficulty', level_menu, menu)
    menu.add.button('Leader board', leaderboard_menu, menu)
    menu.add.button('Settings', settings_menu, menu)
    menu.add.button('Close', menu.disable)

    menu.mainloop(surface)

    while menu.is_enabled():
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                menu.disable()
        if menu.enable():
            menu.update(events)
            menu.draw(surface)
            if menu.get_current().get_selected_widget():  # Не выделяется текущий виджет
                parameters.arrow.draw(surface, menu.get_current().get_selected_widget())

        pygame.display.update()


def select_level(menu: pygame_menu.Menu) -> None:
    adventure_data = {}
    with open('resources\\saves\\adventure.save', 'r') as file:
        _structure_of_file = file.readline()
        for line in file.readlines():
            adventure_data[line.split('|')[0]] = int(line.split('|')[1])

    level = pygame_menu.Menu('Select level', parameters.menu_width, parameters.menu_height,
                             theme=pygame_menu.themes.THEME_SOLARIZED)
    if parameters.nickname in adventure_data.keys():
        for i in range(adventure_data[parameters.nickname]):
            if f'level_{i + 1}.map' in os.listdir('resources\\levels'):
                level.add.button(f'Level {i + 1}', adventure.levels[f'level_{i + 1}'], menu)
            else:
                break
    else:
        level.add.button('Level 1', adventure.levels['level_1'], menu)
    menu._open(level)


def level_menu(menu: pygame_menu.Menu) -> None:
    level = pygame_menu.Menu('Select a Difficulty', parameters.menu_width, parameters.menu_height,
                             theme=pygame_menu.themes.THEME_SOLARIZED)
    level.add.selector('Difficulty level: ', [('Normal', 13), ('Hard', 18), ('Hell', 23), ('Challenge', 30),
                                              ('Very easy', 5), ('Easy', 9)],
                       onchange=set_difficulty)
    menu._open(level)


def leaderboard_menu(menu: pygame_menu.Menu) -> None:
    def change_difficulty(diff: tuple, *_: any) -> None:
        current_diff = diff[0][0]
        i = 0
        for new_item in data[current_diff]:
            labels[i].set_title(f'{i + 1}. {new_item[0]}: {new_item[1]}')
            i += 1

    update_score()
    data = database.read_data()
    pygame.display.set_mode((parameters.leaderboard_width, parameters.leaderboard_height))
    board = pygame_menu.Menu('Leader board', parameters.leaderboard_width, parameters.leaderboard_height,
                             theme=pygame_menu.themes.THEME_SOLARIZED)
    board.add.selector('Difficulty: ', [(key, 1) for key in data.keys()], onchange=change_difficulty)

    labels = []
    num = 1
    for item in data[parameters.difficulty]:
        labels.append(board.add.label(f'{num}. {item[0]}: {item[1]}', align=pygame_menu.locals.ALIGN_LEFT))
        num += 1
    menu._open(board)


def settings_menu(menu: pygame_menu.Menu) -> None:
    settings = pygame_menu.Menu('Settings', parameters.menu_width, parameters.menu_height,
                                theme=pygame_menu.themes.THEME_SOLARIZED)
    settings.add.button('Snake skins', skins_menu, menu)

    menu._open(settings)


def skins_menu(menu: pygame_menu.Menu) -> None:  # Сделать подменю в settings?
    def swap_skin(new_skin):
        with open('resources\\users_settings', 'r') as us:
            file = us.read().replace(f'snake_skin: {resources.snake_skin}', f'snake_skin: {new_skin}')
        with open('resources\\users_settings', 'w') as us:
            us.write(file)
        label.set_title(f'Current skin: {new_skin}')
        resources.snake_skin = new_skin
        parameters.change = True

    skins = pygame_menu.Menu('Snake skins', parameters.menu_width, parameters.menu_height,
                             theme=pygame_menu.themes.THEME_SOLARIZED)

    skins.add.label('In order for the changes to take effect,', underline=True)
    skins.add.label('game will be restarted', margin=(0, 40), underline=True)
    label = skins.add.label(f'Current skin: {resources.snake_skin}')
    skins.add.button('Classic', swap_skin, 'classic')
    skins.add.button('Red', swap_skin, 'red')
    skins.add.button('Green', swap_skin, 'green')

    menu._open(skins)
