import pygame
import pygame_menu
import random
import os
import sys
import database
import parameters
import resources
import adventure


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Snake game')


def current_score(score: int) -> None:
    value = parameters.score_font.render(f'Score: {score}', True, parameters.colors('yellow'))
    parameters.dis.blit(value, [10, 10])


def final_score(score: int) -> None:
    value = parameters.score_font.render(f'Your score: {score}', True, parameters.colors('yellow'))
    parameters.dis.blit(value, value.get_rect(center=(parameters.dis_width // 2, parameters.dis_height // 2)))


def snake(snake_list: list[tuple[tuple[int, int], str]]) -> None:
    parameters.dis.blit(resources.snake_head[snake_list[-1][1]], (snake_list[-1][0][0], snake_list[-1][0][1]))
    condition = snake_list[-1][1]

    if len(snake_list) > 2:
        for x in snake_list[-2:0:-1]:
            if x[1] == condition:
                parameters.dis.blit(resources.snake_body[x[1]], (x[0][0], x[0][1]))
            else:
                parameters.dis.blit(resources.snake_body[f'{x[1]}_to_{condition}'], (x[0][0], x[0][1]))
            condition = x[1]

    if len(snake_list) != 1:
        parameters.dis.blit(resources.snake_tail[condition], (snake_list[0][0][0], snake_list[0][0][1]))


def message(msg: str, color: tuple[int, int, int], font: pygame.font = parameters.font_style,
            x: int = parameters.dis_width // 2, y: int = parameters.dis_height // 2) -> None:
    msg = font.render(msg, True, color)
    parameters.dis.blit(msg, msg.get_rect(center=(x, y)))


def hint() -> None:
    msg_1 = parameters.score_font.render('Use', True, parameters.colors('blue'))
    msg_2 = parameters.score_font.render('to move', True, parameters.colors('blue'))

    parameters.dis.blit(msg_1, (parameters.dis_width // 2 - 230, 450))
    parameters.dis.blit(resources.arrow, (parameters.dis_width // 2 - 130, 460))
    parameters.dis.blit(pygame.transform.rotate(resources.arrow, 270), (parameters.dis_width // 2 - 90, 460))
    parameters.dis.blit(pygame.transform.rotate(resources.arrow, 90), (parameters.dis_width // 2 - 50, 460))
    parameters.dis.blit(pygame.transform.rotate(resources.arrow, 180), (parameters.dis_width // 2 - 10, 460))
    parameters.dis.blit(msg_2, (parameters.dis_width // 2 + 60, 450))


def save_score(score: int) -> None:
    with open('score.save', 'a') as file:
        file.write(f'{parameters.difficulty}\xa0{parameters.nickname}\xa0{score}\n')


def update_score() -> None:
    if 'score.save' not in os.listdir():
        return
    with open('score.save', 'r') as file:
        new_score = file.read().split('\n')[:-1]
    os.remove('score.save')
    data = database.read_data()

    for score in new_score:
        value = int(score.split('\xa0')[2])
        dif = score.split('\xa0')[0]
        if int(value) >= data[dif][9][1]:
            i = 1
            while value >= data[dif][9 - i][1] and i < 10:
                i += 1
            data[dif].insert(10 - i, (score.split('\xa0')[1], value))
            data[dif].pop()
    database.write_data(data)


def set_difficulty(diff: tuple[tuple[str, int], int], speed: int) -> None:
    parameters.snake_speed = speed
    parameters.difficulty = diff[0][0]


def set_nickname(name: str) -> None:
    parameters.nickname = name


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
                level.add.button(f'Level {i + 1}', adventure.levels[f'level_{i + 1}'], menu, f'level_{i + 1}.map')
            else:
                break
    else:
        level.add.button('Level 1', adventure.levels['level_1'], menu, 'level_1.map')
    menu._open(level)


def map_render(map_name: str) -> list[tuple[int, int]]:
    """Отрисовка ландшафта загружаемой карты и возврат списка координат всех объектов"""
    with open(map_name, 'r') as file:
        coordinates = []
        _settings = file.readline()
        for line in file.readlines():
            color, line = line.split('|')[0], line.split('|')[1].split(', ')
            for coordinate in line:
                coordinates.append((int(coordinate.split()[0]), int(coordinate.split()[1])))
                pygame.draw.rect(parameters.dis, parameters.colors(color), [coordinates[-1][0], coordinates[-1][1],
                                                                            parameters.snake_block,
                                                                            parameters.snake_block])
    return coordinates


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
    settings.add.button('Snake skins', snake_skins, menu)

    menu._open(settings)


def snake_skins(menu: pygame_menu.Menu) -> None:
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

    skins.add.label('In order for the changes to take effect,', underline=True)  # Сделать атоматический рестарт
    skins.add.label('game will be restarted', margin=(0, 40), underline=True)
    label = skins.add.label(f'Current skin: {resources.snake_skin}')
    skins.add.button('Classic', swap_skin, 'classic')
    skins.add.button('Red', swap_skin, 'red')
    skins.add.button('Green', swap_skin, 'green')

    menu._open(skins)


def menu_loop() -> None:
    def back_to_menu() -> None:
        if parameters.change is True:
            parameters.change = False
            os.execv(sys.executable, [sys.executable] + sys.argv)  # завершает работу вместо повторного запуска в pycharm
        pygame.display.set_mode((parameters.menu_width, parameters.menu_height))  # Вернуть меню в центр экрана

    surface = pygame.display.set_mode((parameters.menu_width, parameters.menu_height))
    menu = pygame_menu.Menu('Welcome', parameters.menu_width, parameters.menu_height,
                            theme=pygame_menu.themes.THEME_SOLARIZED, onreset=back_to_menu)
    menu.add.text_input('Name: ', default='default', maxchar=20, onchange=set_nickname)
    menu.add.button('Play', classic_game_loop, menu)
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


def classic_game_loop(menu: pygame_menu.Menu, level: str = 'classic.map') -> None:
    pygame.display.set_mode((parameters.dis_width, parameters.dis_height))

    snake_x = parameters.dis_width // 2 // parameters.snake_block * parameters.snake_block
    snake_y = parameters.dis_height // 2 // parameters.snake_block * parameters.snake_block

    snake_x_change = 0
    snake_y_change = 0
    condition = 'up'

    snake_list: list[tuple[tuple[int, int], str]] = []
    snake_length = 1

    food_x = round(random.randrange(0, parameters.dis_width - parameters.snake_block) /
                   parameters.snake_block + 0.0) * parameters.snake_block
    food_y = round(random.randrange(0, parameters.dis_height - parameters.snake_block) /
                   parameters.snake_block + 0.0) * parameters.snake_block

    game_over = False
    game_close = False
    key_is_used = False

    while not game_over:
        while game_close:
            parameters.dis.blit(resources.background, (0, 0))
            message('You lost! Press Q to quit or C to play again...', parameters.colors('orange'), y=300)

            final_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_q:
                            save_score(snake_length - 1)
                            pygame.display.set_mode((parameters.menu_width, parameters.menu_height))
                            return
                        case pygame.K_c:
                            save_score(snake_length - 1)
                            classic_game_loop(menu)
                            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                menu.disable()

            if event.type == pygame.KEYDOWN and not key_is_used:
                match event.key:
                    case pygame.K_LEFT:
                        if snake_x_change != parameters.snake_block:
                            snake_x_change = -parameters.snake_block
                            condition = 'left'
                        snake_y_change = 0
                    case pygame.K_RIGHT:
                        if snake_x_change != -parameters.snake_block:
                            snake_x_change = parameters.snake_block
                            condition = 'right'
                        snake_y_change = 0
                    case pygame.K_DOWN:
                        snake_x_change = 0
                        if snake_y_change != -parameters.snake_block:
                            snake_y_change = parameters.snake_block
                            condition = 'down'
                    case pygame.K_UP:
                        snake_x_change = 0
                        if snake_y_change != parameters.snake_block:
                            snake_y_change = -parameters.snake_block
                            condition = 'up'
                key_is_used = True

        parameters.dis.blit(resources.background, (0, 0))
        obstacle = map_render(f'resources\\levels\\{level}')

        if snake_x_change == snake_y_change == 0:
            hint()

        while (food_x, food_y) in obstacle + [block[0] for block in snake_list]:
            food_x = round(random.randrange(0, parameters.dis_width - parameters.snake_block) /
                           parameters.snake_block + 0.0) * parameters.snake_block
            food_y = round(random.randrange(0, parameters.dis_height - parameters.snake_block) /
                           parameters.snake_block + 0.0) * parameters.snake_block

        snake_x += snake_x_change
        snake_y += snake_y_change

        if snake_x >= parameters.dis_width or snake_x < 0 or snake_y >= parameters.dis_height or snake_y < 0:
            game_close = True

        parameters.dis.blit(resources.apple_picture, (food_x, food_y))

        snake_head = (snake_x, snake_y)
        snake_list.append((snake_head, condition))

        if len(snake_list) > snake_length:
            del snake_list[0]

        if snake_head in obstacle + [block[0] for block in snake_list[:-1]]:
            game_close = True

        current_score(len(snake_list) - 1)
        snake(snake_list)

        pygame.display.update()
        print(snake_list)

        if snake_x == food_x and snake_y == food_y:
            resources.apple_sound.play()
            snake_length += 1

        parameters.clock.tick(parameters.snake_speed)
        key_is_used = False


if __name__ == '__main__':
    menu_loop()
    update_score()
