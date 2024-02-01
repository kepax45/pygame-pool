import pygame.key

import os
from utils import *

os.environ['SDL_VIDEO_CENTERED'] = '1'
running = True
acceleration = 1
window = pygame.display.set_mode((1000, 800))
w1 = Wall(0, -10000, 1000, 50, 1, 1, 0.8)
w2 = Wall(0, 750, 1000, 800, 1, 1, 0.8)
w3 = Wall(0, 0, 50, 1000, 1, 1, 0.8)
w4 = Wall(950, 0, 1000, 800, 1, 1, 0.8)
b1 = Ball(15, 300, 400)
gen_pool(600, 400, 15)
l = Line(b1)
to_handle = False
while running:
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    if pygame.key.get_pressed()[pygame.K_w]:
        b1.vy -= acceleration
    if pygame.key.get_pressed()[pygame.K_s]:
        b1.vy += acceleration
    if pygame.key.get_pressed()[pygame.K_a]:
        b1.vx -= acceleration
    if pygame.key.get_pressed()[pygame.K_d]:
        b1.vx += acceleration
    if pygame.mouse.get_pressed()[0]:
        l.start_display()
        to_handle = True
    if not pygame.mouse.get_pressed()[0] and to_handle:
        l.stop_display()
        mX, mY = l.get_multiplier()
        b1.vx = 15*mX
        b1.vy = 15*mY
        print(b1.vx, b1.vy)
        to_handle = False
    l.draw(window)
    Ball.check_collision()
    Ball.update_all(window)
    w1.handle_collisions()
    w2.handle_collisions()
    w3.handle_collisions()
    w4.handle_collisions()
    w1.draw(window)
    w2.draw(window)
    w3.draw(window)
    w4.draw(window)
    pygame.display.flip()
    window.fill((0, 0, 0))
pygame.quit()