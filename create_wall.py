import pygame

pygame.init()

# 32x32 pixel surface
Tile = pygame.Surface((32, 32))

# Stone base
Tile.fill((35, 42, 52))

# Stone blocks
pygame.draw.rect(Tile, (55, 65, 78), (1, 1, 30, 14))
pygame.draw.rect(Tile, (48, 58, 70), (1, 17, 30, 14))

# Deep mortar lines
pygame.draw.line(Tile, (20, 25, 32), (0, 16), (32, 16), 2)
pygame.draw.line(Tile, (20, 25, 32), (16, 1), (16, 15), 2)
pygame.draw.line(Tile, (20, 25, 32), (9, 17), (9, 31), 2)

# Stone highlights
pygame.draw.line(Tile, (75, 88, 105), (3, 3), (13, 3), 1)
pygame.draw.line(Tile, (68, 80, 95), (19, 19), (28, 19), 1)

# Small cracks
pygame.draw.line(Tile, (28, 34, 42), (22, 7), (25, 10), 1)
pygame.draw.line(Tile, (28, 34, 42), (5, 23), (8, 26), 1)

# Save the image
pygame.image.save(Tile, "assets/tiles/wall.png")

pygame.quit()
