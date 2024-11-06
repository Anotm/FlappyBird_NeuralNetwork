import pygame
from const import *
import sys
import random
from pipe import Pipe
from bird import Bird
from gameDebugger import GameDebugger
import math
from logger import Logger
from button import Button
from NeuralNetwork import NeuralNetwork

class Game:
    def __init__(self) -> None:
        """Game initialization and setup
        """
        pygame.init()
        self.display = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.basic_font = pygame.font.Font("Pixeboy-z8XGD.ttf", 32)
        self.large_font = pygame.font.Font("Pixeboy-z8XGD.ttf", 80)

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

        self.high_pipe_score = 0
        self.best_bird = None
        self.training = False
        self.ai_playing = False
        
        button_size = (250, 50)
        self.home_screen_buttons = [
            Button("Start Training", position=(GAME_WIDTH // 2 - button_size[0] // 2, 130), size=button_size, command=self.launch_training, font=self.basic_font),
            Button("Run AI Gameplay", position=(GAME_WIDTH // 2 - button_size[0] // 2, 210), size=button_size, command=self.launch_ai_gameplay, font=self.basic_font),
            Button("Play Game", position=(GAME_WIDTH // 2 - button_size[0] // 2, 290), size=button_size, command=self.play_game, font=self.basic_font)
        ]
        
        # TODO: make this more automated, needs to be in respect to MAX_NUM_GEN
        self.generation_colors = ["762367", "F038FF" ,"FFD9DA", "F30F00", "74896E"]

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
            for pipe_index in [0]:
                pipe = self.pipes.sprites()[pipe_index]
                if not bird.is_dead and pipe.rect.x + PIPE_WIDTH < bird.x and not getattr(pipe, 'scored', False):
                    bird.inc_score()
                    pipe.scored = True

        for bird in self.birds:
            if not bird.is_dead:
                self.high_pipe_score = max(self.high_pipe_score, bird.score)

    def update_neural_networks(self):
        if not self.pipes:
            return

        index_top = 0
        index_bottom = 1
        pipe_top = self.pipes.sprites()[index_top]
        pipe_bottom = self.pipes.sprites()[index_bottom]

        for bird in self.birds:
            if not bird.is_dead and bird.is_ai:
                while (pipe_top.rect.x + PIPE_WIDTH + 5) < bird.x:
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
        
        if not self.game_started:
            img = pygame.image.load("./img/bird_D5BE24.png")
            img_fix = img.get_rect(center=(BIRD_STARTING_X, BIRD_STARTING_Y))
            self.display.blit(img, img_fix.topleft)
        
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
        
        if not self.game_started:
            for button in self.home_screen_buttons:
                button.draw()

        if self.training:
            display_gen_txt = self.basic_font.render(f"Generation Num: {self.num_gen}", True, (234, 252, 219))
            self.display.blit(display_gen_txt, (10, 10))
            display_score_txt = self.basic_font.render(f"High Score: {self.high_pipe_score}", True, (234, 252, 219))
            self.display.blit(display_score_txt, (10, 30))
        else:
            border_color = (84, 55, 69)  
            display_score_txt = self.large_font.render(f"{self.high_pipe_score}", True, (234, 252, 219))
            border_offsets = [(-3, -3), (-3, 3), (3, -3), (3, 3)]
            for offset in border_offsets:
                border_text = self.large_font.render(f"{self.high_pipe_score}", True, border_color)
                self.display.blit(border_text, (GAME_WIDTH // 2 - border_text.get_width() // 2 + offset[0], 10 + offset[1]))
            self.display.blit(display_score_txt, (GAME_WIDTH // 2 - display_score_txt.get_width() // 2, 10))
        
        return (bg_buildings_clock, bg_bush_clock, bg_floor_clock)
    
    def launch_training(self):
        # training
        Logger.info("Training active")
        self.training = True
        for _ in range(MAX_NUM_BIRDS):
            Bird(NeuralNetwork(NN_LAYOUT), self.generation_colors[(self.num_gen - 1)%5], self.training, self.birds)
        self.game_started = True
        self.spawn_pipe()
        for bird in self.birds:
            bird.jump()
    
    def launch_ai_gameplay(self):
        Logger.info("AI bird active")
        # play with one bird ai on the best network trained
        self.game_started = True
        self.ai_playing = True
        self.spawn_pipe()
        nn = NeuralNetwork(NN_LAYOUT).load_save_network()
        Logger.info(nn)
        Bird(nn, self.generation_colors[0], self.training, self.birds)
        for bird in self.birds:
            bird.jump()
    
    def play_game(self):
        # real user player
        Logger.info("Player bird active")
        self.game_started = True
        self.spawn_pipe()
        Bird(None, self.generation_colors[0], self.training, self.birds)
        for bird in self.birds:
            bird.jump()
    
    def run(self) -> None:
        """
            Main game loop
        """        
            
        bg_buildings_clock = 0
        bg_bush_clock = 0
        bg_floor_clock = 0
        
        Logger.clear_log_file()

        while True:
            for event in pygame.event.get():
                if not self.game_started:
                    for button in self.home_screen_buttons:
                        button.check_click(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if not self.game_started:
                        if event.key == pygame.K_1:
                            self.launch_training()
                        if event.key == pygame.K_2:
                            self.launch_ai_gameplay()
                        if event.key == pygame.K_3:
                            self.play_game()
                    if event.key == pygame.K_SPACE:
                        for bird in self.birds:
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
                if self.ai_playing:
                    self.update_neural_networks()
                for bird in self.birds:
                    bird.move(delta_time)
                self.pipe_timer += delta_time
                if self.pipe_timer >= PIPE_SPAWN_TIME:
                    self.pipe_timer = 0
                    self.spawn_pipe()

                self.pipes.update(delta_time)

            self.check_collision()

            self.set_score()

            if self.training:
                all_dead = True
                for bird in self.birds:
                    if not bird.is_dead:
                        all_dead = False

                if all_dead:
                    Logger.info("--------------GENERATION:", self.num_gen)
                    for bird in self.birds:
                        if not self.best_bird:
                            self.best_bird = bird
                        
                        if bird.score > self.best_bird.score:
                            self.best_bird = bird
                        
                        if len(self.highest_scores) < 4:
                            self.highest_scores.append(bird.time_of_death)

                        if bird.time_of_death > min(self.highest_scores):
                            self.highest_scores[self.highest_scores.index(min(self.highest_scores))] = bird.time_of_death
                                    
                    if self.num_gen >= MAX_NUM_GEN:
                        print(self.best_bird)
                        self.best_bird.network.save_network()
                        pygame.quit()
                        sys.exit()
                        
                    self.highest_scores.sort(reverse = True)
                    Logger.info("Highest Scores (TOD) = ", self.highest_scores)
                    Logger.info("Highest Scores (Pipes) = ", self.high_pipe_score)

                    self.next_networks = []
                    for t in self.highest_scores:
                        match = False
                        for bird in self.birds:
                            if bird.time_of_death == t:
                                Logger.info(bird)
                                for network in bird.get_childs(self.num_gen):
                                    self.next_networks.append(network)
                                match = True
                            if match:
                                break

                    self.pipes = pygame.sprite.Group()
                    self.birds = pygame.sprite.Group()

                    self.num_gen += 1
                    self.highest_scores = []
                    self.elps_time = 0
                    bg_buildings_clock = 0
                    bg_bush_clock = 0
                    bg_floor_clock = 0 
                    self.pipe_timer = 2.5

                    Logger.info(len(self.next_networks))
                    
                    for network in self.next_networks:
                        Bird(network, self.generation_colors[(self.num_gen - 1)%5], self.training, self.birds)

                    Logger.info("birds added: ", self.birds)
                        
                    for bird in self.birds:
                        bird.jump()

            bg_buildings_clock, bg_bush_clock, bg_floor_clock = self.draw_screen(bg_buildings_clock, bg_bush_clock, bg_floor_clock)
            GameDebugger.draw(self.birds, self.pipes)
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()