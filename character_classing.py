import pygame
pygame.font.init()
font = pygame.font.Font("art_Assets/PixelifySans-VariableFont_wght.ttf", 36)

class PlayerClass:
    def __init__(self, x, y, direction, sprite_sheet):
        self.x = x
        self.y = y
        self.speed = 450
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = direction
        self.time_since_last_shot = 0
        self.time_since_last_enemy = 0
        self.time_since_last_damage = 0
        self.enemy_cooldown = 1
        self.shot_cooldown = 0.2
        self.damage_cooldown = 1
        self.max_health = 3
        self.health = 3
        self.ammo = 20
        self.sprites = []
        self.sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()
        self.heart_image = pygame.image.load("art_Assets/heart_img.png").convert_alpha()

        self.sprite_dir = \
        {
            "up": self.sprite_sheet.subsurface(pygame.Rect(0, 0, 32, 32)),
            "right": self.sprite_sheet.subsurface(pygame.Rect(32, 0, 32, 32)),
            "down": self.sprite_sheet.subsurface(pygame.Rect(0, 32, 32, 32)),
            "left": self.sprite_sheet.subsurface(pygame.Rect(32, 32, 32, 32))
        }
        scale_factor = 4

        for direction in self.sprite_dir: # Scales sprite to preference
            original = self.sprite_dir[direction]
            scaled = pygame.transform.scale(original, (32 * scale_factor, 32 * scale_factor))
            self.sprite_dir[direction] = scaled

    def get_hitbox(self):
        sprite = self.sprite_dir[self.direction]
        player_hitbox = pygame.Rect(self.x - sprite.get_width() // 2,
                                    self.y - sprite.get_height() // 2,
                                    sprite.get_width(),
                                    sprite.get_height())
        return player_hitbox


    def update(self, _delta_time, walls):
        # Saves original position of char in the event that there is collision
        old_x = self.x
        old_y = self.y
        self.time_since_last_shot += _delta_time
        self.time_since_last_enemy += _delta_time
        self.time_since_last_damage += _delta_time

        # Tries movement
        self.x += self.velocity_x * self.speed * _delta_time
        self.y += self.velocity_y * self.speed * _delta_time

        player_hitbox = self.get_hitbox()

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

    def can_shoot(self):
        return self.time_since_last_shot >= self.shot_cooldown

    def enemy_can_spawn(self):
        return  self.time_since_last_enemy >= self.enemy_cooldown

    def can_be_damaged(self):
        return  self.time_since_last_damage >= self.damage_cooldown

    def draw_health(self, game_screen):
        for i in range(self.health):
            game_screen.blit(self.heart_image, (10 + i * 70, 10))

    def draw_ammo(self, game_screen):
        text = font.render(f"Ammo: {self.ammo}", True, (255, 255, 255))
        game_screen.blit(text, (10, 60))

    def draw(self, game_screen, cam_x, cam_y):
        sprite = self.sprite_dir[self.direction]
        game_screen.blit(sprite, (
            self.x - cam_x - sprite.get_width() // 2,
            self.y - cam_y - sprite.get_height() // 2
        ))

class BulletClass:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.speed = 1000
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = direction
        self.width = 8
        self.height = 8
        self.set_velocity()

    def set_velocity(self):
        if self.direction == "up":
            self.velocity_y = -1
        if self.direction == "down":
            self.velocity_y = 1
        if self.direction == "left":
            self.velocity_x = -1
        if self.direction == "right":
            self.velocity_x = 1

    def get_hitbox(self):
        bullet_hitbox = pygame.Rect(self.x - self.width // 2,
                                    self.y - self.height // 2,
                                    self.width,
                                    self.height)
        return bullet_hitbox

    def update(self, _delta_time, walls):
        # Saves original position of bullet in the event that there is collision
        old_x = self.x
        old_y = self.y

        # Tries movement
        self.x += self.velocity_x * self.speed * _delta_time
        self.y += self.velocity_y * self.speed * _delta_time

        bullet_hitbox = self.get_hitbox()

        for wall in walls:
            if bullet_hitbox.colliderect(wall):
                # Undoes movement
                self.x = old_x
                self.y = old_y
                return False # needs to be deleted
        return True

    def draw(self, game_screen, cam_x, cam_y):
        pygame.draw.circle(game_screen, (255, 225, 0), (self.x - cam_x, self.y - cam_y), 4)

class EnemyClass(PlayerClass):
    def __init__(self, x, y, direction, sprite_sheet, player):
       super().__init__(x, y, direction, sprite_sheet)
       self.speed = 100
       self.player = player
       self.sprite_dir = \
           {
               "up": self.sprite_sheet.subsurface(pygame.Rect(0, 0, 63, 63)),
               "down": self.sprite_sheet.subsurface(pygame.Rect(63, 0, 63, 63)),
               "left": self.sprite_sheet.subsurface(pygame.Rect(0, 63, 63, 63)),
               "right": self.sprite_sheet.subsurface(pygame.Rect(63, 63, 63, 63))
           }
       scale_factor = 2

       for direction in self.sprite_dir:  # Scales sprite to preference
           original = self.sprite_dir[direction]
           scaled = pygame.transform.scale(original, (64 * scale_factor, 64 * scale_factor))
           self.sprite_dir[direction] = scaled

    def update(self, _delta_time, walls):
        # Saves original position of char in the event that there is collision
        old_x = self.x
        old_y = self.y
        self.time_since_last_shot += _delta_time

        dx = self.player.x - self.x
        dy = self.player.y - self.y

        distance = max((dx ** 2 + dy ** 2) ** 0.5, 0.01)  # avoid division by zero

        self.velocity_x = dx / distance
        self.velocity_y = dy / distance

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

