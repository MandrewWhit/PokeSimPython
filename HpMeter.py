import pygame


class HpMeter:

    def __init__(self, xloc, yloc, width, height, screen):
        self.xloc = xloc
        self.yloc = yloc
        self.width = width
        self.height = height
        self.deduct = 0
        self.start_deduct = False
        self.screen = screen
        for x in range(xloc, xloc + width):
            pygame.draw.rect(screen, (0, 0, 0), (x, yloc, 2, 2))
            pygame.draw.rect(screen, (0, 0, 0), (x, yloc + height, 2, 2))

        for y in range(yloc, yloc + height):
            pygame.draw.rect(screen, (0, 0, 0), (xloc, y, 2, 2))
            pygame.draw.rect(screen, (0, 0, 0), (xloc + width, y, 2, 2))

        self.font = pygame.font.Font("PokemonGb-RAeo.ttf", 15)
        self.message = self.font.render("HP:", True, (0, 0, 0))
        screen.blit(self.message, (xloc + 5, (yloc+(height/2))))

        for i in range(0, 100):
            pygame.draw.rect(screen, (50, 205, 50), (xloc+50+i, yloc+25, 1, 10))

    def show_empty_meter(self):
        for x in range(self.xloc, self.xloc + self.width):
            pygame.draw.rect(self.screen, (0, 0, 0), (x, self.yloc, 2, 2))
            pygame.draw.rect(self.screen, (0, 0, 0), (x, self.yloc + self.height, 2, 2))

        for y in range(self.yloc, self.yloc + self.height):
            pygame.draw.rect(self.screen, (0, 0, 0), (self.xloc, y, 2, 2))
            pygame.draw.rect(self.screen, (0, 0, 0), (self.xloc + self.width, y, 2, 2))

        self.screen.blit(self.message, (self.xloc + 5, (self.yloc+(self.height/2))))

    def hide(self):
        pygame.draw.rect(self.screen, (255, 255, 255), (self.xloc-5, self.yloc-5, self.width+10, self.height+10))

    def show(self, hp):
        for x in range(self.xloc, self.xloc + self.width):
            pygame.draw.rect(self.screen, (0, 0, 0), (x, self.yloc, 2, 2))
            pygame.draw.rect(self.screen, (0, 0, 0), (x, self.yloc + self.height, 2, 2))

        for y in range(self.yloc, self.yloc + self.height):
            pygame.draw.rect(self.screen, (0, 0, 0), (self.xloc, y, 2, 2))
            pygame.draw.rect(self.screen, (0, 0, 0), (self.xloc + self.width, y, 2, 2))

        self.screen.blit(self.message, (self.xloc + 5, (self.yloc+(self.height/2))))

        for i in range(0, hp):
            pygame.draw.rect(self.screen, (50, 205, 50), (self.xloc+50+i, self.yloc+25, 1, 10))

        if hp < 0:
            for i in range(0, 100):
                pygame.draw.rect(self.screen, (255, 255, 255), (self.xloc + 50 + i, self.yloc + 25, 1, 10))
        else:
            for i in range(hp, 100):
                pygame.draw.rect(self.screen, (255, 255, 255), (self.xloc + 50 + i, self.yloc + 25, 1, 10))

    def deduct_hp(self, hp_event, screen, hp):
        self.deduct = hp
        pygame.time.set_timer(hp_event, 1)
        return True
