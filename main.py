import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

class PlayerClass:
    def __init__(self, x, y, direction, sprite_sheet):
        self.x = x
        self.y = y
        self.speed = 200
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = direction
        self.sprites = []
        self.sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()

        self.sprite_dir = \
        {
            "up": self.sprite_sheet.subsurface(pygame.Rect(0, 0, 32, 32)),
            "right": self.sprite_sheet.subsurface(pygame.Rect(32, 0, 32, 32)),
            "down": self.sprite_sheet.subsurface(pygame.Rect(0, 32, 32, 32)),
            "left": self.sprite_sheet.subsurface(pygame.Rect(32, 32, 32, 32))
        }

        scale_factor = 2.2

        for direction in self.sprite_dir:
            original = self.sprite_dir[direction]
            scaled = pygame.transform.scale(original, (32 * scale_factor, 32 * scale_factor))
            self.sprite_dir[direction] = scaled



    def update(self, _delta_time):
        self.x += self.velocity_x * self.speed * delta_time
        self.y += self.velocity_y * self.speed * delta_time

    def up(self):
        self.direction = "up"
        self.velocity_y = -1
    def down(self):
        self.direction = "down"
        self.velocity_y = 1
    def left(self):
        self.direction = "left"
        self.velocity_x = -1
    def right(self):
        self.direction = "right"
        self.velocity_x = 1

    def draw(self, game_screen):
        game_screen.blit(self.sprite_dir[self.direction], (self.x, self.y))

player = PlayerClass(0, 0, "down", "art_Assets/Improved_Sprite_Sheet copy.png")

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