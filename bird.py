import pygame 
from const import *
import math
from NeuralNetwork import NeuralNetwork

class Bird(pygame.sprite.Sprite):
    def __init__(self, NN: NeuralNetwork, *groups):
        super().__init__(*groups)
        self.x = BIRD_STARTING_X
        self.y = BIRD_STARTING_Y
        self.time = 0
        self.velocity = 0 
        self.display_surface = pygame.display.get_surface()
        self.add_time = 0
        self.angle = 0
        self.is_dead = False
        self.score = 0
        self.time_of_death = 0

        self.network = NN

        if self.network == None:
            self.is_ai = False
            self.img = pygame.image.load("./img/birds/bird_D5BE24.png")
        else:
            self.is_ai = True
            self.img = pygame.image.load("./img/birds/bird_F038FF.png")
            self.network.skew_links_bias([-5,5,5], [-5,5,5])
    
    '''
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
    '''

    def run_neural_network(self, input_data: list):
        if not self.is_ai: 
            return

        self.network.set_input(input_data)
        self.network.forward_pass(4)
        output = self.network.get_output()
        jump = output[0]
        not_jump = output[1]

        if max(jump, not_jump) == jump:
            self.jump()

    def __sigmoid(self):
        # https://www.desmos.com/calculator/ranjtciy4v
        diff_between_min_max = abs(BIRD_MAX_ANGLE_UP) + abs(BIRD_MAX_ANGLE_DOWN)
        intensity_of_change = 0.02 # rate of change
        shift_start = -425
        return diff_between_min_max * (1/(1 + math.exp(-1 * intensity_of_change * (-1 * self.velocity - shift_start)))) + BIRD_MAX_ANGLE_DOWN

    def move(self, delta_time):
        self.add_time += delta_time
        # print(self.add_time)
        if not self.is_dead:
            if self.add_time < 0.001: 
                return

            self.y += min(BIRD_MAX_DISPLACEMENT, self.velocity * self.add_time)
            self.velocity -= BIRD_ACC * self.add_time
            self.add_time = 0

            self.angle = self.__sigmoid()
        else:
            if self.add_time >= MOVE_TIME:
                self.x -= PIPE_SPEED
                self.add_time = 0
    
    def jump(self): 
        self.velocity = BIRD_JUMP_VELOCITY
        self.time = 0

    def kill(self, TOD):
        self.is_dead = True;
        self.time_of_death = round(TOD, 3)
        print("Score =", self.score)
        print("Death Time =", self.time_of_death)
        print()

    def inc_score(self):
        self.score += 1
    
    def render(self):
        img = self.img
        rotated_img = pygame.transform.rotate(img, self.angle)
        rotated_rect = rotated_img.get_rect(center=(self.x, self.y))
        self.display_surface.blit(rotated_img, rotated_rect.topleft)
