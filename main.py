import pygame
import sys
from pygame.locals import *

pygame.init()

background_colour = (0,0,0) 
screen = pygame.display.set_mode((1200, 1000)) 
pygame_icon = pygame.image.load('Images/Test_Tube_Icon.png')

pygame.display.set_caption('Tested')
pygame.display.set_icon(pygame_icon)
screen.fill(background_colour) 
pygame.display.flip() 
running = True

class Character:
    def __init__(self, image, x, y):
        self.image = pygame.image.load(image)
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


player = Character('Images/guy.png', 100, 100)

while running: 
    

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()       
    if keys[K_a]:
        player.x -= .5  
    if keys[K_d]:
        player.x += .5
    if keys[K_w]:
        player.y -= .5
    if keys[K_s]:
        player.y += .5

    
    screen.fill(background_colour)  
    player.draw(screen)             
    pygame.display.update()         

