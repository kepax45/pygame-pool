import pygame.key

import os
from utils import *


start_pos = None
end_pos = None
def get_line(x1, y1, x2, y2):
    if x1 == x2:
        k = y1-y2
    else:
        k = (y1 - y2)/(x1-x2)
    n = y1 - k*x1
    return (k, n)
def presek(k1, n1, k2, n2):
    if k1 == k2:
        return (0, 0)
    x = (n2 - n1)/(k1 - k2)
    y = k1*x + n1
    return (x, y)

def check_collision(k, n, rect):
    k1, n1 = get_line(rect.x, rect.y, rect.x + rect.width, rect.y)
    tacka1 = presek(k, n, k1, n1)
    k2, n2 = get_line(rect.x, rect.y+rect.height, rect.x + rect.width, rect.y+rect.height)
    tacka2 = presek(k, n, k2, n2)
    k3, n3 = get_line(rect.x, rect.y, rect.x, rect.y+rect.height)
    tacka3 = presek(k, n, k3, n3)
    k4, n4 = get_line(rect.x+rect.width, rect.y, rect.x+rect.width, rect.y + rect.height)
    tacka4 = presek(k, n, k4, n4)
    x1, y1 = tacka1
    x2, y2 = tacka2
    x3, y3 = tacka3
    x4, y4 = tacka4
    tacke = []
    if rect.x <= x1 <= rect.x + rect.width:
        tacke.append(tacka1)
    if rect.x <= x2 <= rect.x + rect.width:
        tacke.append(tacka2)
    if rect.y <= y3 <= rect.y + rect.height:
        tacke.append(tacka3)
    if rect.y <= y4 <= rect.y + rect.height:
        tacke.append(tacka4)
    return tacke

os.environ['SDL_VIDEO_CENTERED'] = '1'
coords = [(0, 0), (0, 0)]
index = 0
running = True
acceleration = 1
window = pygame.display.set_mode((1000, 800))
w1 = Wall(300, 300, 500, 500, 1, 1, 1)
to_handle = False
while running:
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.MOUSEBUTTONUP:
            coords[index] = pygame.mouse.get_pos()
            index = (index+1)%2
    if pygame.mouse.get_pressed()[0]:
        if not start_pos:
            start_pos = pygame.mouse.get_pos()
        else:
            end_pos = pygame.mouse.get_pos()
    else:
        start_pos = None
        end_pos = None
    w1.draw(window)
    if start_pos and end_pos:
        pygame.draw.line(window, (0, 255, 0), start_pos, end_pos)
        x1, y1 = start_pos
        x2, y2 = end_pos
        k, n = get_line(x1, y1, x2, y2)
        print(check_collision(k, n, w1.r))
    pygame.display.flip()
    window.fill((0, 0, 0))
pygame.quit()