import pygame 
from const import BIRD_RADIUS

class GameDebugger:
    is_acitve = False


    @classmethod
    def draw(cls, birds, pipes):
        if not cls.is_acitve:
            return
        
        for bird in birds:
            pygame.draw.circle(bird.display_surface, (225, 0, 0), (int(bird.x), int(bird.y)), radius=BIRD_RADIUS,  width=2)

        for pipe in pipes:
            pygame.draw.rect(pipe.display_surface, (225,0,0), (pipe.rect.x, pipe.rect.y, pipe.width, pipe.height), 2)