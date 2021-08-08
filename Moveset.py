import pygame
import time


class Move:
    def __init__(self, name, physical, damage, weakness, no_effect):
        self.name = name
        self.physical = physical
        self.damage = damage
        self.weakness = weakness
        self.no_effect = no_effect
        load = pygame.image.load("bolt_2.png")

        self.image = pygame.transform.scale(load, (50, 100))

    def animation(self, event):

        sound_effect = pygame.mixer.Sound("tse.wav")
        pygame.mixer.Sound.play(sound_effect)
        pygame.time.set_timer(event, 10)
