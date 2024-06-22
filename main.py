import pygame
import random
import math

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Protect the Runes")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create a simple background if you don't have an image
background = pygame.Surface((WIDTH, HEIGHT))
background.fill((200, 230, 255))  # Light blue color for a snowy feel

class Viking(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = {
            'right': [self.create_viking_sprite(0), self.create_viking_sprite(0, True)],
            'left': [pygame.transform.flip(self.create_viking_sprite(0), True, False),
                     pygame.transform.flip(self.create_viking_sprite(0, True), True, False)],
            'up': [self.create_viking_sprite(1), self.create_viking_sprite(1, True)],
            'down': [self.create_viking_sprite(2), self.create_viking_sprite(2, True)]
        }
        self.current_sprite = 0
        self.image = self.sprites['right'][self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5
        self.direction = 'right'
        self.health = 100
        self.defense = 5
        self.attack_power = 20
        self.attack_cooldown = 0
        self.is_attacking = False
        self.attack_frame = 0

    def create_viking_sprite(self, direction, alt=False):
        img = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.rect(img, (128, 128, 128), (15, 20, 20, 20))
        pygame.draw.polygon(img, (192, 192, 192), [(15, 20), (35, 20), (25, 10)])
        pygame.draw.rect(img, (0, 0, 0), (20, 20, 5, 5))
        pygame.draw.rect(img, (0, 0, 0), (30, 20, 5, 5))
        pygame.draw.rect(img, (139, 69, 19), (15, 30, 20, 10))
        pygame.draw.rect(img, (139, 69, 19), (15, 40, 5, 5))
        pygame.draw.rect(img, (139, 69, 19), (30, 40, 5, 5))
        if direction == 0:  # Right
            pygame.draw.rect(img, (139, 69, 19), (35, 25, 10, 5))
            pygame.draw.polygon(img, (192, 192, 192), [(40, 20), (45, 20), (45, 30), (40, 30)])
        elif direction == 1:  # Up
            pygame.draw.rect(img, (139, 69, 19), (22, 5, 5, 10))
            pygame.draw.polygon(img, (192, 192, 192), [(20, 5), (30, 5), (25, 0)])
        elif direction == 2:  # Down
            pygame.draw.rect(img, (139, 69, 19), (22, 35, 5, 10))
            pygame.draw.polygon(img, (192, 192, 192), [(20, 45), (30, 45), (25, 50)])
        if alt:
            img = pygame.transform.rotate(img, 5)
        return img

    def update(self):
        self.current_sprite = (self.current_sprite + 1) % 2
        self.image = self.sprites[self.direction][self.current_sprite]
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.is_attacking:
            self.attack_frame += 1
            if self.attack_frame >= 10:  # Attack animation lasts for 10 frames
                self.is_attacking = False
                self.attack_frame = 0

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        if dx > 0:
            self.direction = 'right'
        elif dx < 0:
            self.direction = 'left'
        elif dy > 0:
            self.direction = 'down'
        elif dy < 0:
            self.direction = 'up'
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def attack(self):
        if self.attack_cooldown == 0:
            self.attack_cooldown = 30
            self.is_attacking = True
            self.attack_frame = 0
            attack_rect = pygame.Rect(self.rect)
            if self.direction == 'right':
                attack_rect.left = self.rect.right
            elif self.direction == 'left':
                attack_rect.right = self.rect.left
            elif self.direction == 'up':
                attack_rect.bottom = self.rect.top
            else:  # down
                attack_rect.top = self.rect.bottom
            return attack_rect
        return None

    def take_damage(self, amount):
        actual_damage = max(0, amount - self.defense)
        self.health -= actual_damage
        if self.health <= 0:
            self.kill()

class Draugr(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super().__init__()
        self.sprites = [self.create_draugr_sprite(), self.create_draugr_sprite(True)]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.speed = 2
        self.health = 30
        self.target = None

    def create_draugr_sprite(self, alt=False):
        img = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.rect(img, (107, 142, 35), (10, 10, 20, 25))
        pygame.draw.polygon(img, (112, 128, 144), [(10, 10), (30, 10), (20, 0)])
        pygame.draw.rect(img, (255, 0, 0), (15, 15, 5, 5))
        pygame.draw.rect(img, (255, 0, 0), (25, 15, 5, 5))
        pygame.draw.rect(img, (139, 69, 19), (30, 20, 10, 5))
        if alt:
            img = pygame.transform.rotate(img, 5)
        return img

    def update(self):
        self.current_sprite = (self.current_sprite + 1) % 2
        self.image = self.sprites[self.current_sprite]
        if self.target:
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            dist = math.sqrt(dx**2 + dy**2)
            if dist != 0:
                self.rect.x += (dx / dist) * self.speed
                self.rect.y += (dy / dist) * self.speed

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            return True
        return False

class Rune(pygame.sprite.Sprite):
    def __init__(self, rune_type):
        super().__init__()
        self.rune_type = rune_type
        self.image = pygame.Surface((25, 25))
        self.rect = self.image.get_rect()
        self.draw_rune()

    def draw_rune(self):
        self.image.fill((139, 69, 19))
        pygame.draw.rect(self.image, (210, 105, 30), self.rect, 2)
        if self.rune_type == 'algiz':
            color = (255, 215, 0)
            pygame.draw.line(self.image, color, (12, 5), (12, 20), 2)
            pygame.draw.line(self.image, color, (7, 10), (12, 5), 2)
            pygame.draw.line(self.image, color, (17, 10), (12, 5), 2)
            pygame.draw.line(self.image, color, (5, 15), (20, 15), 2)
        elif self.rune_type == 'mannaz':
            color = (255, 69, 0)
            pygame.draw.line(self.image, color, (8, 5), (8, 20), 2)
            pygame.draw.line(self.image, color, (17, 5), (17, 20), 2)
            pygame.draw.line(self.image, color, (8, 12), (17, 12), 2)
        else:  # dagaz
            color = (30, 144, 255)
            pygame.draw.line(self.image, color, (5, 5), (20, 5), 2)
            pygame.draw.line(self.image, color, (5, 20), (20, 20), 2)
            pygame.draw.line(self.image, color, (5, 5), (20, 20), 2)
            pygame.draw.line(self.image, color, (20, 5), (5, 20), 2)

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
runes = pygame.sprite.Group()

player = Viking()
all_sprites.add(player)

for rune_type in ['algiz', 'mannaz', 'dagaz']:
    rune = Rune(rune_type)
    rune.rect.x = random.randint(WIDTH//2 - 100, WIDTH//2 + 100)
    rune.rect.y = random.randint(HEIGHT//2 - 100, HEIGHT//2 + 100)
    all_sprites.add(rune)
    runes.add(rune)

score = 0
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
spawn_timer = 0
running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                attack_rect = player.attack()
                if attack_rect:
                    for enemy in enemies:
                        if attack_rect.colliderect(enemy.rect):
                            if enemy.take_damage(player.attack_power):
                                score += 10

    spawn_timer += dt
    if spawn_timer > 2:
        spawn_timer = 0
        enemy = Draugr(random.choice([0, WIDTH]), random.randint(0, HEIGHT))
        if runes:
            enemy.target = random.choice(list(runes))
        all_sprites.add(enemy)
        enemies.add(enemy)

    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
    if dx != 0 or dy != 0:
        player.move(dx, dy)

    all_sprites.update()

    for enemy in enemies:
        stolen_runes = pygame.sprite.spritecollide(enemy, runes, True)
        if stolen_runes:
            print("A rune was stolen!")
            enemy.target = None
            if runes:
                enemy.target = random.choice(list(runes))
            if not runes:
                running = False
        if pygame.sprite.collide_rect(enemy, player):
            player.take_damage(10)
            enemy.kill()

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    if player.is_attacking:
        attack_rect = player.attack()
        if attack_rect:
            pygame.draw.rect(screen, RED, attack_rect, 2)

    health_text = font.render(f"Health: {player.health}", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    runes_text = font.render(f"Runes left: {len(runes)}", True, WHITE)
    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 50))
    screen.blit(runes_text, (10, 90))

    pygame.display.flip()

    if player.health <= 0 or not runes:
        running = False

screen.fill(BLACK)
game_over_text = font.render("Game Over", True, WHITE)
final_score_text = font.render(f"Final Score: {score}", True, WHITE)
screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
screen.blit(final_score_text, (WIDTH//2 - final_score_text.get_width()//2, HEIGHT//2 + 50))
pygame.display.flip()

pygame.time.wait(3000)

pygame.quit()