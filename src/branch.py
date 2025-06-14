import pygame
from collections import deque
from bird import Bird

class Branch(pygame.sprite.Sprite):
    branch_size = 4

    def __init__(self, x, y, birds, image, side="left"):
        super().__init__()
        self.x = x
        self.y = y
        self.original_image = image if side == "left" else pygame.transform.flip(image, True, False)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.birds = birds  # Stack to hold bird objects
        self.completed = False
        self.side = side
        self.selected = False

    def update_color(self):
        if self.selected:
            yellow_overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            yellow_overlay.fill((255, 255, 0, 100)) 
            self.image = self.original_image.copy() 
            self.image.blit(yellow_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT) 
        else:
            self.image = self.original_image.copy()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.x == other.x and
                self.y == other.y and
                self.birds == other.birds)
    
    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.x, self.y, tuple(self.birds)))
    ''' - '''

    def __str__(self):
        """String representation of the branch for debugging."""
        birds_str = " ".join(f"({bird.bird_type})" for bird in self.birds)
        status = " Completed" if self.completed else ""
        return f"(Pos: {self.x}, {self.y}, Birds: {birds_str}){status}"


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
            n = 1
            while n < len(self.birds) and self.birds[-(n+1)] == bird:
                n += 1
            return (bird, n)
        return (None, 0)
    
    def is_empty(self):
        return not self.birds

    def full_one_species(self):
        if len(self.birds) == 0:
            return False
        top_birds = self.get_top()
        if top_birds[1] == Branch.branch_size:
            return True
        return False
    
    def evaluate(self):
        points = 0
        if self.full_one_species():
            points += 100
        current_bird = None
        if self.birds:
            for bird in self.birds:
                if bird == current_bird:
                    points += 1
                current_bird = bird
        return points
    
    @classmethod
    def set_branch_size(cls, new_size):
        cls.branch_size = new_size  # Update class-wide branch size

    @staticmethod
    def clone_all_branches(branches, branch_image):
        cloned = []
        for branch in branches:
            new_birds = [Bird(bird.bird_type, bird.image) for bird in branch.birds]
            new_branch = Branch(branch.x, branch.y, new_birds, branch_image, branch.side)
            new_branch.completed = branch.completed
            cloned.append(new_branch)
        return cloned
        
    def highlight(self):
        red_overlay = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        red_overlay.fill((255, 0, 0, 100))  # Red with 100 alpha (transparency)
        self.image = self.original_image.copy()
        self.image.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)