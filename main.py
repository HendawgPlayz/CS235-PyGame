import pygame
from player_class import PlayerClass

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

player = PlayerClass(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, "down", "art_Assets/Improved_Sprite_Sheet copy.png")
background = pygame.image.load("art_Assets/GameBackground.png").convert()

camera_x = 0
camera_y = 0

collision_objects = \
[ # x, y, width, height
    pygame.Rect(20, 25, 10, 950),   # left wall
    pygame.Rect(1500, 25, 10, 950), # right wall
    pygame.Rect(250, 20, 950, 10), # top wall
    pygame.Rect(1500, 25, 10, 950), # bottom wall
    pygame.Rect(600, 800, 64, 64),
]

run = True
while run:

    camera_x = player.x - SCREEN_WIDTH // 2
    camera_y = player.y - SCREEN_HEIGHT // 2
    delta_time = clock.tick(60) / 1000

    screen.blit(background, (-camera_x, -camera_y))

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
    player.update(delta_time, collision_objects)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    player.draw(screen, camera_x, camera_y)
    for wall in collision_objects:
        pygame.draw.rect(screen, (255, 0, 0), (
            wall.x - camera_x, wall.y - camera_y, wall.width, wall.height
        ), 2)
    pygame.display.update()

pygame.quit()