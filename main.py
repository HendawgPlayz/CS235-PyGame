import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# rand_obj = pygame.Rect(())

class PlayerClass:
    def __init__(self, x, y, direction, sprite_sheet):
        self.x = x
        self.y = y
        self.direction = direction
        self.sprites = []
        self.sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()
        print("Sprite sheet size:", self.sprite_sheet.get_size())

        self.sprite_dir = \
        {
            "up": self.sprite_sheet.subsurface(pygame.Rect(0, 0, 32, 32)),
            "right": self.sprite_sheet.subsurface(pygame.Rect(32, 0, 32, 32)),
            "down": self.sprite_sheet.subsurface(pygame.Rect(0, 32, 32, 32)),
            "left": self.sprite_sheet.subsurface(pygame.Rect(32, 32, 32, 32))
        }

    def up(self):
        self.direction = "up"
        self.y -= 1
    def down(self):
        self.direction = "down"
        self.y += 1
    def left(self):
        self.direction = "left"
        self.x -= 1
    def right(self):
        self.direction = "right"
        self.x += 1

    def draw(self, game_screen):
        game_screen.blit(self.sprite_dir[self.direction], (self.x, self.y))

player = PlayerClass(0, 0, "down", "art_Assets/Improved_Sprite_Sheet copy.png")

run = True
while run:

    screen.fill((100, 100, 100))
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        player.left()
    elif key[pygame.K_s]:
        player.down()
    elif key[pygame.K_d]:
        player.right()
    elif key[pygame.K_w]:
        player.up()


    # pygame.draw.rect(screen, (255, 0, 0), rand_obj)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # pygame.draw.rect(screen, (255, 0, 0), (0, 0, 32, 32))
    player.draw(screen)
    pygame.display.update()

pygame.quit()