import pygame

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, bird_type, bird_images):
        super().__init__()
        self.image = bird_images[bird_type]
        self.rect = self.image.get_rect(center=(x, y))
        self.bird_type = bird_type
        self.selected = False

    def update(self):
        # Visual effect when selected
        if self.selected:
            self.rect.y -= 2  # Small lift effect
        else:
            self.rect.y += 2  # Reset position
