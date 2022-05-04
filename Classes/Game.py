import pygame
import sys
import random

from Classes.Block import *
from Classes.Food import *
from Classes.Propirties import *
from Classes.Colors import *
from Classes.Sounds import *


class Game:
    """
    A class to represent a level.

    ...

    Attributes
    ----------
    size : [int, int]
        Current pygame screen size
    screen : pygame.display
        Current screen

    d_x : int
        Snake's direction in row
    d_y : int
        Snake's direction in column
    speed : int
        Current snake's speed
    snake_blocks : Blocks array
        Snake's body and head array: (0) - tail, (-1) - head
    walls : Blocks array
        Walls positions
    lvl_req : int
        Required length of the snake to win this level
    timer : pygame.time.Clock
        Timer for iterations check
    

    Methods
    -------
    put_in_boundary():
        Puts the block in field's boundary.
    """
    def __init__(self, snake_blocks, walls, lvl_req):
        self.size = [Prop.block_size * Info.blocks_amount +
                     2 * Prop.block_size + Prop.delta * Info.blocks_amount,
                     Prop.block_size * Info.blocks_amount +
                     2 * Prop.block_size+Prop.delta * Info.blocks_amount +
                     Prop.up_length]
        self.screen = pygame.display.set_mode(self.size)

        self.d_x = 0
        self.d_y = 0
        self.speed = 1

        self.snake_blocks = snake_blocks
        self.walls = walls
        self.lvl_req = lvl_req

        self.timer = pygame.time.Clock()

    def start(self):
        '''
        Starts the level
        '''
        iteration = 0
        fixed_iteration = 0
        deathless_iteration = 0

        far_block = Block(-100, -100)

        apple = Food(self.get_random_block(), FoodType.lengthUp)
        bonus = Food(far_block, FoodType.scoreUp)

        bonus_flag = False

        cheatsB = False
        cheatsK = False

        pause = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and (self.d_y != 0 or pause):
                        self.d_x = -1
                        self.d_y = 0
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and (self.d_y or pause) != 0:
                        self.d_x = 1
                        self.d_y = 0
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and (self.d_x or pause) != 0:
                        self.d_x = 0
                        self.d_y = -1
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and (self.d_x or pause) != 0:
                        self.d_x = 0
                        self.d_y = 1
                    elif event.key == pygame.K_b:
                        cheatsB = not cheatsB
                    elif event.key == pygame.K_k:
                        cheatsK = not cheatsK
                    elif event.key == pygame.K_m:
                        Info.score += 100
                    elif event.key == pygame.K_ESCAPE:
                        pause = True
                        self.d_x = 0
                        self.d_y = 0

            if self.d_x != 0 or self.d_y != 0:
                pause = False

            self.draw_window()
            self.draw_text()

            head = self.snake_blocks[-1]
            head.put_in_boundary()

            self.draw_env(apple)

            if not pause:
                if self.speed % 2 == 0:
                    if not bonus_flag:
                        bonus_flag = True
                        fixed_iteration = iteration
                        bonus = Food(self.get_random_block(), FoodType.scoreUp)
                else:
                    bonus_flag = False

                if bonus_flag:
                    if iteration - fixed_iteration >= 20:
                        bonus = Food(far_block, FoodType.scoreUp)
                    if bonus.block == head:
                        Sounds.bonus_sound.play()
                        Info.score += 10
                        bonus = Food(far_block, FoodType.scoreUp)
                    else:
                        if iteration % 2 == 0:
                            self.draw_block(Color.yellow,
                                        bonus.block.x, bonus.block.y)
                        else:
                            self.draw_block(Color.green,
                                        bonus.block.x, bonus.block.y)

                length_flag = True
                if apple.block == head:
                    Info.score += 1
                    if apple.type == FoodType.lengthUp:
                        Sounds.eating_sound.play()
                        length_flag = False
                        if len(self.snake_blocks) == self.lvl_req:
                            return True
                    if apple.type == FoodType.speedUp:
                        Sounds.drink_sound.play()
                        if not cheatsK:
                            self.speed += 1
                    if Info.score % 5 == 0:
                        apple = Food(self.get_random_block(), FoodType.speedUp)
                    else:
                        apple = Food(self.get_random_block(),
                                     FoodType.lengthUp)
                else:
                    length_flag = True

                new_head = Block(head.x + self.d_x, head.y + self.d_y)

                if (not cheatsB) and (new_head in self.snake_blocks or new_head in self.walls):
                    if iteration - deathless_iteration > 5:
                        Sounds.hurt_sound.play()
                        Info.lives -= 1
                        if Info.lives == 0:
                            Sounds.death_sound.play()
                            return False
                        deathless_iteration = iteration

                self.snake_blocks.append(new_head)
                if length_flag or cheatsK:
                    self.snake_blocks.pop(0)
                if cheatsK and not length_flag:
                    self.lvl_req -= 1

            pygame.display.flip()
            iteration += 1
            self.timer.tick(3 + self.speed)

    def draw_window(self):
        '''
        Draws window
        '''
        self.screen.fill(Color.black)
        pygame.draw.rect(self.screen, Color.up_menu,
                         [0, 0, self.size[0], Prop.up_length])

    def draw_block(self, color, row, column):
        '''
        Draws a block withs specific parameters.

            Parameters:
                    color (Color): A color of the block
                    row (int): Position in row
                    column (int): Position in column
        '''
        pygame.draw.rect(self.screen, color, [Prop.block_size +
                                              column * Prop.block_size +
                                              Prop.delta * (column + 1),
                                              Prop.up_length +
                                              Prop.block_size +
                                              row * Prop.block_size +
                                              Prop.delta * (row + 1),
                                              Prop.block_size,
                                              Prop.block_size])

    def get_random_block(self):
        '''
        Returns a random block that is not a wall or a part of snake.

            Returns:
                    empty_block (Block): Random empty block
        '''
        x = random.randint(0, Info.blocks_amount - 1)
        y = random.randint(0, Info.blocks_amount - 1)
        empty_block = Block(x, y)
        while empty_block in self.snake_blocks or empty_block in self.walls:
            x = random.randint(0, Info.blocks_amount - 1)
            y = random.randint(0, Info.blocks_amount - 1)
            empty_block = Block(x, y)
        return empty_block

    def draw_env(self, apple):
        '''
        Draws all blocks: field, walls, apples, snake, snake's head.
        '''
        for row in range(Info.blocks_amount):
            for column in range(Info.blocks_amount):
                self.draw_block(Color.white, row, column)

        for wall in self.walls:
            self.draw_block(Color.black, wall.x, wall.y)

        if apple.type == FoodType.lengthUp:
            self.draw_block(Color.red, apple.block.x, apple.block.y)
        elif apple.type == FoodType.speedUp:
            self.draw_block(Color.gray, apple.block.x, apple.block.y)

        for i in range(len(self.snake_blocks) - 1):
            self.draw_block(Color.snake_body,
                            self.snake_blocks[i].x, self.snake_blocks[i].y)

        self.draw_block(Color.snake_head,
                        self.snake_blocks[-1].x, self.snake_blocks[-1].y)

    def draw_text(self):
        '''
        Draws text in up menu: score, curreent speed, lives left, apples to eat left
        '''
        k = Info.blocks_amount / 20
        courier = pygame.font.SysFont('courier', int(25 * k))
        text_score = courier.render(f"Score: {Info.score}", 0, Color.white)
        text_speed = courier.render(f"Speed: {self.speed}", 0, Color.white)
        text_lives = courier.render(f"Lives: {Info.lives}", 0, Color.white)
        left = self.lvl_req - len(self.snake_blocks) + 1
        text_left = courier.render(f"Left: {left}", 0, Color.white)
        self.screen.blit(text_score, (20, 20))
        self.screen.blit(text_speed, (50 + int(150 * k), 20))
        self.screen.blit(text_lives, (20, 60))
        self.screen.blit(text_left, (50 + int(150 * k), 60))
