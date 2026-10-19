import asyncio
import random
import pygame
import time

# Game settings
screenWidth = 1280
screenHeight = 720
playerSize = 100
playerSpeed = 5
obstacleSize = 100
score = 0
pygame.init()
font = pygame.font.SysFont(None, 40)
window = pygame.Window(size=(screenWidth, screenHeight))
window.title = "My First PyGame Program"
screen = window.get_surface()

# The player's position
playerX = 0
playerY = screenHeight - playerSize
# Create obstacles at random positions when the game starts.
obstacles = []


def randomObstacle(player):
    while True:
        obstacleX = random.randint(0, screenWidth - obstacleSize)
        obstacleY = random.randint(0, screenHeight - obstacleSize)

        if random.randint(0, 1) == 0:
            obstacle = pygame.Rect(obstacleX, 0, obstacleSize, screenHeight)
        else:
            obstacle = pygame.Rect(0, obstacleY, screenWidth, obstacleSize)

        if not player.colliderect(obstacle):
            return obstacle


player = pygame.Rect(playerX, playerY, playerSize, playerSize)
lastObstacleTime = time.time()
running = True
while running:
    # Check for events, such as closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Move left and right
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        playerX -= playerSpeed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        playerX += playerSpeed

    # Move up and down
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        playerY -= playerSpeed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        playerY += playerSpeed

    # Keep the player inside the screen
    playerX = max(0, min(playerX, screenWidth - playerSize))
    playerY = max(0, min(playerY, screenHeight - playerSize))

    player = pygame.Rect(playerX, playerY, playerSize, playerSize)

    if obstacles and player.colliderect(obstacles[0]):
        playerX = 0
        playerY = screenHeight - playerSize
        player = pygame.Rect(playerX, playerY, playerSize, playerSize)

    currentTime = time.time()
    if currentTime - lastObstacleTime >= 1:
        obstacles.append(randomObstacle(player))
        score += 1
        lastObstacleTime = currentTime

    # Draw the game
    screen.fill((0, 255, 0))
    for obstacle in obstacles:
        pygame.draw.rect(screen, (0, 0, 255), obstacle)
    pygame.draw.rect(screen, (255, 0, 0), player)

    scoreText = font.render(f"Score: {score}", True, (255, 255, 255))
    scorePosition = scoreText.get_rect(topleft=(20, 20))
    screen.blit(scoreText, scorePosition)

    window.flip()
    # Give the browser time to update the screen
    await asyncio.sleep(1 / 60)

pygame.quit()
