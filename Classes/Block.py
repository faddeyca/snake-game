class Block:
    def __init__(self, x, y, COUNT_BLOCKS):
        self.x = x
        self.y = y
        self.COUNT_BLOCKS = COUNT_BLOCKS

    def __eq__(self, other):
        return isinstance(other, Block) and self.x == other.x and self.y == other.y

    def in_boundary(self):
        self.x += self.COUNT_BLOCKS
        self.x %= self.COUNT_BLOCKS
        self.y += self.COUNT_BLOCKS
        self.y %= self.COUNT_BLOCKS