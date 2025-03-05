import pygame

class Branch(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.birds = []  # Holds bird objects

    def add_bird(self, bird):
        if len(self.birds) < 3:  # Example limit of 3 birds per branch
            self.birds.append(bird)
            bird.rect.center = (self.rect.centerx, self.rect.top - (len(self.birds) * 50))
            return True
        return False
