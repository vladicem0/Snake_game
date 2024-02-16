import pygame
import parameters


control_keys = parameters.users_settings['control_keys']
snake_skin = parameters.users_settings['snake_skin']
apple_skin = parameters.users_settings['apple_skin']
background_image = parameters.users_settings['background_image']


# ---------------------------------------------------IMAGES-------------------------------------------------------------
background = pygame.transform.scale((pygame.image.load(f'resources\\images\\background\\{background_image}'))
                                    .convert_alpha(),(parameters.dis_width, parameters.dis_height))

apple_picture = pygame.transform.scale((pygame.image.load(f'resources\\images\\food\\{apple_skin}')).convert_alpha(),
                                       (parameters.snake_block, parameters.snake_block))

arrow = pygame.transform.scale((pygame.image.load(f'resources\\images\\{control_keys}')).convert_alpha(),
                               (60, 60))

head = pygame.transform.scale((pygame.image.load(f'resources\\images\\snake\\{snake_skin}\\head.png')).convert_alpha(),
                              (parameters.snake_block, parameters.snake_block))
tail = pygame.transform.scale((pygame.image.load(f'resources\\images\\snake\\{snake_skin}\\tail.png')).convert_alpha(),
                              (parameters.snake_block, parameters.snake_block))
body = pygame.transform.scale((pygame.image.load(f'resources\\images\\snake\\{snake_skin}\\body.png')).convert_alpha(),
                              (parameters.snake_block, parameters.snake_block))
turning = pygame.transform.scale((pygame.image.load(f'resources\\images\\snake\\{snake_skin}\\turning.png'))
                                 .convert_alpha(), (parameters.snake_block, parameters.snake_block))

snake_head = {
    'up': head,
    'down': pygame.transform.rotate(head, 180),
    'right': pygame.transform.rotate(head, 270),
    'left': pygame.transform.rotate(head, 90),
}

snake_body = {
    'up': pygame.transform.rotate(body, 90),
    'down': pygame.transform.rotate(body, 270),
    'right': body,
    'left': pygame.transform.rotate(body, 180),
    'up_to_right': pygame.transform.rotate(turning, 180),
    'up_to_left': pygame.transform.rotate(turning, 90),
    'down_to_right': pygame.transform.rotate(turning, 270),
    'down_to_left': turning,
    'right_to_up': turning,
    'right_to_down': pygame.transform.rotate(turning, 90),
    'left_to_up': pygame.transform.rotate(turning, 270),
    'left_to_down': pygame.transform.rotate(turning, 180),
}

snake_tail = {
    'up': tail,
    'down': pygame.transform.rotate(tail, 180),
    'right': pygame.transform.rotate(tail, 270),
    'left': pygame.transform.rotate(tail, 90),
}

# ---------------------------------------------------SOUNDS-------------------------------------------------------------
apple_sound = pygame.mixer.Sound('resources\\sounds\\apple.wav')

# ---------------------------------------------------OTHERS-------------------------------------------------------------
