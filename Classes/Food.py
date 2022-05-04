from enum import Enum


class Food:
    """
    A class to represent a food.

    ...

    Attributes
    ----------
    block : Block
        Food as block(position)
    type : FoodType
        Type
    """
    def __init__(self, block, type):
        self.block = block
        self.type = type


class FoodType(Enum):
    """
    A class to represent a food type.
    """
    #  Increase the length of the snake
    lengthUp = 0
    #  Increase the speed of the snake
    speedUp = 1
    #  Give additional score to player
    scoreUp = 2
