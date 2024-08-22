import pygame
import random

pygame.init()

size=[400, 460]  
info_panel_height=60  
Block_size=20
Block_count=20
Frame_color=(16, 74, 53)
White_color=(255, 255, 255)
Blue_color=(10, 163, 112)
Violet_color=(116, 38, 240)
Black_color=(0, 0, 0)
Red_color=(255, 0, 0)
Gray_color = (105, 105, 105)
margin=1

screen=pygame.display.set_mode(size)
pygame.display.set_caption('SNAKE')


clock=pygame.time.Clock()

snake_size=20
snake_speed=10

message_font=pygame.font.SysFont('Arial', 42)
score_font=pygame.font.SysFont('Arial', 30)

start_time=pygame.time.get_ticks()

food_blink=True

def print_score(score):
    text=score_font.render("Score:"+str(score), True, White_color)
    screen.blit(text, [10, 10])

def print_time():
    elapsed_time=(pygame.time.get_ticks()-start_time) // 1000 
    time_text=score_font.render(f"Time: {elapsed_time} sec", True, White_color)
    screen.blit(time_text, [size[0]-200, 10])

def draw_snake(snake_size, snake_pixels):
    length=len(snake_pixels)
    for i, pixel in enumerate(snake_pixels):
        gradient_color=(
            Violet_color[0]+(White_color[0]-Violet_color[0])*i//length,
            Violet_color[1]+(White_color[1]-Violet_color[1])*i//length,
            Violet_color[2]+(White_color[2]-Violet_color[2])*i//length
        )
        shadow_offset=3
        pygame.draw.rect(screen, Gray_color, [pixel[0]+shadow_offset, pixel[1]+info_panel_height+shadow_offset, snake_size, snake_size])
        pygame.draw.rect(screen, Black_color, [pixel[0], pixel[1]+info_panel_height, snake_size, snake_size])
        pygame.draw.rect(screen, gradient_color, [pixel[0]+2, pixel[1]+info_panel_height+2, snake_size-4, snake_size-4])
def draw_grid():
    for row in range(Block_count):
        for column in range(Block_count):
            if (row+column) % 2==0:
                color=Blue_color
            else:
                color=White_color
            pygame.draw.rect(screen, color, [column*Block_size, row*Block_size+info_panel_height, Block_size, Block_size])

def game_over_screen():
    screen.fill(Black_color)
    game_over_message=message_font.render("Game Over!", True, Red_color)
    try_again_message=score_font.render("Press R to Try Again", True, White_color)
    screen.blit(game_over_message, [size[0]/3, size[1]/3])
    screen.blit(try_again_message, [size[0]/3, size[1]/2])
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_r:
                    run_game()
                if event.key==pygame.K_q:
                    pygame.quit()
                    quit()

def run_game():
    global snake_speed  
    global start_time
    global food_blink
    start_time=pygame.time.get_ticks()  
    game_over=False
    game_close=False

    x=size[0]/2
    y=(size[1]-info_panel_height)/2 

    x_speed=0
    y_speed=0

    snake_pixels=[]
    snake_length=1

    target_x=round(random.randrange(0, size[0]-snake_size)/20.0)*20.0
    target_y=round(random.randrange(0, size[1]-info_panel_height-snake_size)/20.0)*20.0

    while not game_over:

        while game_close:
            game_over_screen()
            break

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game_over=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    x_speed=-snake_size
                    y_speed=0
                if event.key==pygame.K_RIGHT:
                    x_speed=snake_size
                    y_speed=0
                if event.key==pygame.K_UP:
                    x_speed=0
                    y_speed=-snake_size
                if event.key==pygame.K_DOWN:
                    x_speed=0
                    y_speed=snake_size
               
                if event.key==pygame.K_PLUS: #редагування швидкості
                    snake_speed+=5
                if event.key==pygame.K_MINUS:
                    snake_speed-=5

        if x>=size[0] or x<0 or y>=size[1]-info_panel_height or y<info_panel_height:
            game_close=True

        x+=x_speed
        y+=y_speed

        screen.fill(Frame_color)
        draw_grid()

        if food_blink:
            food_color=Red_color
        else:
            food_color=White_color

        pygame.draw.rect(screen, food_color, [target_x, target_y + info_panel_height, snake_size, snake_size])
        food_blink=not food_blink

        snake_pixels.append([x, y])

        if len(snake_pixels)>snake_length:
            del snake_pixels[0]

        for pixel in snake_pixels[:-1]:
            if pixel==[x, y]:
                game_close=True

        draw_snake(snake_size, snake_pixels)
        print_score(snake_length-1)
        print_time()

        pygame.display.update()

        if abs(x-target_x)<Block_size and abs(y-target_y-info_panel_height)<Block_size:
            target_x=round(random.randrange(0, size[0]-snake_size)/20.0)*20.0
            target_y=round(random.randrange(0, size[1]-info_panel_height-snake_size)/20.0)*20.0
            snake_length+=1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

run_game()
