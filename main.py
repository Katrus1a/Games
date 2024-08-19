import pygame
size = [440, 600]

Block_size = 20
Block_count = 20
Frame_color = (16, 74, 53)
White_color = (255, 255, 255)
Blue_color = (10, 163, 112)
margin=1
screen=pygame.display.set_mode(size)
pygame.display.set_caption('SNAKE')

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            print('Exit')
            pygame.quit()

    screen.fill(Frame_color)

    for row in range(Block_count):
        for column in range(Block_count):
            if (row+column)%2==0:
                color = Blue_color
            else:
                color = White_color
            pygame.draw.rect(screen, color, [10+column*Block_size +margin*(column+1),
                                                  20+row*Block_size +margin*(row+1), Block_size, Block_size])

    pygame.display.flip()