import pygame
from collections import deque

class Branch(pygame.sprite.Sprite):
    branch_size = 2

    def __init__(self, x, y, birds, image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.birds = birds  # Stack to hold bird objects

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.x, self.y))
    ''' - '''

    def __str__(self):
        res = f"(Pos: {str(self.x)}, {str(self.y)}, Birds:"
        for bird in self.birds:
            res += f" {str(bird)}"
        res += ")"
        return res

    def add_birds(self, bird, n):
        if n > self.branch_size - len(self.birds):
            return False
        while n > 0:
            self.birds.append(bird)
            n -= 1
        return True
    
    def remove_birds(self, n):
        if n > len(self.birds):
            return False
        while n > 0:
            self.birds.pop()
            n -= 1
        return True
    
    def get_top(self):
        if self.birds:
            bird = self.birds[-1]
            curr_bird = bird
            n = 0
            while curr_bird == bird and n < len(self.birds):
                curr_bird = self.birds[-n]
                n += 1
            return (bird, n)
        return (None, 0)
    
    def is_empty(self):
        return not self.birds

    def full_one_species(self):
        top_birds = self.get_top()
        if top_birds[1] == Branch.branch_size:
            return True
        return False
    
    @classmethod
    def set_branch_size(cls, new_size):
        cls.branch_size = new_size  # Update class-wide branch size


        

