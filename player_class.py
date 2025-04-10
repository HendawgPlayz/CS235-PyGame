import pygame

class PlayerClass:
    def __init__(self, x, y, direction, sprite_sheet):
        self.x = x
        self.y = y
        self.speed = 300
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
        scale_factor = 4

        for direction in self.sprite_dir:
            original = self.sprite_dir[direction]
            scaled = pygame.transform.scale(original, (32 * scale_factor, 32 * scale_factor))
            self.sprite_dir[direction] = scaled


    def update(self, _delta_time, walls):
        # Saves original position in the event that there is collision
        old_x = self.x
        old_y = self.y

        # Tries movement
        self.x += self.velocity_x * self.speed * _delta_time
        self.y += self.velocity_y * self.speed * _delta_time

        sprite = self.sprite_dir[self.direction]
        player_hitbox = pygame.Rect(self.x - sprite.get_width() // 2,
                                    self.y - sprite.get_height() // 2,
                                    sprite.get_width(),
                                    sprite.get_height())

        for wall in walls:
            if player_hitbox.colliderect(wall):
                # Undoes movement
                self.x = old_x
                self.y = old_y
                break

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

    def draw(self, game_screen, cam_x, cam_y):
        sprite = self.sprite_dir[self.direction]
        game_screen.blit(sprite, (
            self.x - cam_x - sprite.get_width() // 2,
            self.y - cam_y - sprite.get_height() // 2
        ))