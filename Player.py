import pygame


class Player:

    def __init__(self, width, height, image):
        self.xloc = -50
        self.yloc = 300
        self.width = width
        self.height = height
        load = pygame.image.load(image)
        self.im = pygame.transform.scale(load, (width, height))

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.xloc-5, self.yloc, self.width+5, self.height))
        screen.blit(self.im, (self.xloc, self.yloc))
