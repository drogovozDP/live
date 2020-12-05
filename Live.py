import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Live:
    def __init__(self, size, screen):
        self.size = size
        # self.const_W = pygame.display.Info().current_w / width
        # self.const_H = pygame.display.Info().current_h / height
        self.world = self.create()
        self.screen = screen
        self.begin()

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

    def next_age(self):
        new_world = self.create()
        for i in range(len(self.world)):
            for j in range(len(self.world[i])):
                lives = 0
                left = i - 1
                right = i + 1
                top = j - 1
                bottom = j + 1
                if right == len(self.world):
                    right = 0
                if bottom == len(self.world[i]):
                    bottom = 0

                if self.world[left][top]: lives += 1 # top-left
                if self.world[i][top]: lives += 1 # top
                if self.world[right][top]: lives += 1 # top-right
                if self.world[left][j]: lives += 1 # left
                if self.world[right][j]: lives += 1 # right
                if self.world[left][bottom]: lives += 1 # bottom-left
                if self.world[i][bottom]: lives += 1 # bottom
                if self.world[right][bottom]: lives += 1 # bottom-right

                if self.world[i][j]:
                    if lives == 2 or lives == 3:
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
        if judgment == 1:
            self.world[x][y] = True
        else:
            self.world[x][y] = False

    def draw(self):
        for i in range(len(self.world)):
            for j in range(len(self.world[i])):
                if self.world[i][j] == True:
                    color = WHITE
                else:
                    color = BLACK
                pygame.draw.rect(self.screen, color, (i * self.size, j * self.size, self.size, self.size))
