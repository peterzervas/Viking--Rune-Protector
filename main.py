import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Protect the Runes")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load the background image
# Make sure to convert the SVG to PNG and place it in the same directory as this script
background = pygame.image.load("snowy_forest_background.png").convert()

class Viking(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = {
            'right': [self.create_viking_sprite(0), self.create_viking_sprite(0, True)],
            'left': [pygame.transform.flip(self.create_viking_sprite(2), True, False),
                     pygame.transform.flip(self.create_viking_sprite(2, True), True, False)],
            'up': [self.create_viking_sprite(3), self.create_viking_sprite(3, True)],
            'down': [self.create_viking_sprite(1), self.create_viking_sprite(1, True)]
        }
        self.current_sprite = 0
        self.image = self.sprites['right'][self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5
        self.direction = 'right'
        self.health = 100
        self.defense = 10
        self.attack_power = 20

    def create_viking_sprite(self, direction, alt=False):
        img = pygame.Surface((50, 50), pygame.SRCALPHA)
        # Body (armor)
        pygame.draw.rect(img, (128, 128, 128), (15, 20, 20, 20))
        # Helmet
        pygame.draw.polygon(img, (192, 192, 192), [(15, 20), (35, 20), (25, 10)])
        # Eyes
        pygame.draw.rect(img, (0, 0, 0), (20, 20, 5, 5))
        pygame.draw.rect(img, (0, 0, 0), (30, 20, 5, 5))
        # Beard
        pygame.draw.rect(img, (139, 69, 19), (15, 30, 20, 10))
        pygame.draw.rect(img, (139, 69, 19), (15, 40, 5, 5))
        pygame.draw.rect(img, (139, 69, 19), (30, 40, 5, 5))
        # Axe
        if direction in [0, 2]:  # Facing right or left
            axe_x = 35 if direction == 0 else 5
            pygame.draw.rect(img, (139, 69, 19), (axe_x, 25, 10, 5))  # Handle
            pygame.draw.polygon(img, (192, 192, 192), [(axe_x + 5, 20), (axe_x + 10, 20), (axe_x + 10, 30), (axe_x + 5, 30)])  # Blade
        if alt:
            # Slightly modify the sprite for animation (e.g., move axe or legs)
            img = pygame.transform.rotate(img, 5)
        return img

    def update(self):
        self.current_sprite = (self.current_sprite + 1) % 2
        self.image = self.sprites[self.direction][self.current_sprite]

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

    def take_damage(self, amount):
        actual_damage = max(0, amount - self.defense)
        self.health -= actual_damage
        if self.health <= 0:
            self.kill()  # Remove the Viking sprite if health reaches 0

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

    def create_draugr_sprite(self, alt=False):
        img = pygame.Surface((40, 40), pygame.SRCALPHA)
        # Body
        pygame.draw.rect(img, (107, 142, 35), (10, 10, 20, 25))
        # Helmet
        pygame.draw.polygon(img, (112, 128, 144), [(10, 10), (30, 10), (20, 0)])
        # Eyes
        pygame.draw.rect(img, (255, 0, 0), (15, 15, 5, 5))
        pygame.draw.rect(img, (255, 0, 0), (25, 15, 5, 5))
        # Weapon
        pygame.draw.rect(img, (139, 69, 19), (30, 20, 10, 5))
        if alt:
            # Slightly modify the sprite for animation
            img = pygame.transform.rotate(img, 5)
        return img

    def update(self):
        self.current_sprite = (self.current_sprite + 1) % 2
        self.image = self.sprites[self.current_sprite]
        # Move towards the center of the screen (where the runes are)
        dx = (WIDTH // 2) - self.rect.centerx
        dy = (HEIGHT // 2) - self.rect.centery
        dist = math.sqrt(dx**2 + dy**2)
        if dist != 0:
            self.rect.x += (dx / dist) * self.speed
            self.rect.y += (dy / dist) * self.speed

class Rune(pygame.sprite.Sprite):
    def __init__(self, rune_type):
        super().__init__()
        self.rune_type = rune_type
        self.image = pygame.Surface((25, 25))  # 5x5 pixels scaled up by 5
        self.rect = self.image.get_rect()
        self.draw_rune()

    def draw_rune(self):
        # Wood background
        self.image.fill((139, 69, 19))  # Dark wood color
        pygame.draw.rect(self.image, (210, 105, 30), self.rect, 2)  # Lighter wood border

        if self.rune_type == 'algiz':
            color = (255, 215, 0)  # Gold
            pygame.draw.line(self.image, color, (12, 5), (12, 20), 2)
            pygame.draw.line(self.image, color, (7, 10), (12, 5), 2)
            pygame.draw.line(self.image, color, (17, 10), (12, 5), 2)
            pygame.draw.line(self.image, color, (5, 15), (20, 15), 2)
        elif self.rune_type == 'mannaz':
            color = (255, 69, 0)   # Orange-Red
            pygame.draw.line(self.image, color, (8, 5), (8, 20), 2)
            pygame.draw.line(self.image, color, (17, 5), (17, 20), 2)
            pygame.draw.line(self.image, color, (8, 12), (17, 12), 2)
        else:  # dagaz
            color = (30, 144, 255) # Blue
            pygame.draw.line(self.image, color, (5, 5), (20, 5), 2)
            pygame.draw.line(self.image, color, (5, 20), (20, 20), 2)
            pygame.draw.line(self.image, color, (5, 5), (20, 20), 2)
            pygame.draw.line(self.image, color, (20, 5), (5, 20), 2)

    def activate(self, player):
        if self.rune_type == 'algiz':
            player.defense += 20  # Increase defense
        elif self.rune_type == 'mannaz':
            player.health = min(player.health + 30, 100)  # Heal player
        else:  # dagaz
            player.attack_power *= 2  # Double attack power

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
runes = pygame.sprite.Group()

# Create the player
player = Viking()
all_sprites.add(player)

# Create runes
for rune_type in ['algiz', 'mannaz', 'dagaz']:
    rune = Rune(rune_type)
    rune.rect.x = random.randint(WIDTH//2 - 100, WIDTH//2 + 100)
    rune.rect.y = random.randint(HEIGHT//2 - 100, HEIGHT//2 + 100)
    all_sprites.add(rune)
    runes.add(rune)

# Game loop
clock = pygame.time.Clock()
spawn_timer = 0
running = True
while running:
    dt = clock.tick(60) / 1000  # delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn enemies
    spawn_timer += dt
    if spawn_timer > 2:  # Spawn an enemy every 2 seconds
        spawn_timer = 0
        enemy = Draugr(random.choice([0, WIDTH]), random.randint(0, HEIGHT))
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Handle player movement
    keys = pygame.key.get_pressed()
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
    if dx != 0 or dy != 0:
        player.move(dx, dy)

    # Update all sprites
    all_sprites.update()

    # Check for collisions
    for enemy in enemies:
        if pygame.sprite.spritecollide(enemy, runes, True):
            print("A rune was stolen!")
        if pygame.sprite.collide_rect(enemy, player):
            player.take_damage(10)
            enemy.kill()

    # Draw everything
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

pygame.quit()