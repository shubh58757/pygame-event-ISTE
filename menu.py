import pygame
import button
pygame.init()
Screen_width=1000
Screen_length=500
screen=pygame.display.set_mode((Screen_width,Screen_length))
pygame.display.set_caption("REALM")
pygame.display.set_caption("QUEST")

font=pygame.font.SysFont("arialblack",40)
font1=pygame.font.SysFont("arialblack",30)
text_col=(255,165,0)
text_col1=(128,0,128)
play_img=pygame.image.load("images/button_play.png").convert_alpha()
play_button=button.Button(304,125,play_img,1)
def draw_text(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    img1=font1.render(text,True,text_col1) 
    screen.blit(img,(x,y))
#game loop
run=1
while(run!=1):
    screen.fill((52,78,91))
        
    for event in pygame.event.get():
        if event.type==pygame.Quit:
            run=0
    pygame.display.update()

pygame.quit()