import pygame
import random
import json
import sys
if 'pyodide' in sys.modules:
    import js  # For handling JavaScript in Pyodide environments


# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Battleground with Player Collision")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT_COLOR = (50, 168, 82)

# Load and scale images
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
bullet_img = pygame.image.load("bullet.png")
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
bullet_img = pygame.transform.scale(bullet_img, (20, 20))

# Clock for frame rate
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 36)

# Player and enemy properties
player = {"x": 100, "y": HEIGHT // 2, "speed": 5, "bullets": []}
enemies = [{"x": random.randint(WIDTH, WIDTH + 200), "y": random.randint(50, HEIGHT - 50)} for _ in range(3)]
score = 0

# Set difficulty variables
enemy_speed = 2
bullet_speed = 10

# Display rules and level selection before the game starts
def display_rules_and_levels():
    screen.fill(BLACK)
    lines = [
        "WELCOME TO THE BATTLEFIELD!",
        "Rules and Controls:",
        "- Use UP and DOWN arrows to move the player.",
        "- Press SPACE to shoot bullets.",
        "- Kill enemies by shooting them. Enemies respawn after being killed.",
        "- Avoid touching enemies, or you'll lose the game.",
        "",
        "Select Difficulty:",
        "1. Easy (Enemies move slowly)",
        "2. Medium (Normal enemy speed)",
        "3. Hard (Enemies move fast)",
        "",
        "Press ENTER to start."
    ]
    y_offset = HEIGHT // 2 - len(lines) * 20  # Center rules vertically
    for i, line in enumerate(lines):
        text_surface = big_font.render(line, True, WHITE)
        screen.blit(text_surface, (50, y_offset + i * 40))
    pygame.display.flip()

    # Wait for the player to select difficulty and press Enter
    waiting = True
    selected_level = None
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_level = "Easy"
                    waiting = False
                elif event.key == pygame.K_2:
                    selected_level = "Medium"
                    waiting = False
                elif event.key == pygame.K_3:
                    selected_level = "Hard"
                    waiting = False
                elif event.key == pygame.K_RETURN and selected_level:
                    waiting = False

    # Set game parameters based on difficulty
    if selected_level == "Easy":
        global enemy_speed, bullet_speed
        enemy_speed = 1
        bullet_speed = 8
    elif selected_level == "Medium":
        enemy_speed = 2
        bullet_speed = 10
    elif selected_level == "Hard":
        enemy_speed = 4
        bullet_speed = 12

# Draw the current state (score, etc.)
def draw_text():
    text_surface = font.render(f"Score: {score}", True, FONT_COLOR)
    screen.blit(text_surface, (20, 20))

# Move player bullets
def move_bullets():
    for bullet in player["bullets"]:
        bullet["x"] += bullet_speed
    player["bullets"] = [bullet for bullet in player["bullets"] if bullet["x"] <= WIDTH]


# Move enemies
def move_enemies():
    for enemy in enemies:
        enemy["x"] -= enemy_speed
        if enemy["x"] < 0:
            enemy["x"] = random.randint(WIDTH, WIDTH + 200)
            enemy["y"] = random.randint(50, HEIGHT - 50)

# Check for collisions (bullets with enemies, player with enemies)
def check_collisions():
    global score
    # Check bullet-enemy collisions
    for bullet in player["bullets"]:
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 50, 50)
            bullet_rect = pygame.Rect(bullet["x"], bullet["y"], 20, 20)
            if enemy_rect.colliderect(bullet_rect):
                player["bullets"].remove(bullet)
                enemies.remove(enemy)
                score += 1
                enemies.append({
                    "x": random.randint(WIDTH, WIDTH + 200),
                    "y": random.randint(50, HEIGHT - 50)
                })
                break  # Exit the inner loop after collision to avoid modifying the list during iteration

    # Check player-enemy collisions
    player_rect = pygame.Rect(player["x"], player["y"], 50, 50)
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 50, 50)
        if player_rect.colliderect(enemy_rect):
            game_over()

# Game over function
def game_over():
    screen.fill(BLACK)
    text_surface = big_font.render("GAME OVER!", True, RED)
    score_surface = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(3000)  # Delay before quitting
    pygame.quit()
    sys.exit()  # Ensure the game exits properly


# Main game loop
def game_loop():
    global score
    running = True
    while running:
        screen.blit(background, (0, 0))
        draw_text()

        # Draw player
        screen.blit(player_img, (player["x"], player["y"]))

        # Draw enemies
        for enemy in enemies:
            screen.blit(enemy_img, (enemy["x"], enemy["y"]))

        # Draw bullets
        for bullet in player["bullets"]:
            screen.blit(bullet_img, (bullet["x"], bullet["y"]))

        # Move bullets and enemies
        move_bullets()
        move_enemies()
        check_collisions()

        pygame.display.flip()
        clock.tick(60)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player["y"] > 0:
            player["y"] -= player["speed"]
        if keys[pygame.K_DOWN] and player["y"] < HEIGHT - 50:
            player["y"] += player["speed"]
        if keys[pygame.K_SPACE]:
            player["bullets"].append({"x": player["x"] + 50, "y": player["y"] + 25})

# Display rules, level selection, and start the game
display_rules_and_levels()
game_loop()
pygame.quit()

# casebased.py



def handler(request):
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello from Python!"})
    }

