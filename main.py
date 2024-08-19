import pygame
size = [500, 600]

screen=pygame.display.set_mode(size)
pygame.display.set_caption('SNAKE')

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            print('Exit')
            pygame.quit()