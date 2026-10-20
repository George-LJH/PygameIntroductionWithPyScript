import asyncio
import random
import pygame
import time
import sys


def randomObstacle(safeRect=None):
    while True:
        obstacleX = random.randint(0, screenWidth - obstacleSize)
        obstacleY = random.randint(0, screenHeight - obstacleSize)

        if random.randint(0, 1) == 0:
            obstacle = pygame.Rect(obstacleX, 0, obstacleSize, screenHeight)
        else:
            obstacle = pygame.Rect(0, obstacleY, screenWidth, obstacleSize)

        if safeRect is None or not obstacle.colliderect(safeRect):
            return obstacle


# Game settings
screenWidth = 1280
screenHeight = 720
playerSize = 100
playerSpeed = 10
obstacleSize = 25
maxObstacles = 10
obstacleInterval = 0.75
pygame.init()


font = pygame.font.SysFont(None, 40)
buttonFont = pygame.font.SysFont(None, 44)
window = pygame.Window(size=(screenWidth, screenHeight))
window.title = "My First PyGame Program"
screen = window.get_surface()
startButton = pygame.Rect(500, 300, 280, 76)
playerImage = pygame.Surface((playerSize, playerSize), pygame.SRCALPHA)
playerImage.fill((255, 0, 0))


def button(surface, rect, text, font, baseColor, hoverColor, textColor, onClick, event=None):
    if event is not None and event.type == pygame.MOUSEBUTTONDOWN:
        if rect.collidepoint(event.pos):
            onClick()

    isHovered = rect.collidepoint(pygame.mouse.get_pos())
    color = hoverColor if isHovered else baseColor
    shadowRect = rect.move(0, 8)
    pygame.draw.rect(surface, (10, 15, 25), shadowRect, border_radius=14)
    pygame.draw.rect(surface, color, rect, border_radius=14)
    pygame.draw.rect(surface, (125, 185, 255), rect, width=2, border_radius=14)

    buttonText = font.render(text, True, textColor)
    textPosition = buttonText.get_rect(center=rect.center)
    surface.blit(buttonText, textPosition)


def resetGame():
    global score, obstacleInterval, playerX, playerY, obstacles
    global nextObstacles, player, lastObstacleTime, gameStarted
    score = 0
    obstacleInterval = 0.75
    playerX = 0
    playerY = screenHeight - playerSize
    player = pygame.Rect(playerX, playerY, playerSize, playerSize)
    obstacles = [randomObstacle(player), randomObstacle(player)]
    nextObstacles = [randomObstacle(player), randomObstacle(player)]
    lastObstacleTime = time.time()
    gameStarted = False


def startGame():
    global gameStarted
    resetGame()
    gameStarted = True


running = True
resetGame()

while running:
    # Check for events, such as closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            button(
                screen, startButton, "START", buttonFont,
                (35, 90, 175), (45, 115, 210), (255, 255, 255),
                startGame, event
            )
    if gameStarted:
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

        for obstacle in obstacles:
            if player.colliderect(obstacle):
                # playerX = 0
                # playerY = screenHeight - playerSize
                # player = pygame.Rect(playerX, playerY, playerSize, playerSize)
                gameStarted = False
                obstacleInterval = 0.75
                break

        currentTime = time.time()
        if currentTime - lastObstacleTime >= obstacleInterval:

            obstacles.pop(0)
            obstaclesToAdd = min(2, maxObstacles - len(obstacles))
            for _ in range(obstaclesToAdd):
                obstacles.append(nextObstacles.pop(0))
                nextObstacles.append(randomObstacle())
            score += 1
            lastObstacleTime = currentTime
            obstacleInterval = max(0.01, obstacleInterval - 0.01)

        # Draw the game
        screen.fill((0, 255, 0))
        for obstacle in obstacles:
            pygame.draw.rect(screen, (0, 0, 255), obstacle)
        screen.blit(playerImage, player)
        for nextObstacle in nextObstacles:
            pygame.draw.rect(screen, (255, 255, 0), nextObstacle, 5)
        scoreText = font.render(f"Score: {score}", True, (255, 255, 255))
        scorePosition = scoreText.get_rect(topleft=(20, 20))
        screen.blit(scoreText, scorePosition)
    else:
        screen.fill((0, 0, 0))
        button(
            screen, startButton, "START", buttonFont,
            (35, 90, 175), (45, 115, 210), (255, 255, 255),
            startGame
        )
    window.flip()
    # Give the browser time to update the screen
    await asyncio.sleep(1 / 120)

pygame.quit()
