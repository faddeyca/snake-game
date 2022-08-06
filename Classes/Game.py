import pygame
import random

from Classes.Block import *
from Classes.Food import *
from Classes.Properties import *
from Classes.Colors import *
from Classes.Sounds import *
from Classes.Level_Info import Info
import Classes.MotionHandler as mh


class Game:
    """
    A class to represent the game.

    ...

    Attributes
    ----------
    size : [int, int]
        Current pygame screen size
    screen : pygame.display
        Current screen
    timer : pygame.time.Clock
        Timer for iterations check


    Methods
    -------
    put_in_boundary():
        Puts the block in field's boundary.
    """
    def __init__(self):
        '''
        Initializes the level
        '''
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
        if not Info.started_from_save:
            Info.apple = Food(self.get_random_block(), FoodType.lengthUp)
            Info.bonus_food = Food(Block(-100, -100), FoodType.scoreUp)

        Info.pause = 1

        while 1:
            move_stack = mh.read_input()

            if move_stack == 0:
                return 0

            result_of_iteration = 0
            skipped_sum = 0
            flag = True
            if len(move_stack) == 1:
                f = move_stack.pop()
                f()
                Info.pause = 0
            while len(move_stack) != 0 and skipped_sum != len(move_stack):
                skipped_sum = 0
                for i in range(len(move_stack)):
                    f = move_stack[i]
                    res = f()
                    if res:
                        skipped_sum = 0
                        del move_stack[i]
                        Info.pause = 0
                        flag = False
                        result_of_iteration = self.Execute_iteration()
                        break
                    else:
                        skipped_sum += 1
                    if skipped_sum == len(move_stack):
                        break

            if flag:
                result_of_iteration = self.Execute_iteration()
            if result_of_iteration != -1:
                return result_of_iteration

    def Execute_iteration(self, double=False):
        '''
        Processing one iteration with drawnings and movings
        '''
        self.draw_window()
        self.draw_text()

        head = Info.snake_blocks[-1]
        head.put_in_boundary()

        self.draw_env()

        if not Info.pause:
            self.generate_bonus_food(head)

            length_flag = 1
            if Info.apple.block == head:
                length_flag = self.eat_food()
            else:
                length_flag = 1

            new_head = Block(head.x + Info.d_x, head.y + Info.d_y)

            if not Info.cheatsB:
                if new_head in Info.snake_blocks or new_head in Info.walls:
                    self.get_damage()

            Info.snake_blocks.append(new_head)
            if length_flag or Info.cheatsK:
                Info.snake_blocks.pop(0)
            if Info.cheatsK and not length_flag:
                Info.lvl_req -= 1
            Info.iteration += 1

        return self.end_iteration_processing(double)

    def get_damage(self):
        '''
        Snake damage processing
        '''
        if Info.iteration - Info.deathless_iteration > 5:
            Sounds.hurt_sound.play()
            Info.lives -= 1
            Info.deathless_iteration = Info.iteration

    def eat_food(self):
        '''
        Food eating processing
        '''
        length_flag = 1
        Info.score += 1
        if Info.apple.type == FoodType.lengthUp:
            Sounds.eating_sound.play()
            length_flag = 0
        elif Info.apple.type == FoodType.speedUp:
            Sounds.drink_sound.play()
            if not Info.cheatsK:
                Info.speed += 1
        if Info.score % 5 == 0:
            Info.apple = Food(self.get_random_block(), FoodType.speedUp)
        else:
            Info.apple = Food(self.get_random_block(),
                              FoodType.lengthUp)
        return length_flag

    def end_iteration_processing(self, double):
        '''
        Iteration end processing
        '''
        pygame.display.flip()
        if not double:
            self.timer.tick(3 + Info.speed)
        else:
            self.timer.tick(1 + Info.speed)
        if Info.lives == 0:
            Sounds.death_sound.play()
            return 0
        if len(Info.snake_blocks) >= Info.lvl_req + 1:
            Sounds.bonus_sound.play()
            return 1
        return -1

    def generate_bonus_food(self, head):
        '''
        Generates bonus food
        '''
        self.create_bonus_food()

        if Info.bonus_flag:
            self.bonus_food_processing(head)

    def bonus_food_processing(self, head):
        if Info.iteration - Info.bonus_food_iteration >= 20:
            Info.bonus_food = Food(Block(-100, -100), FoodType.scoreUp)
        if Info.bonus_food.block == head:
            Sounds.bonus_sound.play()
            Info.score += 10
            Info.bonus_food = Food(Block(-100, -100), FoodType.scoreUp)
        else:
            if Info.iteration % 2 == 0:
                self.draw_block(Color.yellow,
                                Info.bonus_food.block.x,
                                Info.bonus_food.block.y)
            else:
                self.draw_block(Color.green,
                                Info.bonus_food.block.x,
                                Info.bonus_food.block.y)

    def create_bonus_food(self):
        if Info.speed % 2 == 0:
            if not Info.bonus_flag:
                Info.bonus_flag = 1
                Info.bonus_food_iteration = Info.iteration
                Info.bonus_food = Food(self.get_random_block(),
                                       FoodType.scoreUp)
        else:
            Info.bonus_flag = 0

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

    def draw_window(self):
        '''
        Draws window
        '''
        self.screen.fill(Color.black)
        pygame.draw.rect(self.screen, Color.up_menu,
                         [0, 0, self.size[0], Prop.up_length])

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

    def draw_text(self):
        '''
        Draws text in up menu:
        score, curreent speed, lives left, Info.apples to eat left
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
