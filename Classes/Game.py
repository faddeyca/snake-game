import pygame
import sys
import random

from Classes.Block import *
from Classes.Food import *
from Classes.Propirties import *
from Classes.Colors import *
from Classes.Sounds import *


class Game:
    def __init__(self, screen, size, snake_blocks, walls, lvl_req, d_x, d_y):

        self.screen = screen
        self.size = size

        self.snake_blocks = snake_blocks
        self.walls = walls
        self.lvl_req = lvl_req

        self.d_x = d_x
        self.d_y = d_y

        self.timer = pygame.time.Clock()
        self.speed = 1

    def start(self):
        iteration = 0
        fixed_iteration = 0
        deathless_iteration = 0

        far_block = Block(-100, -100)

        apple = Food(self.get_random_block(), FoodType.lengthUp)
        bonus = Food(far_block, FoodType.scoreUp)

        bonus_flag = False

        cheatsB = False
        cheatsK = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.d_y != 0:
                        self.d_x = -1
                        self.d_y = 0
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.d_y != 0:
                        self.d_x = 1
                        self.d_y = 0
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.d_x != 0:
                        self.d_x = 0
                        self.d_y = -1
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.d_x != 0:
                        self.d_x = 0
                        self.d_y = 1
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

            head = self.snake_blocks[-1]
            head.put_in_boundary()

            self.draw_env(apple)

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
                    self.draw_block(Color.yellow, bonus.block.x, bonus.block.y)

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
                    apple = Food(self.get_random_block(), FoodType.lengthUp)
            else:
                length_flag = True

            new_head = Block(head.x + self.d_x, head.y + self.d_y)

            if (not cheatsB) and (new_head in self.snake_blocks or new_head in self.walls):
                if Info.lives == 1:
                    Sounds.death_sound.play()
                    return False
                if iteration - deathless_iteration > 5:
                    Sounds.hurt_sound.play()
                    Info.lives -= 1
                    deathless_iteration = iteration

            self.snake_blocks.append(new_head)
            if length_flag or cheatsK:
                self.snake_blocks.pop(0)

            pygame.display.flip()
            iteration += 1
            self.timer.tick(3 + self.speed)

    def draw_window(self):
        self.screen.fill(Color.black)
        pygame.draw.rect(self.screen, Color.HEADER_COLOR, [0, 0, self.size[0], Prop.up_length])

    def draw_block(self, color, row, column):
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
        x = random.randint(0, Prop.blocks_amount - 1)
        y = random.randint(0, Prop.blocks_amount - 1)
        empty_block = Block(x, y)
        while empty_block in self.snake_blocks or empty_block in self.walls:
            x = random.randint(0, Prop.blocks_amount - 1)
            y = random.randint(0, Prop.blocks_amount - 1)
        return empty_block

    def draw_env(self, apple):
        for row in range(Prop.blocks_amount):
            for column in range(Prop.blocks_amount):
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
        text_total = courier.render(f"Score: {Info.score}", 0, Color.white)
        text_speed = courier.render(f"Speed: {self.speed}", 0, Color.white)
        text_lives = courier.render(f"Lives: {Info.lives}", 0, Color.white)
        self.screen.blit(text_total, (Prop.block_size, Prop.block_size))
        self.screen.blit(text_speed, (Prop.block_size+150, Prop.block_size))
        self.screen.blit(text_lives, (Prop.block_size+300, Prop.block_size))
