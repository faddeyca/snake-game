import pygame
import sys
import random
import pygame_menu
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
timer = pygame.time.Clock()

size = [SIZE_BLOCK*COUNT_BLOCKS+2*SIZE_BLOCK+MARGIN*COUNT_BLOCKS,
        SIZE_BLOCK*COUNT_BLOCKS+2*SIZE_BLOCK+MARGIN*COUNT_BLOCKS+HEADER_MARGIN]

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake")
courier = pygame.font.SysFont('courier', 36)

class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y

    def is_inside(self):
        return 0<=self.x<COUNT_BLOCKS and 0<=self.y<COUNT_BLOCKS
    

def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column*SIZE_BLOCK+MARGIN*(column+1),
                                             HEADER_MARGIN+SIZE_BLOCK+row*SIZE_BLOCK+MARGIN*(row+1),
                                             SIZE_BLOCK,
                                             SIZE_BLOCK])

def start_the_game():
    def get_random_empty_block():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            x = random.randint(0, COUNT_BLOCKS - 1)
            y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block


    snake_blocks = [SnakeBlock(COUNT_BLOCKS // 2 - 1, COUNT_BLOCKS // 2 - 1),
                    SnakeBlock(COUNT_BLOCKS // 2 - 1, COUNT_BLOCKS // 2),
                    SnakeBlock(COUNT_BLOCKS // 2 - 1, COUNT_BLOCKS // 2 + 1)]
    apple = get_random_empty_block()
    d_row = 0
    d_col = 1
    total = 0
    speed = 1

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
        
        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0,0,size[0], HEADER_MARGIN])

        text_total = courier.render(f"Total: {total}", 0, WHITE)
        text_speed = courier.render(f"Speed: {speed}", 0, WHITE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK+230, SIZE_BLOCK))

        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                color = WHITE
                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            empty = screen.Container(width=100, height=100)
            screen.init(empty)
            break
        
        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        flag = True
        if apple == head:
            total += 1
            speed = total // 5 + 1
            flag = False
            apple = get_random_empty_block()
        else:
            flag = True
        
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if new_head in snake_blocks:
            break

        snake_blocks.append(new_head)
        if flag:
            snake_blocks.pop(0)

        pygame.display.flip()
        timer.tick(3 + speed)


menu = pygame_menu.Menu("Menu",300, 200,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(screen)