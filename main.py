import pygame
import sys
import random
import pygame_menu
from enum import Enum
pygame.init()

size = [500, 600]
FRAME_COLOR = (0, 0, 0)
COUNT_BLOCKS = 20
SIZE_BLOCK = 20
MARGIN = 2
SNAKE_COLOR = (0,102,0)
HEADER_MARGIN = 70
HEADER_COLOR = (0, 204, 153)

WHITE = (255,255,255)
BLUE = (204,255,255)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
timer = pygame.time.Clock()

size = [SIZE_BLOCK*COUNT_BLOCKS+2*SIZE_BLOCK+MARGIN*COUNT_BLOCKS,
        SIZE_BLOCK*COUNT_BLOCKS+2*SIZE_BLOCK+MARGIN*COUNT_BLOCKS+HEADER_MARGIN]

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake")
courier = pygame.font.SysFont('courier', 18)

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Block) and self.x == other.x and self.y == other.y

    def in_boundary(self):
        self.x += COUNT_BLOCKS
        self.x %= COUNT_BLOCKS
        self.y += COUNT_BLOCKS
        self.y %= COUNT_BLOCKS


class Food:
    def __init__(self, block, type):
        self.block = block
        self.type = type


class FoodType(Enum):
    lengthUp = 0
    speedUp = 1
    scoreUp = 2
    

def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column*SIZE_BLOCK+MARGIN*(column+1),
                                             HEADER_MARGIN+SIZE_BLOCK+row*SIZE_BLOCK+MARGIN*(row+1),
                                             SIZE_BLOCK,
                                             SIZE_BLOCK])

def start_the_game():
    def get_random_empty_block():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = Block(x, y)
        while empty_block in snake_blocks or empty_block in walls:
            x = random.randint(0, COUNT_BLOCKS - 1)
            y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block


    snake_blocks = [Block(COUNT_BLOCKS // 2 - 1, COUNT_BLOCKS // 2 - 1),
                    Block(COUNT_BLOCKS // 2 - 1, COUNT_BLOCKS // 2)]
    walls = [Block(5, 5)]
    apple = Food(get_random_empty_block(), FoodType.lengthUp)
    bl = Block(-100, -100)
    bonus = Food(bl, FoodType.scoreUp)
    iteration = 0
    local_iteration = 0
    flg = False
    d_row = 0
    d_col = 1
    total = 0
    speed = 1
    lives = 3
    loc_iteration = 0
    cheatsB = False
    cheatsK = False

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and d_col != 0:
                    d_row=-1
                    d_col=0
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and d_col != 0:
                    d_row=1
                    d_col=0  
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and d_row != 0:
                    d_row=0
                    d_col=-1
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and d_row != 0:
                    d_row=0
                    d_col=1
                elif event.key == pygame.K_b:
                    if cheatsB:
                        cheatsB = False
                    else:
                        cheatsB = True
                elif event.key == pygame.K_k:
                    if cheatsK:
                        cheatsK = False
                    else:
                        cheatsK = True
                elif event.key == pygame.K_m:
                    total += 100
        
        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0,0,size[0], HEADER_MARGIN])

        text_total = courier.render(f"Total: {total}", 0, WHITE)
        text_speed = courier.render(f"Speed: {speed}", 0, WHITE)
        text_lives = courier.render(f"Lives: {lives}", 0, WHITE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK+150, SIZE_BLOCK))
        screen.blit(text_lives, (SIZE_BLOCK+250, SIZE_BLOCK))

        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                color = WHITE
                draw_block(color, row, column)
        
        for wall in walls:
            draw_block(BLACK, wall.x, wall.y)

        head = snake_blocks[-1]
        head.in_boundary()
        
        if apple.type == FoodType.lengthUp:
            draw_block(RED, apple.block.x, apple.block.y)
        elif apple.type == FoodType.speedUp:
            draw_block(GRAY, apple.block.x, apple.block.y)

        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        if speed % 2 == 0:
            if not flg:
                flg = True
                local_iteration = iteration
                bonus = Food(get_random_empty_block(), FoodType.scoreUp)
        else:
            flg = False
        
        if flg:
            if iteration - local_iteration >= 20:
                bonus = Food(Block(-100, -100), FoodType.scoreUp)
            if bonus.block == head:
                total += 10
                bonus = Food(Block(-100, -100), FoodType.scoreUp)
            else:
                draw_block(YELLOW, bonus.block.x, bonus.block.y)


        flag = True
        if apple.block == head:
            total += 1
            if apple.type == FoodType.lengthUp:
                flag = False
            if apple.type == FoodType.speedUp:
                if not cheatsK:
                    speed += 1
            if total % 5 == 0:
                apple = Food(get_random_empty_block(), FoodType.speedUp)
            else:
                apple = Food(get_random_empty_block(), FoodType.lengthUp)
        else:
            flag = True
        
        new_head = Block(head.x + d_row, head.y + d_col)


        if (not cheatsB) and (new_head in snake_blocks or new_head in walls):
            if lives == 1:
                break
            if iteration - loc_iteration > 5:
                lives -= 1
                loc_iteration = iteration

        snake_blocks.append(new_head)
        if flag or cheatsK:
            snake_blocks.pop(0)

        pygame.display.flip()
        iteration += 1
        timer.tick(3 + speed)


menu = pygame_menu.Menu("Menu",300, 200,
                       theme=pygame_menu.themes.THEME_BLUE)


menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(screen)