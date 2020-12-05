import pygame
from Live import Live

WIDTH, HEIGHT, FPS = 800, 600, 10
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

live = Live(10, screen)

run = True
next = False
while run:
    clock.tick(FPS)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            live.set_live(event.pos, event.button)

    keys = pygame.key.get_pressed()


    if keys[pygame.K_ESCAPE]:
        run = False

    if keys[pygame.K_UP]:
        if FPS + 10 <= 120:
            FPS += 10
    if keys[pygame.K_DOWN]:
        if FPS - 10 >= 10:
            FPS -= 10

    if keys[pygame.K_SPACE]:
        if next:
            next = False
        else:
            next = True

    if next:
        live.next_age()
    live.draw()
    pygame.display.update()