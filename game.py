import pygame
import time
import os
import functions
import parameters
import resources


def game_loop(menu, level: str = 'classic.map', snake_class=functions.Snake, food_class=functions.Food) -> None:
    pygame.display.set_mode((parameters.dis_width, parameters.dis_height))

    snake = snake_class(coordinates=(parameters.dis_width // 2 // parameters.snake_block * parameters.snake_block,
                                     parameters.dis_height // 2 // parameters.snake_block * parameters.snake_block))

    food = food_class(snake.body)

    game_over = False
    game_close = False
    win = False
    key_is_used = False

    while not game_over:
        while game_close or win:
            parameters.dis.blit(resources.background, (0, 0))
            if win:
                functions.message('You won! Press Q to quit or C to go to next level...',
                                  parameters.colors('orange'), y=300)
            else:
                functions.message('You lost! Press Q to quit or C to play again...', parameters.colors('orange'), y=300)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_q:
                            pygame.display.set_mode((parameters.menu_width, parameters.menu_height))
                            return
                        case pygame.K_c:
                            if win:
                                parameters.dis.blit(resources.background, (0, 0))
                                if f'level_{int(level[-5]) + 1}.map' in os.listdir('resources\\levels'):
                                    game_loop(menu, f'level_{int(level[-5]) + 1}.map', snake_class,
                                              food_class)  # ВКЛЮЧИТЬ СЛЕДУЮЩИЙ УРОВЕНЬ, запомнить, что уровень пройден
                                else:
                                    functions.message('Congratulation! You beat all levels!',
                                                      parameters.colors('orange'), y=300)
                                    pygame.display.update()
                                    time.sleep(3)
                                    pygame.display.set_mode((parameters.menu_width, parameters.menu_height))
                                    return
                            else:
                                game_loop(menu)
                            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                menu.disable()

            if event.type == pygame.KEYDOWN and not key_is_used:
                match event.key:
                    case pygame.K_LEFT:
                        snake.speed[1] = 0
                        if snake.speed[0] != parameters.snake_block:
                            snake.speed[0] = -parameters.snake_block
                            snake.condition = 'left'
                    case pygame.K_RIGHT:
                        snake.speed[1] = 0
                        if snake.speed[0] != -parameters.snake_block:
                            snake.speed[0] = parameters.snake_block
                            snake.condition = 'right'
                    case pygame.K_DOWN:
                        snake.speed[0] = 0
                        if snake.speed[1] != -parameters.snake_block:
                            snake.speed[1] = parameters.snake_block
                            snake.condition = 'down'
                    case pygame.K_UP:
                        snake.speed[0] = 0
                        if snake.speed[1] != parameters.snake_block:
                            snake.speed[1] = -parameters.snake_block
                            snake.condition = 'up'
                key_is_used = True

        parameters.dis.blit(resources.background, (0, 0))
        obstacle = functions.map_render(f'resources\\levels\\{level}')

        snake.rules()

        snake.tick(food.current_food)
        food.current_food = food.get_food(obstacle + [block[0] for block in snake.body])
        game_close = snake.crash(obstacle)

        if type(food.current_food) is tuple:
            parameters.dis.blit(resources.apple_picture, food.current_food)
        else:
            for f in food.current_food:
                parameters.dis.blit(resources.apple_picture, f)

        snake.get_current_score(snake.length - 1)
        snake.draw_snake()

        pygame.display.update()
        win = snake.win_condition()
        # print(snake.body)

        snake.clock_tick()
        key_is_used = False
