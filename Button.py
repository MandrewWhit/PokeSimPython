import pygame


# button class
class Button:
    def __init__(self, screen, xloc, yloc, x_size, y_size, color, message, m_locx, m_locy, font_size):
        self.xloc = xloc
        self.yloc = yloc
        self.x_size = x_size
        self.y_size = y_size
        self.color = color
        self.message = message
        self.m_locx = m_locx
        self.m_locy = m_locy
        self.font_size = font_size
        pygame.draw.rect(screen, color, (xloc, yloc, x_size, y_size), 8)
        font = pygame.font.Font("PokemonGb-RAeo.ttf", font_size)
        start_message = font.render(message, False, (0, 0, 0))
        screen.blit(start_message, (xloc+m_locx, yloc+m_locy))

    def hide(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.xloc, self.yloc, self.x_size, self.y_size), 8)

    def show(self, screen):
        pygame.draw.rect(screen, self.color, (self.xloc, self.yloc, self.x_size, self.y_size), 8)
        font = pygame.font.Font("PokemonGb-RAeo.ttf", self.font_size)
        start_message = font.render(self.message, False, (0, 0, 0))
        screen.blit(start_message, (self.xloc + self.m_locx, self.yloc + self.m_locy))

