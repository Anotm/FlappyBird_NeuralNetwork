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
        self.angle = 0
        
        self.img = pygame.image.load("./img/birds/bird0.png")
    
    def moveOLD(self, delta_time):
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
        
        if displacement < 0:
            self.angle += max(BIRD_ANGLE_ACC * (BIRD_MAX_ANGLE_UP - self.angle), BIRD_INC_ANGLE)
            self.angle = min(self.angle, BIRD_MAX_ANGLE_UP)
        else:
            self.angle -= abs(min(BIRD_ANGLE_ACC * (BIRD_MAX_ANGLE_DOWN - self.angle), -BIRD_INC_ANGLE))
            self.angle = max(self.angle, BIRD_MAX_ANGLE_DOWN)

    def __sigmoid(self):
        # https://www.desmos.com/calculator/ranjtciy4v
        a = abs(BIRD_MAX_ANGLE_UP) + abs(BIRD_MAX_ANGLE_DOWN)
        k = 0.02
        b = -425
        c = BIRD_MAX_ANGLE_DOWN
        return a * (1/(1 + math.exp(-1 * k * (-1 * self.velocity - b)))) + c

    def move(self, delta_time):
        self.add_time += delta_time
        # print(self.add_time)
        if self.add_time < 0.001: 
            return
            
        self.y += min(BIRD_MAX_DISPLACEMENT, self.velocity * self.add_time)
        self.velocity -= BIRD_ACC * self.add_time
        self.add_time = 0

        self.angle = self.__sigmoid()

    
    def jump(self): 
        self.velocity = BIRD_JUMP_VELOCITY
        self.time = 0
    
    def render(self, hitbox, img):
        if hitbox:
            pygame.draw.circle(self.display_surface, (255, 0, 0), (int(self.x), int(self.y)), BIRD_RADIUS)
        if img:
            img = self.img
            rotate_img = pygame.transform.rotate(img, self.angle)
            self.display_surface.blit(rotate_img, (int(self.x-BIRD_RADIUS-1), int(self.y-BIRD_RADIUS)))