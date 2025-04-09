import pygame

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
        self.x += self.velocity_x * self.speed * _delta_time
        self.y += self.velocity_y * self.speed * _delta_time

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