import pygame
import random
import time

size = [440, 600]

Block_size = 20
Block_count = 20
Frame_color = (16, 74, 53)
White_color = (255, 255, 255)
Blue_color = (10, 163, 112)
Violet_color = (116, 38, 240)
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

clock = pygame.time.Clock()

snake_size=20
snake_speed=15
message_font=pygame.font.SysFont('Arial', 42)
score_font=pygame.font.SysFont('Arial', 42)

def print_score(score):
    text=score_font.render("Score:"+str(score), True, White_color)
    game_display.blit(text,[0,0])

def draw_snake (snake_size, snake_pixels):
    for pixel in snake_pixels:
        pygame.draw.rect(game_display, Violet_color,[pixel[0], pixel[1], snake_size, snake_size])
def run_game():
    game_over = False
    game_close = False

    x=width/2
    y=height/2

    x_speed=0
    y_speed=0

    snake_pixels=[]
    snake_length=1

    target_x=round(random.randrange(0, width-snake_size)/10.0)*10.0
    target_y=round(random.randrange(0, height-snake_size)/10.0)*10.0

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_speed==-snake_size
                        y_speed = 0
                    if event.key == pygame.K_RIGHT:
                        x_speed == snake_size
                        y_speed = 0
                    if event.key == pygame.K_UP:
                        x_speed == 0
                        y_speed = -snake_size
                    if event.key == pygame.K_DOWN:
                        x_speed == 0
                        y_speed = snake_size

        # if x>=width or x<0 or y>=height or y<0:
        #     game_close=True
        #
        # x+=x_speed
        # y+=y_speed



