import pygame 
from const import *

class Pipe(pygame.sprite.Sprite):
    def __init__(self, y, height, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((PIPE_WIDTH, height))
        self.image.fill(PIPE_COLOR)
        self.rect = self.image.get_rect(topleft=(GAME_WIDTH, y))
        self.move_time = 0
        self.display_surface = pygame.display.get_surface()
        self.height = height

    def update(self, delta_time):
        # Move pipe to the left
        self.move_time += delta_time
        if self.move_time >= MOVE_TIME:
            self.rect.x -= PIPE_SPEED
            self.move_time = 0

        # Remove pipe if it moves off-screen
        if self.rect.right < 0:
            self.kill()

    def render(self):
        pygame.draw.rect(self.display_surface, PIPE_COLOR, self.rect)