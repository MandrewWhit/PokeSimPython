import pygame


class BattleBar:
    def __init__(self):
        img1 = pygame.image.load("battlebar1.jpg")
        self.battlebar1 = pygame.transform.scale(img1, (200, 50))
        img2 = pygame.image.load("battlebar2.jpg")
        self.battlebar2 = pygame.transform.scale(img2, (200, 50))

    def draw(self, screen):
        screen.blit(self.battlebar1, (400, 290))
        screen.blit(self.battlebar2, (0, 50))

    def erase(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (400, 290, 200, 50))
        pygame.draw.rect(screen, (255, 255, 255), (0, 50, 200, 50))
