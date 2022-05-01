from enum import Enum


class Food:
    def __init__(self, block, type):
        self.block = block
        self.type = type


class FoodType(Enum):
    lengthUp = 0
    speedUp = 1
    scoreUp = 2