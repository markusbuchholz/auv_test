import pygame
import math
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
ROBOT_RADIUS = 20
VELOCITY = 4

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RVO Simulation")

class Robot:
    def __init__(self, x, y, color, goal):
        self.x = x
        self.y = y
        self.color = color
        self.goal = goal

    def compute_new_velocity(self, other):
        # Calculate the relative position
        rel_x = other.x - self.x
        rel_y = other.y - self.y
        distance = math.sqrt(rel_x**2 + rel_y**2)

        if distance < 4 * ROBOT_RADIUS + VELOCITY:
            # Calculate the avoidance force
            avoidance_x = -rel_y
            avoidance_y = rel_x

            # Normalize the avoidance force
            length = math.sqrt(avoidance_x**2 + avoidance_y**2)
            avoidance_x /= length
            avoidance_y /= length

            # Adjust the position based on the avoidance force
            self.x += avoidance_x * VELOCITY
            self.y += avoidance_y * VELOCITY

    def move_towards_goal(self):
        angle = math.atan2(self.goal[1] - self.y, self.goal[0] - self.x)
        self.x += VELOCITY * math.cos(angle)
        self.y += VELOCITY * math.sin(angle)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), ROBOT_RADIUS)

def main():
    clock = pygame.time.Clock()
    robot1 = Robot(100, HEIGHT // 2, RED, (WIDTH - 100, HEIGHT // 2))
    robot2 = Robot(WIDTH - 100, HEIGHT // 2, BLUE, (100, HEIGHT // 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        # Adjust velocities based on the other robot's position
        robot1.compute_new_velocity(robot2)
        robot2.compute_new_velocity(robot1)

        # Move robots towards their goals
        robot1.move_towards_goal()
        robot2.move_towards_goal()

        robot1.draw()
        robot2.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
