import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 48)
large_font = pygame.font.Font(None, 72)
clock = pygame.time.Clock()

# Game constants
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
SNAKE_SPEED = 10  # Frames per second

# Direction constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hovered = False

    def draw(self, surface):
        color = (min(self.color[0] + 30, 255), 
                min(self.color[1] + 30, 255), 
                min(self.color[2] + 30, 255)) if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                return True
        return False

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        for i in range(1, self.length):
            self.positions.append((self.positions[0][0], self.positions[0][1] + i))
        self.direction = UP
        self.next_direction = UP
        self.score = 0
        self.growing = False

    def update(self):
        # Update snake direction
        self.direction = self.next_direction
        
        # Move head
        head = self.get_head_position()
        x, y = head[0] + self.direction[0], head[1] + self.direction[1]
        
        # Wrap around screen
        if x < 0:
            x = GRID_WIDTH - 1
        elif x >= GRID_WIDTH:
            x = 0
        if y < 0:
            y = GRID_HEIGHT - 1
        elif y >= GRID_HEIGHT:
            y = 0
        
        # Check for self collision
        if (x, y) in self.positions[1:]:
            return False  # Game over
        
        # Move snake
        self.positions.insert(0, (x, y))
        
        if not self.growing:
            self.positions.pop()
        else:
            self.growing = False
        
        return True  # Game continues
    
    def get_head_position(self):
        return self.positions[0]
    
    def grow(self):
        self.growing = True
        self.score += 1
    
    def draw(self, surface):
        # Draw snake head
        head_rect = pygame.Rect(
            self.positions[0][0] * GRID_SIZE,
            self.positions[0][1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, GREEN, head_rect)
        pygame.draw.rect(surface, DARK_GREEN, head_rect, 1)
        
        # Draw snake body
        for position in self.positions[1:]:
            rect = pygame.Rect(
                position[0] * GRID_SIZE,
                position[1] * GRID_SIZE,
                GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(surface, DARK_GREEN, rect)
            pygame.draw.rect(surface, GREEN, rect, 1)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )

    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)


class PowerUp:
    def __init__(self):
        self.position = (0, 0)
        self.color = YELLOW
        self.active = False
        self.spawn_time = 0
        self.duration = 10  # Duration in seconds

    def spawn(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )
        self.active = True
        self.spawn_time = time.time()

    def update(self):
        if self.active and time.time() - self.spawn_time > self.duration:
            self.active = False

    def draw(self, surface):
        if self.active:
            rect = pygame.Rect(
                self.position[0] * GRID_SIZE,
                self.position[1] * GRID_SIZE,
                GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, WHITE, rect, 1)


def draw_grid(surface):
    """Draw grid lines on the game surface"""
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, (50, 50, 50), (0, y), (WINDOW_WIDTH, y))
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, (50, 50, 50), (x, 0), (x, WINDOW_HEIGHT))


def draw_home_screen():
    """Draw the home screen with menu options"""
    global high_score
    screen.fill(BLACK)
    
    # Title
    title_text = title_font.render("Snake Game!", True, GREEN)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH/2, 150))
    screen.blit(title_text, title_rect)
    
    # Display high score
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    high_score_rect = high_score_text.get_rect(topright=(WINDOW_WIDTH - 20, 20))
    screen.blit(high_score_text, high_score_rect)
    
    # Create buttons
    start_button = Button(WINDOW_WIDTH/2 - 100, 250, 200, 50, "Start Game", (0, 100, 0))
    instructions_button = Button(WINDOW_WIDTH/2 - 100, 325, 200, 50, "How to Play?", (0, 0, 100))
    quit_button = Button(WINDOW_WIDTH/2 - 100, 400, 200, 50, "Quit", (100, 0, 0))
    
    # Main menu loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if start_button.handle_event(event):
                return "start"
            if instructions_button.handle_event(event):
                return "instructions"
            if quit_button.handle_event(event):
                pygame.quit()
                sys.exit()
        
        # Draw buttons
        start_button.draw(screen)
        instructions_button.draw(screen)
        quit_button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)


def draw_instruction_screen():
    """Draw the instruction screen with game information"""
    screen.fill(BLACK)
    
    # Title
    title_text = title_font.render("How to Play Snake", True, GREEN)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH/2, 60))
    screen.blit(title_text, title_rect)
    
    # Instructions
    instructions = [
        "Game Controls:",
        "- Use ARROW KEYS to control the snake",
        "- Press ESC or P to pause the game",
        "",
        "Game Rules:",
        "- Eat red apples to grow longer and score points",
        "- Yellow power-ups appear randomly and give special abilities",
        "- Don't run into yourself!",
        "- You can go through walls to come out on the other side",
        "",
        "Click or press any key to return to menu"
    ]
    
    y_position = 120
    for line in instructions:
        text = font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, y_position))
        screen.blit(text, text_rect)
        y_position += 40
    
    pygame.display.flip()
    
    # Wait for any key press or mouse click
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def show_game_over(score):
    """Show game over screen with score"""
    global high_score
    
    # Update high score if needed
    if score > high_score:
        high_score = score
    
    screen.fill(BLACK)
    game_over_text = large_font.render("GAME OVER", True, RED)
    text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50))
    screen.blit(game_over_text, text_rect)
    
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 20))
    screen.blit(score_text, score_rect)
    
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 60))
    screen.blit(high_score_text, high_score_rect)
    
    continue_text = font.render("Press any key to continue", True, WHITE)
    continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 120))
    screen.blit(continue_text, continue_rect)
    
    pygame.display.flip()
    
    # Wait for key press
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def pause_game():
    """Pause the game and display a pause message"""
    paused_text = large_font.render("PAUSED", True, WHITE)
    text_rect = paused_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    screen.blit(paused_text, text_rect)
    
    continue_text = font.render("Press P to continue", True, WHITE)
    continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 60))
    screen.blit(continue_text, continue_rect)
    
    pygame.display.flip()
    
    # Wait for unpause
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    paused = False


def game_loop():
    """Main game loop"""
    snake = Snake()
    food = Food()
    power_up = PowerUp()
    power_up_chance = 0.005  # 0.5% chance per frame
    
    # Main game loop
    running = True
    paused = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    pause_game()
                elif event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.next_direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.next_direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.next_direction = RIGHT
        
        # Update power-up
        power_up.update()
        
        # Spawn power-up randomly
        if not power_up.active and random.random() < power_up_chance:
            power_up.spawn()
        
        # Update snake position
        if not snake.update():
            running = False
        
        # Check for food collision
        if snake.get_head_position() == food.position:
            snake.grow()
            food.randomize_position()
            
            # Make sure food doesn't spawn on snake
            while food.position in snake.positions:
                food.randomize_position()
        
        # Check for power-up collision
        if power_up.active and snake.get_head_position() == power_up.position:
            snake.score += 5  # Bonus points
            power_up.active = False
        
        # Update display
        screen.fill(BLACK)
        draw_grid(screen)
        
        # Draw entities
        snake.draw(screen)
        food.draw(screen)
        if power_up.active:
            power_up.draw(screen)
        
        # Draw score
        score_text = font.render(f"Score: {snake.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(SNAKE_SPEED)
    
    return snake.score


# Initialize high score
high_score = 0

# Main game loop
def main():
    while True:
        # Show home screen and get action
        action = draw_home_screen()
        
        if action == "start":
            # Start the game
            final_score = game_loop()
            show_game_over(final_score)
        elif action == "instructions":
            # Show instruction screen
            draw_instruction_screen()

if __name__ == "__main__":
    main()