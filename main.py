import pygame # 5 hour in
from character_classing import PlayerClass, BulletClass, EnemyClass

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

player = PlayerClass(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, "down", "art_Assets/Improved_Sprite_Sheet copy.png")
background = pygame.image.load("art_Assets/GameBackground.png").convert()


camera_x = 0
camera_y = 0
wave_timer = 0
wave_interval = 3

player_collision_objects = \
[ # x, y, width, height
    pygame.Rect(20, 25, 10, 950),   # left wall
    pygame.Rect(1500, 25, 10, 950), # right wall
    pygame.Rect(30, 180, 1500, 10), # top wall
    pygame.Rect(30, 850, 1500, 10), # bottom wall
    pygame.Rect(935, 335, 10, 125), # left bathroom wall
    pygame.Rect(975, 380, 140, 10), # bottom bathroom wall
    pygame.Rect(975, 425, 140, 10), # bedroom top wall
    pygame.Rect(1275, 380, 140, 10), # bottom bathroom right wall
    pygame.Rect(1275, 445, 140, 10), # bedroom right top wall
    pygame.Rect(935, 720, 10, 230), # kitchen wall
    pygame.Rect(550, 480, 10, 400), # Kitch left wall
    pygame.Rect(470, 480, 10, 400), # odd wall
    pygame.Rect(420, 480, 10, 100), # odd wall 2
    pygame.Rect(110, 480, 10, 100), # odd wall 3
    pygame.Rect(600, 760, 150, 64), # Kitchen stove
    pygame.Rect(110, 330, 30, 15),  # Living room table
]

enemy_collision_objects = \
[ # x, y, width, height
    pygame.Rect(20, 25, 10, 950),   # left wall
    pygame.Rect(1500, 25, 10, 950), # right wall
    pygame.Rect(30, 40, 1500, 10), # top wall
    pygame.Rect(30, 1000, 1500, 10), # bottom wall
    # pygame.Rect(935, 335, 10, 125), # left bathroom wall
    # pygame.Rect(975, 380, 140, 10), # bottom bathroom wall
    # pygame.Rect(975, 425, 140, 10), # bedroom top wall
    # pygame.Rect(1275, 380, 140, 10), # bottom bathroom right wall
    # pygame.Rect(1275, 445, 140, 10), # bedroom right top wall
    # pygame.Rect(935, 720, 10, 230), # kitchen wall
    # pygame.Rect(550, 480, 10, 400), # Kitch left wall
    # pygame.Rect(470, 480, 10, 400), # odd wall
    # pygame.Rect(420, 480, 10, 100), # odd wall 2
    # pygame.Rect(110, 480, 10, 100), # odd wall 3
    # pygame.Rect(600, 760, 150, 64), # Kitchen stove
    # pygame.Rect(110, 330, 30, 15),  # Living room table
]

bullets = []

enemies = []

enemy_queue = []

run = True
while run:

    camera_x = player.x - SCREEN_WIDTH // 2
    camera_y = player.y - SCREEN_HEIGHT // 2
    delta_time = clock.tick(60) / 1000
    wave_timer += delta_time

    if wave_timer >= wave_interval:
        for i in range(3):
            enemy_queue.append(i)
        wave_timer = 0

    if player.time_since_last_enemy >= player.enemy_cooldown and len(enemy_queue) > 0:
        enemy = EnemyClass(650, 150, "down", "art_Assets/Enemy_SpriteSheet.png", player)
        enemies.append(enemy)
        enemy_queue.pop()
        player.time_since_last_enemy = 0


    player.velocity_x = 0
    player.velocity_y = 0

    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        player.left()
    if key[pygame.K_s]:
        player.down()
    if key[pygame.K_d]:
        player.right()
    if key[pygame.K_w]:
        player.up()
    if key[pygame.K_SPACE] and player.can_shoot() and player.ammo > 0:
        bullet = BulletClass(player.x, player.y, player.direction)
        bullets.append(bullet)
        player.time_since_last_shot = 0
        player.ammo -= 1

    player.update(delta_time, player_collision_objects)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # DRAWING #

    screen.fill((0,0,0))
    screen.blit(background, (-camera_x, -camera_y))

    for bul_round in bullets[:]:
        for enemy in enemies[:]:
            if enemy.get_hitbox().colliderect(bul_round.get_hitbox()):
                enemies.remove(enemy)
        if bul_round.update(delta_time, player_collision_objects):
            bul_round.draw(screen, camera_x, camera_y)
        else:
            bullets.remove(bul_round)
    for enemy in enemies[:]:
        enemy.update(delta_time, enemy_collision_objects)
        enemy.draw(screen, camera_x, camera_y)
        if player.get_hitbox().colliderect(enemy.get_hitbox()) and player.can_be_damaged():
            player.health -= 1
            player.time_since_last_damage = 0
            if player.health <= 0:
                pygame.quit()


    player.draw(screen, camera_x, camera_y)
    player.draw_health(screen)
    player.draw_ammo(screen)

    # for wall in player_collision_objects: # Shows hit boxes
    #     pygame.draw.rect(screen, (255, 0, 0), (
    #         wall.x - camera_x, wall.y - camera_y, wall.width, wall.height
    #     ), 2)
    #
    # for wall in enemy_collision_objects: # Shows hit boxes
    #     pygame.draw.rect(screen, (0, 255, 0), (
    #         wall.x - camera_x, wall.y - camera_y, wall.width, wall.height
    #     ), 2)

    pygame.display.update()
pygame.quit()