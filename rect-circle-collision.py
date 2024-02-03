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
def presek(k, n, cx, cy):
    x1 = (-(2 * k * n - 2 * k * cy - 2 * cx) + ((2 * k * n - 2 * k * cy - 2 * cx) ** 2 - 4 * (1 + k ** 2) * (
                cx ** 2 + n ** 2 - 2 * n * cy + cy ** 2 - r ** 2)) ** 0.5) / (2 * (1 + k ** 2))
    x2 = (-(2 * k * n - 2 * k * cy - 2 * cx) - ((2 * k * n - 2 * k * cy - 2 * cx) ** 2 - 4 * (1 + k ** 2) * (
                cx ** 2 + n ** 2 - 2 * n * cy + cy ** 2 - r ** 2)) ** 0.5) / (2 * (1 + k ** 2))
    y1 = k * x1 + n
    y2 = k * x2 + n
    tacke = []
    if is_real(x1) and is_real(y1):
        tacke.append((x1, y1))
    if is_real(x2) and is_real(y2):
        tacke.append((x2, y2))
    return tacke
def is_real(complex_number):
    return complex_number.imag == 0

def check_collision(cx, cy, rect):
    tacke = []
    k1, n1 = get_line(rect.x, rect.y, rect.x + rect.width, rect.y)
    tacke.extend(presek(k1, n1, cx, cy))
    k2, n2 = get_line(rect.x, rect.y+rect.height, rect.x + rect.width, rect.y+rect.height)
    tacke.extend(presek(k2, n2, cx, cy))
    k3, n3 = get_line(rect.x, rect.y, rect.x, rect.y+rect.height)
    tacke.extend(presek(k3, n3, cx, cy))
    k4, n4 = get_line(rect.x+rect.width, rect.y, rect.x+rect.width, rect.y + rect.height)
    tacke.extend(presek(k4, n4, cx, cy))
    r = []
    for tacka in tacke:
        x, y = tacka
        if rect.x <= math.ceil(x) <= rect.x + rect.width and rect.y <= math.ceil(y) <= rect.y + rect.height:
            r.append(tacka)
    return r
def prosecna_tacka(points):
    duzina = len(points)
    sumX = 0
    sumY = 0
    for point in points:
        sumX += point[0]
        sumY += point[1]
    if duzina == 0:
        return (0, 0)
    return (sumX/duzina, sumY/duzina)
def reduce(points, x1, y1, x2, y2):
    r = []
    for tacka in points:
        x3, y3 = tacka
        if in_range(x1, y1, x2, y2, x3, y3):
            r.append(tacka)
    return r
def in_range(x1, y1, x2, y2, x3, y3):
    minX = min(x1, x2)
    maxX = max(x1, x2)
    minY = min(y1, y2)
    maxY = max(y1, y2)
    if minX <= x3 <= maxX and minY <= y3 <= maxY:
        return True
    return False
def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5
def find_nearest(x1, y1, x2, y2, points):
    nearest = (x2, y2)
    minDistance = distance(x1, y1, x2, y2)
    for point in points:
        x3, y3 = point
        if distance(x1, y1, x3, y3) < minDistance:
            minDistance = distance(x1, y1, x3, y3)
            nearest = point
    return nearest

os.environ['SDL_VIDEO_CENTERED'] = '1'
index = 0
running = True
acceleration = 1
window = pygame.display.set_mode((1000, 800))
w1 = Wall(300, 300, 500, 500, 1, 1, 1)
cx = 0
cy = 0
radius = 0
to_handle = False
while running:
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.MOUSEBUTTONUP:
            index = (index+1)%2
    w1.draw(window)
    if pygame.mouse.get_pressed()[0]:
        cx, cy = pygame.mouse.get_pos()
        r = 20
        pygame.draw.circle(window, (255, 0, 0), (cx, cy), r)
        tacke = check_collision(cx, cy, w1.r)
        for tacka in tacke:
            pygame.draw.rect(window, (0, 255, 0), (tacka[0], tacka[1], 5, 5))
    pygame.display.flip()
    window.fill((0, 0, 0))
pygame.quit()