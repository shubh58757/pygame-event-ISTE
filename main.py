import pygame
pygame.init()
width = 1000
height =  500
screen = pygame.display.set_mode((1000,500))
FPS = 30
fpsClock = pygame.time.Clock()

pygame.display.set_caption('Game')
background_img = pygame.image.load('assests/images/pixel-art-pixelated-wallpaper-preview.jpg')
background_img = pygame.transform.scale(background_img, (1000,500))
main_loop =  True

class character:
    def __init__(self , x, y):
        self.x = x
        self.y = y
        self.img =  pygame.image.load('assests/images/man.png')
        self.img = pygame.transform.scale(self.img,(50,50))
        self.rect = self.img.get_rect()
        self.rect.center = (x,y)
        self.is_jump = False
        self.jump_count = 10

    def draw(self):
        self.rect.center = (self.x,self.y)
        screen.blit(self.img, self.rect)

    def jump(self):
        if(self.jump_count>=-10):
            n =1
            if(self.jump_count<0):
                n=-1
            self.y-=(self.jump_count**2)/10*n
            self.jump_count-=1
        else:
            self.is_jump=False
            self.jump_count =10


player = character(100, 400)
while main_loop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_loop = False
        if event.type == pygame.KEYDOWN:
            if not player.is_jump:
                if(event.key == pygame.K_SPACE):
                    player.is_jump = True
    if(player.is_jump):
        player.jump()
    screen.blit(background_img,(0,0))
    player.draw()
    pygame.display.update()
    fpsClock.tick(FPS)


