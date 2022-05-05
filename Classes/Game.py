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
                     2 * Prop.block_size+Prop.delta * Info.blocks_amount +
                     Prop.up_length]
        self.screen = pygame.display.set_mode(self.size)

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
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and (Info.d_y != 0 or pause):
                        Info.d_x = -1
                        Info.d_y = 0
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and (Info.d_y or pause) != 0:
                        Info.d_x = 1
                        Info.d_y = 0
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and (Info.d_x or pause) != 0:
                        Info.d_x = 0
                        Info.d_y = -1
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and (Info.d_x or pause) != 0:
                        Info.d_x = 0
                        Info.d_y = 1
                    elif event.key == pygame.K_b:
                        cheatsB = not cheatsB
                    elif event.key == pygame.K_k:
                        cheatsK = not cheatsK
                    elif event.key == pygame.K_m:
                        Info.score += 100
                    elif event.key == pygame.K_ESCAPE:
                        if pause:
                            return False
                        pause = True
                        Info.d_x = 0
                        Info.d_y = 0
                    elif event.key == pygame.K_p:
                        if pause:
                            save()


            if Info.d_x != 0 or Info.d_y != 0:
                pause = False

            self.draw_window()
            self.draw_text()

            head = Info.snake_blocks[-1]
            head.put_in_boundary()

            self.draw_env(apple)

            if not pause:
                if Info.speed % 2 == 0:
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
                        if len(Info.snake_blocks) == Info.lvl_req:
                            return True
                    if apple.type == FoodType.speedUp:
                        Sounds.drink_sound.play()
                        if not cheatsK:
                            Info.speed += 1
                    if Info.score % 5 == 0:
                        apple = Food(self.get_random_block(), FoodType.speedUp)
                    else:
                        apple = Food(self.get_random_block(),
                                     FoodType.lengthUp)
                else:
                    length_flag = True

                new_head = Block(head.x + Info.d_x, head.y + Info.d_y)

                if (not cheatsB) and (new_head in Info.snake_blocks or new_head in Info.walls):
                    if iteration - deathless_iteration > 5:
                        Sounds.hurt_sound.play()
                        Info.lives -= 1
                        if Info.lives == 0:
                            Sounds.death_sound.play()
                            return False
                        deathless_iteration = iteration

                Info.snake_blocks.append(new_head)
                if length_flag or cheatsK:
                    Info.snake_blocks.pop(0)
                if cheatsK and not length_flag:
                    Info.lvl_req -= 1

            pygame.display.flip()
            iteration += 1
            self.timer.tick(3 + Info.speed)

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

    def draw_env(self, apple):
        '''
        Draws all blocks: field, walls, apples, snake, snake's head.
        '''
        for row in range(Info.blocks_amount):
            for column in range(Info.blocks_amount):
                self.draw_block(Color.white, row, column)

        for wall in Info.walls:
            self.draw_block(Color.black, wall.x, wall.y)

        if apple.type == FoodType.lengthUp:
            self.draw_block(Color.red, apple.block.x, apple.block.y)
        elif apple.type == FoodType.speedUp:
            self.draw_block(Color.gray, apple.block.x, apple.block.y)

        for i in range(len(Info.snake_blocks) - 1):
            self.draw_block(Color.snake_body,
                            Info.snake_blocks[i].x, Info.snake_blocks[i].y)

        self.draw_block(Color.snake_head,
                        Info.snake_blocks[-1].x, Info.snake_blocks[-1].y)

    def draw_text(self):
        '''
        Draws text in up menu: score, curreent speed, lives left, apples to eat left
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
