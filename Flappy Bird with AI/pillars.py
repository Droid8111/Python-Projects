import pygame
import random

class Pillar:
    def __init__(self, screen_width, screen_height, gap_size, pillar_width, pillar_color, speed):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.gap_size = gap_size
        self.pillar_width = pillar_width
        self.pillar_color = pillar_color
        self.speed = speed
        self.pillars = []  # List of tuples: (top_pillar, bottom_pillar, scored_flag)

    def spawn_pillar(self):
        # Randomize the height of the gap
        gap_y = random.randint(self.gap_size, self.screen_height - self.gap_size)
        top_pillar_height = gap_y - self.gap_size // 2
        bottom_pillar_height = self.screen_height - gap_y - self.gap_size // 2

        # Create top and bottom pillars
        top_pillar = pygame.Rect(self.screen_width, 0, self.pillar_width, top_pillar_height)
        bottom_pillar = pygame.Rect(self.screen_width, gap_y + self.gap_size // 2, self.pillar_width, bottom_pillar_height)

        # Add the pillars to the list with a scored flag set to False
        self.pillars.append((top_pillar, bottom_pillar, False))

    def update_pillars(self):
        # Move pillars to the left
        for pair in self.pillars:
            pair[0].x -= self.speed
            pair[1].x -= self.speed

        # Remove pillars that are off-screen
        self.pillars = [pair for pair in self.pillars if pair[0].x + self.pillar_width > 0]

    def draw_pillars(self, screen):
        for top_pillar, bottom_pillar, _ in self.pillars:
            pygame.draw.rect(screen, self.pillar_color, top_pillar)
            pygame.draw.rect(screen, self.pillar_color, bottom_pillar)