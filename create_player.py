import pygame

pygame.init()

PlayerImage = pygame.Surface((32, 32), pygame.SRCALPHA)

# Head
pygame.draw.rect(PlayerImage, (220, 190, 120), (8, 3, 16, 12))

# Adventurer hat
pygame.draw.rect(PlayerImage, (100, 65, 35), (8, 0, 16, 4))
pygame.draw.rect(PlayerImage, (130, 85, 45), (3, 3, 26, 4))
pygame.draw.rect(PlayerImage, (65, 45, 30), (8, 3, 16, 2))

# Hat band
pygame.draw.rect(PlayerImage, (170, 120, 45), (8, 3, 16, 2))

# Eyes
pygame.draw.rect(PlayerImage, (30, 30, 30), (11, 10, 3, 3))
pygame.draw.rect(PlayerImage, (30, 30, 30), (18, 10, 3, 3))

# Body
pygame.draw.rect(PlayerImage, (60, 90, 130), (6, 15, 20, 12))

# Legs
pygame.draw.rect(PlayerImage, (70, 55, 45), (8, 27, 6, 5))
pygame.draw.rect(PlayerImage, (70, 55, 45), (18, 27, 6, 5))

pygame.image.save(PlayerImage, "assets/characters/player.png")

PlayerRightImage = PlayerImage.copy()

# Hide left eye
pygame.draw.rect(PlayerRightImage, (220, 190, 120), (11, 10, 3, 3))

pygame.image.save(PlayerRightImage, "assets/characters/player_right.png")

PlayerLeftImage = pygame.transform.flip(PlayerImage, True, False)

# Hide original eyes
pygame.draw.rect(PlayerLeftImage, (220, 190, 120), (18, 10, 3, 3))

# Draw one eye
pygame.draw.rect(PlayerLeftImage, (30, 30, 30), (11, 10, 3, 3))

pygame.image.save(PlayerLeftImage, "assets/characters/player_left.png")

# Create downward-facing player
PlayerDownImage = PlayerImage.copy()

# Hide original eyes
pygame.draw.rect(PlayerDownImage, (220, 190, 120), (11, 10, 10, 3))

# Draw downward-facing eyes
pygame.draw.rect(PlayerDownImage, (30, 30, 30), (11, 12, 3, 2))
pygame.draw.rect(PlayerDownImage, (30, 30, 30), (18, 12, 3, 2))

pygame.image.save(PlayerDownImage, "assets/characters/player_down.png")

pygame.image.save(PlayerDownImage, "assets/characters/player_down.png")

# Draw upward-facing player
PlayerUpImage = PlayerImage.copy()

pygame.draw.rect(PlayerUpImage, (220, 190, 120), (8, 10, 16, 5))

pygame.image.save(PlayerUpImage, "assets/characters/player_up.png")

pygame.quit()
