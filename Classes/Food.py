from enum import Enum


class Food:
    """
    A class to represent a food

    ...

    Attributes
    ----------
    block : Block
        Food as block(position)
    type : FoodType
        Type of food
    """
    def __init__(self, block, type):
        '''
        Initializes food
        '''
        self.block = block
        self.type = type

    def __eq__(self, other):
        '''
        Compares food
        '''
        is_this_type = isinstance(other, Food)
        if is_this_type:
            return self.block == other.block and self.type == other.type
        return False


class FoodType(Enum):
    """
    A class to represent a food type
    """
    #  Increase the length of the snake
    lengthUp = 0
    #  Increase the speed of the snake
    speedUp = 1
    #  Give additional score to player
    scoreUp = 2


def enum_to_int(food):
    '''
    Converts enum to int
    '''
    if food == FoodType.lengthUp:
        return 0
    if food == FoodType.speedUp:
        return 1
    if food == FoodType.scoreUp:
        return 2


def int_to_enum(i):
    '''
    Converts int to enum
    '''
    if i == 0:
        return FoodType.lengthUp
    if i == 1:
        return FoodType.speedUp
    if i == 2:
        return FoodType.scoreUp
