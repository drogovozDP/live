import pygame
from live import Live

WIDTH, HEIGHT, FPS = 0, 0, 10
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

live = Live(10, screen)

run = True
next = False
mouse_down = False
mouse_button = None
while run:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_button = event.button
            live.set_live(event.pos, mouse_button)
            mouse_down = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_button = None
            mouse_down = False

        if mouse_down and event.type == pygame.MOUSEMOTION:
            live.set_live(event.pos, mouse_button)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                next = not next
                if next:
                    live.save_age()

            if event.key == pygame.K_UP:
                FPS += 10 if FPS + 10 < 130 else 0

            if event.key == pygame.K_DOWN:
                FPS -= 10 if FPS - 10 > 9 else 0

            if event.key == pygame.K_z and pygame.key.get_mods() and pygame.KMOD_CTRL and not next:
                live.set_age(-1)

            if event.key == pygame.K_y and pygame.key.get_mods() and pygame.KMOD_CTRL and not next:
                live.set_age(1)

            if event.key == pygame.K_BACKSPACE:
                live.reset()
                next = False

            if event.key == pygame.K_ESCAPE:
                run = False

    if next:
        live.next_age(clock, FPS)
    live.draw()
    pygame.display.update()
