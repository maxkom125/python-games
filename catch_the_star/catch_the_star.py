import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Catch the Star!")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PINK = (255, 192, 203)

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 48)
clock = pygame.time.Clock()

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

def draw_home_screen():
    """Draw the home screen with menu options"""
    global high_score, last_score
    screen.fill(BLACK)
    
    # Title
    title_text = title_font.render("Catch the Star!", True, WHITE)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH/2, 150))
    screen.blit(title_text, title_rect)
    
    # Display high score and last score
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    last_score_text = font.render(f"Last Score: {last_score}", True, WHITE)
    
    # Position the scores in the top right corner with padding
    padding = 20
    high_score_rect = high_score_text.get_rect(topright=(WINDOW_WIDTH - padding, padding))
    last_score_rect = last_score_text.get_rect(topright=(WINDOW_WIDTH - padding, padding + 40))
    
    screen.blit(high_score_text, high_score_rect)
    screen.blit(last_score_text, last_score_rect)
    
    # Create buttons
    start_button = Button(WINDOW_WIDTH/2 - 100, 250, 200, 50, "Start Game", (50, 50, 150))
    instructions_button = Button(WINDOW_WIDTH/2 - 100, 325, 200, 50, "How to Play?", (50, 150, 50))
    quit_button = Button(WINDOW_WIDTH/2 - 100, 400, 200, 50, "Quit", (150, 50, 50))
    
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

def spawn_star():
    x = random.randint(0, WINDOW_WIDTH - star_size)
    return {'x': x, 'y': -star_size}

def spawn_obstacle():
    x = random.randint(0, WINDOW_WIDTH - obstacle_width)
    return {'x': x, 'y': -obstacle_height}

def spawn_green_object():
    x = random.randint(0, WINDOW_WIDTH - green_size)
    return {'x': x, 'y': -green_size}

def draw_heart(surface, x, y, size, color):
    """Draw a heart shape at the specified position"""
    # Create a surface for the heart
    heart_surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Calculate the center and radius
    center_x = size // 2
    center_y = size // 2
    radius = size // 4  # Changed from size // 3 to size // 4 for better proportions
    
    # Draw the two circles for the top of the heart
    pygame.draw.circle(heart_surface, color, (center_x - radius//2, center_y - radius//2), radius)
    pygame.draw.circle(heart_surface, color, (center_x + radius//2, center_y - radius//2), radius)
    
    # Draw the triangle for the bottom of the heart
    points = [
        (center_x - radius, center_y - radius//2),  # Left circle bottom
        (center_x + radius, center_y - radius//2),  # Right circle bottom
        (center_x, center_y + radius * 1.5)         # Bottom point (made longer)
    ]
    pygame.draw.polygon(heart_surface, color, points)
    
    # Blit the heart onto the main surface
    surface.blit(heart_surface, (x - size//2, y - size//2))

def draw_star(surface, x, y, size, color):
    """Draw a star shape at the specified position"""
    # Calculate points for a 5-pointed star
    outer_points = []
    inner_points = []
    
    # Adjust the ratio between outer and inner radius for better star shape
    outer_radius = size / 2
    inner_radius = size / 5  # Changed from size/4 to size/5 for sharper points
    
    for i in range(5):
        # Outer points (points of the star)
        angle = (i * 72 - 72) * math.pi / 180.0  # Convert to radians
        outer_points.append((
            x + outer_radius * math.cos(angle),
            y + outer_radius * math.sin(angle)
        ))
        
        # Inner points (between the star's points)
        angle += 36 * math.pi / 180.0
        inner_points.append((
            x + inner_radius * math.cos(angle),
            y + inner_radius * math.sin(angle)
        ))
    
    # Combine points to create star shape, starting from the top point
    points = []
    for i in range(5):
        points.append(outer_points[i])
        points.append(inner_points[i])
    
    # Draw the star
    pygame.draw.polygon(surface, color, points)
    # Add an outline to make the star more visible
    pygame.draw.polygon(surface, (min(color[0] + 50, 255), 
                                min(color[1] + 50, 255), 
                                min(color[2] + 50, 255)), points, 2)

def draw_instruction_screen():
    """Draw the instruction screen with game information"""
    screen.fill(BLACK)
    
    # Title
    title_text = title_font.render("Catch the Star!", True, WHITE)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH/2, 60))  # Moved up from 80
    screen.blit(title_text, title_rect)
    
    # Instructions
    control_instructions = [
        "Game Controls:",
        "- Use LEFT and RIGHT arrow keys to move",
        "- Press ESC to quit the game",
        "",
        "Game Objects:"
    ]
    
    y_position = 120  # Moved up from 150
    for line in control_instructions:
        text = font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, y_position))
        screen.blit(text, text_rect)
        y_position += 28  # Reduced from 30
    
    # Draw objects with their descriptions
    object_spacing = 32  # Reduced from 35
    left_margin = 100
    text_margin = 40
    
    # Yellow star
    draw_star(screen, left_margin, y_position, star_size, YELLOW)
    text = font.render("Yellow Stars: Catch for +1 point", True, WHITE)
    screen.blit(text, (left_margin + text_margin, y_position - 10))
    y_position += object_spacing
    
    # Green star
    draw_star(screen, left_margin, y_position, green_size, GREEN)
    text = font.render("Green Stars: Catch for +3 points, miss for -2 points", True, WHITE)
    screen.blit(text, (left_margin + text_margin, y_position - 10))
    y_position += object_spacing
    
    # Red star
    draw_star(screen, left_margin, y_position, obstacle_width, RED)
    text = font.render("Red Stars: Avoid or game over", True, WHITE)
    screen.blit(text, (left_margin + text_margin, y_position - 10))
    y_position += object_spacing + 8  # Reduced from 10
    
    # Hearts section
    hearts_text = font.render("Hearts:", True, WHITE)
    hearts_rect = hearts_text.get_rect(center=(WINDOW_WIDTH/2, y_position))
    screen.blit(hearts_text, hearts_rect)
    y_position += 28  # Reduced from 30
    
    # Draw hearts
    heart_size = 20
    heart_spacing = 25
    for i in range(max_hearts):
        x = WINDOW_WIDTH/2 + (i - 1) * heart_spacing
        draw_heart(screen, x, y_position, heart_size, PINK)
    
    y_position += 32  # Reduced from 35
    
    # Hearts description
    hearts_desc = [
        "- Miss a green star: -1 heart",
        "- Catch a green star: +1 heart",
        "- Game ends when you lose all hearts",
        "",
        "Click or press any key to return to menu"
    ]
    
    for line in hearts_desc:
        text = font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, y_position))
        screen.blit(text, text_rect)
        y_position += 28  # Reduced from 30
    
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

def draw_frog(surface, x, y, width, height):
    """Draw a frog silhouette at the specified position"""
    # Main body color
    frog_color = (34, 145, 50)  # Green
    
    # Draw the main body (pear-shaped)
    body_points = [
        (x + width * 0.2, y + height * 0.4),  # Left side
        (x + width * 0.5, y + height * 0.2),  # Top middle
        (x + width * 0.8, y + height * 0.4),  # Right side
        (x + width * 0.8, y + height * 0.7),  # Bottom right
        (x + width * 0.5, y + height * 0.8),  # Bottom middle
        (x + width * 0.2, y + height * 0.7),  # Bottom left
    ]
    pygame.draw.polygon(surface, frog_color, body_points)
    
    # Draw the eyes (white ovals)
    eye_width = width * 0.25
    eye_height = height * 0.25
    left_eye_x = x + width * 0.25 - eye_width/2
    right_eye_x = x + width * 0.75 - eye_width/2
    eye_y = y + height * 0.3
    
    pygame.draw.ellipse(surface, WHITE, (left_eye_x, eye_y, eye_width, eye_height))
    pygame.draw.ellipse(surface, WHITE, (right_eye_x, eye_y, eye_width, eye_height))
    
    # Draw front legs (splayed out)
    leg_width = width * 0.3
    leg_height = height * 0.3
    
    # Left front leg
    left_leg_points = [
        (x, y + height * 0.5),  # Outer point
        (x + width * 0.2, y + height * 0.4),  # Top
        (x + width * 0.3, y + height * 0.6),  # Inner
        (x + width * 0.1, y + height * 0.7),  # Bottom
    ]
    pygame.draw.polygon(surface, frog_color, left_leg_points)
    
    # Right front leg
    right_leg_points = [
        (x + width, y + height * 0.5),  # Outer point
        (x + width * 0.8, y + height * 0.4),  # Top
        (x + width * 0.7, y + height * 0.6),  # Inner
        (x + width * 0.9, y + height * 0.7),  # Bottom
    ]
    pygame.draw.polygon(surface, frog_color, right_leg_points)
    
    # Draw back legs (splayed out)
    # Left back leg
    left_back_points = [
        (x + width * 0.1, y + height * 0.8),  # Top
        (x, y + height),  # Outer point
        (x + width * 0.3, y + height * 0.9),  # Inner
    ]
    pygame.draw.polygon(surface, frog_color, left_back_points)
    
    # Right back leg
    right_back_points = [
        (x + width * 0.9, y + height * 0.8),  # Top
        (x + width, y + height),  # Outer point
        (x + width * 0.7, y + height * 0.9),  # Inner
    ]
    pygame.draw.polygon(surface, frog_color, right_back_points)

def game_loop():
    """Main game loop"""
    # Initialize game variables
    player_x = WINDOW_WIDTH // 2 - player_width // 2
    player_y = WINDOW_HEIGHT - player_height - 10
    stars = []
    obstacles = []
    green_object = None
    missed_greens = 0
    score = 0
    speed_multiplier = 1.0
    
    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WINDOW_WIDTH - player_width:
            player_x += player_speed

        # Update speed multiplier based on score
        speed_multiplier = 1.0 + (score // 10) * speed_increase

        # Spawn stars and obstacles
        if random.random() < 0.02:  # 2% chance each frame
            stars.append(spawn_star())
        if random.random() < 0.01:  # 1% chance each frame
            obstacles.append(spawn_obstacle())
        
        # Spawn green object if none exists
        if green_object is None and random.random() < 0.005:  # 0.5% chance each frame
            green_object = spawn_green_object()

        # Update stars
        for star in stars[:]:
            star['y'] += base_star_speed * speed_multiplier
            if star['y'] > WINDOW_HEIGHT:
                stars.remove(star)

        # Update obstacles
        for obstacle in obstacles[:]:
            obstacle['y'] += base_obstacle_speed * speed_multiplier
            if obstacle['y'] > WINDOW_HEIGHT:
                obstacles.remove(obstacle)
        
        # Update green object
        if green_object is not None:
            green_object['y'] += base_green_speed * speed_multiplier
            if green_object['y'] > WINDOW_HEIGHT:
                # Decrease score if green object is missed
                score = max(0, score - 2)  # Don't go below 0
                missed_greens += 1  # Increment missed greens counter
                green_object = None
                
                # Check if 3 green objects were missed in a row
                if missed_greens >= max_hearts:
                    running = False

        # Collision detection
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        
        for star in stars[:]:
            star_rect = pygame.Rect(star['x'], star['y'], star_size, star_size)
            if player_rect.colliderect(star_rect):
                stars.remove(star)
                score += 1

        for obstacle in obstacles[:]:
            obstacle_rect = pygame.Rect(obstacle['x'], obstacle['y'], obstacle_width, obstacle_height)
            if player_rect.colliderect(obstacle_rect):
                running = False
        
        # Check collision with green object
        if green_object is not None:
            green_rect = pygame.Rect(green_object['x'], green_object['y'], green_size, green_size)
            if player_rect.colliderect(green_rect):
                score += 3  # Bonus points for catching green object
                missed_greens = max(0, missed_greens - 1)  # Regain only one heart
                green_object = None

        # Drawing
        screen.fill(BLACK)
        
        # Draw player (frog)
        draw_frog(screen, player_x, player_y, player_width, player_height)
        
        # Draw stars
        for star in stars:
            draw_star(screen, star['x'], star['y'], star_size, YELLOW)
        
        # Draw obstacles
        for obstacle in obstacles:
            draw_star(screen, obstacle['x'], obstacle['y'], obstacle_width, RED)
        
        # Draw green object
        if green_object is not None:
            draw_star(screen, green_object['x'], green_object['y'], green_size, GREEN)
        
        # Draw score and speed
        score_text = font.render(f"Score: {score}", True, WHITE)
        speed_text = font.render(f"Speed: {speed_multiplier:.1f}x", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(speed_text, (10, 40))
        
        # Draw hearts in the bottom left corner
        heart_size = 30
        heart_spacing = 40
        for i in range(max_hearts):
            x = 20 + i * heart_spacing
            y = WINDOW_HEIGHT - 50
            if i < max_hearts - missed_greens:
                # Draw filled heart
                draw_heart(screen, x, y, heart_size, PINK)
            else:
                # Draw empty heart (outline)
                draw_heart(screen, x, y, heart_size, (100, 100, 100))
        
        pygame.display.flip()
        clock.tick(60)
    
    return score

def show_game_over(score):
    """Show game over screen with score"""
    screen.fill(BLACK)
    game_over_text = font.render(f'Game Over! Score: {score}', True, WHITE)
    text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
    screen.blit(game_over_text, text_rect)
    
    continue_text = font.render('Click or press any key to continue', True, WHITE)
    continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 50))
    screen.blit(continue_text, continue_rect)
    
    pygame.display.flip()
    
    # Wait for key press or mouse click
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

# Game constants (player, star, obstacle properties remain the same)
player_width = 50
player_height = 50
player_speed = 5

star_size = 20
base_star_speed = 3

obstacle_width = 30
obstacle_height = 30
base_obstacle_speed = 6

green_size = 25
base_green_speed = 4
max_hearts = 3

speed_increase = 0.2

# Score tracking
high_score = 0
last_score = 0

# Main game loop
while True:
    # Show home screen
    action = draw_home_screen()
    
    if action == "start":
        # Start the game directly
        final_score = game_loop()
        # Update scores
        last_score = final_score
        high_score = max(high_score, final_score)
        # Show game over screen
        show_game_over(final_score)
        # Loop back to home screen
    elif action == "instructions":
        # Show instruction screen
        draw_instruction_screen()
        # Loop back to home screen 