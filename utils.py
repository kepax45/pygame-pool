import pygame
import math

floor_friction = 0.05

class Ball:
    ball_list = []
    def __init__(self, radius, x, y, m=5):
        self.radius = radius
        self.x = x
        self.y = y
        self.color = (255, 0, 0)
        self.vx = 0
        self.vy = 0
        self.m = m
        Ball.ball_list.append(self)
    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius, 0)
    def update(self):
        self.x += self.vx
        self.y += self.vy
    def get_angle(self):
        theta = math.atan2(self.vy, self.vx)
        return theta

    @staticmethod
    def update_all(window):
        for ball in Ball.ball_list:
            ball.vx *= (1 - floor_friction)
            ball.vy *= (1 - floor_friction)
            ball.update()
            ball.draw(window)
    @staticmethod
    def __euclidean_distance__(x1, y1, x2, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5
    @staticmethod
    def colliding(ball1, ball2):
        distance = Ball.__euclidean_distance__(ball1.x, ball1.y, ball2.x, ball2.y)
        two_r = ball1.radius + ball2.radius
        if distance > two_r:
            return False
        return True
    # v2f (m1, v1i, m2, v2i)
    # v1f (m2, v2i, m1, v1i)
    def get_velocity(self):
        return (self.vx**2 + self.vy ** 2) ** 0.5
    @staticmethod
    def __calc_final_velocity__(m1, v1, m2, v2, theta1, theta2, phi):
        v1x = (v1*math.cos(theta1 - phi)*(m1 - m2) + 2*m2*v2*math.cos(theta2 - phi))/(m1 + m2)*math.cos(phi) + v1*math.sin(theta1 - phi)*math.cos(phi + 1.5708)
        v1y = (v1*math.cos(theta1-phi)*(m1-m2) + 2*m2*v2*math.cos(theta2 - phi))/(m1+m2)*math.sin(phi)+v1*math.sin(theta1 - phi)*math.sin(phi + 1.5708)
        return v1x, v1y
    @staticmethod
    def pen_res(ball1, ball2):
        ydist = ball1.y - ball2.y
        xdist = ball1.x - ball2.x
        alpha = math.atan2(ydist, xdist)
        pen_depth = Ball.__euclidean_distance__(ball1.x, ball1.y, ball2.x, ball2.y) - ball1.radius - ball2.radius
        ball1.x -= pen_depth/2*math.cos(alpha)
        ball1.y -= pen_depth/2*math.sin(alpha)
        ball2.x += pen_depth / 2 * math.cos(alpha)
        ball2.y += pen_depth / 2 * math.sin(alpha)
        return alpha
    @staticmethod
    def check_collision():
        for i in range(len(Ball.ball_list)):
            for j in range(i+1, len(Ball.ball_list)):
                ball1 = Ball.ball_list[i]
                ball2 = Ball.ball_list[j]
                if Ball.colliding(ball1, ball2):
                    phi = Ball.pen_res(ball1, ball2)
                    theta1 = ball1.get_angle()
                    theta2 = ball2.get_angle()
                    v1 = ball1.get_velocity()
                    v2 = ball2.get_velocity()
                    v1x, v1y = Ball.__calc_final_velocity__(ball1.m, v1, ball2.m, v2, theta1, theta2, phi)
                    v2x, v2y = Ball.__calc_final_velocity__(ball2.m, v2, ball1.m, v1, theta2, theta1, phi)
                    ball1.vx = v1x
                    ball1.vy = v1y
                    ball2.vx = v2x
                    ball2.vy = v2y
class Line:
    def __init__(self, ball):
        self.display = False
        self.ref_ball = ball
        self.set_mouse()
        self.set_center()
    def set_center(self):
        self.center = (self.ref_ball.x, self.ref_ball.y)
    def set_mouse(self):
        self.mouse = pygame.mouse.get_pos()
    def start_display(self):
        self.display = True
    def stop_display(self):
        self.display = False

    @staticmethod
    def __euclidean_distance__(x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    def draw(self, window):
        if self.display:
            self.set_mouse()
            self.set_center()
            dx = self.mouse[0]-self.center[0]
            dy = self.mouse[1]-self.center[1]
            pygame.draw.line(window, (0, 255, 0), self.center, (self.center[0]-dx, self.center[1]-dy))
    def get_multiplier(self):
        return (-(self.mouse[0]-self.center[0])/100, -(self.mouse[1]-self.center[1])/100)

class Wall:
    def __init__(self, startX, startY, endX, endY, yMultiplier, xMultiplier, dampingFactor):
        self.r = pygame.Rect(startX, startY, endX-startX, endY-startY)
        self.x = startX
        self.y = startY
        self.width = endX - startX
        self.height = endY - startY
        self.dampingFactor = dampingFactor
        self.xMultiplier = xMultiplier
        self.yMultiplier = yMultiplier

    def collide_ball(self, ball):
        cx = ball.x
        cy = ball.y
        testX = cx
        testY = cy
        xMul = 1
        yMul = 1
        if cx < self.x:
            testX = self.x
            xMul = -1
        elif cx > self.x + self.width:
            testX = self.x + self.width
            xMul = -1

        if cy < self.y:
            testY = self.y
            yMul = -1
        elif cy > self.y + self.height:
            testY = self.y + self.height
            yMul = -1

        distance = Wall.__euclidean_distance__(cx, cy, testX, testY)
        return (distance <= ball.radius, distance, xMul, yMul)
    def pen_res(self, ball):
        vel = ball.get_velocity()
        angle1 = ball.get_angle()
        angle = self.collide_ball(ball)[2]
        pen_depth = ball.radius + 1- self.collide_ball(ball)[1]
        # Resolve penetration and update ball's position
        ball.x += pen_depth * math.cos(angle)
        ball.y += pen_depth * math.sin(angle)
        return (vel, angle)
    def handle_collisions(self):
        for ball in Ball.ball_list:
            if self.collide_ball(ball)[0]:
                #self.pen_res(ball)
                xMul, yMul = self.collide_ball(ball)[-2:]
                print(xMul, yMul)
                ball.vx *= xMul
                ball.vy *= yMul


                # Apply damping factor to the reflected velocity
    @staticmethod
    def __euclidean_distance__(x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    def draw(self, window):
        pygame.draw.rect(window, (0, 0, 255), self.r)

def gen_pool(x, y, radius):
    pool_balls = []
    for i in range(1, 6):
        for j in range(i):
            b = Ball(radius, x+radius*2*i, y-(radius*i)+radius*2*j, m=5)
            pool_balls.append(b)
    return pool_balls