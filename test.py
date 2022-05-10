from Classes.Block import *
from Classes.Level_Info import *
from Classes.Food import *


def test_init():
    x = 3
    y = 5
    block = Block(x, y)
    assert block.x == x and block.y == y

def test_eq():
    block1 = Block(0, 0)
    block2 = Block(0, 0)
    assert block1 == block2

def test_not_eq():
    block1 = Block(0, 0)
    block2 = Block(1, 1)
    assert block1 != block2

def test_put_in_boundary():
    Info.blocks_amount = 5
    block = Block(5, 5)
    block.put_in_boundary()
    assert block.x == 0 and block.y == 0


def test_init():
    type = FoodType.scoreUp
    pos = Block(1, 1)
    food = Food(pos, type)
    assert food.block == pos and food.type == type  

def test_enum_to_int():
    type = FoodType.scoreUp
    number = enum_to_int(type)
    assert number == 2   

def test_int_to_enum():
    number = 1
    type = int_to_enum(number)
    assert type == FoodType.speedUp
