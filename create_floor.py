import pygame

pygame.init()

# Create a 32x32 pixel surface
Tile = pygame.Surface((32, 32))

# Base floor color
Tile.fill((105, 95, 80))

# Outer stone border
pygame.draw.rect(Tile, (65, 60, 55), (0, 0, 32, 32), 2)

# Stone highlights
pygame.draw.line(Tile, (135, 125, 105), (3, 4), (27, 4), 1)
pygame.draw.line(Tile, (135, 125, 105), (3, 4), (3, 27), 1)

# Small details
pygame.draw.rect(Tile, (85, 78, 68), (8, 11, 3, 2))
pygame.draw.rect(Tile, (85, 78, 68), (21, 22, 4, 2))
pygame.draw.line(Tile, (75, 68, 60), (13, 15), (17, 18), 1)

# Save the image
pygame.image.save(Tile, "assets/tiles/floor.png")

pygame.quit()
