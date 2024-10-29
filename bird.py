import pygame 
from const import *
import math

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

        self.img = pygame.image.load("./img/birds/bird0.png")
    
    def move(self, delta_time):
        self.add_time += delta_time
        # print(self.add_time)
        if self.add_time < 0.001: 
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
    
    def render(self, hitbox):
        if hitbox:
            pygame.draw.circle(self.display_surface, (255, 0, 0), (int(self.x), int(self.y)), BIRD_RADIUS)
        self.display_surface.blit(self.img, (int(self.x-BIRD_RADIUS-1), int(self.y-BIRD_RADIUS)))