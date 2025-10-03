# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
pygame.display.set_caption("Show Text Example")
font = pygame.font.SysFont(None, 48)
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
original_player_image = pygame.image.load("Pic/herta_sama_ver2.1.png").convert_alpha()
width, height = original_player_image.get_size()
player_image = pygame.transform.scale(original_player_image, (width*0.1, height*0.1))
# player_rect = player_image.get_rect(center=(player_pos.x, player_pos.y))
facing_right = False #we want to make a move animation  
# player_image = pygame.image.load("Pic/herta_sama.png").convert_alpha()
walk_frames = []
walk_frames_up_down = []
speed = 20
current_frame = 0
frame_duration = 0.5  # Seconds per frame
frame_timer = 0
moving = False
facing_up = True
for i in range(1,3):
    img = pygame.image.load(f"Pic/herta_sama_ver2.{i}.png").convert_alpha()
    img = pygame.transform.scale(img, (width*0.1, height*0.1))  # Resize if needed
    walk_frames_up_down.append(img)
    
for i in range(1, 3):  # Assuming walk1, walk2
    img = pygame.image.load(f"Pic/herta_sama_walking_{i}-removebg-preview.png").convert_alpha()
    img = pygame.transform.scale(img, (width*0.1, height*0.1))  # Resize if needed
    walk_frames.append(img)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    radian = 40
    top = 30
    if moving:
        frame_image = walk_frames[current_frame]
    else:
        frame_image = player_image

    # Flip image if facing right
    if facing_right :
        frame_image = pygame.transform.flip(frame_image, True, False)

    frame_rect = frame_image.get_rect(center=(player_pos.x, player_pos.y))
    screen.blit(frame_image, frame_rect)
    
    # pygame.draw.circle(screen, "red", player_pos, radian)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        print("Nahh I would win")
        text_surface = font.render("Nahh I would win", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center = (player_pos.x, player_pos.y-radian-top))  # Centered horizontally
        screen.blit(text_surface, text_rect)  # Draw at position (100, 100)    
        
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    move_dir = pygame.Vector2(0, 0)
    if keys[pygame.K_w]:
        move_dir.y -= 1
    if keys[pygame.K_s]:
        move_dir.y += 1
    if keys[pygame.K_a]:
        move_dir.x -= 1
    if keys[pygame.K_d]:
        move_dir.x += 1
    
    if move_dir.length_squared() > 0:
        move_dir = move_dir.normalize()
        player_pos += move_dir * speed * dt
        moving = True
    else:
        moving = False
    
    if moving:
        frame_timer += dt
        if frame_timer >= frame_duration:
            frame_timer = 0
            current_frame = (current_frame + 1) % len(walk_frames)
    else:
        current_frame = 0  # Stand still on first fram
    # flip() the display to put your work on screen
    
    if move_dir.x > 0:
        facing_right = True
    elif move_dir.x < 0:
        facing_right = False
    if move_dir.y > 0:
        facing_up = True
    elif move_dir.y < 0:
        facing_up = False

    
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()