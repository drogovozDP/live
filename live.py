from collections import deque

import pygame
import numpy as np


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREED_COLOR = (50, 50, 50)
MAX_SAVED_AGES_LEN = 20


class Live:
    world = None

    def __init__(self, size, screen):
        self.size = size
        self.saved_ages = deque(maxlen=MAX_SAVED_AGES_LEN)
        self.current_age_idx = 0
        self.reset()
        self.step_world = np.zeros(self.world.shape)
        self.screen = screen
        self.grid = []
        self._begin()
        self.save_age()

    def reset(self):
        self.world = self._create()

    def _begin(self):
        width = pygame.display.Info().current_w
        height = pygame.display.Info().current_h

        for i in range(0, len(self.world) - 1, 2):
            for x, y in zip([i, i, i + 1, i + 1, i + 2], [0, height, height, 0, 0]):
                self.grid.append([self.size * x, y])

        for i in range(0, len(self.world[0]) - 1, 2):
            for x, y in zip([0, width, width, 0, 0], [i, i, i + 1, i + 1, i + 2]):
                self.grid.append([x, self.size * y])

    def _create(self):
        width = pygame.display.Info().current_w
        height = pygame.display.Info().current_h
        return np.zeros((width // self.size, height // self.size))

    def save_age(self):
        [self.saved_ages.pop() for _ in range(len(self.saved_ages) - self.current_age_idx - 1)]
        if len(self.saved_ages) == 0 or not np.array_equal(self.saved_ages[-1], self.world):
            self.saved_ages.append(self.world.copy())
        self.current_age_idx = len(self.saved_ages) - 1

    def set_age(self, next):
        new_age_idx = self.current_age_idx + next
        if 0 <= new_age_idx < len(self.saved_ages):
            if self.current_age_idx == len(self.saved_ages) - 1:
                self.save_age()
            self.current_age_idx += next
            self.world = self.world * 0 + self.saved_ages[self.current_age_idx]

    def next_age(self, clock, FPS):
        clock.tick(FPS)
        self.step_world *= 0
        for i in range(len(self.world)):
            for j in range(len(self.world[i])):
                lives = 0
                left = i - 1
                right = i + 1 if i + 1 < len(self.world) else 0
                top = j - 1
                bottom = j + 1 if j + 1 < len(self.world[i]) else 0

                lives += 1 if self.world[left][top] else 0  # top-left
                lives += 1 if self.world[i][top] else 0  # top
                lives += 1 if self.world[right][top] else 0  # top-right
                lives += 1 if self.world[left][j] else 0  # left
                lives += 1 if self.world[right][j] else 0  # right
                lives += 1 if self.world[left][bottom] else 0  # bottom-left
                lives += 1 if self.world[i][bottom] else 0  # bottom
                lives += 1 if self.world[right][bottom] else 0  # bottom-right

                if self.world[i][j]:
                    self.step_world[i, j] = 1 if 2 <= lives <= 3 else 0
                else:
                    self.step_world[i, j] = 1 if lives == 3 else 0

        self.world = self.world * 0 + self.step_world

    def set_live(self, pos, judgment):
        x = pos[0] // self.size
        y = pos[1] // self.size
        self.world[x, y] = 1 if judgment == 1 else 0

    def draw(self):
        for i in range(1, len(self.world) - 1):
            for j in range(1, len(self.world[i]) - 1):
                color = WHITE if self.world[i, j] else BLACK
                pygame.draw.rect(self.screen, color, (i * self.size, j * self.size, self.size, self.size))

        pygame.draw.lines(self.screen, GREED_COLOR, False, self.grid)
        # pygame.draw.lines(
        #     self.screen,
        #     (255, 0, 144),
        #     False,
        #     [
        #
        #     ]
        # )
