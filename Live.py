import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Live:
    world = None

    def __init__(self, size, screen):
        self.size = size
        self.reset()
        self.screen = screen
        self.begin()

    def reset(self):
        self.world = self.create()

    def begin(self):
        self.world[3][2] = True
        self.world[3][3] = True
        self.world[3][4] = True

    def create(self):
        live = []
        width = pygame.display.Info().current_w
        height = pygame.display.Info().current_h
        for i in range(width // self.size):
            row = [False] * (height // self.size)
            live.append(row)
        return live

    def next_age(self, clock, FPS):
        clock.tick(FPS)
        new_world = self.create()
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
                    if 2 <= lives <= 3:
                        new_world[i][j] = True
                    else:
                        new_world[i][j] = False
                else:
                    if lives == 3:
                        new_world[i][j] = True
        del self.world
        self.world = new_world

    def set_live(self, pos, judgment):
        x = pos[0] // self.size
        y = pos[1] // self.size
        self.world[x][y] = 1 if judgment == 1 else 0

    def draw(self):
        for i in range(1, len(self.world) - 1):
            for j in range(1, len(self.world[i]) - 1):
                color = WHITE if self.world[i][j] else BLACK
                pygame.draw.rect(self.screen, color, (i * self.size, j * self.size, self.size, self.size))
