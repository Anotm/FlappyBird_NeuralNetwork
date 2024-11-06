import pygame

class Button:
    def __init__(self, text: str, position: tuple, size: tuple, command, font, font_size=24):
        self.text = text
        self.position = position
        self.size = size
        self.command = command
        self.font_size = font_size
        self.font = font
        
        self.bg_color = (255, 255, 0)   # Yellow
        self.border_color = (0, 0, 0)   # Black
        self.border_width = 2
        
        self.display = pygame.display.get_surface()
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect(topleft=position)
    
    
    def draw(self):
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
            if self.rect.collidepoint(event.pos):
                self.command()