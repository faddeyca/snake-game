from Classes.Block import *
from Classes.Food import *


def save():
    '''
    Writes everything from Info to file
    '''
    f = open("save.txt", "w")
    f.write(str(Info.current_level) + "\n")
    f.write(str(Info.score) + "\n")
    f.write(str(Info.lives) + "\n")
    f.write(str(Info.blocks_amount) + "\n")
    f.write(str(Info.lvl_req) + "\n")
    f.write(str(Info.d_x) + "\n")
    f.write(str(Info.d_y) + "\n")
    f.write(str(Info.speed) + "\n")
    f.write(str(Info.iteration) + "\n")
    f.write(str(Info.bonus_food_iteration) + "\n")
    f.write(str(Info.deathless_iteration) + "\n")
    f.write(str(Info.bonus_flag) + "\n")
    f.write(str(Info.cheatsB) + "\n")
    f.write(str(Info.cheatsK) + "\n")

    f.write(f"{Info.apple.block.x},{Info.apple.block.y}" + "\n")
    f.write(str(enum_to_int(Info.apple.type)) + "\n")
    f.write(f"{Info.bonus_food.block.x},{Info.bonus_food.block.y}" + "\n")
    f.write(str(enum_to_int(Info.bonus_food.type)) + "\n")

    for block in Info.snake_blocks:
        f.write(f"{block.x},{block.y};")
    f.write("\n")
    for block in Info.walls:
        f.write(f"{block.x},{block.y};")


def load_save():
    '''
    Reads file and writes Info
    '''
    try:
        f = open("save.txt", "r")
        Info.current_level = int(f.readline())
        Info.score = int(f.readline())
        Info.lives = int(f.readline())
        Info.blocks_amount = int(f.readline())
        Info.lvl_req = int(f.readline())
        Info.d_x = int(f.readline())
        Info.d_y = int(f.readline())
        Info.speed = int(f.readline())
        Info.iteration = int(f.readline())
        Info.bonus_food_iteration = int(f.readline())
        Info.deathless_iteration = int(f.readline())
        Info.bonus_flag = int(f.readline())
        Info.cheatsB = int(f.readline())
        Info.cheatsK = int(f.readline())

        block = f.readline()
        xy = block.split(',')
        type = int_to_enum(int(f.readline()))
        Info.apple = Food(Block(int(xy[0]), int(xy[1])), FoodType(type))

        block = f.readline()
        xy = block.split(',')
        type = int_to_enum(int(f.readline()))
        Info.bonus_food = Food(Block(int(xy[0]), int(xy[1])), FoodType(type))

        snake_blocks = f.readline().split(';')
        for block in snake_blocks:
            if block == '\n':
                continue
            xy = block.split(',')
            Info.snake_blocks.append(Block(int(xy[0]), int(xy[1])))
        walls = f.readline().split(';')
        for block in walls:
            if block == '\n' or len(block) <= 1:
                continue
            xy = block.split(',')
            Info.walls.append(Block(int(xy[0]), int(xy[1])))
    except FileNotFoundError:
        return -1
