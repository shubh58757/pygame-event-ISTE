import pygame

pygame.init()

# Screen dimensions
screen_width = 1000
screen_height = 500

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jump")

# Load the background image
background_image = pygame.image.load("assets/background.png").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
bg_width = background_image.get_width()

# Load the character image
character_image = pygame.image.load("assets/man.png").convert_alpha()
character_image = pygame.transform.scale(character_image, (100, 100))

# Character class
class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = character_image.get_rect()
        self.rect.center = (x, y)
        self.is_jump = False
        self.jump_count = 20

    def draw(self):
        self.rect.center = (self.x, self.y)
        screen.blit(character_image, self.rect)
        
    def jump(self):
        if self.jump_count >= -20:
            n = 1
            if self.jump_count < 0:
                n = -1
            self.y -= (self.jump_count ** 2) / 10 * n
            self.jump_count -= 1
        else:
            self.is_jump = False
            self.jump_count = 20



# Create the character
player = Character(100, 382)

# Game loop
running = True
clock = pygame.time.Clock()
speed_increasing_rate = 0
bg_x = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not player.is_jump:
                if event.key == pygame.K_SPACE:
                    player.is_jump = True

    if player.is_jump:
        player.jump()

    speed_increasing_rate += 0.006
    bg_x -= (10 + speed_increasing_rate)

    if bg_x < -bg_width:
        bg_x = 0

    screen.blit(background_image, (bg_x, 0))
    screen.blit(background_image, (bg_x + bg_width, 0))

    player.draw()

    pygame.display.update()
    clock.tick(30)

pygame.quit()
