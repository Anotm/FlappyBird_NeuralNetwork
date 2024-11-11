import pygame

class Button:
    def __init__(self, is_img:bool=False, filename:str="./img/button_bg.png", text:str="", position:tuple=(0,0), size:tuple=(250, 50), command=None, font=None, font_size=24):
        
        self.is_img=is_img
        if self.is_img:
            self.img = pygame.image.load(filename)

        else:
            self.text = text
            self.size = size
            self.font_size = font_size
            self.font = font
            self.bg_color = (255, 255, 0)   # Yellow
            self.border_color = (0, 0, 0)   # Black
            self.border_width = 2
            self.rect = self.surface.get_rect(topleft=position)

        self.position = position
        self.command = command
        
        self.display = pygame.display.get_surface()
        self.surface = pygame.Surface(size)
    
    
    def draw(self):
        if self.is_img:
            self.display.blit(self.img, self.position)

        else:
            # Draw the button with border
            pygame.draw.rect(self.display, self.border_color, self.rect, 0) 
            inner_rect = self.rect.inflate(-self.border_width * 2, - self.border_width * 2)
            pygame.draw.rect(self.display, self.bg_color, inner_rect)       
            
            # Render text
            text_surf = self.font.render(self.text, True, self.border_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            self.display.blit(text_surf, text_rect)
    
    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_img:
                if self.img.collidepoint(event.pos):
                    self.command()
            else:
                if self.rect.collidepoint(event.pos):
                    self.command()