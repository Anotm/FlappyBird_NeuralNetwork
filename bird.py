import pygame 
from const import *

class Bird(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.x = BIRD_STARTING_X
        self.y = BIRD_STARTING_Y
        self.time = 0 
        self.velocity = 0 
        self.display_surface = pygame.display.get_surface()
        self.add_time = 0
        self.pipes_passed = 0
    
    def move(self, delta_time):
        self.add_time += delta_time
        # print(self.add_time)
        if self.add_time < 0.01: 
            return
        
        self.time += 1
        self.add_time = 0
        displacement = self.velocity * self.time +  0.5 * BIRD_ACC * self.time ** 2
        if displacement > BIRD_MAX_DISPLACEMENT:
            displacement = BIRD_MAX_DISPLACEMENT
        
        self.y += displacement
    
    def jump(self): 
        self.velocity = BIRD_JUMP_VELOCITY
        self.time = 0
    
    def render(self):
        pygame.draw.circle(self.display_surface, (255, 0, 0), (int(self.x), int(self.y)), BIRD_RADIUS)