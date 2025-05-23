import pygame

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gravity = 1
        self.lift = -13
        self.velocity = 0
        self.radius = 15  # Size of the bird

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        # Prevent the bird from falling below the screen
        if self.y > 600:  # Assuming screen height is 600
            self.y = 600
            self.velocity = 0

    def jump(self):
        self.velocity = self.lift

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, int(self.y)), self.radius)