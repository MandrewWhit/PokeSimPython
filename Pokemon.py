import pygame
from Moveset import Move


# Pokemon class
class Pokemon:
    def __init__(self, image, type, xloc, yloc, width, height, moves):
        self.image = image
        self.xloc = xloc
        self.yloc = yloc
        self.width = width
        self.height = height
        self.type = type
        load = pygame.image.load(image)
        self.s = pygame.transform.scale(load, (width, height))
        self.moves = moves
        self.hp = 100

    def show(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.xloc, self.yloc, self.width, self.height))
        screen.blit(self.s, (self.xloc, self.yloc))

    def hide(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.xloc, self.yloc, self.width, self.height))

    def set_yloc(self, yloc):
        self.yloc = yloc

    def set_xloc(self, xloc):
        self.xloc = xloc

    def use_move(self, index, event):
        if len(self.moves) != 0:
            self.moves[index].animation(event)
