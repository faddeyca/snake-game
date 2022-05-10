import pygame
import sys
import random

from Classes.Block import *
from Classes.Food import *
from Classes.Propirties import *
from Classes.Colors import *
from Classes.Sounds import *
from Classes.Level_Info import Info
from Classes.Saver import save


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
    def __init__(self):
        self.size = [Prop.block_size * Info.blocks_amount +
                     2 * Prop.block_size + Prop.delta * Info.blocks_amount,
                     Prop.block_size * Info.blocks_amount +
                     2 * Prop.block_size + Prop.delta * Info.blocks_amount +
                     Prop.up_length]
        self.screen = pygame.display.set_mode(self.size)

        self.timer = pygame.time.Clock()

    def start(self):
        '''
        Starts the level
        '''
        self.far_block = Block(-100, -100)

        if not Info.started_from_save:
            Info.apple = Food(self.get_random_block(), FoodType.lengthUp)
            Info.bonus_food = Food(self.far_block, FoodType.scoreUp)

        self.pause = 1

        self.st = []

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and (Info.d_y != 0 or self.pause):
                        self.st.append(lambda: self.Move_up())
                    if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and (Info.d_y or self.pause) != 0:
                        self.st.append(lambda: self.Move_down())
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and (Info.d_x or self.pause) != 0:
                        self.st.append(lambda: self.Move_left())
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and (Info.d_x or self.pause) != 0:
                        self.st.append(lambda: self.Move_right())
                    if event.key == pygame.K_b:
                        Info.cheatsB = (Info.cheatsB) + 1 % 2
                    if event.key == pygame.K_k:
                        Info.cheatsK = (Info.cheatsK) + 1 % 2
                    if event.key == pygame.K_m:
                        Info.score += 100
                    if event.key == pygame.K_ESCAPE:
                        if self.pause:
                            return 0
                        self.pause = 1
                        Info.d_x = 0
                        Info.d_y = 0
                    if event.key == pygame.K_p:
                        if self.pause:
                            save()
            if len(self.st) > 0:
                f = self.st.pop()
                f()
                self.Move()
            if len(self.st) > 0:
                f = self.st.pop()
                f()
                self.Move()
            self.Move()


    def Move_up(self):
        Info.d_x = -1
        Info.d_y = 0

    def Move_down(self):
        Info.d_x = 1
        Info.d_y = 0

    def Move_left(self):
        Info.d_x = 0
        Info.d_y = -1

    def Move_right(self):
        Info.d_x = 0
        Info.d_y = 1

    def Move(self):
        if Info.d_x != 0 or Info.d_y != 0:
            self.pause = 0

        self.draw_window()
        self.draw_text()

        head = Info.snake_blocks[-1]
        head.put_in_boundary()

        self.draw_env()

        if not self.pause:
            if Info.speed % 2 == 0:
                if not Info.bonus_flag:
                    Info.bonus_flag = 1
                    Info.fixed_iteration = Info.iteration
                    Info.bonus_food = Food(self.get_random_block(), FoodType.scoreUp)
            else:
                Info.bonus_flag = 0

            if Info.bonus_flag:
                if Info.iteration - Info.fixed_iteration >= 20:
                    Info.bonus_food = Food(self.far_block, FoodType.scoreUp)
                if Info.bonus_food.block == head:
                    Sounds.bonus_sound.play()
                    Info.score += 10
                    Info.bonus_food = Food(self.far_block, FoodType.scoreUp)
                else:
                    if Info.iteration % 2 == 0:
                        self.draw_block(Color.yellow,
                                    Info.bonus_food.block.x, Info.bonus_food.block.y)
                    else:
                        self.draw_block(Color.green,
                                    Info.bonus_food.block.x, Info.bonus_food.block.y)

            length_flag = 1
            if Info.apple.block == head:
                Info.score += 1
                if Info.apple.type == FoodType.lengthUp:
                    Sounds.eating_sound.play()
                    length_flag = 0
                    if len(Info.snake_blocks) == Info.lvl_req:
                        return 1
                if Info.apple.type == FoodType.speedUp:
                    Sounds.drink_sound.play()
                    if not Info.cheatsK:
                        Info.speed += 1
                if Info.score % 5 == 0:
                    Info.apple = Food(self.get_random_block(), FoodType.speedUp)
                else:
                    Info.apple = Food(self.get_random_block(),
                                    FoodType.lengthUp)
            else:
                length_flag = 1

            new_head = Block(head.x + Info.d_x, head.y + Info.d_y)

            if (not Info.cheatsB) and (new_head in Info.snake_blocks or new_head in Info.walls):
                if Info.iteration - Info.deathless_iteration > 5:
                    Sounds.hurt_sound.play()
                    Info.lives -= 1
                    if Info.lives == 0:
                        Sounds.death_sound.play()
                        return 0
                    Info.deathless_iteration = Info.iteration

            Info.snake_blocks.append(new_head)
            if length_flag or Info.cheatsK:
                Info.snake_blocks.pop(0)
            if Info.cheatsK and not length_flag:
                Info.lvl_req -= 1
            Info.iteration += 1

        pygame.display.flip()
        self.timer.tick(1)

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
        while empty_block in Info.snake_blocks or empty_block in Info.walls:
            x = random.randint(0, Info.blocks_amount - 1)
            y = random.randint(0, Info.blocks_amount - 1)
            empty_block = Block(x, y)
        return empty_block

    def draw_env(self):
        '''
        Draws all blocks: field, walls, Info.apples, snake, snake's head.
        '''
        for row in range(Info.blocks_amount):
            for column in range(Info.blocks_amount):
                self.draw_block(Color.white, row, column)

        for wall in Info.walls:
            self.draw_block(Color.black, wall.x, wall.y)

        if Info.apple.type == FoodType.lengthUp:
            self.draw_block(Color.red, Info.apple.block.x, Info.apple.block.y)
        elif Info.apple.type == FoodType.speedUp:
            self.draw_block(Color.gray, Info.apple.block.x, Info.apple.block.y)

        for i in range(len(Info.snake_blocks) - 1):
            self.draw_block(Color.snake_body,
                            Info.snake_blocks[i].x, Info.snake_blocks[i].y)

        self.draw_block(Color.snake_head,
                        Info.snake_blocks[-1].x, Info.snake_blocks[-1].y)

    def draw_text(self):
        '''
        Draws text in up menu: score, curreent speed, lives left, Info.apples to eat left
        '''
        k = Info.blocks_amount / 20
        courier = pygame.font.SysFont('courier', int(25 * k))
        text_score = courier.render(f"Score: {Info.score}", 0, Color.white)
        text_speed = courier.render(f"Speed: {Info.speed}", 0, Color.white)
        text_lives = courier.render(f"Lives: {Info.lives}", 0, Color.white)
        left = Info.lvl_req - len(Info.snake_blocks) + 1
        text_left = courier.render(f"Left: {left}", 0, Color.white)
        self.screen.blit(text_score, (20, 20))
        self.screen.blit(text_speed, (50 + int(150 * k), 20))
        self.screen.blit(text_lives, (20, 60))
        self.screen.blit(text_left, (50 + int(150 * k), 60))
