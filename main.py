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
obstacleInterval = 0.75
maxObstacles = 1
teleportDistance = 300
teleportCooldown = 1000
lastTeleportTime = -teleportCooldown
pygame.init()


font = pygame.font.SysFont(None, 40)
window = pygame.Window(size=(screenWidth, screenHeight))
window.title = "My First PyGame Program"
screen = window.get_surface()
playerImage = pygame.Surface((playerSize, playerSize), pygame.SRCALPHA)
playerImage.fill((255, 0, 0))
teleportPreview = pygame.Surface((playerSize, playerSize), pygame.SRCALPHA)
teleportPreview.fill((255, 0, 0, 100))

def resetGame():
    global score, obstacleInterval, playerX, playerY, obstacles
    global nextObstacles, player, lastObstacleTime, gameStarted
    global obstacleSize, lastTeleportTime
    obstacleSize = 25
    score = 0
    obstacleInterval = 0.75
    playerX = (screenWidth/2)-(playerSize)/2
    playerY = (screenHeight/2)-(playerSize)/2
    player = pygame.Rect(playerX, playerY, playerSize, playerSize)
    obstacles = [randomObstacle(player), randomObstacle(player)]
    nextObstacles = [randomObstacle(player), randomObstacle(player)]
    lastObstacleTime = time.time()
    lastTeleportTime = pygame.time.get_ticks() - teleportCooldown
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not gameStarted:
                startGame()
            if event.key == pygame.K_SPACE and gameStarted:
                currentTeleportTime = pygame.time.get_ticks()
                if currentTeleportTime - lastTeleportTime >= teleportCooldown:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_UP] or keys[pygame.K_w]:
                        playerY -= teleportDistance
                    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                        playerY += teleportDistance
                    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                        playerX += teleportDistance
                    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                        playerX -= teleportDistance

                    lastTeleportTime = currentTeleportTime

                    playerX = max(0, min(playerX, screenWidth - playerSize))
                    playerY = max(0, min(playerY, screenHeight - playerSize))
    if gameStarted:
        # Draw the game
        screen.fill((0, 255, 0))
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

        currentTimeObstacleGeneration = time.time()
        if currentTimeObstacleGeneration - lastObstacleTime >= obstacleInterval:
            
            obstacleSize = min(obstacleSize + 1, 50)

            obstacles.pop(0)
            obstaclesToAdd = min(2, maxObstacles - len(obstacles))
            for _ in range(obstaclesToAdd):
                obstacles.append(nextObstacles.pop(0))
                nextObstacles.append(randomObstacle())
            score += 1
            lastObstacleTime = currentTimeObstacleGeneration
            obstacleInterval = max(0.01, obstacleInterval - 0.01)


        for obstacle in obstacles:
            pygame.draw.rect(screen, (0, 0, 255), obstacle)
        screen.blit(teleportPreview, (max(0, playerX - teleportDistance), playerY))
        screen.blit(teleportPreview, (min(screenWidth - teleportPreview.get_width(), playerX + teleportDistance), playerY))
        screen.blit(teleportPreview, (playerX, max(0, playerY - teleportDistance)))
        screen.blit(teleportPreview, (playerX, min(screenHeight - teleportPreview.get_height(), playerY + teleportDistance)))
        screen.blit(playerImage, player)
        for nextObstacle in nextObstacles:
            pygame.draw.rect(screen, (255, 255, 0), nextObstacle, 5)
        scoreText = font.render(f"Score: {score}", True, (255, 255, 255))
        scorePosition = scoreText.get_rect(topleft=(20, 20))
        screen.blit(scoreText, scorePosition)
    else:
        screen.fill((0, 0, 0))
        startText = font.render("Press ENTER to start", True, (255, 255, 255))
        startPosition = startText.get_rect(center=(screenWidth // 2, screenHeight // 2))
        screen.blit(startText, startPosition)
    window.flip()
    # Give the browser time to update the screen
    await asyncio.sleep(1 / 120)

pygame.quit()
