import pygame

class Bird(pygame.sprite.Sprite):
    def __init__(self, bird_type, bird_image):
        super().__init__()
        self.image = bird_image
        self.bird_type = bird_type
        self.selected = False
        self.rect = self.image.get_rect()


    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.bird_type))
    ''' - '''

    def __str__(self):
        return f"({str(self.bird_type)})"

