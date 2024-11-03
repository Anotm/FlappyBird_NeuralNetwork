import pygame
from const import *
import sys
import random
from pipe import Pipe
from bird import Bird
from gameDebugger import GameDebugger
import math

from NeuralNetwork import NeuralNetwork

class Game:
    def __init__(self) -> None:
        """Game initialization and setup
        """
        pygame.init()
        self.display = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.basic_font = pygame.font.SysFont("Arial", 20)
        self.clock = pygame.time.Clock()
        self.elps_time = 0
        
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

        self.num_gen = 1
        self.highest_scores = []
        self.next_networks = []

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
            if (bird.y - BIRD_RADIUS < - 10 or bird.y + BIRD_RADIUS + BG_FLOOR_HEIGHT > GAME_HEIGHT + 10) and not bird.is_dead:
                bird.suspend(self.elps_time)
                # return True  # Bird is off screen
        
        if not self.pipes:
            return

        for bird in self.birds:
            even = False
            for pipe_index in [0, 1]: 
                pipe = self.pipes.sprites()[pipe_index]

                # Find the closest point on the rectangle to the circle
                closest_x = max(pipe.rect.x, min(bird.x, pipe.rect.x + PIPE_WIDTH - 5))
                closest_y = max(pipe.rect.y, min(bird.y, pipe.rect.y + pipe.height - 5))

                # Calculate the distance between the circle's center and this point
                distance_x = bird.x - closest_x
                distance_y = bird.y - closest_y
                distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

                # Return True if collision occurs for any bird-pipe pair
                if distance <= BIRD_RADIUS and not bird.is_dead:
                    bird.suspend(self.elps_time)
                    # return True

        # Return False if no collisions found
        return False

    def set_score(self):
        if not self.pipes:
            return

        for bird in self.birds:
            pipes_passed = 0;
            for pipe_index in [0, 1]:
                pipe = self.pipes.sprites()[pipe_index]
                if not bird.is_dead and pipe.rect.x + PIPE_WIDTH == bird.x:
                    pipes_passed += 1
            if pipes_passed > 0:
                bird.inc_score()

    def update_neural_networks(self):
        if not self.pipes:
            return

        index_top = 0
        index_bottom = 1
        pipe_top = self.pipes.sprites()[index_top]
        pipe_bottom = self.pipes.sprites()[index_bottom]

        for bird in self.birds:
            if not bird.is_dead and bird.is_ai:
                while (pipe_top.rect.x + (PIPE_WIDTH/2)) < bird.x:
                    index_top += 1
                    index_bottom += 1
                    pipe_top = self.pipes.sprites()[index_top]
                    pipe_bottom = self.pipes.sprites()[index_bottom]

                bird_height = GAME_HEIGHT - bird.y - BG_FLOOR_HEIGHT                
                bird_pipes_dis = pipe_bottom.rect.x + (PIPE_WIDTH/2) - bird.x
                bird_top_pipe_dis = pipe_top.height - bird.y
                bird_bottom_pipe_dis = pipe_bottom.rect.y - bird.y

                bird.run_neural_network([bird_height, bird_pipes_dis, bird_top_pipe_dis, bird_bottom_pipe_dis])

    def draw_screen(self, bg_buildings_clock, bg_bush_clock, bg_floor_clock):
        # set sky bg
        self.display.blit(self.bg_sky, (0,0))

        # add buildings
        for i in range(self.bg_buildings_count + 1):
            x = i*self.bg_buildings.get_width()
            x_dis = BG_BUILDINGS_SPEED * bg_buildings_clock / BG_MOVE_TIME
            if x_dis > BG_BUILDINGS_WIDTH:
                x_dis = 0
                bg_buildings_clock = 0
            y = GAME_HEIGHT - self.bg_buildings.get_height()
            self.display.blit(self.bg_buildings, (x - x_dis, y))

        # add bushes
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
        
        # Render all birds
        for bird in self.birds:
            bird.render()

        # add floor
        for i in range(self.bg_floor_count + 1):
            x = i*self.bg_floor.get_width()
            x_dis = BG_FLOOR_SPEED * bg_floor_clock / BG_MOVE_TIME
            if x_dis > BG_FLOOR_WIDTH:
                x_dis = 0
                bg_floor_clock = 0
            y = GAME_HEIGHT - self.bg_floor.get_height()
            self.display.blit(self.bg_floor, (x - x_dis, y))

        return (bg_buildings_clock, bg_bush_clock, bg_floor_clock)
    
    def run(self) -> None:
        """
            Main game loop
        """        
            
        bg_buildings_clock = 0
        bg_bush_clock = 0
        bg_floor_clock = 0

        for _ in range(MAX_NUM_BIRDS):
            Bird(NeuralNetwork([4,4,2]), self.birds)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_started = True
                        self.spawn_pipe()
                        for bird in self.birds:
                            bird.jump()
                    if event.key == pygame.K_SPACE:
                        bird.jump()
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            # delta time needed to make everything frame rate independent 
            # so, regardless of the fps, the game will be executed at the same speed.
            delta_time = self.clock.tick() / 1000
            self.elps_time += delta_time
            bg_buildings_clock += delta_time
            bg_bush_clock += delta_time
            bg_floor_clock += delta_time
            
            if self.game_started:
                self.update_neural_networks()
                for bird in self.birds:
                    bird.move(delta_time)
                self.pipe_timer += delta_time
                if self.pipe_timer >= 2.5:
                    self.pipe_timer = 0
                    self.spawn_pipe()

                self.pipes.update(delta_time)

            
            self.check_collision()

            self.set_score()

            all_dead = True
            for bird in self.birds:
                if not bird.is_dead:
                    all_dead = False

            if all_dead:
                if self.num_gen >= MAX_NUM_GEN:
                    pygame.quit()
                    sys.exit()
                for bird in self.birds:
                    if len(self.highest_scores) < 4:
                        self.highest_scores.append(bird.time_of_death)

                    if bird.time_of_death > min(self.highest_scores):
                        self.highest_scores[self.highest_scores.index(min(self.highest_scores))] = bird.time_of_death

                self.highest_scores.sort(reverse = True)
                print("Highest Scores =", self.highest_scores)

                self.next_networks = []
                for t in self.highest_scores:
                    match = False
                    for bird in self.birds:
                        if bird.time_of_death == t:
                            for network in bird.get_childs(self.num_gen):
                                self.next_networks.append(network)
                            match = True
                        if match:
                            break


                self.pipes = pygame.sprite.Group()
                self.birds = pygame.sprite.Group()
                print("birds after delete: ", self.birds)
                self.num_gen += 1
                self.highest_scores = []
                self.elps_time = 0
                bg_buildings_clock = 0
                bg_bush_clock = 0
                bg_floor_clock = 0 
                self.pipe_timer = 0

                print(len(self.next_networks))
                print()
                
                for network in self.next_networks:
                    Bird(network, self.birds)
                print("birds added: ", self.birds)
                    
                self.spawn_pipe()
                for bird in self.birds:
                    bird.jump()

            bg_buildings_clock, bg_bush_clock, bg_floor_clock = self.draw_screen(bg_buildings_clock, bg_bush_clock, bg_floor_clock)
            # GameDebugger.draw(self.birds, self.pipes)
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()