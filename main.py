import pygame
from player_class import PlayerClass

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

player = PlayerClass(365, 230, "down", "art_Assets/Improved_Sprite_Sheet copy.png")

run = True
while run:

    screen.fill((100, 100, 100))
    delta_time = clock.tick(60) / 1000

    player.velocity_x = 0
    player.velocity_y = 0

    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        player.left()
    elif key[pygame.K_s]:
        player.down()
    elif key[pygame.K_d]:
        player.right()
    elif key[pygame.K_w]:
        player.up()

    player.update(delta_time)


    # pygame.draw.rect(screen, (255, 0, 0), rand_obj)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # pygame.draw.rect(screen, (255, 0, 0), (0, 0, 32, 32))
    player.draw(screen)
    pygame.display.update()

pygame.quit()