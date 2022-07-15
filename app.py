import pygame
from pygame.locals import *
from abc import ABC, abstractmethod


class App(ABC):

    def __init__(self, width=600, height=600, fps=60):
        pygame.init()
        flags = RESIZABLE
        self.running = True
        self.pause = False

        self.fps = fps
        self.clock = pygame.time.Clock()

        self.width, self.height = width, height

        self.screen = pygame.display.set_mode((width, height), flags)

    def draw(self):
        pass

    def update(self, dt):
        pass

    def event_handler(self, event):
        pass

    def run(self):
        dt = 1/self.fps
        while self.running:
            self.draw()
            pygame.display.update()
            self.update(dt)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                self.event_handler(event)

            dt = self.clock.tick(self.fps)
        pygame.quit()
