from Classes.Game import *
from Classes.Block import *


def save():
    f = open("save.txt", "w")
    f.write(str(Info.current_level) + "\n")
    f.write(str(Info.score) + "\n")
    f.write(str(Info.lives) + "\n")
    f.write(str(Info.blocks_amount) + "\n")
    f.write(str(Info.lvl_req) + "\n")
    f.write(str(Info.d_x) + "\n")
    f.write(str(Info.d_y) + "\n")
    f.write(str(Info.speed) + "\n")

    for block in Info.snake_blocks:
        f.write(f"{block.x},{block.y};")
    f.write("\n")   
    for block in Info.walls:
        f.write(f"{block.x},{block.y};")


def load_save():
    f = open("save.txt", "r")
    Info.current_level = int(f.readline())
    Info.score = int(f.readline())
    Info.lives = int(f.readline())
    Info.blocks_amount = int(f.readline())
    Info.lvl_req = int(f.readline())
    Info.d_x = int(f.readline())
    Info.d_y = int(f.readline())
    Info.speed = int(f.readline())

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
