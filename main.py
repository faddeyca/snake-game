import pygame, pygame_menu
import sys, random
from pathlib import Path

from Classes.Block import *
from Classes.Food import *
from Classes.Propirties import *
from Classes.Colors import *


def build_window():
    size = [Propirties.SIZE_BLOCK*Propirties.COUNT_BLOCKS+2*Propirties.SIZE_BLOCK+Propirties.MARGIN*Propirties.COUNT_BLOCKS,
        Propirties.SIZE_BLOCK*Propirties.COUNT_BLOCKS+2*Propirties.SIZE_BLOCK+Propirties.MARGIN*Propirties.COUNT_BLOCKS+Propirties.HEADER_MARGIN]
    pygame.display.set_caption("Snake")
    return pygame.display.set_mode(size), size


class Level:
    def __init__(self, screen, size):
        self.screen = screen
        self.size = size
        self.timer = pygame.time.Clock()

    def draw_window(self):
        self.screen.fill(Color.FRAME_COLOR)
        pygame.draw.rect(self.screen, Color.HEADER_COLOR, [0,0,self.size[0], Propirties.HEADER_MARGIN])
        

    def draw_block(self, color, row, column):
        pygame.draw.rect(self.screen, color, [Propirties.SIZE_BLOCK + column*Propirties.SIZE_BLOCK+Propirties.MARGIN*(column+1),
                                                Propirties.HEADER_MARGIN+Propirties.SIZE_BLOCK+row*Propirties.SIZE_BLOCK+Propirties.MARGIN*(row+1),
                                                Propirties.SIZE_BLOCK,
                                                Propirties.SIZE_BLOCK])

    def start_the_game(self):
        pygame.mixer.music.play()

        def get_random_empty_block():
            x = random.randint(0, Propirties.COUNT_BLOCKS - 1)
            y = random.randint(0, Propirties.COUNT_BLOCKS - 1)
            empty_block = Block(x, y, Propirties.COUNT_BLOCKS)
            while empty_block in snake_blocks or empty_block in walls:
                x = random.randint(0, Propirties.COUNT_BLOCKS - 1)
                y = random.randint(0, Propirties.COUNT_BLOCKS - 1)
            return empty_block


        snake_blocks = [Block(Propirties.COUNT_BLOCKS // 2 - 1, Propirties.COUNT_BLOCKS // 2 - 1, Propirties.COUNT_BLOCKS),
                        Block(Propirties.COUNT_BLOCKS // 2 - 1, Propirties.COUNT_BLOCKS // 2, Propirties.COUNT_BLOCKS)]
        walls = [Block(5, 5, Propirties.COUNT_BLOCKS)]
        apple = Food(get_random_empty_block(), FoodType.lengthUp)
        bl = Block(-100, -100, Propirties.COUNT_BLOCKS)
        bonus = Food(bl, FoodType.scoreUp)
        iteration = 0
        local_iteration = 0
        flg = False
        d_row = 0
        d_col = 1
        score = 0
        speed = 1
        lives = 3
        loc_iteration = 0
        cheatsB = False
        cheatsK = False
        go = False

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    go = True
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
                        score += 100
        
            self.draw_window()
            courier = pygame.font.SysFont('courier', 18)
            text_total = courier.render(f"Score: {score}", 0, Color.WHITE)
            text_speed = courier.render(f"Speed: {speed}", 0, Color.WHITE)
            text_lives = courier.render(f"Lives: {lives}", 0, Color.WHITE)
            self.screen.blit(text_total, (Propirties.SIZE_BLOCK, Propirties.SIZE_BLOCK))
            self.screen.blit(text_speed, (Propirties.SIZE_BLOCK+150, Propirties.SIZE_BLOCK))
            self.screen.blit(text_lives, (Propirties.SIZE_BLOCK+300, Propirties.SIZE_BLOCK))

            for row in range(Propirties.COUNT_BLOCKS):
                for column in range(Propirties.COUNT_BLOCKS):
                    self.draw_block(Color.WHITE, row, column)
            
            for wall in walls:
                self.draw_block(Color.BLACK, wall.x, wall.y)

            head = snake_blocks[-1]
            head.in_boundary()
            
            if apple.type == FoodType.lengthUp:
                self.draw_block(Color.RED, apple.block.x, apple.block.y)
            elif apple.type == FoodType.speedUp:
                self.draw_block(Color.GRAY, apple.block.x, apple.block.y)

            for block in snake_blocks:
                self.draw_block(Color.SNAKE_COLOR, block.x, block.y)

            if speed % 2 == 0:
                if not flg:
                    flg = True
                    local_iteration = iteration
                    bonus = Food(get_random_empty_block(), FoodType.scoreUp)
            else:
                flg = False
            
            if flg:
                if iteration - local_iteration >= 20:
                    bonus = Food(Block(-100, -100, Propirties.COUNT_BLOCKS), FoodType.scoreUp)
                if bonus.block == head:
                    score += 10
                    bonus = Food(Block(-100, -100, Propirties.COUNT_BLOCKS), FoodType.scoreUp)
                else:
                    self.draw_block(Color.YELLOW, bonus.block.x, bonus.block.y)


            flag = True
            if apple.block == head:
                score += 1
                if apple.type == FoodType.lengthUp:
                    flag = False
                if apple.type == FoodType.speedUp:
                    if not cheatsK:
                        speed += 1
                if score % 5 == 0:
                    apple = Food(get_random_empty_block(), FoodType.speedUp)
                else:
                    apple = Food(get_random_empty_block(), FoodType.lengthUp)
            else:
                flag = True
            
            new_head = Block(head.x + d_row, head.y + d_col, Propirties.COUNT_BLOCKS)


            if (not cheatsB) and (new_head in snake_blocks or new_head in walls):
                if lives == 1:
                    pygame.mixer.music.stop()
                    break
                if iteration - loc_iteration > 5:
                    lives -= 1
                    loc_iteration = iteration

            snake_blocks.append(new_head)
            if flag or cheatsK:
                snake_blocks.pop(0)

            pygame.display.flip()
            iteration += 1
            self.timer.tick(3 + speed)

def start_the_game(screen, size):
    lvl = Level(screen, size)
    lvl.start_the_game()

def start():
    screen, size = build_window()
    menu = pygame_menu.Menu("Menu",300, 200,
                        theme=pygame_menu.themes.THEME_BLUE)

    menu.add.button('Play', lambda:start_the_game(screen, size))
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(screen)


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.music.load(Path("sounds/Dramatic-emotional-background-music.mp3"))
    start()
    sys.exit()