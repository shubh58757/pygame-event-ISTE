import pygame
import random
import sys

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
YELLOW_LASER = pygame.image.load("assets/pixel_laser_yellow.png")

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)


    def draw(self, window):
        window.blit(self.img, (self.x, self.y)) #changed

    def move(self, vel):
        self.x += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)        

    def move_lasers(self, vel, objs):
        # self.cooldown()
        for laser in self.lasers:
            # laser.move(vel)
            if laser.off_screen(WIDTH): #changed
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = player.y
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
        self.jump_count = 20
        self.lasers = []
        self.laser_img = YELLOW_LASER #laser 
        # self.cool_down_counter = 30
        
    # Getters
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    #laser function
    # def move_lasers(self, vel, objs):
    #     # self.cooldown()
    #     for laser in self.lasers:
    #         laser.move(vel)
    #         if laser.off_screen(WIDTH): #changed
    #             self.lasers.remove(laser)
    #         else:
    #             for obj in objs:
    #                 if laser.collision(obj):
    #                     objs.remove(obj)
    #                     if laser in self.lasers:
    #                         self.lasers.remove(laser)    
        # Character.move_lasers(laser_vel, enemies)
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        # if self.cool_down_counter == 0:
            laser = Laser(self.x - 28, self.y - 28, self.laser_img)
            # laser = Laser(self.x + self.rect.width, self.y + self.rect.height // 2, self.laser_img)
            self.lasers.append(laser)
            # self.cool_down_counter = 1    

    # def shoot(self, xpos, ypos):
    #     laser = Laser(xpos + 500, ypos, self.laser_img)                    

    def draw(self, window): #
        self.rect.center = (self.x, self.y)
        screen.blit(self.img, self.rect)
        for laser in self.lasers:
            laser.draw(window)
            laser.move(5)

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

            self.is_jump = False
            self.jump_count = 15

player = Character(100, 375)
game_over_font = pygame.font.Font(None, 64)  

last_enemy_spawn_time = pygame.time.get_ticks()

# Create the character
player = Character(100, 382)

# Game loop
running = True
clock = pygame.time.Clock()
speed_increasing_rate = 0
bg_x = 0

while running:
    laser_vel = 5
    # Character.move_lasers(laser_vel, enemies) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not player.is_jump:
                if event.key == pygame.K_SPACE:
                    player.is_jump = True 
            if event.key == pygame.K_RIGHT:
                player.shoot()
                
    if player.is_jump:
        player.jump()

    keys = pygame.key.get_pressed()

    # if keys[pygame.K_UP]:
    #     player.shoot()

    speed_increasing_rate += 0.006
    bg_x -= (10 + speed_increasing_rate)

    if bg_x < -bg_width:
        bg_x = 0

    screen.blit(background_image, (bg_x, 0))
    screen.blit(background_image, (bg_x + bg_width, 0))

    player.draw(screen) #changed
    current_time = pygame.time.get_ticks()  

    if current_time - last_enemy_spawn_time >= 2000:
        if random.randint(0, 100) < 2:
            enemy_x = screen_width
            enemy_y = 375
            enemy = Enemy(enemy_x, enemy_y)
            enemies.append(enemy)
            last_enemy_spawn_time = current_time  

    for enemy in enemies:
        enemy.x -= 5
        enemy.draw()

        if enemy.rect.colliderect(player.rect):
            game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
            screen.blit(game_over_text, (screen_width // 2-120, screen_height // 2))
            pygame.display.update()
            pygame.time.wait(2000)  
            pygame.quit()
            sys.exit()

        if enemy.x + enemy.rect.width < 0:
            enemies.remove(enemy)

    pygame.display.update()
    clock.tick(30)

pygame.quit()
