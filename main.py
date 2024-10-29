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
            if bird.y - BIRD_RADIUS < - 10 or bird.y + BIRD_RADIUS > GAME_HEIGHT + 10:
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

            if self.game_started:
                #start managing the pipes and ai birds
                bird.move(delta_time)
                self.pipe_timer += delta_time
                # print(self.pipe_timer)
                if self.pipe_timer >= 2.5:
                    self.pipe_timer = 0
                    self.spawn_pipe()

                self.pipes.update(delta_time)
            self.display.fill(SKY_COLOR)

            # Render all pipes
            for pipe in self.pipes:
                pipe.render()
            
            for bird in self.birds:
                bird.render()
            
            if self.check_collision():
                print("hit")
                pygame.quit()
                sys.exit()
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()