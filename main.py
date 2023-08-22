import pygame
import random
import sys


pygame.init()

# Screen dimensions
screen_width = 1000
screen_height = 500
score=0

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jump")

# Load the background image
background_image = pygame.image.load("assets/background.png").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
bg_width = background_image.get_width()

# Load the character image
character_image = pygame.image.load("assets/man.png").convert_alpha()
character_image = pygame.transform.scale(character_image, (50, 100))

player_lives = 3
font = pygame.font.Font(None, 36)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = player.y+25
        self.img = pygame.image.load('assets/enemy1.png') 
        self.img = pygame.transform.scale(self.img, (50, 50))
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)
        self.run_animation_count=0
        self.img_dict = {
            0:'assets/enemy1.png',
            1:'assets/enemy2.png', 
            2:'assets/enemy3.png',
        }
    def draw(self):
        self.rect.center = (self.x, self.y)
        screen.blit(self.img, self.rect)
    def run_animation_enemy(self):
        self.img = pygame.image.load(self.img_dict[int(self.run_animation_count)])
        self.img = pygame.transform.scale(self.img, (50, 50))
        self.rect = self.img.get_rect()
        self.rect.center = (self.x, self.y)
        self.run_animation_count+=0.3
        self.run_animation_count=self.run_animation_count%3
enemies = []

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load('assets/run1.png')
        self.img = pygame.transform.scale(self.img, (100, 100))
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)
        self.is_jump = False
        self.jump_count = 15
        self.run_animation_count = 0
        self.img_dict = {
            0:'assets/run1.png',
            1:'assets/run2.png',
            2:'assets/run3.png',
            3:'assets/run4.png',
        }
        

    def draw(self):
        self.rect.center = (self.x, self.y)
        screen.blit(self.img, self.rect)

    def jump(self):
        if self.jump_count >= -15:
            n = 1
            if self.jump_count < 0:
                n = -1
            jump_count_x=10
            self.y -= ((self.jump_count ** 2) / 10 * n)
            #self.x +=((jump_count_x)/10*n)
            self.jump_count -= 1

        else:
            self.is_jump = False
            self.jump_count = 15

    def run_animation_player(self):
        if(not self.is_jump ):
            self.img = pygame.image.load(self.img_dict[int(self.run_animation_count)])
            self.img = pygame.transform.scale(self.img, (100, 100))
            self.rect = self.img.get_rect()
            self.rect.center = (self.x, self.y)
            self.run_animation_count+=0.5
            self.run_animation_count=self.run_animation_count%4
            
player = Character(100, 386)
game_over_font = pygame.font.Font(None, 64)  

last_enemy_spawn_time = pygame.time.get_ticks()

# Create the character
player = Character(100, 386)

# Game loop
running = True
clock = pygame.time.Clock()
speed_increasing_rate = 0
bg_x = 0

while running:
    score=score+1
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
    current_time = pygame.time.get_ticks()  

    if current_time - last_enemy_spawn_time >= 2000:
        if random.randint(0, 100) < 2:
            enemy_x = screen_width
            enemy_y = 386
            enemy = Enemy(enemy_x, enemy_y)
            enemies.append(enemy)
            last_enemy_spawn_time = current_time  

    for enemy in enemies:
        enemy.x -= 15
        enemy.draw()
        enemy.run_animation_enemy()

        if enemy.rect.colliderect(player.rect):
            player_lives -= 1
            player.x = 100  # Reset player's x position
            player.y = 386  # Reset player's y position
            speed_increasing_rate = 0

            if player_lives <= 0:
                game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
                screen.blit(game_over_text, (screen_width // 2 - 120, screen_height // 2))
                pygame.display.update()
                pygame.time.wait(2000)
                pygame.quit()
                sys.exit()

            enemies.remove(enemy)  # Move this line inside the collision check loop

        if enemy.x + enemy.rect.width < 0:
            enemies.remove(enemy)

    lives_text = font.render(f"Lives: {player_lives}", True, (0, 0, 0))
    screen.blit(lives_text, (screen_width - 120, 10))
    
    score_text= font.render(f"Score:{score}",True,(0,0,0))
    screen.blit(score_text,(20,10))

    player.run_animation_player()
    pygame.display.update()
    clock.tick(30)

pygame.quit()
