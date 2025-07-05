
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 150, 0)

# Game settings
FPS = 10

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Start moving right
        self.grow = False
        
    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False
            
        # Check self collision
        if new_head in self.positions:
            return False
            
        self.positions.insert(0, new_head)
        
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
            
        return True
        
    def change_direction(self, direction):
        # Prevent moving in opposite direction
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
            
    def eat_food(self):
        self.grow = True
        
    def draw(self, screen):
        for i, pos in enumerate(self.positions):
            x, y = pos[0] * GRID_SIZE, pos[1] * GRID_SIZE
            color = GREEN if i == 0 else DARK_GREEN  # Head is brighter
            pygame.draw.rect(screen, color, (x, y, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, GRID_SIZE, GRID_SIZE), 1)

class Food:
    def __init__(self):
        self.position = self.generate_position()
        
    def generate_position(self):
        return (random.randint(0, GRID_WIDTH - 1), 
                random.randint(0, GRID_HEIGHT - 1))
                
    def draw(self, screen):
        x, y = self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE
        pygame.draw.rect(screen, RED, (x, y, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BLACK, (x, y, GRID_SIZE, GRID_SIZE), 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Python Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()
        
    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        
        # Make sure food doesn't spawn on snake
        while self.food.position in self.snake.positions:
            self.food.position = self.food.generate_position()
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        return False
                else:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
        return True
        
    def update(self):
        if not self.game_over:
            if not self.snake.move():
                self.game_over = True
                return
                
            # Check if snake ate food
            if self.snake.positions[0] == self.food.position:
                self.snake.eat_food()
                self.score += 10
                self.food.position = self.food.generate_position()
                
                # Make sure new food doesn't spawn on snake
                while self.food.position in self.snake.positions:
                    self.food.position = self.food.generate_position()
                    
    def draw(self):
        self.screen.fill(BLACK)
        
        if not self.game_over:
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over screen
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, WHITE)
            restart_text = self.font.render("Press 'R' to restart or 'Q' to quit", True, WHITE)
            
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)
            
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

# Instructions for running the game
if __name__ == "__main__":
    print("Snake Game Controls:")
    print("- Use arrow keys to move")
    print("- Eat red food to grow and increase score")
    print("- Avoid hitting walls or yourself")
    print("- Press 'R' to restart when game over")
    print("- Press 'Q' to quit when game over")
    print("\nStarting game...")
    
    game = Game()
    game.run()

