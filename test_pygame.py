import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# player
player = pygame.Rect(400, 300, 50, 50)
speed = 5

# สร้าง platform แบบ rectangle
platforms = [pygame.Rect(x * 200, 500, 150, 50) for x in range(10)]

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    if keys[pygame.K_UP]:
        player.y -= speed
    if keys[pygame.K_DOWN]:
        player.y += speed

    # camera offset (ทำให้ player อยู่กลางจอ)
    camera_x = player.x - screen.get_width() // 4
    camera_y = player.y - screen.get_height() // 4

    # วาด
    screen.fill((135, 206, 235))  # sky blue

    # วาด platform (world - camera)
    for plat in platforms:
        pygame.draw.rect(screen, (0, 200, 0),
                         (plat.x - camera_x, plat.y - camera_y, plat.width, plat.height))

    # วาด player (ให้อยู่กลางจอ)
    pygame.draw.rect(screen, (200, 50, 50),
                     (player.x - camera_x, player.y - camera_y, player.width, player.height))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
