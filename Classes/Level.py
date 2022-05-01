import pygame
import sys, random

from Classes.Block import *
from Classes.Food import *
from Classes.Propirties import *
from Classes.Colors import *

      
class Level:
    def __init__(self, screen, size):
        self.screen = screen
        self.size = size
        self.timer = pygame.time.Clock()
        self.score = 0
        self.speed = 1
        self.lives = 3
        self.snake_blocks = [Block(Propirties.blocks_amount // 2 - 1, Propirties.blocks_amount // 2 - 1, Propirties.blocks_amount),
                        Block(Propirties.blocks_amount // 2 - 1, Propirties.blocks_amount // 2, Propirties.blocks_amount)]
        self.walls = [Block(5, 5, Propirties.blocks_amount)]

    def start(self):
        iteration = 0
        fixed_iteration = 0
        deathless_iteration = 0

        empty_block = Block(-100, -100, Propirties.blocks_amount)

        apple = Food(self.get_random_block(), FoodType.lengthUp)
        bonus = Food(empty_block, FoodType.scoreUp)

        bonus_flag = False
        d_x = 0
        d_y = 1
        
        cheatsB = False
        cheatsK = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and d_y != 0:
                        d_x=-1
                        d_y=0
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and d_y != 0:
                        d_x=1
                        d_y=0  
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and d_x != 0:
                        d_x=0
                        d_y=-1
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and d_x != 0:
                        d_x=0
                        d_y=1
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
            self.draw_text()
            self.draw_env(apple)

            head = self.snake_blocks[-1]
            head.put_in_boundary()

            if self.speed % 2 == 0:
                if not bonus_flag:
                    bonus_flag = True
                    fixed_iteration = iteration
                    bonus = Food(self.get_random_block(), FoodType.scoreUp)
            else:
                bonus_flag = False
                
            if bonus_flag:
                if iteration - fixed_iteration >= 20:
                    bonus = Food(empty_block, FoodType.scoreUp)
                if bonus.block == head:
                    self.score += 10
                    bonus = Food(empty_block, FoodType.scoreUp)
                else:
                    self.draw_block(Color.yellow, bonus.block.x, bonus.block.y)

            flag = True
            if apple.block == head:
                self.score += 1
                if apple.type == FoodType.lengthUp:
                    flag = False
                if apple.type == FoodType.speedUp:
                    if not cheatsK:
                        self.speed += 1
                if self.score % 5 == 0:
                    apple = Food(self.get_random_block(), FoodType.speedUp)
                else:
                    apple = Food(self.get_random_block(), FoodType.lengthUp)
            else:
                flag = True
            
            new_head = Block(head.x + d_x, head.y + d_y, Propirties.blocks_amount)

            if (not cheatsB) and (new_head in self.snake_blocks or new_head in self.walls):
                if self.lives == 1:
                    pygame.mixer.music.stop()
                    break
                if iteration - deathless_iteration > 5:
                    self.lives -= 1
                    deathless_iteration = iteration

            self.snake_blocks.append(new_head)
            if flag or cheatsK:
                self.snake_blocks.pop(0)

            pygame.display.flip()
            iteration += 1
            self.timer.tick(3 + self.speed)
        
    def draw_window(self):
        self.screen.fill(Color.black)
        pygame.draw.rect(self.screen, Color.HEADER_COLOR, [0,0,self.size[0], Propirties.up_length])

    def draw_block(self, color, row, column):
        pygame.draw.rect(self.screen, color, [Propirties.block_size + column*Propirties.block_size+Propirties.delta*(column+1),
                                                Propirties.up_length+Propirties.block_size+row*Propirties.block_size+Propirties.delta*(row+1),
                                                Propirties.block_size,
                                                Propirties.block_size])

    def get_random_block(self):
        x = random.randint(0, Propirties.blocks_amount - 1)
        y = random.randint(0, Propirties.blocks_amount - 1)
        empty_block = Block(x, y, Propirties.blocks_amount)
        while empty_block in self.snake_blocks or empty_block in self.walls:
            x = random.randint(0, Propirties.blocks_amount - 1)
            y = random.randint(0, Propirties.blocks_amount - 1)
        return empty_block

    def draw_env(self, apple):
        for row in range(Propirties.blocks_amount):
            for column in range(Propirties.blocks_amount):
                self.draw_block(Color.white, row, column)
            
        for wall in self.walls:
            self.draw_block(Color.black, wall.x, wall.y)
            
        if apple.type == FoodType.lengthUp:
            self.draw_block(Color.red, apple.block.x, apple.block.y)
        elif apple.type == FoodType.speedUp:
            self.draw_block(Color.gray, apple.block.x, apple.block.y)

        for block in self.snake_blocks:
            self.draw_block(Color.green, block.x, block.y)

    def draw_text(self):
        courier = pygame.font.SysFont('courier', 18)
        text_total = courier.render(f"Score: {self.score}", 0, Color.white)
        text_speed = courier.render(f"Speed: {self.speed}", 0, Color.white)
        text_lives = courier.render(f"Lives: {self.lives}", 0, Color.white)
        self.screen.blit(text_total, (Propirties.block_size, Propirties.block_size))
        self.screen.blit(text_speed, (Propirties.block_size+150, Propirties.block_size))
        self.screen.blit(text_lives, (Propirties.block_size+300, Propirties.block_size))