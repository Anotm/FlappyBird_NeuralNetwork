import pygame
from const import *
import sys
import random
from pipe import Pipe
from bird import Bird
import math

class Game:
    def __init__(self) -> None:
        """Game initialization and setup
        """
        pygame.init()
        self.display = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.basic_font = pygame.font.SysFont("Arial", 20)
        self.clock = pygame.time.Clock()
        
        self.game_started = False 
        self.pipe_timer = 0
        self.pipes = pygame.sprite.Group()
        self.birds = pygame.sprite.Group()

        self.bg_sky = pygame.image.load("./img/bg/sky.png")
        self.bg_buildings = pygame.image.load("./img/bg/buildings.png")
        self.bg_bush = pygame.image.load("./img/bg/bush.png")
        self.bg_floor = pygame.image.load("./img/bg/floor.png")

        self.bg_buildings_count = math.ceil(GAME_WIDTH / self.bg_buildings.get_width())
        self.bg_bush_count = math.ceil(GAME_WIDTH / self.bg_bush.get_width())
        self.bg_floor_count = math.ceil(GAME_WIDTH / self.bg_floor.get_width())
    
    def spawn_pipe(self):
        # top pipe
        pipe_height = random.randint(100, 250)
        pipe_top_y = 0
        
        #bottom pipe
        pipe_top_y_2 = pipe_height + FIXED_GAP_SIZE
        pipe_height_2 = GAME_HEIGHT - pipe_top_y_2
        
        # Create top and bottom pipes
        Pipe(pipe_top_y, pipe_height, self.pipes)
        Pipe(pipe_top_y_2, pipe_height_2, self.pipes)
            
    def check_collision(self): 
        
        for bird in self.birds:
            if bird.y - BIRD_RADIUS < - 10 or bird.y + BIRD_RADIUS + BG_FLOOR_HEIGHT > GAME_HEIGHT + 10:
                return True  # Bird is off screen
        
        if not self.pipes:
            return
        
        for pipe_index in [0, 1]: 
            pipe = self.pipes.sprites()[pipe_index]

            for bird in self.birds:
                # Find the closest point on the rectangle to the circle
                closest_x = max(pipe.rect.x, min(bird.x, pipe.rect.x + PIPE_WIDTH))
                closest_y = max(pipe.rect.y, min(bird.y, pipe.rect.y + pipe.height))

                # Calculate the distance between the circle's center and this point
                distance_x = bird.x - closest_x
                distance_y = bird.y - closest_y
                distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

                # Return True if collision occurs for any bird-pipe pair
                if distance <= BIRD_RADIUS:
                    return True  
        
        # Return False if no collisions found
        return False
    
    def run(self) -> None:
        """
            Main game loop
        """
        bird = Bird(self.birds)

        bg_buildings_clock = 0
        bg_bush_clock = 0
        bg_floor_clock = 0

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_ENTER:
                        self.game_started = True
                    if event.key == pygame.K_SPACE:
                        bird.jump()

            # delta time needed to make everything frame rate independent 
            # so, regardless of the fps, the game will be executed at the same speed.
            delta_time = self.clock.tick() / 1000
            bg_buildings_clock += delta_time
            bg_bush_clock += delta_time
            bg_floor_clock += delta_time

            if self.game_started:
                #start managing the pipes and ai birds
                bird.move(delta_time)
                self.pipe_timer += delta_time
                # print(self.pipe_timer)
                if self.pipe_timer >= 2.5:
                    self.pipe_timer = 0
                    self.spawn_pipe()

                self.pipes.update(delta_time)


            # self.display.fill(SKY_COLOR)
            # set sky bg
            self.display.blit(self.bg_sky, (0,0))

            for i in range(self.bg_buildings_count + 1):
                x = i*self.bg_buildings.get_width()
                x_dis = BG_BUILDINGS_SPEED * bg_buildings_clock / BG_MOVE_TIME
                if x_dis > BG_BUILDINGS_WIDTH:
                    x_dis = 0
                    bg_buildings_clock = 0
                y = GAME_HEIGHT - self.bg_buildings.get_height()
                self.display.blit(self.bg_buildings, (x - x_dis, y))

            # add bushes to bg
            for i in range(self.bg_bush_count + 1):
                x = i*self.bg_bush.get_width()
                x_dis = BG_BUSH_SPEED * bg_bush_clock / BG_MOVE_TIME
                if x_dis > BG_BUSH_WIDTH:
                    x_dis = 0
                    bg_bush_clock = 0
                y = GAME_HEIGHT - self.bg_bush.get_height()
                self.display.blit(self.bg_bush, (x - x_dis, y))

            # Render all pipes
            for pipe in self.pipes:
                pipe.render()
            
            for bird in self.birds:
                bird.render(False)
            
            if self.check_collision():
                print("hit")
                pygame.quit()
                sys.exit()

            # add floor
            for i in range(self.bg_floor_count + 1):
                x = i*self.bg_floor.get_width()
                x_dis = BG_FLOOR_SPEED * bg_floor_clock / BG_MOVE_TIME
                if x_dis > BG_FLOOR_WIDTH:
                    x_dis = 0
                    bg_floor_clock = 0
                y = GAME_HEIGHT - self.bg_floor.get_height()
                self.display.blit(self.bg_floor, (x - x_dis, y))


            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()