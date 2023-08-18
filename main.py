import pygame
import random
import sys

pygame.init()
width = 1000
height =  500
screen = pygame.display.set_mode((width, height))
FPS = 30
fpsClock = pygame.time.Clock()

pygame.display.set_caption('Game')
background_img = pygame.image.load('assets/pixel-art-pixelated-wallpaper-preview.jpg')
background_img = pygame.transform.scale(background_img, (1000,500))
main_loop =  True

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load('assets/enemy.png') 
        self.img = pygame.transform.scale(self.img, (100, 100))
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        self.rect.center = (self.x, self.y)
        screen.blit(self.img, self.rect)

enemies = []

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load('assets/man.png')
        self.img = pygame.transform.scale(self.img, (100, 100))
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)
        self.is_jump = False
        self.jump_count = 15

    def draw(self):
        self.rect.center = (self.x, self.y)
        screen.blit(self.img, self.rect)

    def jump(self):
        if self.jump_count >= -15:
            n = 1
            if self.jump_count < 0:
                n = -1
            self.y -= (self.jump_count ** 2) / 15 * n
            self.jump_count -= 1
        else:
            self.is_jump = False
            self.jump_count = 15

player = Character(100, 375)
game_over_font = pygame.font.Font(None, 64)  

last_enemy_spawn_time = pygame.time.get_ticks()

while main_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_loop = False
        if event.type == pygame.KEYDOWN:
            if not player.is_jump:
                if event.key == pygame.K_SPACE:
                    player.is_jump = True

    if player.is_jump:
        player.jump()

    screen.blit(background_img, (0, 0))
    player.draw()
    current_time = pygame.time.get_ticks()  

    if current_time - last_enemy_spawn_time >= 2000:
        if random.randint(0, 100) < 2:
            enemy_x = width
            enemy_y = 375
            enemy = Enemy(enemy_x, enemy_y)
            enemies.append(enemy)
            last_enemy_spawn_time = current_time  

    for enemy in enemies:
        enemy.x -= 5
        enemy.draw()

        if enemy.rect.colliderect(player.rect):
            game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
            screen.blit(game_over_text, (width // 2-120, height // 2))
            pygame.display.update()
            pygame.time.wait(2000)  
            pygame.quit()
            sys.exit()

        if enemy.x + enemy.rect.width < 0:
            enemies.remove(enemy)

    pygame.display.update()
    fpsClock.tick(FPS)
