import pygame
import random
from collections import deque

from hamiltonian_path import hamiltonian_path, hamiltonian_path_snake

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Snake Directions
MOVEMENTS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
SPACE_SNAKE = 0.10 * GRID_SIZE

class Point():
    """Represents a point in the game matrix."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h_number = -1  # Hamiltonian path number
        self.previous = None
        self.next = None

class Snake_Game():
    """The main class for the Snake Game."""

    def __init__(self):
        pygame.init()
        self.fps = 10
        self.game_matrix = [[Point(x, y) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
        self.snake = deque()
        self.snake.appendleft((0, 0))
        self.food_position = [(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT) if x != 0 or y != 0]
        
        # Generate Hamiltonian path for the game matrix
        path = hamiltonian_path_snake(self.game_matrix, GRID_WIDTH, GRID_HEIGHT)
        if path == None:
            print("Don't exist a hamiltonian path")
        
        # Assign Hamiltonian path numbers to game matrix points
        last = None
        for pos, value in enumerate(path):
            self.game_matrix[value // GRID_WIDTH][value % GRID_WIDTH].h_number = pos

            self.game_matrix[value // GRID_WIDTH][value % GRID_WIDTH].previous = last

            if pos != 0:
                last.next = self.game_matrix[value // GRID_WIDTH][value % GRID_WIDTH]

            last = self.game_matrix[value // GRID_WIDTH][value % GRID_WIDTH]

        last.next = self.game_matrix[0][0]
        self.game_matrix[0][0].previous = last

        # Initialize the screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")

        self.clock = pygame.time.Clock()
        self.solve()
        

    def solve(self):
        """Main game loop."""
        running = True
        food = self.generate_food()
        food_pos = self.game_matrix[food[1]][food[0]].h_number

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.fps += 10
                    elif event.key == pygame.K_s:
                        self.fps -= 10

            head_x, head_y = self.snake[0]
            act_pos = self.game_matrix[head_y][head_x].h_number
            new_head = None
            new_head_dist = None

            # Find the best possible move
            for move in MOVEMENTS:
                if head_x + move[0] >= 0 and head_x + move[0] < GRID_WIDTH and head_y + move[1] >= 0 and head_y + move[1] < GRID_HEIGHT and (head_x + move[0], head_y + move[1]) not in self.snake:
                    new_pos = self.game_matrix[head_y + move[1]][head_x + move[0]].h_number
                    distance = float("inf")
                    new_head_x, new_head_y = head_x + move[0], head_y + move[1]

                    # Check collision when moving forward
                    last = self.game_matrix[new_head_y][new_head_x]
                    i = 1
                    while i != len(self.snake):
                        if (last.x, last.y) in list(self.snake)[i: len(self.snake)]:
                            break
                        i += 1
                        last = last.next

                    if i == len(self.snake):
                        if food_pos >= new_pos:
                            distance = min(food_pos - new_pos, distance)
                        else:
                            distance = min(GRID_WIDTH * GRID_HEIGHT - new_pos + food_pos, distance)

                    # Check collision when moving backward
                    last = self.game_matrix[new_head_y][new_head_x]
                    i = 1
                    while i != len(self.snake):
                        if (last.x, last.y) in list(self.snake)[i: len(self.snake)]:
                            break
                        i += 1
                        last = last.previous

                    if i == len(self.snake):
                        if food_pos <= new_pos:
                            distance = min(new_pos - food_pos, distance)
                        else:
                            distance = min(new_pos + GRID_WIDTH * GRID_HEIGHT - food_pos, distance)

                    # Evaluate the possible move
                    if len(self.snake) <= distance or new_pos in [(act_pos + 1) % (GRID_WIDTH * GRID_HEIGHT), (act_pos - 1) % (GRID_WIDTH * GRID_HEIGHT)]:
                        if new_head is None or new_head_dist > distance:
                            new_head = (new_head_x, new_head_y)
                            new_head_dist = distance

            if new_head == None or self.check_collision(new_head):
                running = False
                print("I lose! );")
                break
            self.snake.appendleft(new_head)
            self.food_position.remove(new_head)

            if new_head == food:
                food = self.generate_food()
                food_pos = self.game_matrix[food[1]][food[0]].h_number
            else:
                self.food_position.append(self.snake.pop())

            self.draw_game(food)
            self.clock.tick(self.fps)
            
            if len(self.snake) == GRID_WIDTH * GRID_HEIGHT - 1:
                running = False
                print("I Won! :)")


    def draw_game(self, food):
        """Draws the entire game scene."""
        self.screen.fill(BLACK)
        self.draw_snake()
        pygame.draw.rect(self.screen, RED, (food[0] * GRID_SIZE + SPACE_SNAKE, food[1] * GRID_SIZE + SPACE_SNAKE, GRID_SIZE - 2*SPACE_SNAKE, GRID_SIZE - 2*SPACE_SNAKE))
        pygame.display.flip()


    def draw_snake(self):
        """Draws the snake on the screen."""
        if len(self.snake) == 1:
            x, y = self.snake[0]
            pygame.draw.rect(self.screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            return

        for index, segment in enumerate(self.snake):
            x, y = segment
            if index != 0 and index != len(self.snake) -1:
                x_p, y_p = self.snake[index -1]
                x_n, y_n = self.snake[index +1]

                direction_p = (x_p - x, y_p - y)
                direction_n = (x_n - x, y_n - y)

                if direction_n[0] == direction_p[0] or direction_n[1] == direction_p[1]:
                    if direction_n[1] == 0: # (1, 0) or (-1, 0)
                        pygame.draw.rect(self.screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE + SPACE_SNAKE, GRID_SIZE, GRID_SIZE - 2*SPACE_SNAKE))
                    else: # (0, 1) or (0, -1)
                        pygame.draw.rect(self.screen, GREEN, (x * GRID_SIZE + SPACE_SNAKE, y * GRID_SIZE, GRID_SIZE - 2*SPACE_SNAKE, GRID_SIZE))
                else:
                    gen_direction = (direction_n[0] + direction_p[0], direction_n[1] + direction_p[1])
                    if gen_direction[1] == -1:
                        pygame.draw.rect(self.screen, GREEN, (x * GRID_SIZE + SPACE_SNAKE, y * GRID_SIZE, GRID_SIZE - 2*SPACE_SNAKE, SPACE_SNAKE))
                        
                        if gen_direction[0] == 1:
                            pygame.draw.rect(self.screen, GREEN, (x * GRID_SIZE + SPACE_SNAKE, y * GRID_SIZE + SPACE_SNAKE, GRID_SIZE, GRID_SIZE - 2*SPACE_SNAKE))# see
                        else:
                            pygame.draw.rect(self.screen,  GREEN, (x * GRID_SIZE, y * GRID_SIZE + SPACE_SNAKE, GRID_SIZE - SPACE_SNAKE, GRID_SIZE - 2*SPACE_SNAKE))# see
                    else:
                        pygame.draw.rect(self.screen, GREEN, (x * GRID_SIZE + SPACE_SNAKE, (y+1) * GRID_SIZE - SPACE_SNAKE, GRID_SIZE - 2*SPACE_SNAKE, SPACE_SNAKE))

                        if gen_direction[0] == 1:
                            pygame.draw.rect(self.screen, GREEN, (x * GRID_SIZE + SPACE_SNAKE, y * GRID_SIZE + SPACE_SNAKE, GRID_SIZE - SPACE_SNAKE, GRID_SIZE - 2*SPACE_SNAKE))# see
                        else:
                            pygame.draw.rect(self.screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE + SPACE_SNAKE, GRID_SIZE - SPACE_SNAKE, GRID_SIZE - 2*SPACE_SNAKE))# see

            else:
                if index == 0:
                    x_n, y_n = self.snake[index +1]
                    direction = (x - x_n, y - y_n)
                else: # index = len(self.snake)
                    x_p, y_p = self.snake[index -1]
                    direction = (x_p - x, y_p - y)
                
                if direction[0] == 0:
                    pygame.draw.rect(self.screen, GREEN, (x * GRID_SIZE + SPACE_SNAKE, y * GRID_SIZE, GRID_SIZE - 2*SPACE_SNAKE, GRID_SIZE))
                else:
                    pygame.draw.rect(self.screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE + SPACE_SNAKE, GRID_SIZE, GRID_SIZE - 2*SPACE_SNAKE))


    def check_collision(self, new_head):
        """Checks for collisions with walls and snake's own body."""
        head_x, head_y = new_head

        if head_x < 0 or head_x >= GRID_WIDTH:
            return True
        elif head_y < 0 or head_y >= GRID_HEIGHT:
            return True
        elif new_head in self.snake:
            return True
        else:
            return False


    def generate_food(self):
        """Generates a new food position for the snake."""
        return self.food_position[random.randint(0, len(self.food_position) - 1)]


# Main entry point
if __name__ == "__main__":
    Snake_Game()
