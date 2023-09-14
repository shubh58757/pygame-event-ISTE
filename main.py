import pygame 
import random
import sys

pygame.init()

# Initialize the game
screen_width = 1000
screen_height = 500
score = 0

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jump")

# Load the background image for the menu
menu_background = pygame.image.load("assets/menu.png")
menu_background = pygame.transform.scale(menu_background, (screen_width, screen_height))


#Load the background image for the game 
background_image = pygame.image.load("assets/background.png").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
bg_width = background_image.get_width()

player_lives = 3
font = pygame.font.Font(None, 36)

#Laser Class
class Bullet:
    def __init__(self,x,y, img):
        self.x = x
        self.y = y
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (20, 20))
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

    def draw(self, window):
        self.rect.center = (self.x, self.y)
        screen.blit(self.img, self.rect)

    def move(self, vel):
        self.x += vel

    def enemy_move(self,vel):
        self.x -= vel
    def off_screen(self):
        return not(self.x <= screen_width and self.x >= 0) 

enemy_bullets = []

#Enemy Class
class Enemy:
    #constructor for enemy class
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load('assets/enemy1.png') 
        self.img = pygame.transform.scale(self.img, (75, 75))
        self.bullet_img = 'assets/enemy_bullet.png'
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)
        self.run_animation_count=0
        self.img_dict = {
            0:'assets/enemy1.png',
            1:'assets/enemy2.png', 
            2:'assets/enemy3.png',
        }
        self.last_shot_time = pygame.time.get_ticks()       

    #Drawing the enemy on the screen
    def draw(self):
        self.rect.center = (self.x, self.y)
        screen.blit(self.img, self.rect)

    #running animation of the enemy
    def run_animation_enemy(self):
        self.img = pygame.image.load(self.img_dict[int(self.run_animation_count)])
        self.img = pygame.transform.scale(self.img, (75, 75))
        self.rect = self.img.get_rect()
        self.rect.center = (self.x, self.y)
        self.run_animation_count+=0.3
        self.run_animation_count=self.run_animation_count%3

    #Shooting the enemy bullets
    def shoot(self):
        print("enemy bullets")
        enemy_laser = Bullet(self.x - 28, self.y, self.bullet_img)
        enemy_bullets.append(enemy_laser)
        self.last_shot_time = current_time
        print("Shooting enemy bullet:", enemy_laser.x, enemy_laser.y)

#enemy and player
enemies = []
player_bullets = []

# class for the main character 
class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load('assets/run1.png')
        self.img = pygame.transform.scale(self.img, (100, 100))
        self.bullet_img = 'assets/bullet.png'
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
        
    #drawing the main character on the screen
    def draw(self):
        self.rect.center = (self.x, self.y)
        screen.blit(self.img, self.rect)

    #jumping function for the player
    def jump(self):
        if self.jump_count >= -15:
            n = 1
            if self.jump_count < 0:
                n = -1
            self.y -= ((self.jump_count ** 2) / 10 * n)
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

    def shoot(self):
        bullet = Bullet(self.x -28, self.y -18, self.bullet_img)
        player_bullets.append(bullet)
        print("Shooting player bullet:", bullet.x, bullet.y)


# Shield class 
class Shield:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load('assets/shield.png') 
        self.img = pygame.transform.scale(self.img, (100, 100)) 
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        self.rect.center = (self.x, self.y)
        screen.blit(self.img, self.rect)

    #funcion created to check collision with enemy bullet 
    def collides_with_enemy_laser(self, enemy_laser):
        return pygame.Rect.colliderect(self.rect, enemy_laser.rect)

#Game over font 
game_over_font = pygame.font.Font(None, 64)  

#tells the time at which the last enemy was spawned, helps to keep track of the plan
last_enemy_spawn_time = pygame.time.get_ticks()

# Create the character
player = Character(100, 386)

# Game state
menu_active = True
game_active = False

# Game loop
running = True
clock = pygame.time.Clock()
speed_increasing_rate = 0
bg_x = 0


shield = None
shield_active = False   


while running:
    # Menu
    if menu_active:
        screen.blit(menu_background,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and menu_active:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 400 <= mouse_x <= 600 and 300 <= mouse_y <= 400:  # Replace these coordinates with the button area
                    menu_active = False
                    game_active = True
                    last_enemy_spawn_time = pygame.time.get_ticks()
        pygame.display.update()
        clock.tick(30)
    
    # Game
    if game_active:
        #infinite running background 
        speed_increasing_rate += 0.006
        bg_x -= (10 + speed_increasing_rate)

        if bg_x < -bg_width:
            bg_x = 0

        screen.blit(background_image, (bg_x, 0))
        screen.blit(background_image, (bg_x + bg_width, 0))


        score=score+1  # scoring 

        #Drawing the player 
        player.draw()          
        player.run_animation_player()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #Jumping code     
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not player.is_jump:
                        player.is_jump = True
                if event.key == pygame.K_RETURN: # Checking if shield is open or no 
                    if not shield_active:
                        shield_active = True
                        shield = Shield(player.x, player.y)
                    else:
                        shield_active = False
                #command for shooting         
                if event.key == pygame.K_RIGHT and not shield_active: 
                    player.shoot()

        if player.is_jump:
            player.jump()

        # Update and draw lasers
        for bullet in player_bullets:
            bullet.move(10)  # Move the bullet horizontally
            bullet.draw(screen)  # Draw the bullet

            if bullet.off_screen():
                player_bullets.remove(bullet)  # Removing offscreen lasers

        #update the enemy bullets 
        for enemy_laser in enemy_bullets:
            enemy_laser.move(-20)  
            enemy_laser.draw(screen)
            if shield_active and shield is not None:  
                if shield.collides_with_enemy_laser(enemy_laser):
                    enemy_bullets.remove(enemy_laser)

            if enemy_laser.off_screen():
                enemy_bullets.remove(enemy_laser)

        #Forming shield in front of the player         
        if shield_active:
            shield.x = player.x
            shield.y = player.y
            shield.draw()
        current_time = pygame.time.get_ticks()  


        #Conditions for the spawing of enemy
        if current_time - last_enemy_spawn_time >= 2000:
            if random.randint(0, 100) < 3:
                enemy_x = screen_width + 900
                enemy_y = 396
                enemy = Enemy(enemy_x, enemy_y)
                enemies.append(enemy)
                last_enemy_spawn_time = current_time  

        # Spawing enemies 
        for enemy in enemies:
            enemy.x -= 15
            enemy.draw()
            enemy.run_animation_enemy()
            current_time = pygame.time.get_ticks()
            # Enemy shooting time constraint 
            if current_time - enemy.last_shot_time >= 2000:
                enemy.shoot()

            #collision for enenemy and player buller
            for bullet in player_bullets:
                if pygame.Rect.colliderect(enemy.rect, bullet.rect):
                    print("Collision detected!")
                    player_bullets.remove(bullet)
                    enemies.remove(enemy)
                    score+= 10
                    print("Remaining lasers:", len(player_bullets))
                    break

            #coliison for enemy bullet and player 
            for bullet in enemy_bullets:
                if pygame.Rect.colliderect(player.rect, bullet.rect):
                    print("Collision detected!")
                    enemy_bullets.remove(enemy_laser)

                    if not shield_active:
                        player_lives-= 1
                        print("Remaining lasers:", len(enemy_bullets))
                        break

            #collision between enemy and player 
            if enemy.rect.colliderect(player.rect):
                speed_increasing_rate = 0
                player_lives -= 1
                enemies.remove(enemy)
                if player_lives <= 0:
                    game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
                    screen.blit(game_over_text, (screen_width // 2 - 120, screen_height // 2))
                    pygame.display.update()
                    pygame.time.wait(2000)
                    pygame.quit()
                    sys.exit()

            #Removing enemy from screen 
            if enemy.x + enemy.rect.width < 0:
                enemies.remove(enemy)

        #Displaying lives
        lives_text = font.render(f"Lives: {player_lives}", True, (0, 0, 0))
        screen.blit(lives_text, (screen_width - 120, 10))
        
        #Displaying Score 
        score_text= font.render(f"Score:{score}",True,(0,0,0))
        screen.blit(score_text,(20,10))

        #Updating the screen 
        pygame.display.update()
        clock.tick(30) # Timer for the FPS

pygame.quit()